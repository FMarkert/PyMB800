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
        

def generate_print_data(questions_origin,user_answers_list):

    print_list = []
    questions = questions_origin
        
    for question in questions:
            if question.get('type') == 'dropdown':  # Relevante Daten für Fragetyp Dropdown
                id = question.get('id')
                question_type = question.get('type')
                question_text = question.get('question_text')
                items_raw = question.get('items') # Dictionary - Schlüssel sind Nummerierung und Werte sind Dictionary mit Textteil der Antwort und den optionen
                items = []
                for i in items_raw:
                    item = items_raw[i]
                    items.append(item)    
                correct_answer = question.get('correct_answer')
                user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
                print_unit = [question_type, id, question_text, items, correct_answer, user_answer]
                print(print_unit)
                print_list.append(print_unit)            

                #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
                # Item i, options, correct_answer i, user_answer i

            elif question.get('type') == 'multiple_choice':
                id = question.get('id')
                question_type = question.get('type')

                question_text = question.get('question_text')
                items = question.get('items') # Dictionary mit Aufzählung (A-Z) als Schlüssel und den Antwortmöglichkeiten als Werten

                correct_answer = question.get('correct_answer') # Liste mit den Schlüsseln der korrekten Antworten
                user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
                print_unit = [question_type, id, question_text, items, correct_answer, user_answer]
                print_list.append(print_unit)
                #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
                # Werte aus items_raw aufgelistet untereinander mit den Schlüsseln als Aufzählungszeichen, dann correct_answer, dann user_answer
            
            elif question.get('type') == 'drag_drop_order':
                id = question.get('id')
                question_type = question.get('type')
                question_text = question.get('question_text')
                items = question.get('items') # Dictionary mit Zahlen als String, die die Reihenfolge darstellen sollen als Schlüssel und der jeweiligen Antwort als Schlüssel
                user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
                print_unit = [question_type, id, question_text, items, user_answer]
                print_list.append(print_unit)
            
                
                #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
                # Werte aus items_raw aufgelistet untereinander mit den Schlüsseln als Aufzählungszeichen stellt die richtige Antwort da, danach user_answer in gleicher Form darstellen
            
            elif question.get('type') == 'drag_drop_pairs':
                id = question.get('id')
                question_type = question.get('type')
                question_text = question.get('question_text')
                items = question.get('items') # Dictionary: Schlüssel und Wert geben immer ein Paar
                user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
                print_unit = [question_type, id, question_text, items, user_answer]
                print_list.append(print_unit)

                #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
                #Schlüssel und Werte aus items_raw sollen jeweils in einer eingenen Zeile aufgelistet untereinenderstehen, danach soll user_answer im gleichen Stil angezeigt werden
    
    return print_list