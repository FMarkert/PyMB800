import tkinter as tk
from tkinter import messagebox
import sys
import os
import functions
import classes


def main():
    root = tk.Tk()
    root.title("PyMB800")

   
    root.attributes('-fullscreen', True) # Aktivieren des Vollbildmodus

    logo = tk.Label(root, text="PyMB800", font=("Roboto", 45, 'bold', 'italic'), bg='blue', fg="orange")
    logo.pack(pady=25)
    button1 = tk.Button(root, text="START DEMO", font=("Roboto", 45, 'bold', 'italic'), bg="blue", fg="orange", command=lambda: start_demo(root))
    button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()




class QuizFrame(tk.Frame):
    def __init__(self, parent, questions):
        super().__init__(parent) # Initialisiert den Frame als Teil des übergeordneten tk-Objekts
        self.questions = questions # Speichert die Liste der Fragenobjekte
        self.current_question_index = 0 # Startet mit der ersten Frage
        self.user_answers = {} # Dictnionary zum Speichern von Nutzerantworten 
        self.user_score = {} # Dictionary zum Punktestand des Nutzers 
        self.temp_user_answer = None # Temporärer Speicher für die aktuelle Benutzerantwort
        self.mc_vars = {}
        self.cancel_button = None # Abbruch-Button initialisieren
        self.create_widgets() # Erstellt die Widgets im Frame

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", font=("Roboto", 20))
        self.question_label.pack(pady=20)
        self.back_button = tk.Button(self, text="Zurück", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(self, text="Weiter", command=self.go_next)
        self.next_button.pack(side=tk.RIGHT, padx=10)
         
    def cancel_quiz(self):
        response = messagebox.askyesno("Quiz abbrechen", "Bro, bist du sicher, dass du das Quiz abbrechen möchtest?")
        if response:
            self.pack_forget()  # Aktuellen Quiz-Frame ausblenden
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


    def create_ddo_widget(self, question):
        self.temp_user_answer = []  # Liste zum Speichern der ausgewählten Indizes
        self.dropdown_vars = []  # Liste zum Speichern der StringVar-Objekte

        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()

        for item in question.items:
            frame = tk.Frame(self)
            frame.pack(pady=5, anchor='center')

            dropdown_var = tk.StringVar(frame)
            self.dropdown_vars.append(dropdown_var)
        
            options = list(range(1, len(question.items) + 1)) # Erstellen der Dropdown-Menüoptionen (1 bis Anzahl der Antworten)
            dropdown = tk.OptionMenu(frame, dropdown_var, *options)
            dropdown.pack(side=tk.LEFT)

            label = tk.Label(frame, text=item, font=('Roboto', 20)) # Erstellen eines Labels neben dem Dropdown-Menü für die Antwortmöglichkeit
            label.pack(side=tk.LEFT)

            self.temp_user_answer.append(dropdown_var)

        back_button = tk.Button(self, text="Zurück", command=self.go_back)
        back_button.place(relx=0.5, rely=1.0, x=-60, y=-10, anchor='s')

        next_button = tk.Button(self, text="Weiter", command=self.go_next)
        next_button.place(relx=0.5, rely=1.0, x=60, y=-10, anchor='s')

        self.cancel_button = tk.Button(self, text="Quiz abbrechen", command=self.cancel_quiz)
        self.cancel_button.place(relx=0.9, rely=1.0, x=-30, y=-10, anchor='s')

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10, anchor='center')


    def create_ddp_widget(self, question):
        self.temp_user_answer = {}  # Initialisiere temp_user_answer für DDP-Fragen als Dictionary

        all_options = set()  # Ein Set, um Duplikate zu vermeiden
        for value in question.pairs.values():
            all_options.add(value)
        all_options = list(all_options) # Konvertiere das Set zurück in eine Liste

        for widget in self.winfo_children():
                if widget != self.question_label:
                    widget.destroy()

        for key in question.pairs.keys():
                frame = tk.Frame(self)
                frame.pack(pady=5, anchor='center')

                label_key = tk.Label(frame, text=key, font=('Roboto', 20))
                label_key.pack(side=tk.LEFT)

                selected_value = tk.StringVar(frame)
                dropdown = tk.OptionMenu(frame, selected_value, *all_options)
                dropdown.pack(side=tk.LEFT)

                self.temp_user_answer[key] = selected_value  # Füge das StringVar-Objekt zum Dictionary hinzu

        back_button = tk.Button(self, text="Zurück", command=self.go_back)
        back_button.place(relx=0.5, rely=1.0, x=-60, y=-10, anchor='s')

        next_button = tk.Button(self, text="Weiter", command=self.go_next)
        next_button.place(relx=0.5, rely=1.0, x=60, y=-10, anchor='s')

        self.cancel_button = tk.Button(self, text="Quiz abbrechen", command=self.cancel_quiz)
        self.cancel_button.place(relx=0.9, rely=1.0, x=-30, y=-10, anchor='s')
        
        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)

  
    def create_mc_widget(self, question):
        self.temp_user_answer = []  # Initialisiere temp_user_answer für MC-Fragen als Liste
        self.mc_vars = {}  # Dictionary zum Speichern der Variablen für jeden Radiobutton

        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()
        
        def toggle_option(key):
            self.mc_vars[key] = not self.mc_vars.get(key, False)   # Kehrt den Wert um, wenn die Checkbox angeklickt wird

        for option_key, option_text in question.items.items():
                # Setzt den Anfangswert des booleschen Wertes
                self.mc_vars[option_key] = False
                cb = tk.Checkbutton(self, text=f"{option_key}: {option_text}", command=lambda key=option_key: toggle_option(key), font=('Roboto', 20))
                cb.pack(anchor='center')

        back_button = tk.Button(self, text="Zurück", command=self.go_back)
        back_button.place(relx=0.5, rely=1.0, x=-60, y=-10, anchor='s')

        next_button = tk.Button(self, text="Weiter", command=self.go_next)
        next_button.place(relx=0.5, rely=1.0, x=60, y=-10, anchor='s')

        self.cancel_button = tk.Button(self, text="Quiz abbrechen", command=self.cancel_quiz)
        self.cancel_button.place(relx=0.9, rely=1.0, x=-30, y=-10, anchor='s')
        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)

    def create_dd_widget(self, question):
        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()

        self.temp_user_answer = []  # Initialisiere temp_user_answer für Dropdown-Fragen als Dictionary


        for item in question.items:
            frame = tk.Frame(self)
            frame.pack(pady=5, anchor='center')

            label = tk.Label(frame, text=item['text'], font=('Roboto', 20))
            label.pack(side=tk.LEFT)

            selected_value = tk.StringVar(frame)
            dropdown = tk.OptionMenu(frame, selected_value, *item['options'])
            dropdown.pack(side=tk.LEFT)

            self.temp_user_answer.append(selected_value)

        back_button = tk.Button(self, text="Zurück", command=self.go_back)
        back_button.place(relx=0.5, rely=1.0, x=-60, y=-10, anchor='s')

        next_button = tk.Button(self, text="Weiter", command=self.go_next)
        next_button.place(relx=0.5, rely=1.0, x=60, y=-10, anchor='s')

        self.cancel_button = tk.Button(self, text="Quiz abbrechen", command=self.cancel_quiz)
        self.cancel_button.place(relx=0.9, rely=1.0, x=-30, y=-10, anchor='s')

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)


    def collect_user_answer(self, question):
        if isinstance(question, classes.Drag_Drop_Order):
            user_answer = []
            for dropdown_var in self.dropdown_vars:
                try:
                    idx = int(dropdown_var.get()) - 1
                    if 0 <= idx < len(question.items):
                        user_answer.append(question.items[idx])
                    else:
                        user_answer.append("Ungültiger Index")
                except ValueError:
                    user_answer.append("Keine gültige Zahl")
            self.user_answers[question.id] = user_answer
            self.check_answers(question, user_answer)
        elif isinstance(question, classes.Multiple_Choice):
            print(f"Das ist self.mc.vars: {self.mc_vars}")
            selected_options = [key for key, value in self.mc_vars.items() if value == True] # Packt vom Anwender gewählte Optionen in eine Liste
            user_answer = [] # Liste zum Vergleichen der User Antworten mit den korrekten Antworten
            for key in selected_options:
                user_answer.append(key)
            print(f"Das sind die gewählten Antworten: {user_answer}")
            self.user_answers[question.id] = selected_options
            self.check_answers(question, user_answer)
        elif isinstance(question, classes.Drag_Drop_Pairs):
            user_answer = {key: var.get() for key, var in self.temp_user_answer.items()}
            print(f"Die user_answer für die DDP Frage lautet: {user_answer}")
            self.user_answers[question.id] = user_answer
            self.check_answers(question, user_answer)
        elif isinstance(question, classes.Dropdown):
            self.user_answers[question.id] = [var.get() for var in self.temp_user_answer]  # Speichert die tatsächlichen ausgewählten Werte aus den StringVar-Objekten
            user_answer = [var.get() for var in self.temp_user_answer]
            print(f"Dropdown User Answer:{user_answer}")
            self.check_answers(question, user_answer)
        print(self.user_answers)

    def submit_and_load_next(self, question): # Funktion für das Laden der nächsten Frage
        self.collect_user_answer(question)
        self.load_question()
            
    def check_answers(self,question,user_answer): # Logik zum Überprüfen der Antwort
        answer_to_check = question.check_answer(user_answer)
        self.user_score[question.id] = answer_to_check 
        print(f"answer_to_check lautet {answer_to_check} und self.user_score lautet {self.user_score}")  

   
    def handle_quiz_end(self): # Logik, was passiert, wenn das Quiz endet (z.B. Ergebnisse anzeigen, danach zum Hauptmenü)     
        total_questions = len(self.questions)
        correct_answers = sum(self.user_score.values())  
        stats = {"total": total_questions, "correct": correct_answers}
        
        self.pack_forget()  # Aktuellen Quiz-Frame ausblenden
        end_frame = QuizEndFrame(self.master, self, self.master, stats)  # Neuen Frame für Quiz-Ende erstellen
        end_frame.pack(fill='both', expand=True)  # Neuen Frame anzeigen
    
class QuizEndFrame(tk.Frame):
    def __init__(self, parent, main_frame, root, stats):
        super().__init__(parent)
        self.main_frame = main_frame  # Referenz zum Haupt-Frame
        self.root = root  # Referenz zum Hauptfenster (root)
        self.stats = stats

        label = tk.Label(self, text="Quiz beendet", font=("Roboto", 20)) # Label für "Quiz beendet"
        label.pack(pady=20)

        stats_label = tk.Label(self, text=f"Richtig beantwortete Fragen: {self.stats['correct']}/{self.stats['total']}", font=("Roboto", 20))
        stats_label.pack(pady=20)

        if self.stats['correct'] / self.stats['total'] >= 0.9:
            pass_label = tk.Label(self, text="Glückwunsch!!!", font=("Roboto", 20))
            pass_label.pack(pady=20)
        else:
            pass_label = tk.Label(self, text="Schade!!!", font=("Roboto", 20))
            pass_label.pack(pady=20)

        self.pack_propagate(0)  # Verhindert, dass sich der Frame an den Inhalt anpasst
        spacer = tk.Frame(self, height=300)  # Ändern Sie die Höhe nach Bedarf
        spacer.pack(fill='both', expand=True)

        back_button = tk.Button(self, text="Zurück zur Hauptseite", command=self.back_to_main) # Button, um zum Haupt-Frame zurückzukehren
        back_button.pack(anchor='se', padx=10, pady=10)

    def back_to_main(self):
        self.destroy()  # Aktuellen Frame schließen
        self.root.deiconify()  # Hauptfenster wieder anzeigen

def start_demo(root):
    gamemode = "l4d_1-40"
    directory = functions.gamemode_directory(gamemode)
    questions = functions.json_to_object(directory)  
    if not questions: #Überprüft ob Fragen geladen wurden
        print ('Keine Fragen geladen') 
    quiz_frame = QuizFrame(root, questions)
    quiz_frame.pack(fill='both', expand=True)

    quiz_frame.load_question()



if __name__ == "__main__":
    main()
