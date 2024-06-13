import random
import time

def result(roll, user_choice):
    rolltotal = 0
    while True:
        if user_choice == 1:  # Pass Line bet
            if roll in (7, 11):
                return 1
            elif roll in (2, 3, 12):
                return 0
            else:
                while rolltotal not in (roll, 7):
                    print(f"Rerolling for {roll}", end="")
                    time.sleep(0.4)
                    print(".", end="")
                    time.sleep(0.4)
                    print(".", end="")
                    time.sleep(0.4)
                    print()
                    roll1 = random.randint(1, 6)
                    roll2 = random.randint(1, 6)
                    rolltotal = roll1 + roll2
                    print(f"({rolltotal})")
                if rolltotal != 7:
                    return 1
                else:
                    return 0

        elif user_choice == 2:  # Don't Pass Line bet
            if roll in (2, 3):
                return 1
            elif roll in (7, 11):
                return 0
            else:
                while rolltotal not in (roll, 7):
                    print(f"Rerolling for {roll}", end="")
                    time.sleep(0.4)
                    print(".", end="")
                    time.sleep(0.4)
                    print(".", end="")
                    time.sleep(0.4)
                    print()
                    roll1 = random.randint(1, 6)
                    roll2 = random.randint(1, 6)
                    rolltotal = roll1 + roll2
                    print(f"({rolltotal})")
                if rolltotal != 7:
                    return 1
                else:
                    return 0

def main():
    user_balance = 1000
    print(f"Welcome to Craps, you currently have ${user_balance}")
    print("""Here are the basic rules:
Two dice will be rolled, and you will compete against our dealer
You can bet either Pass Line or Don't Pass Line
        
Pass Line: If the first roll is a 7 or 11, win. If the dice rolls 2, 3 or 12, you lose
Don't Pass Line: Win if the first roll is a 2 or 3, lose if it's a 7 or 11. If the dice rolls 12, push (no win or lose)
If the dice rolls neither of these numbers, keep rolling until the dice rolls either the same number again (win) or 7 (lose) """)

    while True:
        print("""What type of bet would you like to place?
    1) Pass Line
    2) Don't Pass Line
    3) Exit""")
        user_choice = int(input())
        if user_choice in (1, 2):
            print(f"How much would you like to bet? (You currently have ${user_balance}.")
            user_bet = int(input())
            if user_bet <= user_balance:
                print("Rolling the dice", end="")
                time.sleep(0.7)
                print(".", end="")
                time.sleep(0.7)
                print(".",end="")
                time.sleep(0.7)
                print()
                roll1 = random.randint(1, 6)
                roll2 = random.randint(1, 6)
                rolltotal = roll1 + roll2
                print(f"({rolltotal})")
                win = result(rolltotal, user_choice)
                if win == 1:
                    print(f"You won ${user_bet}!")
                    user_balance += user_bet
                else:
                    print(f"Sorry! You lost ${user_bet}!")
                    user_balance -= user_bet
            else:
                print("Enter a valid bet!")
        elif user_choice == 3:
            break
        else:
            print("Please enter a valid option!")

        if user_balance == 0:
            break

    if user_balance == 0:
        print("You lost all your money and got kicked out as a result.")
    print("You have exited the game, see you next time!")

if __name__ == "__main__":
    main()

