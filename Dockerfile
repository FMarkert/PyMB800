# Basierend auf dem offiziellen Python-Image
FROM python:3.8

# Installieren der erforderlichen Pakete und Abhängigkeiten für WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libcairo2-dev \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren des gesamten Projektinhalts in das Arbeitsverzeichnis des Containers
COPY . /app

# Installieren von Python-Bibliotheken
RUN pip install Flask weasyprint

# Umgebungsvariable für Flask festlegen
ENV FLASK_APP=app.py

# Port 5000 für den Zugriff von außerhalb des Containers freigeben
EXPOSE 5000

# Startbefehl für die Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]
