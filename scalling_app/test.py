import time
import subprocess

DURATION = 30  # czas testu w sekundach
IMAGE_URL = "http://localhost:5001/static/SampleJPGImage_5mbmb.jpg"

end_time = time.time() + DURATION

while time.time() < end_time:
    subprocess.run(["ab", "-n", "100", "-c", "20", IMAGE_URL])
    time.sleep(1)