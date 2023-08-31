from tkinter import *
from tkinter import simpledialog

root = Tk()
root.title("To-Do-list")
root.geometry("400x650+470+25")
root.resizable(False, False)

task_list = []

def edit_task(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_task = task_list[selected_index[0]]
        updated_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=selected_task['task'])

        if updated_task:
            selected_task['task'] = updated_task
            listbox.delete(selected_index)
            listbox.insert(selected_index, format_task(selected_task))
            with open("tasklist.txt", "w") as taskfile:
                for task in task_list:
                    taskfile.write(f"{task['task']}\n{task['completed']}\n")

def format_task(task):
    return f"[{'✔' if task['completed'] else ' '}] {task['task']}"

def toggle_completion_status(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_task = task_list[selected_index[0]]
        selected_task['completed'] = not selected_task['completed']
        listbox.delete(selected_index)
        listbox.insert(selected_index, format_task(selected_task))

def addTask():
    task_text = task_entry.get()
    task_entry.delete(0, END)
    if task_text:
        task = {'task': task_text, 'completed': False}
        task_list.append(task)
        with open("tasklist.txt", "a") as taskfile:
            taskfile.write(f"\n{task['task']}\n{task['completed']}\n")
        listbox.insert(END, format_task(task))

def deleteTask():
    selected_index = listbox.curselection()
    if selected_index:
        task_list.pop(selected_index[0])
        listbox.delete(selected_index)
        with open("tasklist.txt", "w") as taskfile:
            for task in task_list:
                taskfile.write(f"{task['task']}\n{task['completed']}\n")

def openTaskFile():
    try:
        global task_list
        with open("tasklist.txt", "r") as taskfile:
            lines = taskfile.readlines()

        for i in range(0, len(lines), 2):
            task_text = lines[i].strip()
            completed = lines[i + 1].strip() == "True"
            task_list.append({'task': task_text, 'completed': completed})
            listbox.insert(END, format_task(task_list[-1]))
    except:
        file = open("tasklist.txt", "w")
        file.close()

image_icon = PhotoImage(file="assets/images/task.png")
root.iconphoto(False, image_icon)

top_image = PhotoImage(file="assets/images/topbar.png")
Label(root, image=top_image).pack()

dock_image = PhotoImage(file="assets/images/dock.png")
Label(root, image=dock_image, bg="#32405b").place(x=30, y=25)

note_image = PhotoImage(file="assets/images/task.png")
Label(root, image=note_image, bg="#32405b").place(x=340, y=25)

heading = Label(root, text="ALL TASK", font="arial 20 bold", fg="white", bg="#32405b")
heading.place(x=130, y=20)

frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=180)

task_entry = Entry(frame, width=18, font="arial 20", bd=0)
task_entry.place(x=10, y=7)
task_entry.focus()

button = Button(frame, text="ADD", font="arial 20 bold", width=6, bg="#5a95ff", fg="#fff", bd=0, command=addTask)
button.place(x=300, y=0)

frame_listbox = Frame(root, bd=3, width=700, height=280, bg="#32405b")
frame_listbox.pack(pady=(160, 0))

listbox = Listbox(frame_listbox, font=('arial', 12), width=40, height=16, bg="#32405b", fg="white",
                cursor="hand2", selectbackground="#5a95ff")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame_listbox)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

openTaskFile()

del_icon = PhotoImage(file="assets/images/delete.png")
Button(root, image=del_icon, bd=0, command=deleteTask).pack(side=BOTTOM, pady=13)

listbox.bind("<Button-3>", edit_task)
listbox.bind("<Button-1>", toggle_completion_status)

root.mainloop()
