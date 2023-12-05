import tkinter as tk
import sys
import os

act_path = os.path.dirname(os.path.abspath(__file__))
func_path =  os.path.join(act_path, '..', 'utils')
class_path = os.path.join(act_path, '..', 'models')
if func_path not in sys.path:
    sys.path.append(func_path)
if class_path not in sys.path:
    sys.path.append(class_path)

import functions
import classes 


def main():
    root = tk.Tk()
    root.title("PyMB800")
    root.geometry("1000x1000")

    logo = tk.Label(root, text="PyMB800", font=("Roboto",45,'bold','italic'), bg='orange',fg="blue")
    logo.pack(pady=25)
    button1 =  tk.Button(root, text="START DEMO", font=("Roboto",45,'bold','italic'), bg='orange',fg="blue", command=lambda: start_demo(root))
    button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()


class QuizFrame(tk.Frame):
    def __init__(self, parent, questions):
        super().__init__(parent) # Initialisiert den Frame als Teil des übergeordneten tk-Objekts
        self.questions = questions # Speichert die Liste der Fragenobjekte
        self.current_question_index = 0 # Startet mit der ersten Frage
        self.user_answers = {} # Dictnionary zum Speichern von Nutzerantworten 
        self.temp_user_answer = None # Temporärer Speicher für die aktuelle Benutzerantwort
        self.create_widgets() # Erstellt die Widgets im Frame

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", font=("Roboto", 20))
        self.question_label.pack(pady=20)
        # Hier können weitere Widgets wie Buttons oder Eingabefelder hinzugefügt werden

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

        self.temp_user_answer = []  # Initialisiere temp_user_answer für DDO-Fragen als Liste
        self.entry_widgets = []  # Liste zum Speichern der Entry-Widgets

        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()

        for item in question.items:
            frame = tk.Frame(self)
            frame.pack(pady=5, anchor='center')

            entry = tk.Entry(frame, width=2)
            entry.pack(side=tk.LEFT)
            self.entry_widgets.append(entry)  # Füge das Entry-Widget zur Liste hinzu

            label = tk.Label(frame, text=item, font=('Roboto', 20))
            label.pack(side=tk.LEFT)

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10, anchor='center')



    def create_ddp_widget(self, question):
        self.temp_user_answer = {}  # Initialisiere temp_user_answer für DDP-Fragen als Dictionary

        all_options = set()  # Ein Set, um Duplikate zu vermeiden
        for value in question.pairs.values():
            all_options.add(value)
        all_options = list(all_options)  # Konvertiere das Set zurück in eine Liste

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

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)

  
    def create_mc_widget(self, question):
        self.temp_user_answer = []  # Initialisiere temp_user_answer für MC-Fragen als Liste
        self.mc_vars = {}  # Dictionary zum Speichern der Variablen für jeden Radiobutton

        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()

        for option_key, option_text in question.items.items():
            var = tk.BooleanVar(value=False)
            self.mc_vars[option_key] = var
            rb = tk.Radiobutton(self, text=f"{option_key}: {option_text}", variable=var, value=option_key, font=('Roboto', 20))
            rb.pack(anchor='center')

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)


    def create_dd_widget(self, question):
        for widget in self.winfo_children():
            if widget != self.question_label:
                widget.destroy()

        self.temp_user_answer = {}  # Initialisiere temp_user_answer für Dropdown-Fragen als Dictionary

        for item in question.items:
            frame = tk.Frame(self)
            frame.pack(pady=5, anchor='center')

            label = tk.Label(frame, text=item['text'], font=('Roboto', 20))
            label.pack(side=tk.LEFT)

            selected_value = tk.StringVar(frame)
            dropdown = tk.OptionMenu(frame, selected_value, *item['options'])
            dropdown.pack(side=tk.LEFT)

            # Speichere die StringVar für jede Dropdown-Option
            self.temp_user_answer[item['text']] = selected_value

        submit_button = tk.Button(self, text="Antwort bestätigen", command=lambda: self.submit_and_load_next(question))
        submit_button.pack(pady=10)

    def collect_user_answer(self, question):
        if isinstance(question, classes.Drag_Drop_Order):
            self.user_answers[question.id] = [entry.get() for entry in self.entry_widgets]
        elif isinstance(question, classes.Multiple_Choice):
            selected_options = [key for key, var in self.mc_vars.items() if var.get() == key]
            self.user_answers[question.id] = selected_options
        elif isinstance(question, classes.Drag_Drop_Pairs):
            pairs_answers = {key: var.get() for key, var in self.temp_user_answer.items()}
            self.user_answers[question.id] = pairs_answers
        elif isinstance(question, classes.Dropdown):
            self.user_answers[question.id] = {key: var.get() for key, var in self.temp_user_answer.items()}
        print(self.user_answers)

    def submit_and_load_next(self, question): # Funktion für das Laden der nächsten Frage
        self.collect_user_answer(question)
        self.load_question()
            

    def handle_quiz_end(self):
        # Logik, was passiert, wenn das Quiz endet (z.B. Ergebnisse anzeigen)
        pass
    
    def check_answer(self, question):
        # Logik zum bestätigen der Antwort
        pass


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
    
