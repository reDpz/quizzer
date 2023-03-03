import os  # in order to delete and create new files
import customtkinter as ck
import sqlite3 as sq  # to make it easier to type
# converts string into array/list


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
            # check contents of index, if index returns 'None' it means qNum does not exist
            if self.cursor.fetchone()[0] != None:
                # this means index does not exist so take early exit
                return True
            # iterate until invalid entry is found
        # after its done iterating with no errors
        return True

    def fetchSingle(self, target, row):
        self.cursor.execute("""SELECT {}
        FROM quiz
        WHERE qNum = {}""".format(target, row))
        return self.cursor.fetchone()[0]


compSci = quiz('compSci')
# compSci.delete(1)
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
print(compSci.length())
# print validity
print(compSci.validLen())