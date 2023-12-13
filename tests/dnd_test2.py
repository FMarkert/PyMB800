import tkinter as tk

def drag_widget(event):
    if (w:=root.dragged_widget):
        cx, cy = w.winfo_x(), w.winfo_y()
        dx = root.marked_pointx - root.winfo_pointerx()
        dy = root.marked_pointy - root.winfo_pointery()
        w.place(x=cx-dx, y=cy-dy)
        root.marked_pointx = root.winfo_pointerx()
        root.marked_pointy = root.winfo_pointery()

def drag_init(event):
    if event.widget in value_labels:
        root.dragged_widget = event.widget
        event.widget.lift()
        root.marked_pointx = root.winfo_pointerx()
        root.marked_pointy = root.winfo_pointery()

def finalize_dragging(event):
    root.dragged_widget = None

def submit():
    pairs = {}
    for key_label in key_labels:
        key = key_label.cget("text")
        closest_value_label = min(value_labels, key=lambda label: abs(label.winfo_y() - key_label.winfo_y()))
        value = closest_value_label.cget("text")
        pairs[key] = value
    print(pairs)

root = tk.Tk()

root.event_add('<<Drag>>', '<B1-Motion>')
root.event_add('<<DragInit>>', '<ButtonPress-1>')
root.event_add('<<DragFinal>>', '<ButtonRelease-1>')

root.bind('<<DragInit>>', drag_init)
root.bind('<<Drag>>', drag_widget)
root.bind('<<DragFinal>>', finalize_dragging)

key_labels = []
value_labels = []

for i in range(4):
    key_label = tk.Label(root, text=f"Key {i+1}", bg='lightgrey')
    value_label = tk.Label(root, text=f"Value {i+1}", bg='darkgrey')

    key_label.pack()
    value_label.place(x=100, y=i*30)  # Startposition der verschiebbaren Labels

    key_labels.append(key_label)
    value_labels.append(value_label)

# Spacer hinzufügen
spacer = tk.Frame(root, height=50)
spacer.pack()

# Submit-Button (nicht verschiebbar)
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
