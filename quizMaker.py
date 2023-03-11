import os  # in order to delete and create new files
import tkinter as tk
import customtkinter as ck
import sqlite3 as sq  # to make it easier to type
import time 

# define fonts
counter_font = (
    'Montserrat',
    30,
    "bold"
)

quizName_font = (
    'Montserrat',
    10,
    'normal'
)

def stringToList(inp):
    return inp[1:-1].strip().split(',')


class quiz():
    def __init__(self, quizName):
        # will be used later to store files with an appropriate name
        self.name = quizName
        # create connection
        self.connection = sq.connect('quizzes/'+self.name+'.db')
        # create cursor
        self.cursor = self.connection.cursor()
        # define command to create a table
        self.create = """CREATE TABLE IF NOT EXISTS
        quiz(
            qNum INTEGER PRIMARY KEY,
            question TEXT,
            options TEXT,
            answer INTEGER,
            qType NUMBER(1)
            )"""  # NUMBER(1) will only allow 0-1 inputs as there is no boolean in sql
        # execute command to create table
        self.cursor.execute(self.create)

    def add(self, qNum, question, options, answer, qType):
        try:
            self.cursor.execute("INSERT INTO quiz VALUES({},{},{},{},{})".format(
                qNum, question, options, answer, qType))
        except:
            print('invalid data entered')
        self.connection.commit()

    
    def results(self):
        self.cursor.execute("SELECT * FROM quiz")
        print(self.cursor.fetchall())

    def delete(self, row):
        try:
            self.cursor.execute("DELETE FROM quiz WHERE qNum = {}".format(row))
            self.connection.commit()
        except:
            print('Cant delete entry, qNum {} may not exist'.format(row))
    
    # returns questions
    def ask(self, qNum):
        return self.fetchSingle('question', qNum)
    
    # return options
    def options(self, qNum):
        return stringToList(
            self.fetchSingle('options', qNum)
        )
    
    # return True For correct answer and False otherwise
    def answer(self, inp, qNum):
        if inp != self.fetchSingle('answer', qNum):
            return False
        else:
            return True
    
    # returns number of questions (highest index) in quiz
    def length(self):
        self.cursor.execute(
            """SELECT MAX(qNum)
            FROM quiz"""
        )
        return self.cursor.fetchone()[0]
        
    # returns true if all index(s) are present else false
    def validLen(self):
        # Initiate loop that will repeat for every qNum entry.
        # The loop is going backwards as this way it will result in the fastest detection of
        # an empty entry.
        for i in range (self.length() - 1, 0, -1):
            # Start from index lower than highest index
            # because we know that the highest index must exist.
            # Get index
            self.cursor.execute(
                f"""
                SELECT qNum
                FROM quiz
                WHERE qNum = {i}
                """
            )
            # check contents of index, if index returns 'None' it means qNum does not exist.
            if self.cursor.fetchone() == None:
                # this means index does not exist so take early exit
                return False
            # iterate until invalid entry is found
        # after its done iterating with no errors
        return True

    def fetchSingle(self, target, row):
        self.cursor.execute("""SELECT {}
        FROM quiz
        WHERE qNum = {}""".format(target, row))
        return self.cursor.fetchone()[0]

# interface for quizzes
class mainWindow(ck.CTkFrame):
    def __init__(self,master, quiz, **kwargs):
        super().__init__(master, fg_color = '#161616', **kwargs) # color will be replaced later

        # store quiz
        self.quiz = quiz
        
        # f = frame, so fQuestion = frame question 
        self.fQuestion = ck.CTkFrame(self, height = 100, fg_color = 'red', corner_radius = 0) # rgb colours to see frames more clearly
        self.fOptions = ck.CTkFrame(self, fg_color = 'green', corner_radius = 0)
        self.fBottom = ck.CTkFrame(self, height = 60, fg_color = 'blue', corner_radius = 0)
        
        # set grid weights
        for i in range(3):
            self.grid_columnconfigure(i,weight = 1)
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 0)
        
        # make sure frame doesnt resize to contents
        self.fQuestion.grid_propagate(False)
        self.fBottom.grid_propagate(False)
        
        # place frame contents
        self.fillQ(self.fQuestion)
        
        # button to increment counter
        button   = tk.Button(
            self.fOptions,
            text = 'Increment',
            command = self.counter.increment
        )
        button.pack()
        
        # place frames
        self.fQuestion.grid(row = 0, column = 0, sticky = 'ew', columnspan = 3)
        self.fOptions.grid(row = 1, column = 0, sticky = 'news', columnspan = 3)
        self.fBottom.grid(row = 2, column = 0, sticky = 'ew', columnspan = 3)
    
    # fill question frame
    def fillQ(self, frame):
        # configure grid for this frame
        for i in range(2):
            frame.grid_rowconfigure(i, weight=0)
            frame.grid_columnconfigure(i, weight = 0)
        
        # add counter
        self.counter = counter(
            frame,
            fg_color = '#FFFFFF',
            bg_colour = '#000000',
            x = 100,
            y = 100,
            font = counter_font
        )
        # sticky to 'west' so that counter sticks all the way at the left.
        self.counter.grid(column = 0, row = 0, sticky = '')

        # frame containing quiz name and question
        self.info_frame = tk.Frame(
            frame,
            bg = 'blue'
        )
        # insert frame, make sure it doesnt resize to contents
        self.info_frame.grid(row = 0, column = 1, sticky = 'news')
        self.info_frame.pack_propagate(False)

        # add quiz name
        name_label = tk.Label(
            self.info_frame,
            text = self.quiz.name,
            bg = 'white'
        )
        # place label with pack method
        name_label.pack(expand = True, fill = 'both')


# creates a counter with a square box
class counter(tk.Frame):
    # x = x dimension (size) y = y dimension (size)
    def __init__(self, master, startNum=1, *, fg_color, bg_colour, x, y, font):
        # create container
        tk.Frame.__init__(
            self,
            master,
            bg = bg_colour,
            width = x,
            height = y    
        )
        
        # stop frame from resizing to its contents
        self.pack_propagate(False)
        
        # initialise variables, counter is the actual counter and string var is what is displayed
        self.counter = startNum; self.counter_var = tk.StringVar(self,str(self.counter))

        # create label containig StringVar
        self.label = tk.Label(
            self,
            textvariable = self.counter_var,
            fg = fg_color,
            bg = bg_colour,
            font = font
        )

        # pack frame
        self.label.pack(expand=True)
    
    def increment(self, step = 1):
        self.counter += step
        self.counter_var.set(str(self.counter))


compSci = quiz('compSci')

# test window
root = ck.CTk()
root.geometry('1280x720')
main = mainWindow(root, compSci)
main.grid(row = 0, column = 0, sticky = 'news')
root.grid_columnconfigure(0, weight = 1)
root.grid_rowconfigure(0,weight = 1)
root.mainloop()


# compSci.delete(90)
# compSci.add(90,
#             '"Invalid"',
#             '"[Invalid]"',
#             3,
#             0
#             )
# print(compSci.ask(1))
# print(compSci.options(1))
# answer = int(input('Enter answer: '))
# print(compSci.answer(answer, 1))

# print length
# print(compSci.length())
# print validity
# print(compSci.validLen())