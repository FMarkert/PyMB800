import json
import os 

def load_json(directory): # Nutzt Verzeichnis als Argument und gibt 
    questions = [] # Eine leere Liste, um die geladenen Fragenobjekte zu speichern

    for filename in os.listdir(directory):  # Iteriere über alle Dateien im angegebenen Verzeichnis
        with open(os.path.join(directory, filename), 'r') as file: # Vollständiger Pfad zur Datei wird erstellt 
            data = json.load(file) 
            return data 
