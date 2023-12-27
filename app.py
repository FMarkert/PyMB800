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
    questions, errors = utils.start_demo()
    session['questions'] = questions
    session['errors'] = errors
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
        # Keine Fragen geladen, leite zur Startseite um
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
    # Setze die gesamte Session zurück
    session.clear()

    # Hier könntest du auch das Quiz-Ergebnis speichern oder weitere Aktionen durchführen

    return redirect(url_for('index'))  # Leite zurück zur Startseite


if __name__ == '__main__':
    app.run(debug=True)
