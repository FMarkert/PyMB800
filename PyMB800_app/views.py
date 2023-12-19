from django.shortcuts import render, redirect
from PyMB800_app.utils import gamemode_directory, json_to_object, shuffle_questionpool


# Ihre Startseite-View
def index(request):
    return render(request, 'index.html')

# Die View, die aufgerufen wird, wenn der "START DEMO"-Button gedrückt wird
def start_quiz(request):
    gamemode = "l4d_1-40"
    directory = gamemode_directory(gamemode)
    questions, errors = json_to_object(directory)
    #shuffle_questionpool(questions)
    # Daten an das Template übergeben
    return render(request, 'check_page.html', {
        'questions': questions,
        'errors': errors
    })

def check_page(request):
    return render(request, 'check_page.html')

def quiz_page(request):
    return render(request, 'quiz_page.html')