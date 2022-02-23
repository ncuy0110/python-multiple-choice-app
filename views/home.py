import json
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from question import Questions
from student import Student

large_font = ("Verdana", 35)

student = Student()

with open('../data.json', 'r') as openfile:
    data = json.load(openfile)

# create list question from file
qts = Questions(data)
qts.change_position()


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = page(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Welcome!", font=large_font)
        label.place(x=130, y=40)

        name = tk.Text(self, width=20, height=2)
        name.place(x=170, y=200)

        def next_page1():
            if name.get("1.0", "end-1c") == "":
                messagebox.showerror("Name", "Name is empty!")
            else:
                student.set_name(name.get("1.0", "end-1c"))
                controller.show_frame(Page1)

        button1 = ttk.Button(self, text="Next",
                             command=next_page1)
        button1.place(x=200, y=400)


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=f"Hello {student.name}!", font=large_font)
        label.place(x=130, y=40)

        lbl_clock = ttk.Label(self, text="00:00", font=("Courier", 20))
        lbl_clock.place(x=180, y=100)

        def countdown(seconds):
            while seconds > 0:
                lbl_clock.config(text=f"{seconds // 60}:{seconds % 60}")
                seconds -= 1
                time.sleep(1)
            controller.show_frame(Page2)

        thread_countdown = threading.Thread(target=countdown, args=(10,))
        thread_countdown.daemon = True
        thread_countdown.start()

        ques = qts.questions[student.selecting]

        lbl_question = ttk.Label(self, text=f"Question {student.selecting + 1}/10:{ques['question']}", wraplength=350)
        lbl_question.place(x=40, y=140)

        var = tk.IntVar()
        R0 = ttk.Radiobutton(self, text=ques['options'][0], variable=var, value=0)
        R0.place(x=60, y=180)

        R1 = ttk.Radiobutton(self, text=ques['options'][1], variable=var, value=1)
        R1.place(x=60, y=200)

        R2 = ttk.Radiobutton(self, text=ques['options'][2], variable=var, value=2)
        R2.place(x=60, y=220)

        R3 = ttk.Radiobutton(self, text=ques['options'][3], variable=var, value=3)
        R3.place(x=60, y=240)

        var.set(0)

        def pre_question():
            if student.selecting > 0:
                student.selecting -= 1
                quest = qts.questions[student.selecting]
                lbl_question.config(text=f"Question {student.selecting + 1}/10:{quest['question']}")
                options = quest['options']
                R0.config(text=options[0])
                R1.config(text=options[1])
                R2.config(text=options[2])
                R3.config(text=options[3])
                var.set(student.selection[student.selecting])

        def next_question():
            student.choose_option(var.get())
            if student.selecting < 9:
                student.selecting += 1
                quest = qts.questions[student.selecting]
                lbl_question.config(text=f"Question {student.selecting + 1}/10:{quest['question']}")
                options = quest['options']
                R0.config(text=options[0])
                R1.config(text=options[1])
                R2.config(text=options[2])
                R3.config(text=options[3])
                if student.selection[student.selecting] > -1:
                    var.set(student.selection[student.selecting])
                else:
                    var.set(0)
            else:
                controller.show_frame(Page2)

        button1 = ttk.Button(self, text="Pre",
                             command=pre_question)

        button1.place(x=150, y=400)

        button2 = ttk.Button(self, text="Next",
                             command=next_question)
        button2.place(x=250, y=400)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        scores = 0
        for i in range(10):
            if student.selection[i] == qts.answers[i]:
                scores += 1

        lbl_name = ttk.Label(self, text=f"Name: {student.name}", font=("Arial", 20))
        lbl_name.place(x=100, y=100)

        label = ttk.Label(self, text=f"Score: {scores}", font=("Arial", 20))
        label.place(x=100, y=150)

        lbl_quest = ttk.Label(self, text=f"Correct answers: {scores}/10", font=("Arial", 20))
        lbl_quest.place(x=100, y=200)

        def save_to_file():
            user_info = {'name': student.name,
                         'scores': scores}
            json_object = json.dumps(user_info, indent=2)

            with open("user.json", "w") as outfile:
                outfile.write(json_object)

            controller.destroy()

        btn_close = ttk.Button(self, text="Close", command=save_to_file)
        btn_close.place(x=200, y=400)


app = tkinterApp()
app.mainloop()
