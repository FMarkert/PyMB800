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
    button1 =  tk.Button(root, text="START DEMO", font=("Roboto",45,'bold','italic'), bg='orange',fg="blue", command=start_demo)
    button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()


class QuizFrame(tk.Frame):
    def __init__(self, parent, questions):
        super().__init__(parent) # Initialisiert den Frame als Teil des übergeordneten tk-Objekts
        self.questions = questions # Speichert die Liste der Fragen
        self.current_question_index = 0 # Startet mit der ersten Frage
        self.create_widgets() # Erstellt die Widgets im Frame

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", font=("Roboto", 20))
        self.question_label.pack(pady=20)
        # Hier können weitere Widgets wie Buttons oder Eingabefelder hinzugefügt werden

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question.display_question_text())
            # Weitere Logik zum Anzeigen der spezifischen Frageelemente
            self.current_question_index += 1
        else:
            self.handle_quiz_end()

    def handle_quiz_end(self):
        # Logik, was passiert, wenn das Quiz endet (z.B. Ergebnisse anzeigen)
        pass


def start_demo():
    gamemode = "l4d_1-40"
    directory = functions.gamemode_directory(gamemode)
    questions = functions.json_to_object(directory)
    print(questions)
    return questions


if __name__ == "__main__":
    main()
