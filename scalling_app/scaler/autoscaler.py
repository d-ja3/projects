import requests
import subprocess
import time

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
QUERY = '''
sum(rate(container_network_receive_bytes_total{container_label_com_docker_swarm_service_name=~".+"}[1m]) 
    + rate(container_network_transmit_bytes_total{container_label_com_docker_swarm_service_name=~".+"}[1m])) 
  by (container_label_com_docker_swarm_service_name)
'''

SERVICE_NAME = "network_scaling_backend"  # Nazwa usługi
MIN_REPLICAS = 1
MAX_REPLICAS = 10
NETWORK_THRESHOLD = 0.5*1e6

def get_network_usage():
    response = requests.get(PROMETHEUS_URL, params={"query": QUERY})
    data = response.json().get("data", {}).get("result", [])
    return data

def scale_service(service_name, replicas):
    subprocess.run(["docker", "service", "scale", f"{service_name}={replicas}"], check=True)

def main():
    current_replicas = MIN_REPLICAS

    while True:
        try:
            metrics = get_network_usage()
            total_network = sum(float(metric["value"][1]) for metric in metrics)

            # Print zużycie sieci w danym momencie
            print(f"Current network usage: {(total_network/1e6):.2f} mb/s")

            if total_network > NETWORK_THRESHOLD * current_replicas:
                if current_replicas < MAX_REPLICAS:
                    current_replicas += 1
                    print(f"Scaling up to {current_replicas} replicas")
                    scale_service(SERVICE_NAME, current_replicas)
            elif total_network < NETWORK_THRESHOLD * (current_replicas - 1):
                if current_replicas > MIN_REPLICAS:
                    current_replicas -= 1
                    print(f"Scaling down to {current_replicas} replicas")
                    scale_service(SERVICE_NAME, current_replicas)

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10)


if __name__ == "__main__":
    main()
