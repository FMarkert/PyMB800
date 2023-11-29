import json
import os 
import random
import sys 

act_path = os.path.dirname(os.path.abspath(__file__))
class_path = os.path.join(act_path, '..', 'models')
if class_path not in sys.path:
    sys.path.append(class_path)

import classes

def gamemode_directory(gamemode): # Bestimmt passendes Verzeichnis mit Fragen anhand des gewählten Spielmodus

    if gamemode == "l4d_1-40":
        mode_directory = ['l4d', '1-40']
    elif gamemode == "l4d_41-80":
        mode_directory = ['l4d', '41-80']
    elif gamemode == "l4d_81-136":
        mode_directory = ['l4d', '81-136']
    elif gamemode == "l4d_complete":
        print("not available yet") # Wird im späteren Verlauf integriert   
        pass
    elif gamemode == "xt":
        mode_directory = ["xt"]
    else:
        print("Error: Mode not found")
        mode_directory = "Error"
    
# Bestimmt den Pfad zum Verzeichnis der Fragen:

    act_path = os.path.dirname(os.path.abspath(__file__))
    dict_path = os.path.dirname(act_path)
    mode_path = [dict_path,"data","questions"]+ mode_directory
    directory = os.path.join("/".join(mode_path))
    return directory

# Es wird noch eine Funktion benötigt, die je nach Gamemode einen Fragenpool aus mehreren Verzeichnissen bildet

def json_to_object(directory): # Funktion, um JSON-Dateien zu Quizfragen-Objekten zu konvertieren.
    questions = []
    for filename in os.listdir(directory):  # Durchläuft alle Dateien im angegebenen Verzeichnis.
        if filename.endswith(".json"):  # Prüft, ob die Datei eine JSON-Datei ist.
            filepath = os.path.join(directory, filename) # Erstellt den vollständigen Dateipfad.
            try:
                with open(filepath, 'r') as file:  # Versucht, die Datei zu öffnen.
                    data = json.load(file)  # Lädt den JSON-Inhalt.

                    # Überprüft den Fragetyp und erstellt das entsprechende Frageobjekt.
                    if data['type'] == 'drag_drop_order':
                        question = classes.Drag_Drop_Order(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],
                            comment=data['comment'],
                            casestudy=data['casestudy'],
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    elif data['type'] == 'drag_drop_pairs':
                        question = classes.Drag_Drop_Pairs(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],
                            comment=data['comment'],
                            casestudy=data['casestudy'],
                            pairs=data['pairs']
                        )
                    elif data['type'] == 'dropdown':
                        question = classes.Dropdown(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],
                            comment=data['comment'],
                            casestudy=data['casestudy'],
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    elif data['type'] == 'multiple_choice':
                        question = classes.Multiple_Choice(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],
                            comment=data['comment'],
                            casestudy=data['casestudy'],
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    else:
                        print(f"Unbekannter Fragetyp: {data['type']} in Datei {filename}")
                        continue # Überspringt das Hinzufügen dieser Frage, falls der Typ unbekannt ist.

                    questions.append(question)  # Fügt das erstellte Frageobjekt zur Liste hinzu.
            
            # Fehlerbehandlungen für verschiedene Arten von Fehlern.
            except FileNotFoundError:
                print(f"Datei {filename} wurde nicht gefunden.")
            except json.JSONDecodeError:
                print(f"Datei {filename} ist kein gültiges JSON-Format.")
            except Exception as e:
                print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    return questions

def shuffle_questionpool(questions): # Die Liste mit Fragen wird durchgemischt 
    random.shuffle(questions)

