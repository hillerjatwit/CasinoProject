import random
import time
import os
import tkinter
import tkinter as tk

# Define symbols for slots
SPADE = '♠'
CLUB = '♣'
HEART = '♥'
IDRK = '★'
IDK = '●'
DIAMOND = '♦'

def checkwin(multiplier, slot1, slot2, slot3):
    winnings = 0
    if slot1 == slot2 == slot3 == 0:
        print("You Hit The Tiny Jackpot!!!")
        winnings = multiplier * 250
    elif slot1 == slot2 == slot3 == 1:
        print("You Hit The Small Jackpot!!!")
        winnings = multiplier * 500
    elif slot1 == slot2 == slot3 == 2:
        print("You Hit The Medium Jackpot!!!")
        winnings = multiplier * 800
    elif slot1 == slot2 == slot3 == 3:
        print("You Hit The Big Jackpot!!!")
        winnings = multiplier * 1000
    elif slot1 == slot2 == slot3 == 4:
        print("You Hit The Large Jackpot!!!")
        winnings = multiplier * 1600
    elif slot1 == slot2 == slot3 == 5:
        print("You Hit The MEGA Jackpot!!!")
        winnings = multiplier * 4000
    elif (slot1 == slot2 == 0 and slot3 == 5) or (slot1 == slot3 == 0 and slot2 == 5) or (slot2 == slot3 == 0 and slot1 == 5):
        print("You Hit The Tiny Wild Jackpot!!!")
        winnings = multiplier * 250 / 4
    elif (slot1 == slot2 == 1 and slot3 == 5) or (slot1 == slot3 == 1 and slot2 == 5) or (slot2 == slot3 == 1 and slot1 == 5):
        print("You Hit The Small Wild Jackpot!!!")
        winnings = multiplier * 500 / 4
    elif (slot1 == slot2 == 2 and slot3 == 5) or (slot1 == slot3 == 2 and slot2 == 5) or (slot2 == slot3 == 2 and slot1 == 5):
        print("You Hit The Medium Wild Jackpot!!!")
        winnings = multiplier * 800 / 4
    elif (slot1 == slot2 == 3 and slot3 == 5) or (slot1 == slot3 == 3 and slot2 == 5) or (slot2 == slot3 == 3 and slot1 == 5):
        print("You Hit The Big Wild Jackpot!!!")
        winnings = multiplier * 1000 / 4
    elif (slot1 == slot2 == 4 and slot3 == 5) or (slot1 == slot3 == 4 and slot2 == 5) or (slot2 == slot3 == 4 and slot1 == 5):
        print("You Hit The Large Wild Jackpot!!!")
        winnings = multiplier * 1600 / 4
    else:
        print("No Hit")
        winnings = 0
    print(f"You Win ${winnings}")
    return winnings


def main():
    bank = 1000
    random.seed(time.time())
    multiplier = 1
    cont = 1
    slotChoice=3
    r = tk.Tk()
    r.title('Slot Machine Choices')
    slotChoice = tk.IntVar()
    slotChoice.set(0)
    while cont == 1 and bank > 0:
        print(f"You currently have: ${bank}")
        print("1) $10 spins, jackpot: $4000")
        print("2) $50 spins, jackpot: $20000")
        print("3) $100 spins, jackpot: $40000")
        print(f"{SPADE}: 0")
        print(f"{DIAMOND}: 1")
        print(f"{CLUB}: 2")
        print(f"{HEART}: 3")
        print(f"{IDK}: 4")
        print(f"{IDRK}: JOKER")
        # slotChoice = int(input("Your choice: "))
        def slotChoiceis1():
            slotChoice=1
            button.config(state=tk.DISABLED)

        def slotChoiceis2():
            slotChoice=2
        def slotChoiceis3():
            slotChoice=3
        
        button = tk.Button(r, text='1', width=25,command=slotChoiceis1 )
        button.pack()
        r.mainloop()

        if slotChoice == 1:
            multiplier = 1
        elif slotChoice == 2:
            multiplier = 5
        elif slotChoice == 3:
            multiplier = 10
        bank -= multiplier * 10

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Spinning", end='', flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end='', flush=True)
        print()

        slot1 = random.randint(0, 5)
        slot = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot1]
        print(f"You got a {slot}")

        print("Spinning", end='', flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end='', flush=True)
        print()

        slot2 = random.randint(0, 5)
        slot = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot2]
        print(f"You got a {slot}")

        print("Spinning", end='', flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end='', flush=True)
        print()

        slot3 = random.randint(0, 5)
        slot = [SPADE, DIAMOND, CLUB, HEART, IDK, IDRK][slot3]
        if slot1 == slot2:
            for _ in range(2):
                time.sleep(0.3)
                print(".", end='', flush=True)
        print(f"You got a {slot}")

        bank += checkwin(multiplier, slot1, slot2, slot3)
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        cont = int(input("Would you like to continue (1 - Yes) (2 - No): "))

    if bank < 1:
        print("You ran out of money haha")
    else:
        print(f"You ended with ${bank}. Thanks for playing")

if __name__ == "__main__":
    main()
