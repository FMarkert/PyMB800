import tkinter as tk
from tkinter import messagebox
import sys
import os
import core_functions
import classes
import quizframe
import quiz_endframe



def main():
    root = tk.Tk()
    root.title("PyMB800")

    # Konfigurieren der Spalten und Zeilen für eine gleichmäßige Verteilung
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)

    root.attributes('-fullscreen', True) # Aktivieren des Vollbildmodus

    # Logo
    logo = tk.Label(root, text="PyMB800", font=("Roboto", 45, 'bold', 'italic'), bg='blue', fg="orange")
    logo.grid(row=0, column=1, sticky='n', pady=25)

    # Button
    button1 = tk.Button(root, text="START DEMO", font=("Roboto", 45, 'bold', 'italic'), bg="blue", fg="orange", command=lambda: start_demo(root))
    button1.grid(row=2, column=1, sticky='n')

    root.mainloop()

def start_demo(root):
    # Entferne den vorhandenen Inhalt
    for widget in root.winfo_children():
        widget.grid_forget()

    gamemode = "l4d_1-40"
    directory = core_functions.gamemode_directory(gamemode)
    questions = core_functions.json_to_object(directory)  
    if not questions:  # Überprüft ob Fragen geladen wurden
        print('Keine Fragen geladen')
        return
    quiz_frame = quizframe.QuizFrame(root, questions) # Erstelle den Quiz-Frame und füge ihn mit grid hinzu

    root.columnconfigure(0, weight=1) # Konfiguriere die Spalten und Zeilen für den Quiz-Frame
    root.rowconfigure(0, weight=1)

    quiz_frame.grid(row=0, column=0, sticky="nsew") # Füge den Quiz-Frame hinzu
  
    quiz_frame.load_question()  # Lade die erste Frage

if __name__ == "__main__":
    main()
