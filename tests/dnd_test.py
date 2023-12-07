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
    if event.widget is not root and event.widget != submit_button:
        root.dragged_widget = event.widget
        event.widget.lift()
        root.marked_pointx = root.winfo_pointerx()
        root.marked_pointy = root.winfo_pointery()

def finalize_dragging(event):
    root.dragged_widget = None

def submit():
    label_positions = {label.cget("text"): label.winfo_y() for label in labels}
    sorted_labels = dict(sorted(label_positions.items(), key=lambda item: item[1]))
    placements = {label: f"{idx+1}." for idx, label in enumerate(sorted_labels)}
    print(placements)

root = tk.Tk()

root.event_add('<<Drag>>', '<B1-Motion>')
root.event_add('<<DragInit>>', '<ButtonPress-1>')
root.event_add('<<DragFinal>>', '<ButtonRelease-1>')

root.bind('<<DragInit>>', drag_init)
root.bind('<<Drag>>', drag_widget)
root.bind('<<DragFinal>>', finalize_dragging)

root.event_generate('<<DragFinal>>')

labels = []
for i, color in enumerate(['yellow', 'red', 'green', 'orange']):
    label = tk.Label(root, text=f"Test {i+1}", bg=color)
    label.pack()
    labels.append(label)

# Spacer hinzufügen
spacer = tk.Frame(root, height=50)
spacer.pack()

# Submit-Button (nicht verschiebbar)
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
