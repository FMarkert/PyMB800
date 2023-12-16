import tkinter as tk
from tkinter import messagebox
import classes 


class QuizFrame(tk.Frame):
    
    def __init__(self, parent, questions):
        super().__init__(parent) # Initialisiert den Frame als Teil des übergeordneten tk-Objekts
        self.questions = questions # Speichert die Liste der Fragenobjekte
        self.current_question_index = 0 # Startet mit der ersten Frage
        self.user_answers = {} # Dictnionary zum Speichern von Nutzerantworten 
        self.user_score = {} # Dictionary zum Punktestand des Nutzers 
        self.temp_user_answer = None # Temporärer Speicher für die aktuelle Benutzerantwort
        self.mc_vars = {}
        self.question_label = tk.Label(self, text="", font=("Roboto", 20))
        self.back_button = tk.Button(self, text="Zurück", command=self.go_back)
        self.next_button = tk.Button(self, text="Weiter", command=self.go_next)
        self.question_label = tk.Label(self, text="", font=("Roboto", 20))
        self.create_widgets() # Erstellt die Widgets im Frame

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)
        self.rowconfigure(6, weight=0)
        self.rowconfigure(7, weight=0)
        self.question_label.grid(row=0, column=3, pady=20)
        self.question_label.config(justify="center")
        self.back_button.grid(row=6, column=3, padx=10)
        self.next_button.grid(row=6, column=4, padx=10)

         
    def cancel_quiz(self):
        response = messagebox.askyesno("Quiz abbrechen", "Bro, bist du sicher, dass du das Quiz abbrechen möchtest?")
        if response:
            self.grid_forget()  # Aktuellen Quiz-Frame ausblenden
            self.master.deiconify()  # Hauptfenster wieder anzeigen

    def go_back(self):
            self.current_question_index -= 2
            self.load_question()

    def go_next(self):
        if self.current_question_index < len(self.questions):
            self.load_question()

    def load_question(self):
        
        if self.current_question_index < len(self.questions): # Überprüft, ob noch Fragen vorhanden sind
            question = self.questions[self.current_question_index] # Hole die aktuelle Frage

            self.question_label.config(text=question.display_question_text()) # Zeige den Fragetext an

            if isinstance(question, classes.Drag_Drop_Order):
                self.create_ddo_widget(question)
            elif isinstance(question,classes.Drag_Drop_Pairs):
                self.create_ddp_widget(question)
            elif isinstance(question, classes.Multiple_Choice):
                self.create_mc_widget(question)
            elif isinstance(question, classes.Dropdown):
                self.create_dd_widget(question)
            else:
                print("Fragenart nicht gefunden")

            self.current_question_index += 1 # Inkrementiere den Index für die nächste Frage
        else:
            self.handle_quiz_end() # Wenn keine weiteren Fragen vorhanden sind, beende das Quiz