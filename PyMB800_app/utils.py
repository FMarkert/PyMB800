from django.conf import settings
import os
import json
import random
from PyMB800_app.models import DragDropOrder, DragDropPairs, DropDown, MultipleChoice


def gamemode_directory(gamemode):
    base_dir = settings.BASE_DIR

 
    if gamemode == "l4d_1-40":   # Deine Spielmodi-Logik
        mode_directory = ['l4d', '1-40']
    elif gamemode == "l4d_41-80":
        mode_directory = ['l4d', '41-80']
    elif gamemode == "l4d_81-136":
        mode_directory = ['l4d', '81-136']
    elif gamemode == "l4d_complete":
        print("not available yet") # Wird im späteren Verlauf integriert   
        return None
    elif gamemode == "xt":
        mode_directory = ["xt"]
    else:
        print("Error: Mode not found")
        return None

    # Baue den Pfad basierend auf dem gewählten Spielmodus
    mode_path = os.path.join(base_dir, "data", "questions", *mode_directory)

    # Überprüfe, ob das Verzeichnis existiert
    if not os.path.isdir(mode_path):
        print(f"Verzeichnis für Spielmodus '{gamemode}' existiert nicht: {mode_path}")
        return None

    return mode_path


# Es wird noch eine Funktion benötigt, die je nach Gamemode einen Fragenpool aus mehreren Verzeichnissen bildet

def json_to_object(directory):
    questions = []
    errors = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)

                    if data['type'] == 'drag_drop_order':
                        question = DragDropOrder(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    elif data['type'] == 'drag_drop_pairs':
                        question = DragDropPairs(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            pairs=data['pairs']
                        )
                    elif data['type'] == 'dropdown':
                        question = DropDown(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    elif data['type'] == 'multiple_choice':
                        question = MultipleChoice(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    else:
                        print(f"Unbekannter Fragetyp: {data['type']} in Datei {filename}")
                        continue

                    questions.append(question)
            except Exception as e:
                errors.append(f"Fehler beim Laden der Frage aus {filename}: {e}")
    return questions, errors


def shuffle_questionpool(questions): # Die Liste mit Fragen wird durchgemischt 
    random.shuffle(questions)

