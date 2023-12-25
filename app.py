import utils
import models
from flask import Flask, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Ein zufälliger Schlüssel für Sessions


@app.route('/')
def index():
    return render_template('index.html')

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



if __name__ == '__main__':
    app.run(debug=True)
