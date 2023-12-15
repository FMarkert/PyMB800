import tkinter as tk


class QuizEndFrame(tk.Frame):
    def __init__(self, parent, main_frame, root, stats):
        super().__init__(parent)
        self.main_frame = main_frame
        self.root = root
        self.stats = stats

        # Konfigurieren der Zeilen und Spalten
        self.columnconfigure(0, weight=1)
        for i in range(4):  # Angenommen, Sie haben 4 Zeilen
            self.rowconfigure(i, weight=1)

        # Hinzufügen der Widgets
        label = tk.Label(self, text="Quiz beendet", font=("Roboto", 20))
        label.grid(row=0, column=0, sticky="ew", pady=20)

        stats_label = tk.Label(self, text=f"Richtig beantwortete Fragen: {self.stats['correct']}/{self.stats['total']}", font=("Roboto", 20))
        stats_label.grid(row=1, column=0, sticky="ew", pady=20)

        # Bedingtes Label
        pass_label_text = "Glückwunsch!!!" if self.stats['correct'] / self.stats['total'] >= 0.9 else "Schade!!!"
        pass_label = tk.Label(self, text=pass_label_text, font=("Roboto", 20))
        pass_label.grid(row=2, column=0, sticky="ew", pady=20)

        # Zurück-Button
        back_button = tk.Button(self, text="Zurück zur Hauptseite", command=self.back_to_main)
        back_button.grid(row=3, column=0, sticky="e", padx=10, pady=10)


    def back_to_main(self):
        self.destroy()  # Aktuellen Frame schließen
        self.root.deiconify()  # Hauptfenster wieder anzeigen
