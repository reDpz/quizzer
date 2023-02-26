import tkinter as tk
from tkinter import Button
from tkinter.font import Font
import customtkinter as ck
import os
import sqlite3
import json as j

prgName = "Quizzer"

# setting empty variables as colours to avoid problems in VSC
accent = ''
pBG = ''
pFG = ''
fl025 = ''
fl1 = ''
fl2 = ''
al1 = ''

class colourScheme:
    def __init__(self, dir):
        self.dir = dir
        self.default = {
            'accent':'#9747FF',
            'pBG':'#1B1B1B', # background
            'pFG':'#FFFFFF', # foreground (e.g. text)
            'fl025':'#262626', # focus level 0.25 (more highlighted background)
            'fl1':'#373737', # focus level 1 (more highlighted fl0.25)
            'fl2':'#585858', # focus level 2 (more highligted fl1)
            'al1':'#AE98CB' # accent level 1 (more highlted acccent)
        }
        self.scheme = {}
        self.schemeValidate()
        globals().update(self.scheme)
    def schemeValidate(self):
        # basic check to make sure scheme file exists
        if not os.path.exists(self.dir):
            self.createDefault()
        else:
            with open(self.dir, 'r') as schemeFile:
                try:
                    self.scheme = j.load(schemeFile)
                except Exception as e:
                    # print error instead of crashing
                    print('Could not load scheme from', self.dir,'\nError:',e)
                    # reset scheme as this means that self.dir is corrupt
                    self.createDefault()
                finally:
                    # if file has loaded successfully it now needs to be valid
                    if not self.validity:
                        self.createDefault()
    def createDefault(self):
        # this creates a default schemes.json file
        try:
            with open(self.dir,'w+') as schemeFile:
                schemeFile.write(j.dumps(self.default, indent = 4))
        except Exception as e:
            # if self.dir does not exist (e.g. first startup) it may fail to create scheme file.
            print('Could create default scheme file at', self.dir, '\nError:', e)
        self.scheme = self.default
    def validity(self):
        for key in self.default:
            if key not in self.scheme:
                return False
        return True
colours = colourScheme('data/scheme.json')



# make sure that programming is using the correct directory
# os.chdir(os.path.abspath(os.path.dirname(__file__)))
# creates sidebar used for mainpageimage.png
class sidebar(ck.CTkFrame):
    def __init__(self,master, width, backg, foreg):
        ck.CTkFrame.__init__(
            self,
            master,
            fg_color = backg,
            width = width,
            corner_radius = 15
            )
        userLabel = tk.Label(
            self,
            text = client.username,
            fg = foreg,
            bg = backg,
            font = sidebarFont[0]
            )
        userLabel.pack()
    def addButton(self, buttons):
        # initialise button list
        self.button = []
        # create index
        i = 0
        for bText, bCommand in buttons.items():
            # bText = button text (string), bCommand = button command
            self.button.append(
                ck.CTkButton(
                    self,
                    text = bText,
                    command = bCommand,
                    fg_color = fl1,
                    text_color = pFG,
                    hover_color = fl2,
                    font = sidebarFont[1],
                    anchor = 'w',
                    corner_radius = 10,
                    height = 35
                    )
            )
            #add button
            self.button[i].pack(pady = 5)
            # increment index to pack next button
            i += 1
            
# handles all user data
class user:
    def __init__(self, username):
        self.username = username

    # __str__ returns a string, when asked to print for example.
    def __str__(self):
        return self.username

    def store(self):  # stores userdata in /data/userData.txt, this includes username
        userData = open('data/userData.txt', 'w+')  # w+ creates a file if there is no file existing in the directory.
        userData.write(
            "{\n" + "'username':" + "'" + self.username + "'" + '\n}')  # writes down the username onto the file
        # add a , at the end if storing multiple variables
        userData.close()  # File is closed immediately after use in order to avoid corruption


# lmtFld = limited Field
class lmtdFld(tk.Entry):
    global maxLenPrompt

    def __init__(self, master=None, max_len=5, **kwargs):
        self.var = tk.StringVar()
        self.max_len = max_len
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)

    def check(self, *args):
        if len(self.get()) <= self.max_len:
            self.old_value = self.get()  # accept change
        else:  # executed when more than 16 characters inputted
            self.var.set(self.old_value)  # reject change
            # print('max length reached') debug
            maxLenPrompt.set('Username may not contain more than 16 characters')


# executed when the program is opened
def onstart():
    global user
    global client
    output = validateFile()
    if not output:
        enterUser()
    else:
        client = user(output)
        mainpage()


# returns true if valid username exists and also creates missing directories needed.
def validateFile():
    if not os.path.exists('quizzes'):
        os.mkdir('quizzes')
    if not os.path.exists('data'):  # first ensure that the folder exists
        print('data folder does not exist')  # debug
        os.mkdir('data')  # makes data folder so that userData.txt can be stored
        return False
    elif not os.path.exists('data/userData.txt'):  # now check that the file exists
        print('data folder exists but userData.txt does not')  # debug
        return False
    else:  # debug
        print('userData.txt exists')
    userData = open('data/userData.txt', 'r')
    contents = userData.read()  # stores contents of userData as a string
    try:
        contents = eval(contents)  # converted contents into a dictionary
        print(contents)
        print(contents['username'])  # debugging to make sure that eval has worked properly
    except:
        print('eval failed, contents may be corrupt')  # debug
        userData.close()
        return False
    if validate(3, 16, True, contents['username']):
        print('Valid username')
        userData.close()
        return contents['username']
    else:
        print('Invalid username')
        userData.close()
        return False


def validate(moreThan, lessThan, alnum,
             inp):  # returns true or false depending on whether the input string is valid or not.
    if len(inp) <= lessThan and len(inp) >= moreThan:
        if alnum:
            if inp.isalnum() == True:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def usernameValidate(self, var):
    global user  # declares the user class as a global variable
    global client  # this will be the user object
    if validate(3, 16, True, var):
        print("Valid username")
        client = user(var)  # creates an instance of the user class
        client.store()  # stores username
        self.destroy()  # Closes enterUser
        onstart()
    else:
        print("Invalid username")
        prompt(
            "Invalid username",
            "Please enter a valid username, a username should contain more than 3 characters and less than 16 characters and must be alphanumerical.",
            "Ok"
        )

class welcome(ck.CTk):
    def __init__(self):
        super().__init__(fg_color = pBG)
        self.titleFont = ck.CTkFont(
            'Poppins',
            60,
            'bold'
        )
        self.entryFont = ck.CTkFont(
            'Montserrat',
            15,
            'normal'
        )
        self.geometry("500x300")
        self.resizable(False, False)
        self.title("Welcome - " + prgName)
        # add title
        self.qTitle()
        # add user entry field
        self.userEntry = usernEntry(
            self,
            'Username',
            font = self.entryFont,
            width = 200
            )
        self.userEntry.pack(ipady = 5)
        # stop window from closing
        self.mainloop()
    def qTitle(self):
        # title label with the program name.
        self.titleLabel = ck.CTkLabel(
            self,
            text = prgName,
            fg_color = pBG,
            font = self.titleFont,
            text_color = pFG
        )
        self.titleLabel.pack(pady = 10)
        
# username entry
class usernEntry(ck.CTkEntry):
    def __init__(self, master, text, **kwargs):
        ck.CTkEntry.__init__(
            self,
            master,
            placeholder_text = text,
            fg_color = fl025,
            corner_radius = 10,
            border_color = fl1,
            **kwargs
            )
        # set focus to be false
        self.qFocus = False
        # bind focus in and out
        self.bind('<FocusIn>', self.onFocus)
        self.bind('<FocusOut>', self.offFocus)
        # bind on mouse hover and out, mEnter = mouse enter
        self.bind('<Enter>', self.mEnter)
        self.bind('<Leave>', self.mExit)
    def onFocus(self, event):
        self.configure(
            border_color = accent,
            fg_color = fl1
            )
        # variable used to make sure hover doesnt affect focus
        self.qFocus = True
    def offFocus(self, event):
        self.configure(
            border_color = fl1,
            fg_color = fl025
            )
        self.qFocus = False
    def mEnter(self, event):
        # check to make sure widget is not focused
        if not self.qFocus:
            self.configure(
                border_color  = al1,
                fg_color = fl1
            )
    def mExit(self, event):
        if not self.qFocus:
            self.configure(
                border_color = fl1,
                fg_color = fl025
            )

qWelcome = welcome()
def enterUser():
    global maxLenPrompt  # this variable is the prompt that the user
    # receives when they attempt to enter more
    # than 16 characters
    # creates window
    root = tk.Tk()
    # Prompt to tell the user that max character limit is 16
    maxLenPrompt = tk.StringVar(root, '')  # set as string so that it can be refreshed
    # Resolution
    root.geometry("400x200")
    # Titlebar
    root.title("Welcome - " + prgName)
    # Ask user to enter username
    usernamePrompt = tk.Label(root, text="Enter username:")
    usernamePrompt.pack()
    # Warns the user when they attempt to exceed the 16 character limit
    maxLenWarning = tk.Label(root, textvariable=maxLenPrompt)
    maxLenWarning.pack()
    # field for user to enter their username
    usernameField = lmtdFld(
        root,
        max_len=16,
    )
    usernameField.pack()
    submit = Button(
        root,
        text='Ok',
        command=lambda: usernameValidate(root, usernameField.get())  # destroys root if username is valid
    )
    submit.pack()
    root.mainloop()


def prompt(title, info, buttonText):
    # Create main window
    prompt = tk.Tk()
    prompt.geometry("350x200")
    # titlebar title
    prompt.title(title)
    # Title of prompt
    promptTitle = tk.Label(prompt, text=title, font=("Arial", 15))
    promptTitle.pack()
    # Prompt information
    promptInfo = tk.Label(prompt, text=info, wraplength=330, justify="left")
    promptInfo.pack()
    # prompt button
    promptButton = Button(
        prompt,
        text=buttonText,
        command=prompt.destroy
    )
    promptButton.pack()
    # makes sure window is always on top the other windows
    prompt.focus_force()  # Get user focus
    prompt.lift()  # Raises window above others
    # Dont allow window from being resized
    prompt.resizable(False, False)
    # prevent window from automatically closing
    prompt.mainloop()


def mainpage():
    global client, sidebarFont
    # Create window for main page
    main = tk.Tk()
    # resolution
    main.geometry("1280x720")
    # Set background colour to be dark grey
    main.configure(bg = pBG)
    # Titlebar title
    main.title("Main page - " + prgName)
    # fonts
    sidebarFont = []
    sidebarFont.append(
        Font(
        family = 'Montserrat',
        size = 15,
        weight = "bold"
        )
    )
    sidebarFont.append(
        ck.CTkFont(
        family = 'Montserrat',
        size = 15,
        weight = "bold"    
        )
    )
    # sidebar
    pSidebar = sidebar(
        main,
        215,
        fl025,
        pFG
        )
    pSidebar.grid(
        row = 0,
        column = 0,
        sticky = 'news',
        pady = 10,
        padx = 10
        )
    pSidebar.pack_propagate(False)
    main.grid_rowconfigure(0, weight = 1)
    main.grid_columnconfigure(0,weight = 0)
    # add buttons to sidebar
    pSidebar.addButton(
        {
            'button 1':lambda:print('button 1'),
            'button 2':lambda:print('button 2'),
            'button 3':lambda:mainpage(),
        }
    )
    # set minimum window size
    main.minsize(854, 480)
    # prevent window from instantly closing
    main.mainloop()


# mainpage()
onstart()