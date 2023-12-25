# Basierend auf dem offiziellen Python-Image
FROM python:3.8

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren des gesamten Projektinhalts in das Arbeitsverzeichnis des Containers
COPY . /app

# Installieren von Flask (ersetzen Sie dies durch Ihre requirements.txt, wenn Sie eine haben)
RUN pip install Flask

# Umgebungsvariable für Flask festlegen
ENV FLASK_APP=app.py

# Port 5000 für den Zugriff von außerhalb des Containers freigeben
EXPOSE 5000

# Startbefehl für die Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]
