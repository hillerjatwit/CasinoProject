import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import numpy as np 
import random
import time
import os
import tkinter
from tkinter.ttk import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image 

# Initialize the user database (in a real application, use a secure database)
user_db = {}

class dbConnection: #FOR EASE OF USE

    DatabaseURI="CasinoDB.db"
    cur=None
    db=None
    
    def __init__(self):     
        self.db = sqlite3.connect(self.DatabaseURI)
        self.cur = self.db.cursor()
        
    def query(self, query):     #IF YOU WANT TO RUN A QUERY
        self.cur.execute(query)
        return self.cur.fetchone()

    def queryall(self, query):     #IF YOU WANT TO RUN A QUERY
        self.cur.execute(query)
        return self.cur.fetchall()    

    def queryExecute(self, query):      #IF YOU WANT TO RUN AN EXCECUTABLE
        self.cur.execute(query)
        self.db.commit()

# Function to handle user login
def login():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()


    username = login_username_entry.get()
    password = login_password_entry.get()
    user_db =conn.queryall("SELECT * FROM ADMIN")
    for user in user_db:
        if user[0]==username:
            if user[1]==password:
                messagebox.showinfo("Login Success", f"Welcome, {user[0]}!")
                show_main_page()
                break
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


    # if username in user_db and user_db[0] == password:
    #     messagebox.showinfo("Login Success", f"Welcome, {user_db[1]}!")
    #     show_main_page()
    # else:
        # messagebox.showerror("Login Failed", "Invalid username or password")

# Function to handle user signup
def signup():
    name = signup_name_entry.get()
    email = signup_email_entry.get()
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = signup_confirm_password_entry.get()
    
    if not name or not email or not username or not password or not confirm_password:
        messagebox.showerror("Signup Failed", "All fields are required")
    elif password != confirm_password:
        messagebox.showerror("Signup Failed", "Passwords do not match")
    elif username in user_db:
        messagebox.showerror("Signup Failed", "Username already exists")
    else:
        user_db[username] = {'name': name, 'email': email, 'password': password}
        messagebox.showinfo("Signup Success", "Account created successfully")
        show_login_page()

# Function to handle password reset
def reset_password():
    username = login_username_entry.get()
    
    if username in user_db:
        new_password = tk.simpledialog.askstring("Reset Password", "Enter new password", show="*")
        if new_password:
            user_db[username]['password'] = new_password
            messagebox.showinfo("Password Reset", "Password reset successfully")
    else:
        messagebox.showerror("Reset Failed", "Username not found")

# Function to show the main page
def show_main_page():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# Function to show the login page
def show_login_page():
    signup_frame.pack_forget()
    main_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Function to show the signup page
def show_signup_page():
    login_frame.pack_forget()
    main_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)


# Placeholder functions for games
def play_blackjack():
    messagebox.showinfo("Blackjack", "Starting Blackjack game...")

def play_roulette():
    messagebox.showinfo("Roulette", "Starting Roulette game...")

def play_roulette():
    messagebox.showinfo("Roulette", "Starting Roulette game...")

def play_craps():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()
    global bank
    global result
    global cont
    global oldestbank
    user = 'user1'

    def get_bank():
       cursor.execute(f"SELECT BALANCE FROM USER WHERE USERID = '{user}'")
       bank = cursor.fetchone()[0]
       return int(bank)
    def get_time():
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
        return timestamp
    bank = get_bank()
    oldestbank = bank
    cont = 1
    result = "win"

    random.seed(time.time())    #GETTING RANDOM SEED FOR THE SPINS

    while cont == 1 and bank > 0: 


        r = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
        root.minsize(700, 300)
        r.pack(fill="both", expand=True)    
        #LABELS DISPLAYING INFORMATION 
        Lab1 =Label(r, text=f"You currently have: ${bank}").grid(row=0,column = 2)
            
        maxbet = str((conn.query("SELECT MAXBET FROM GAMES WHERE GAMEID = 'Craps'"))[0])
        #print(maxbet)
        betenter = ttk.Label(r, text = f'Enter the amount of money to bet, max bet allowed is {maxbet}').grid(row = 2, column = 2)

        user_entry = tk.Entry(r)#gets the user specified bet amount
        user_entry.grid(row = 3, column = 2, pady = 10)
        #user_entry.insert(0, 100)
        bettype = ttk.Label(r, text = f'Please select the kind of bet you would like to perform')    
        passbutton = ttk.Button(r, text = 'Pass Line Bet', width = 25, command = lambda:[play_game(1)]).grid(row = 5, column = 2)
        datetimepassbutton = ttk.Button(r, text = """Don't Pass Line Bet""", width = 25, command = lambda:[play_game(0)]).grid(row = 6, column = 2)


        dpassbutton = ttk.Button()

        def play_game(type):

            def dice_animation(dice, pos):
                if (dice == 1):
                    dice = '⚀'
                if (dice == 2):
                    dice = '⚁'
                if (dice == 3):
                    dice = '⚂'
                if (dice == 4):
                    dice = '⚃'
                if (dice == 5):
                    dice = '⚄'
                if (dice == 6):
                    dice = '⚅'
                dice1 = Label(f, text = dice, font = ('Arial',100), width = 4).grid(row = 4, column = pos)
                f.update_idletasks()    

            bank = get_bank()
            if (type == 1): #determines the win and loss conditions when the user selected pass line or don't pass line bet
                wincon = {7, 11}
                losecon = {2, 3, 12}
            else:
                wincon = {2, 3}
                losecon = {7, 11}                

            f = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
            root.minsize(700, 300)
            f.pack(fill= "both", expand = True)

            userbet = int(user_entry.get())
            if (((userbet % 1) == 0) and (userbet <= int(maxbet)) and (userbet > 0)):
                r.pack_forget()

                def roll_dice():
                    for x in range(12):
                        time.sleep(.1)
                        roll1 = random.randint(1, 6)
                        roll2 = random.randint(1, 6)
                        
                        dice_animation(roll1, 1)
                        dice_animation(roll2, 2)
                    rolltotal = roll1 + roll2
                    return rolltotal        

                roll = roll_dice()
                rolltotal = 0
                print(roll)
                timestamp = get_time()
                if roll in (wincon):
                    win = Label(f, text = f'You Won ${userbet}!').grid(row = 6, column = 1)
                    bank += userbet
                elif roll in (losecon):
                    lose = Label(f, text = f'You Lost ${userbet}!').grid(row = 6, column = 1)
                    bank -= userbet
                else:
                    while rolltotal not in (roll, 7):
                        time.sleep(1)
                        rroll = Label(f, text = f'Rerolling for {roll}...').grid(row = 6, column = 1)
                        f.update_idletasks
                        rolltotal = roll_dice()
                        print(f"({rolltotal})")
                    if rolltotal != 7:
                        win = Label(f, text = f'You Won ${userbet}!').grid(row = 7, column = 1)
                        bank += userbet
                    else:
                        lose = Label(f, text = f'You Lost ${userbet}!').grid(row = 7, column = 1)
                        bank -= userbet
                    f.update_idletasks()

                if (bank>oldestbank): #USER WIN     BANK LOSS
                    losses =conn.query(f"SELECT LOSSES FROM GAMES WHERE GAMEID = 'Craps' ")
                    losses=int(losses[0])+1
                    result = "Loss"
                    conn.queryExecute(f"UPDATE GAMES SET LOSSES = {losses} WHERE GAMEID = 'Craps'")
                elif(bank<=oldestbank): #USER LOSS BANK WIN
                    wins =conn.query("SELECT WINS FROM GAMES WHERE GAMEID = 'Craps' ")
                    wins = int(wins[0])+1
                    result = "Win"
                    conn.queryExecute(f"UPDATE GAMES SET WINS = {wins} WHERE GAMEID = 'Craps'")
        
                #UPDATES THE AMOUNT OF TIMES THE GAME HAS BEEN PLAYED 
                timeplayed =conn.query("SELECT TIMESPLAYED FROM GAMES WHERE GAMEID = 'Craps' ")
                timeplayed=int(timeplayed[0])+1
                conn.queryExecute(f"UPDATE GAMES SET TIMESPLAYED = {timeplayed} WHERE GAMEID = 'Craps'")
        
                #THE USER SLEEPS -> UPDATES THE TEXT -> SLEEPS
                time.sleep(1)
                f.update_idletasks()
                time.sleep(1)

                conn.queryExecute(f"UPDATE USER SET BALANCE = {bank} WHERE USERID = '{user}'")
         
                #UPDATE GAMES NET GAIN
                CasinoNet =conn.query(f"SELECT NETGAIN FROM GAMES WHERE GAMEID = 'Craps' ")
                CasinoNet=int(CasinoNet[0])-bank+oldestbank
                conn.queryExecute(f"UPDATE GAMES SET NETGAIN = {CasinoNet} WHERE GAMEID = 'Craps'")

                #GET THE DATE
                now = datetime.now()

                dt_string = now.strftime(f"%Y-%m-%d-%H:%M:%S")
                #STORE THE DATA FROM THE MOST RECENT WIN AND PUT IT IN THE DATABASE 
                conn.queryExecute(f"INSERT INTO HISTORY VALUES ('{dt_string}', 'Craps', '{user}', '{result}', {abs(bank-oldestbank)} )")
                netgain=conn.query(f"SELECT NETGAIN FROM USER WHERE USERID = '{user}'")
                netgain = int(netgain[0]) +bank-oldestbank
                conn.queryExecute(f"UPDATE USER SET NETGAIN = {netgain} WHERE USERID = '{user}'")
                        
                f.mainloop
                #IF THE USER WANTS TO CONTINUE CONT = 1
                def contu():
                    global cont
                    cont = 1
                def endu():
                    global cont
                    cont = 0

                time.sleep(3)#shows the results to the user for a time
                f.pack_forget
                k = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
                k.pack(fill="both", expand=True)
                #UPDATE USER BALANCE
                

                #ASK USER IF THEY WANT TO CONTINUE
                L1 = Label(k,text = "Would You Like to Continue?",width = 25).grid(row=3, column =2)
                hidden9 = Label(k, text='', width=5).grid(row=1, column=0)
                hidden10 = Label(k, text='', width=5).grid(row=2, column=4)
                hidden11 = Label(k, text='', width=5).grid(row=3, column=4)
                hidden12 = Label(k, text='', width=5).grid(row=4, column=4)
                hidden13 = Label(k, text='', width=5).grid(row=5, column=4)
                
                conti = ttk.Button(k, text='Continue', width=25,command=lambda:[contu(),k.pack_forget(),f.pack_forget(),play_craps()] ).grid(row=6, column=1)
                end = ttk.Button(k, text='End', width=25,command=lambda:[endu(),k.pack_forget(),f.pack_forget(),show_main_page()] ).grid(row= 6, column= 3)

                k.mainloop()
                
                #SOME HIDDEN LABELS USED FOR CREATING SPACING
                hidden =Label(r, text = "", width = 5).grid(row=9, column = 4)
                hidden2 =Label(r, text = "", width = 5).grid(row=9, column = 0)
            else:
                messagebox.showerror("Bet cancelled", "Please enter a valid bet amount")
                f.destroy()

            
            
        #THE MAIN LOOP FOR THE TKINTER WINDOW
        r.mainloop()
        #r.pack_forget()
        #THE AMOUNT OF MONEY DEDUCTED FROM THE USERS BANK



    else: #returns to main page
        show_main_page()

def play_slots():

  #CONNECTING TO DATABASE
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()
    global bank
    global result
    global cont
    global oldestbank

    user = 'user1'
    # Function to get the bank balance
    def get_bank():
       cursor.execute(f"SELECT BALANCE FROM USER WHERE USERID = '{user}'")
       bank = cursor.fetchone()[0]
       return int(bank)

    bank = get_bank()
    oldestbank = bank
    cont = 1
    result = "win"
    multiplier = 1  #STORING BANK VALUE IN VARIABLE

    random.seed(time.time())    #GETTING RANDOM SEED FOR THE SPINS
   
    while cont == 1 and bank > 0:           #WHILE THE USER HAS MORE THEN 0 DOLLARS AND THEY WANT TO CONTINUE
      
        #CREATE A TKINTER OBJECT AND SET SOME BASIC PROPERTIES
        r = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
        root.minsize(700, 300)
        r.pack(fill="both", expand=True)
        Apple1 = Image.open((os.getcwd())+f"/Apple.png").resize((25,25))
        Cherry1 = Image.open((os.getcwd())+f"/Cherry.png").resize((25,25))
        Grape1 = Image.open((os.getcwd())+f"/Grape.png").resize((25,25))
        Orange1= Image.open((os.getcwd())+f"/Orange.png").resize((25,25))
        HorseShoe1 = Image.open((os.getcwd())+f"/HorseShoe.png").resize((25,25))
        Bar1 = Image.open((os.getcwd())+f"/Bar.png").resize((25,25))

        Apple = ImageTk.PhotoImage(Apple1)
        Cherry = ImageTk.PhotoImage(Cherry1)
        Grape = ImageTk.PhotoImage(Grape1)
        Orange = ImageTk.PhotoImage(Orange1)
        HorseShoe = ImageTk.PhotoImage(HorseShoe1)
        Bar = ImageTk.PhotoImage(Bar1)
        #LABELS DISPLAYING INFORMATION 
        Lab1 =Label(r, text=f"You currently have: ${bank}").grid(row=0,column = 2)
        Lab2=Label(r,text ="1) $10 spins, jackpot: $4000" ).grid(row=1,column=2)
        Lab3=Label(r,text="2) $50 spins, jackpot: $20000").grid(row=2,column=2)
        Lab4 = Label(r, text="3) $100 spins, jackpot: $40000").grid(row=3,column=2)
       
        Lab51=Label(r,text="               : 0").grid(row=4, column =1)
        Lab5=Label(r,image=Apple).grid(row=4, column =1)
       
        Lab61=Label(r,text="               : 1").grid(row=4, column =3)
        Lab6=Label(r,image = Cherry).grid(row=4, column = 3)
        
        Lab71=Label(r,text="               : 2").grid(row=5, column =1)
        Lab7=Label(r,image=Grape).grid(row=5,column=1)
        
        Lab81=Label(r,text="               : 3").grid(row=5, column =3)
        Lab8=Label(r, image = Orange).grid(row=5, column=3)
        
        Lab91=Label(r,text="               : 4").grid(row=6, column =1)
        Lab9=Label(r,image = HorseShoe).grid(row=6, column =1)
        
        Lab101=Label(r,text="                      : WILD").grid(row=6, column =3)
        Lab10=Label(r,image = Bar).grid(row = 6, column =3)

        
        #SETTING SOME METHODS FOR LATER USE WHICH WILL BE WHICH AMOUNT THE USER WANTS TO BET 
        def slotChoiceis1():
            global slotChoice
            slotChoice=1
        def slotChoiceis2():
            global slotChoice
            slotChoice=2
        def slotChoiceis3():
            global slotChoice
            slotChoice=3
        def openmanual():
            v = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
            v.pack(fill="both", expand=True)     # THE SIZE OF THE WINDOW IS SET ALONG WITH ITS LOCATION 

            Apple1 = Image.open((os.getcwd())+f"/Apple.png").resize((25,25))
            Cherry1 = Image.open((os.getcwd())+f"/Cherry.png").resize((25,25))
            Grape1 = Image.open((os.getcwd())+f"/Grape.png").resize((25,25))
            Orange1= Image.open((os.getcwd())+f"/Orange.png").resize((25,25))
            HorseShoe1 = Image.open((os.getcwd())+f"/HorseShoe.png").resize((25,25))
            Bar1 = Image.open((os.getcwd())+f"/Bar.png").resize((25,25))

            Apple = ImageTk.PhotoImage(Apple1)
            Cherry = ImageTk.PhotoImage(Cherry1)
            Grape = ImageTk.PhotoImage(Grape1)
            Orange = ImageTk.PhotoImage(Orange1)
            HorseShoe = ImageTk.PhotoImage(HorseShoe1)
            Bar = ImageTk.PhotoImage(Bar1)

            invis1=Label(v,text="",width=20).grid(row=0,column=0)
            invis2=Label(v,text="",width=20).grid(row=0,column=1)
            invis3=Label(v,text="",width=20).grid(row=0,column=2)
           # invis4=Label(v,text="",width=25).grid(row=0,column=3)

            Title=Label(v,text="Welcome to the slots manual",justify="center").grid(row=0,column = 1,columnspan=1)   
            Title2=Label(v,text="The rules are as follows",justify="center").grid(row=1,column = 1,columnspan=1)     

            Rule1=Label(v,text="\t\t          : Has a value of 1").grid(row=2, column =0)
            Rule1Image=Label(v,image=Apple,justify = "left").grid(row=2, column =0)   
            
            Rule2=Label(v,text="\t\t          : Has a value of 2").grid(row=2, column =2)
            Rule2Image=Label(v,image=Cherry).grid(row=2, column =2)   
            
            Rule3=Label(v,text="\t\t          : Has a value of 3").grid(row=3, column =0)
            Rule3Image=Label(v,image=Grape).grid(row=3, column =0)   
            
            Rule4=Label(v,text="\t\t          : Has a value of 4").grid(row=3, column =2)
            Rule4Image=Label(v,image=Orange).grid(row=3, column =2) 

            Rule5=Label(v,text="\t\t          : Has a value of 5").grid(row=4, column =0)
            Rule5Image=Label(v,image=HorseShoe).grid(row=4, column =0)   
            
            Rule6=Label(v,text="\t\t    : Is a wildcard").grid(row=4, column =2)
            Rule6Image=Label(v,image=Bar).grid(row=4, column =2)   
            
            Rule7=Label(v,text="If you get 3 Apples -> the Jackpot is 25* your initial bet ").grid(row=5,columnspan=3)
            Rule8=Label(v,text="If you get 3 Cherries -> the Jackpot is 50* your initial bet ").grid(row=6,columnspan=3)
            Rule9=Label(v,text="If you get 3 Grapes -> the Jackpot is 80* your initial bet ").grid(row=7,columnspan=3)
            Rule10=Label(v,text="If you get 3 Oranges -> the Jackpot is 100* your initial bet ").grid(row=8,columnspan=3)
            Rule11=Label(v,text="If you get 3 HorseShoes -> the Jackpot is 160* your initial bet ").grid(row=9,columnspan=3)
            Rule12=Label(v,text="If you get 3 Bars -> the Jackpot is 400* your initial bet ").grid(row=10,columnspan=3)
            Rule12=Label(v,text="If you get 2 of the same and 1 Bar you get a mini jackpot\n that is worth 1/4 the corrosponding jacpot").grid(row=11,columnspan=3)
            close =Button(v, text='Exit', width=25,command=lambda:[v.pack_forget(),play_slots()]).grid(row=12,column =1)

            v.mainloop()  

        def playgame():
                f = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
                root.minsize(700, 300)
                f.pack(fill="both", expand=True)

                Apple1 = Image.open((os.getcwd())+f"/Apple.png").resize((85,85))
                Cherry1 = Image.open((os.getcwd())+f"/Cherry.png").resize((85,85))
                Grape1 = Image.open((os.getcwd())+f"/Grape.png").resize((85,85))
                Orange1= Image.open((os.getcwd())+f"/Orange.png").resize((85,85))
                HorseShoe1 = Image.open((os.getcwd())+f"/HorseShoe.png").resize((85,85))
                Bar1 = Image.open((os.getcwd())+f"/Bar.png").resize((85,85))

                Apple = ImageTk.PhotoImage(Apple1)
                Cherry = ImageTk.PhotoImage(Cherry1)
                Grape = ImageTk.PhotoImage(Grape1)
                Orange = ImageTk.PhotoImage(Orange1)
                HorseShoe = ImageTk.PhotoImage(HorseShoe1)
                Bar = ImageTk.PhotoImage(Bar1)

                #RANDOM VALUE FOR WHAT SYMBOL THEY GET 
                slot1 = random.randint(0, 5)
                slotRes1 = [Apple, Cherry, Grape, Orange, HorseShoe, Bar][slot1]
            
                slot2 = random.randint(0, 5)
                slotRes2 = [Apple, Cherry, Grape, Orange, HorseShoe, Bar][slot2]

                slot3 = random.randint(0, 5)
                slotRes3 = [Apple, Cherry, Grape, Orange, HorseShoe, Bar][slot3]
            
                f.update_idletasks()        #ALLOWS FOR THE STRINGVAR'S TO BE UPDATED LIVE

                #HIDDEN LABELS FOR SPACING
                hidden3=Label(f,text="",width=5).grid(row=0,column=1)
                hidden4=Label(f,text="",width=5).grid(row=1,column=5)
                hidden5=Label(f,text="",width=5).grid(row=2,column=0)
                hidden6=Label(f,text="",width=5).grid(row=3,column=0)
                hidden7=Label(f,text="",width=5).grid(row=4,column=0)
                hidden8=Label(f,text="",width=5).grid(row=5,column=0)
                f.update_idletasks()

                #SETS THE INITAL TEXT TO BE SPINNING... AS A VARIABLE STRING
                spin1 = StringVar()
                spin1.set("Spinning...")
                spinning1 = Label(f, text="Spinning",width=25).grid(row=4,column=1)       #THE FIRST SLOT
                spin2 = StringVar()
                spin2.set("Spinning...")
                spinning2 = Label(f, text="Spinning",width = 25).grid(row=4,column=2)        #THE SECOND SLOT
                spin3= StringVar()
                spin3.set("Spinning...")
                spinning3 = Label(f,  text="Spinning", width = 25).grid(row=4,column=3)           #THE THIRD SLOT
                #UPDATES EACH SLOTS VALUE 1 AT A TIME WITH 1 SECOND DELAYS

                f.update_idletasks()
                time.sleep(1)
                spinning1=Label(f,image=slotRes1).grid(row=4,column=1)

                f.update_idletasks()
        
                time.sleep(1)
                spinning2=Label(f,image=slotRes2).grid(row=4,column=2)

                f.update_idletasks()
                time.sleep(1)
                spinning2=Label(f,image=slotRes3).grid(row=4,column=3)
              
                f.update_idletasks()
                time.sleep(1)  
                
                def checkwin(multiplier, slot1, slot2, slot3): #USED TO CHECK IF THE USER HAS WON ANY WACH WITH A SPECIFIC CASE 
                    winnings = 0
                    if slot1 == slot2 == slot3 == 0:                        #USER GETS 3 SPADES
                        win.set(f"Tiny Jackpot $:{multiplier*250}")
                        print("You Hit The Tiny Jackpot!!!")
                        winnings = multiplier * 250 
                    elif slot1 == slot2 == slot3 == 1:                      #USER GETS 3 DIAMONDS
                        win.set(f"Small Jackpot $:{multiplier*500}")
                        print("You Hit The Small Jackpot!!!")
                        winnings = multiplier * 500
                    elif slot1 == slot2 == slot3 == 2:                      #USER GETS 3 CLUBS
                        win.set(f"Medium Jackpot $:{multiplier*800}")
                        print("You Hit The Medium Jackpot!!!")
                        winnings = multiplier * 800
                    elif slot1 == slot2 == slot3 == 3:                      #USER GETS 3 HEARTS
                        win.set(f"Big Jackpot $:{multiplier*1000}")
                        print("You Hit The Big Jackpot!!!")
                        winnings = multiplier * 1000
                    elif slot1 == slot2 == slot3 == 4:                      #USER GETS 3 CIRCLES
                        win.set(f"Large Jackpot $:{multiplier*1600}")                
                        print("You Hit The Large Jackpot!!!")
                        winnings = multiplier * 1600
                    elif slot1 == slot2 == slot3 == 5:                      #USER GETS 3 STARS  
                        win.set(f"MEGA Jackpot $:{multiplier*4000}")
                        print("You Hit The MEGA Jackpot!!!")
                        winnings = multiplier * 4000
                    elif (slot1 == slot2 == 0 and slot3 == 5) or (slot1 == slot3 == 0 and slot2 == 5) or (slot2 == slot3 == 0 and slot1 == 5):      #USER GETS 2 SPADES AND 1 STAR
                        win.set(f"Tiny Wild Jackpot $:{multiplier*250/4}")
                        print("You Hit The Tiny Wild Jackpot!!!")
                        winnings = multiplier * 250 / 4
                    elif (slot1 == slot2 == 1 and slot3 == 5) or (slot1 == slot3 == 1 and slot2 == 5) or (slot2 == slot3 == 1 and slot1 == 5):      #USER GET 2 DIAMONDS AND 1 STAR
                        win.set(f"Small Wild Jackpot $:{multiplier*500/4}")
                        print("You Hit The Small Wild Jackpot!!!")
                        winnings = multiplier * 500 / 4
                    elif (slot1 == slot2 == 2 and slot3 == 5) or (slot1 == slot3 == 2 and slot2 == 5) or (slot2 == slot3 == 2 and slot1 == 5):      #USER GETS 2 CLUBS AND 1 STAR
                        win.set(f"Medium Wild Jackpot $:{multiplier*800/4}")
                        print("You Hit The Medium Wild Jackpot!!!")
                        winnings = multiplier * 800 / 4
                    elif (slot1 == slot2 == 3 and slot3 == 5) or (slot1 == slot3 == 3 and slot2 == 5) or (slot2 == slot3 == 3 and slot1 == 5):      #USER GETS 2 HEARTS AND 1 STAR 
                        win.set(f"Big Wild Jackpot $:{multiplier*1000/4}")
                        print("You Hit The Big Wild Jackpot!!!")
                        winnings = multiplier * 1000 / 4
                    elif (slot1 == slot2 == 4 and slot3 == 5) or (slot1 == slot3 == 4 and slot2 == 5) or (slot2 == slot3 == 4 and slot1 == 5):      #USER GETS 2 CIRCLES AND 1 STAR
                        win.set(f"Large Wild Jackpot $:{multiplier*1600/4}")
                        print("You Hit The Large Wild Jackpot!!!")
                        winnings = multiplier * 1600 / 4
                    else:                                 #USER GETS NO WIN
                        win.set("No Win")
                        winnings = 0
                    print(f"You Win ${winnings}")
                    return winnings
                    
                bank=get_bank()
                if (slotChoice == 1):
                    multiplier = 1
                elif (slotChoice == 2):
                    multiplier = 5
                elif (slotChoice == 3):
                    multiplier = 10
                bank = bank- multiplier * 10
                #CREATING A VARIABLE STRING FOR CHECKIGN A WIN
                win=StringVar()
                win.set("Checking Win...")
                winCheck=Label(f,textvariable=win,width=25,justify='center').grid(row=2 ,column = 2)
                time.sleep(1)
                
                bank += checkwin(multiplier, slot1, slot2, slot3)   #BANK GETS UPDATED TO 

                if (bank>oldestbank): #USER WIN     BANK LOSS
                    losses =conn.query(f"SELECT LOSSES FROM GAMES WHERE GAMEID = 'Slots' ")
                    losses=int(losses[0])+1
                    result = "Loss"
                    conn.queryExecute(f"UPDATE GAMES SET LOSSES = {losses} WHERE GAMEID = 'Slots'")
                elif(bank<=oldestbank): #USER LOSS BANK WIN
                    wins =conn.query("SELECT WINS FROM GAMES WHERE GAMEID = 'Slots' ")
                    wins = int(wins[0])+1
                    result = "Win"
                    conn.queryExecute(f"UPDATE GAMES SET WINS = {wins} WHERE GAMEID = 'Slots'")
        
                #UPDATES THE AMOUNT OF TIMES THE GAME HAS BEEN PLAYED 
                timeplayed =conn.query("SELECT TIMESPLAYED FROM GAMES WHERE GAMEID = 'Slots' ")
                timeplayed=int(timeplayed[0])+1
                conn.queryExecute(f"UPDATE GAMES SET TIMESPLAYED = {timeplayed} WHERE GAMEID = 'Slots'")
        
                #THE USER SLEEPS -> UPDATES THE TEXT -> SLEEPS
                time.sleep(1)
                f.update_idletasks()
                time.sleep(1)

                conn.queryExecute(f"UPDATE USER SET BALANCE = {bank} WHERE USERID = '{user}'")
         
                #UPDATE GAMES NET GAIN
                CasinoNet =conn.query(f"SELECT NETGAIN FROM GAMES WHERE GAMEID = 'Slots' ")
                CasinoNet=int(CasinoNet[0])-bank+oldestbank
                conn.queryExecute(f"UPDATE GAMES SET NETGAIN = {CasinoNet} WHERE GAMEID = 'Slots'")

                #GET THE DATE
                now = datetime.now()

                dt_string = now.strftime(f"%Y-%m-%d-%H:%M:%S")
                #STORE THE DATA FROM THE MOST RECENT WIN AND PUT IT IN THE DATABASE 
                conn.queryExecute(f"INSERT INTO HISTORY VALUES ('{dt_string}', 'Slots', '{user}', '{result}', {abs(bank-oldestbank)} )")
                netgain=conn.query(f"SELECT NETGAIN FROM USER WHERE USERID = '{user}'")
                netgain = int(netgain[0]) +bank-oldestbank
                conn.queryExecute(f"UPDATE USER SET NETGAIN = {netgain} WHERE USERID = '{user}'")
                f.mainloop
                  #CREATING A NEW TKINTER OBJECT FOR THE SPINNING OF THE SLOTS
       
                #IF THE USER WANTS TO CONTINUE CONT = 1
                def contu():
                    global cont
                    cont = 1
                def endu():
                    global cont
                    cont = 0
                
                k = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
                k.pack(fill="both", expand=True)
                #UPDATE USER BALANCE
                

                #ASK USER IF THEY WANT TO CONTINUE
                L1 = Label(k,text = "Would You Like to Continue?",width = 25).grid(row=3, column =2)
                hidden9 = Label(k, text='', width=5).grid(row=1, column=0)
                hidden10 = Label(k, text='', width=5).grid(row=2, column=4)
                hidden11 = Label(k, text='', width=5).grid(row=3, column=4)
                hidden12 = Label(k, text='', width=5).grid(row=4, column=4)
                hidden13 = Label(k, text='', width=5).grid(row=5, column=4)
                
                conti = ttk.Button(k, text='Continue', width=25,command=lambda:[contu(),k.pack_forget(),f.pack_forget(),play_slots()] ).grid(row=6, column=1)
                end = ttk.Button(k, text='End', width=25,command=lambda:[endu(),k.pack_forget(),f.pack_forget(),show_main_page()] ).grid(row= 6, column= 3)


                k.mainloop()
                    
        #CREATING BUTTONS FOR THE USER TO INTERACT WITH ALONG WITH COMMANDS AND ATTRIBUTES
        button = ttk.Button(r, text='10$ Spins ',width=25,command=lambda:[r.pack_forget(),slotChoiceis1(),playgame()] ).grid(row=9,column = 1)
        button2 = ttk.Button(r, text='50$ Spins', width=25,command=lambda:[r.pack_forget(),slotChoiceis2(),playgame()] ).grid(row=9, column =2)
        button3 = ttk.Button(r, text='100$ Spins', width=25,command=lambda:[r.pack_forget(),slotChoiceis3(),playgame()] ).grid(row=9,column =3)
        manual = ttk.Button(r, text='Game Manual', width=25,command=lambda:[r.pack_forget(),openmanual()] ).grid(row=10,column =2)
        

        #SOME HIDDEN LABELS USED FOR CREATING SPACING
        hidden =Label(r, text = "", width = 5).grid(row=9, column = 4)
        hidden2 =Label(r, text = "", width = 5).grid(row=9, column = 0)
        
        #THE MAIN LOOP FOR THE TKINTER WINDOW
        r.mainloop()
        #r.pack_forget()
        #THE AMOUNT OF MONEY DEDUCTED FROM THE USERS BANK
    else: #returns to main page
        show_main_page()
    
      
    

def play_other_games():
    messagebox.showinfo("Other Games", "Starting other casino games...")

def check_stats():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()

   # main_frame.pack_forget()
    cs = tk.Frame(root, padx=20, pady=20)
    cs.pack(fill="both", expand=True)

    data=conn.queryall("select RESULT FROM HISTORY") 
    x = [] 
    add= 0
    y = [] 
    for i in data: 
        x.append(add)	#x column contain data(1,2,3,4,5) 
        y.append(i[0])	#y column contain data(1,2,3,4,5) 
        add=add+1
    plt.plot(x,y) 
    plt.title("HOUSE WINS/LOSSES")
    plt.show() 
            



# Create the main application window

root = tk.Tk()
root.title("User Authentication System")
root.geometry("400x450")

# Create the login frame
login_frame = tk.Frame(root, padx=20, pady=20)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="e")
login_username_entry = tk.Entry(login_frame, font=("Arial", 12))
login_username_entry.grid(row=0, column=1, pady=10)

tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
login_password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
login_password_entry.grid(row=1, column=1, pady=10)

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, pady=10)

signup_button = ttk.Button(login_frame, text="Sign Up", command=show_signup_page)
signup_button.grid(row=2, column=1, pady=10)

reset_button = ttk.Button(login_frame, text="Forgot Password", command=reset_password)
reset_button.grid(row=3, columnspan=2, pady=10)

# Create the signup frame
signup_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(signup_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="e")
signup_name_entry = tk.Entry(signup_frame, font=("Arial", 12))
signup_name_entry.grid(row=0, column=1, pady=10)

tk.Label(signup_frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
signup_email_entry = tk.Entry(signup_frame, font=("Arial", 12))
signup_email_entry.grid(row=1, column=1, pady=10)

tk.Label(signup_frame, text="Username:", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
signup_username_entry = tk.Entry(signup_frame, font=("Arial", 12))
signup_username_entry.grid(row=2, column=1, pady=10)

tk.Label(signup_frame, text="Password:", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="e")
signup_password_entry = tk.Entry(signup_frame, show="*", font=("Arial", 12))
signup_password_entry.grid(row=3, column=1, pady=10)

tk.Label(signup_frame, text="Confirm Password:", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
signup_confirm_password_entry = tk.Entry(signup_frame, show="*", font=("Arial", 12))
signup_confirm_password_entry.grid(row=4, column=1, pady=10)

signup_confirm_button = ttk.Button(signup_frame, text="Sign Up", command=signup)
signup_confirm_button.grid(row=5, column=0, pady=10)

signup_cancel_button = ttk.Button(signup_frame, text="Cancel", command=show_login_page)
signup_cancel_button.grid(row=5, column=1, pady=10)

# Create the main page frame
main_frame = tk.Frame(root, padx=20, pady=20)

welcome_label = tk.Label(main_frame, text="Welcome to the Main Page!", font=("Arial", 16))
welcome_label.pack(pady=20)

blackjack_button = ttk.Button(main_frame, text="Play Blackjack", command=play_blackjack)
blackjack_button.pack(pady=10)

slots_button = ttk.Button(main_frame, text="Play Slots", command=lambda:[main_frame.pack_forget(),login_frame.pack_forget(), signup_frame.pack_forget(),play_slots()])
slots_button.pack(pady=10)

slots_button = ttk.Button(main_frame, text="Play Craps", command=lambda:[main_frame.pack_forget(),login_frame.pack_forget(), signup_frame.pack_forget(),play_craps()])
slots_button.pack(pady=10)

roulette_button = ttk.Button(main_frame, text="Play Roulette", command=play_roulette)
roulette_button.pack(pady=10)

statistics_button = ttk.Button(main_frame, text="Check Stats", command=check_stats)
statistics_button.pack(pady=10)

logout_button = ttk.Button(main_frame, text="Logout", command=show_login_page)
logout_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()