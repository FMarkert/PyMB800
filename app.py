import utils
import models
from flask import Flask, render_template, session, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Ein zufälliger Schlüssel für Sessions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    items = {
        "Customer Posting Group": "Specific posting group",
        "Gen. Business Posting Group": "General posting group",
        # Füge hier weitere Paare hinzu
    }
    return render_template('test.html', items=items)

@app.route('/start_demo')
def demo():
    questions, errors, user_answers, user_results = utils.start_demo()
    session['questions'] = questions
    session['errors'] = errors
    session['user_answers'] = user_answers
    session['user_results'] = user_results

    return redirect(url_for('checkpage'))

@app.route('/checkpage')
def checkpage():
    base_dir = session.get('base_dir')
    directory = session.get('directory')
    questions = session.get('questions', [])
    errors = session.get('errors', [])
    return render_template('check_page.html', base_dir=base_dir, directory=directory, questions=questions, errors=errors)

@app.route('/quiz')
def quiz():
    current_question_index = session.get('current_question_index', 0)

    questions = session.get('questions', [])

    if not questions:
        return redirect(url_for('index'))

    current_question = questions[current_question_index]
    return render_template('quiz.html', question=current_question, question_index=current_question_index, total_questions=len(questions))
    

@app.route('/change_question')
def change_question():
    direction = request.args.get('direction', 'next')
    current_question_index = session.get('current_question_index', 0)
    questions = session.get('questions', [])
    
    if direction == 'next':
        current_question_index = min(current_question_index + 1, len(questions) - 1)
    elif direction == 'prev':
        current_question_index = max(current_question_index - 1, 0)
    
    session['current_question_index'] = current_question_index
    return redirect(url_for('quiz'))

@app.route('/end_quiz')
def end_quiz():
    session.clear()
    return redirect(url_for('index'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    current_question_index = session.get('current_question_index', 0)
    questions = session.get('questions', [])

    # Debugging-Ausgaben
    print(f"Current question index: {current_question_index}")
    print(f"Number of questions: {len(questions)}")

    # Überprüfung, ob der Index im gültigen Bereich liegt
    if current_question_index >= len(questions):
        print("Error: current_question_index is out of range.")
        return redirect(url_for('index'))

    current_question = questions[current_question_index]

    # Debugging: Ausgabe der POST-Daten
    print("POST-Daten:", request.form)

    if current_question['type'] == 'drag_drop_order':
        user_answer = {}
        ordered_ids = request.form.getlist('order-list')
        for index, item_id in enumerate(ordered_ids):
            user_answer[str(index + 1)] = current_question['items'][item_id]
        print(current_question['items'])
        print(f"user_answer = {user_answer}")
        user_result = utils.check_answer(current_question, user_answer)
        print(f"User_Answer = {current_question['id']} : {user_answer}")
        print(f"User_Result = {current_question['id']} : {user_result}")

    elif current_question['type'] == 'drag_drop_pairs':
        user_answer = {}
        keys_order = request.form.get('keys-order').split(',')
        values_order = request.form.get('values-order').split(',')
        for key, value in zip(keys_order, values_order):
            user_answer[key] = current_question['items'][value]
        user_result = utils.check_answer(current_question, user_answer)
        print(f"User_Answer = {current_question['id']} : {user_answer}")
        print(f"User_Result = {current_question['id']} : {user_result}")

    elif current_question['type'] == 'dropdown':
        user_answer = request.form.getlist(f'answer_{current_question["id"]}')
        user_result = utils.check_answer(current_question, user_answer)
        print(f"User_Answer = {current_question['id']} : {user_answer}")
        print(f"User_Result = {current_question['id']} : {user_result}")

    elif current_question['type'] == 'multiple_choice':
        user_answer = []
        for key in request.form.keys():
                user_answer =request.form.getlist(key)
        print(f"User_Answer = {current_question['id']} : {user_answer}")
        user_result = utils.check_answer(current_question, user_answer)
        print(f"User_Result = {current_question['id']} : {user_result}")

#answer_{{ question.id }}[]

    # Aktualisieren des Frage-Indexes
    session['current_question_index'] = min(current_question_index + 1, len(questions) - 1)
    return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True)

