# Użyj oficjalnego obrazu Pythona jako bazy
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik requirements.txt do kontenera
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę plików aplikacji
COPY . .

# Otwórz port 5000 dla aplikacji
EXPOSE 5001

# Uruchom aplikację
CMD ["python", "app.py"]