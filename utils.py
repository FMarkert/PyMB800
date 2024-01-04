import os
import json
import random
import models


def gamemode_directory(gamemode):
    
    base_dir = os.path.abspath(os.path.dirname(__file__))

 
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
                        question = models.Drag_Drop_Order(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],  # Hinzufügen des fehlenden Parameters
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                        )
                    elif data['type'] == 'drag_drop_pairs':
                        question = models.Drag_Drop_Pairs(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],  # Hinzufügen des fehlenden Parameters
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items']
                        )
                    elif data['type'] == 'dropdown':
                        question = models.Dropdown(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],  # Hinzufügen des fehlenden Parameters
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    elif data['type'] == 'multiple_choice':
                        question = models.Multiple_Choice(
                            id=data['id'],
                            question_text=data['question_text'],
                            src=data['src'],
                            type=data['type'],  # Hinzufügen des fehlenden Parameters
                            comment=data.get('comment', ''),
                            casestudy=data.get('casestudy', ''),
                            items=data['items'],
                            correct_answer=data['correct_answer']
                        )
                    else:
                        print(f"Unbekannter Fragetyp: {data['type']} in Datei {filename}")
                        continue

                    question_dict = object_to_dict(question)
                    questions.append(question_dict)
            except Exception as e:
                error_message = f"Fehler beim Laden der Frage aus {filename}: {e}"
                errors.append(error_message)
    return questions, errors                  



def shuffle_questionpool(questions): # Die Liste mit Fragen wird durchgemischt 
    random.shuffle(questions)

def start_demo():
    gamemode = "l4d_1-40"
    directory = gamemode_directory(gamemode)
    questions, errors = json_to_object(directory)
    user_answers = {}
    user_answers_list = []
    user_results = []
    return questions, errors, user_answers, user_results, user_answers_list

def object_to_dict(obj):
    if obj.type == 'drag_drop_pairs' or obj.type == 'drag_drop_order':
        return {
            'id': obj.id,
            'question_text': obj.question_text,
            'src': obj.src,
            'type': obj.type,
            'comment': obj.comment,
            'casestudy': obj.casestudy,
            'items': obj.items
        }
    else:
        return {
            'id': obj.id,
            'question_text': obj.question_text,
            'src': obj.src,
            'type': obj.type,
            'comment': obj.comment,
            'casestudy': obj.casestudy,
            'items': obj.items,
            'correct_answer': obj.correct_answer
        }

def check_answer(current_question, user_answer):
    if current_question['type'] == 'drag_drop_order' or current_question['type'] == 'drag_drop_pairs':
        user_result = user_answer == current_question['items']
    else:
        user_result = user_answer == current_question['correct_answer']
    return user_result

def catch_results(user_result,current_question,user_results):
    key_found = False

    for i, d in enumerate(user_results):
        if str(current_question['id']) in d:
            user_results[i] = user_result
            key_found = True
            break
    if not key_found:
        user_results.append(user_result)

    return user_results

def catch_answer(user_answer,user_answers_list ,current_question):
    user_answers = {}
    user_answers[current_question['id']] = user_answer
    user_answers_list.append(user_answers)
    return user_answers_list
        