import random
import time
import os
import tkinter
import tkinter as tk
from tkinter.ttk import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime

# Define symbols for slots
SPADE = '♠'
CLUB = '♣'
HEART = '♥'
IDRK = '★'
IDK = '●'
DIAMOND = '♦'

class dbConnection: #FOR EASE OF USE

    DatabaseURI="CasinoDB.db"
    cur=None
    db=None
    
    def __init__(self):     
        self.db = sqlite3.connect(self.DatabaseURI);
        self.cur = self.db.cursor()
        
    def query(self, query):     #IF YOU WANT TO RUN A QUERY
        self.cur.execute(query)
        return self.cur.fetchone()
    
    def queryExecute(self, query):      #IF YOU WANT TO RUN AN EXCECUTABLE
        self.cur.execute(query)
        self.db.commit()

global slotChoice

def main():
    #CONNECTING TO DATABASE
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()

    #GETTING BANK VALUE 
    bank =conn.query("SELECT BALANCE FROM USER WHERE USERID = 'user1' ")
    bank=int(bank[0])
    oldestbank=bank     #STORING BANK VALUE IN VARIABLE


    random.seed(time.time())    #GETTING RANDOM SEED FOR THE SPINS
    multiplier = 1              #DEPENDING ON SLOT CHOICE WILL BE THE BET MULTIPLIER
    global cont                 #GLOBAL VARIABLE FOR CONTINUING
    cont = 1                    #SET = 1
   
    while cont == 1 and bank > 0:           #WHILE THE USER HAS MORE THEN 0 DOLLARS AND THEY WANT TO CONTINUE
      
        #CREATE A TKINTER OBJECT AND SET SOME BASIC PROPERTIES
        r = tk.Tk()
        r.title('Slot Machine Choices')                             #TITLE IS SLOT MACHINE CHOICES
        r.geometry('{}x{}+{}+{}'.format(640, 300, 475, 200))        # THE SIZE OF THE WINDOW IS SET ALONG WITH ITS LOCATION 
   
        #LABELS DISPLAYING INFORMATION 
        Lab1 =Label(r, text=f"You currently have: ${bank}").grid(row=0,column = 2)
        Lab2=Label(r,text ="1) $10 spins, jackpot: $4000" ).grid(row=1,column=2)
        Lab3=Label(r,text="2) $50 spins, jackpot: $20000").grid(row=2,column=2)
        Lab4 = Label(r, text="3) $100 spins, jackpot: $40000").grid(row=3,column=2)
        Lab5=Label(r,text=f"{SPADE}: 0").grid(row=4, column =1)
        Lab6=Label(r,text=f"{DIAMOND}: 1").grid(row=4, column = 3)
        Lab7=Label(r,text=f"{CLUB}: 2").grid(row=5,column=1)
        Lab8=Label(r, text=f"{HEART}: 3").grid(row=5, column=3)
        Lab9=Label(r,text = f"{IDK}: 4").grid(row=6, column =1)
        Lab10=Label(r,text=f"{IDRK}: JOKER").grid(row = 6, column =3)

        
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

        
        r.attributes('-topmost',True)   #MAKING IT SO IT IS ON THE TOP LAYER ALWAYS

        #CREATING BUTTONS FOR THE USER TO INTERACT WITH ALONG WITH COMMANDS AND ATTRIBUTES
        button = tk.Button(r, text='10$ Spins ',width=25,command=lambda:[ r.attributes('-topmost',False),slotChoiceis1(),r.destroy()] ).grid(row=9,column = 1)
        button2 = tk.Button(r, text='50$ Spins', width=25,command=lambda:[r.attributes('-topmost',False),slotChoiceis2(),r.destroy()] ).grid(row=9, column =2)
        button3 = tk.Button(r, text='100$ Spins', width=25,command=lambda:[r.attributes('-topmost',False),slotChoiceis3(), r.destroy()] ).grid(row=9,column =3)
       
        #SOME HIDDEN LABELS USED FOR CREATING SPACING
        hidden =Label(r, text = "", width = 5).grid(row=9, column = 4)
        hidden2 =Label(r, text = "", width = 5).grid(row=9, column = 0)
        
        #THE MAIN LOOP FOR THE TKINTER WINDOW
        r.mainloop()

        #THE AMOUNT OF MONEY DEDUCTED FROM THE USERS BANK
        if (slotChoice == 1):
            multiplier = 1
        elif (slotChoice == 2):
            multiplier = 5
        elif (slotChoice == 3):
            multiplier = 10
        bank -= multiplier * 10

        #CREATING A NEW TKINTER OBJECT FOR THE SPINNING OF THE SLOTS
        f=tk.Tk()
        f.title('Spinning')
        f.geometry('{}x{}+{}+{}'.format(640, 300, 475, 200))


        #RANDOM VALUE FOR WHAT SYMBOL THEY GET 
        slot1 = random.randint(0, 5)
        slotRes1 = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot1]
    
        slot2 = random.randint(0, 5)
        slotRes2 = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot2]
  
        slot3 = random.randint(0, 5)
        slotRes3 = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot3]
    
        #UPDATES THE VALUES INSIDE THE WINDOW
        def updateFirstSpin():
            spin1.set(slotRes1)
        def updateSecondSpin():
            spin2.set(slotRes2)
        def updateThirdSpin():
            spin3.set(slotRes3)

        #SETS THE INITAL TEXT TO BE SPINNING... AS A VARIABLE STRING
        spin1 = StringVar()
        spin1.set("Spinning...")


        f.update_idletasks()        #ALLOWS FOR THE STRINGVAR'S TO BE UPDATED LIVE

        #HIDDEN LABELS FOR SPACING
        hidden3=Label(f,text="",width=5,background="white").grid(row=0,column=0)
        hidden4=Label(f,text="",width=5,background="white").grid(row=1,column=5)
        hidden5=Label(f,text="",width=5,background="white").grid(row=2,column=0)
        hidden6=Label(f,text="",width=5,background="white").grid(row=3,column=0)
        hidden7=Label(f,text="",width=5,background="white").grid(row=4,column=0)
        hidden8=Label(f,text="",width=5,background="white").grid(row=5,column=0)

        
        spinning1 = Label(f, textvariable=spin1,width=25,background="white").grid(row=9,column=1)       #THE FIRST SLOT
        spin2 = StringVar()
        spin2.set("Spinning...")
        spinning2 = Label(f, textvariable=spin2,width = 25,background="white").grid(row=9,column=2)        #THE SECOND SLOT
        spin3= StringVar()
        spin3.set("Spinning...")
        spinning3 = Label(f, textvariable=spin3, width = 25,background="white").grid(row=9,column=3)           #THE THIRD SLOT
        
        #UPDATES EACH SLOTS VALUE 1 AT A TIME WITH 1 SECOND DELAYS
        f.update_idletasks()
        time.sleep(1)
        f.update_idletasks()
        updateFirstSpin()
        f.update_idletasks()
        time.sleep(1)
        f.update_idletasks()
        updateSecondSpin()
        f.update_idletasks()
        time.sleep(1)
        f.update_idletasks()
        updateThirdSpin()
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
            
        #CREATING A VARIABLE STRING FOR CHECKIGN A WIN
        win=StringVar()
        win.set("Checking Win...")
        winCheck=Label(f,textvariable=win,width=25,justify='center',background="white").grid(row=2 ,column = 2)
        time.sleep(1)
        
        global result   #CREATING A GLOBAL VAR 

        bank += checkwin(multiplier, slot1, slot2, slot3)   #BANK GETS UPDATED TO 

        if (bank>oldestbank): #USER WIN     BANK LOSS
            losses =conn.query(f"SELECT LOSSES FROM GAMES WHERE GAMEID = 'Slots' ")
            losses=int(losses[0])+1
            result = "Loss"
            conn.queryExecute(f"UPDATE GAMES SET LOSSES = {losses} WHERE GAMEID = 'Slots'")
        elif(bank<oldestbank): #USER LOSS BANK WIN
            wins =conn.query("SELECT WINS FROM GAMES WHERE GAMEID = 'Slots' ")
            wins = int(wins[0])+1
            result = "Win"
            conn.queryExecute(f"UPDATE GAMES SET WINS = {wins} WHERE GAMEID = 'Slots'")
 
 
        timeplayed =conn.query("SELECT TIMESPLAYED FROM GAMES WHERE GAMEID = 'Slots' ")
        timeplayed=int(timeplayed[0])+1
        conn.queryExecute(f"UPDATE GAMES SET TIMESPLAYED = {timeplayed} WHERE GAMEID = 'Slots'")
 
 
        time.sleep(1)
        f.update_idletasks()
        time.sleep(1)
        f.destroy()
        f.mainloop
        
        def contu():
            global cont
            cont = 1
        def endu():
            global cont
            cont = 0
        
        k=tk.Tk()
       # k.eval('tk::PlaceWindow . center')
        k.geometry('{}x{}+{}+{}'.format(640, 300, 475, 200))
        conn.queryExecute(f"UPDATE USER SET BALANCE = {bank} WHERE USERID = 'user1'")
         
        CasinoNet =conn.query(f"SELECT NETGAIN FROM GAMES WHERE GAMEID = 'Slots' ")
        CasinoNet=int(CasinoNet[0])-bank+oldestbank
        conn.queryExecute(f"UPDATE GAMES SET NETGAIN = {CasinoNet} WHERE GAMEID = 'Slots'")




        now = datetime.now()

        dt_string = now.strftime(f"%Y-%m-%d-%H:%M:%S")

        conn.queryExecute(f"INSERT INTO HISTORY VALUES ('{dt_string}', 'Slots', 'user1', '{result}', {abs(bank-oldestbank)} )")
        netgain=conn.query("SELECT NETGAIN FROM USER WHERE USERID = 'user1'")
        netgain = int(netgain[0]) +bank-oldestbank
        conn.queryExecute(f"UPDATE USER SET NETGAIN = {netgain} WHERE USERID = 'user1'")


        k.title('Continue?')
        L1 = Label(k,text = "Would You Like to Continue?",width = 25).grid(row=3, column =2)
        hidden9 = Label(k, text='', width=5).grid(row=1, column=0)
        hidden10 = Label(k, text='', width=5).grid(row=2, column=4)
        hidden11 = Label(k, text='', width=5).grid(row=3, column=4)
        hidden12 = Label(k, text='', width=5).grid(row=4, column=4)
        hidden13 = Label(k, text='', width=5).grid(row=5, column=4)
        
        conti = tk.Button(k, text='Continue', width=25,command=lambda:[contu(),k.destroy()] ).grid(row=6, column=1)
        end = tk.Button(k, text='End', width=25,command=lambda:[endu(),k.destroy()] ).grid(row= 6, column= 3)


        k.mainloop()
       # cont = int(input("Would you like to continue (1 - Yes) (2 - No): "))

    if bank < 1:
        b=tk.Tk()
        b.geometry('{}x{}+{}+{}'.format(640, 300, 475, 200))
        label = Label(b, text='You ran out of money, haha', width=25).grid(row=3, column=2)
        hidden14 = Label(b, text='', width=5).grid(row=1, column=0)
        hidden15 = Label(b, text='', width=5).grid(row=2, column=4)
        hidden16 = Label(b, text='', width=5).grid(row=3, column=4)
        hidden17 = Label(b, text='', width=5).grid(row=4, column=4)
        hidden18 = Label(b, text='', width=5).grid(row=5, column=4)
        b.mainloop()
    else:
        v=tk.Tk()  
        v.geometry('{}x{}+{}+{}'.format(640, 300, 475, 200))
        label = Label(v,text='Thank you for playing', width=25).grid(row=2, column=1)
        hidden19 = Label(v, text='', width=30).grid(row=1, column=0)
        hidden20 = Label(v, text='', width=30).grid(row=2, column=0)
        hidden21 = Label(v, text='', width=30).grid(row=3, column=0)
        hidden22 = Label(v, text='', width=25).grid(row=4, column=0)
        hidden23 = Label(v, text='', width=25).grid(row=5, column=4)
        v.mainloop()
if __name__ == "__main__":
    main()
