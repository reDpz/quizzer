import os #in order to delete and create new files
import customtkinter as tk
import sqlite3 as sq #to make it easier to type
# converts string into array/list
def stringToList(inp):
    return inp[1:-1].strip().split(',')
class quiz():
    def __init__(self, quizName):
        #will be used later to store files with an appropriate name
        self.name = quizName
        #create connection
        self.connection = sq.connect('quizzes/'+self.name+'.db')
        #create cursor
        self.cursor = self.connection.cursor()
        #define command to create a table
        self.create = """CREATE TABLE IF NOT EXISTS
        quiz(
            qNum INTEGER PRIMARY KEY,
            question TEXT,
            options TEXT,
            answer INTEGER,
            qType NUMBER(1)
            )""" #NUMBER(1) will only allow 0-1 inputs as there is no boolean in sql
        #execute command to create table
        self.cursor.execute(self.create)
    def add(self, qNum, question, options, answer, qType):
        try:
            self.cursor.execute("INSERT INTO quiz VALUES({},{},{},{},{})".format(qNum, question, options, answer, qType))
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
        return self.fetchSingle('question',qNum)
    # return options
    def options(self, qNum):
        return stringToList(
            self.fetchSingle('options',qNum)
            )    
    # return True For correct answer and False otherwise
    def answer(self, inp, qNum):
        if inp != self.fetchSingle('answer',qNum):
            return False
        else:
            return True
    def fetchSingle(self, target, row):
        self.cursor.execute("""SELECT {}
        FROM quiz
        WHERE qNum = {}""".format(target,row))
        return self.cursor.fetchone()[0]
    def mainWindow(self):
        root = tk.CTk()
        root.geometry('1280x720')
        root.title(self.name)
        question = tk.CTkFrame(root,bg_color='#00FF00')
        answer = tk.CTkFrame(root,bg_color='#0000FF')
        submit = tk.CTkFrame(root,bg_color='#FF0000')
        question.grid(row = 0, column = 0, sticky = 'nsew')
        answer.grid(row = 1, column = 0, sticky = 'nsew')
        submit.grid(row = 2, column = 0, sticky = 'nsew')
        root.grid_rowconfigure(0,weight=1)
        root.grid_rowconfigure(1,weight=2)
        root.grid_rowconfigure(2,weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.mainloop()
        
compSci = quiz('compSci')
compSci.add(1,'"Test question"','"[option1,option2,option3]"',1,0)
compSci.delete(1)
compSci.add(2,'"Test question"','"[option1,option2,option3]"',1,0)
compSci.delete(1)
compSci.results()
compSci.add(1,'"Which one of these affects CPU performane"','"[Clock Speed, Cache, Core Count, All of the above]"',3,0)
print(compSci.ask(1))
print(compSci.options(1))
answer = int(input('Enter answer: '))
print(compSci.answer(answer,1))
compSci.mainWindow()