from django.shortcuts import render, redirect

# Ihre Startseite-View
def index(request):
    return render(request, 'index.html')

# Die View, die aufgerufen wird, wenn der "START DEMO"-Button gedrückt wird
def start_quiz(request):
    # Leiten Sie hier zu Ihrer Quiz-Logik weiter
    return redirect('quiz_page')
