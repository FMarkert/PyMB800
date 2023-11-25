import tkinter as tk


def main():
    root = tk.Tk()
    root.title("PyMB800")
    root.geometry("1000x1000")

    logo = tk.Label(root, text="PyMB800", font=("Roboto",45,'bold','italic'), bg='orange',fg="blue")
    logo.pack(pady=25)
    button1 =  tk.Button(root, text="START DEMO", font=("Roboto",45,'bold','italic'), bg='orange',fg="blue", command=start_demo)
    button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()


def start_demo():
    pass


if __name__ == "__main__":
    main()
