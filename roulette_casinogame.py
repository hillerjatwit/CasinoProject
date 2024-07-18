import random
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Function to generate a random number between 0 and 36
def spin_wheel():
    return random.randint(0, 36)

# Function to generate a random color (black or red)
def generate_color():
    return "Black" if random.randint(0, 1) == 0 else "Red"

# Function to validate street number
def is_valid_street(number):
    return 0 <= number <= 34

# Function to display game rules
def show_rules():
    rules = (
        "Roulette Rules:\n\n"
        "1. The game starts by placing a bet on a specific type of bet.\n"
        "2. The wheel is spun and a ball lands on a number (0-36).\n"
        "3. The color of the number can be either black or red.\n"
        "4. Based on the outcome, the winnings are calculated and added to or subtracted from the total money.\n"
    )
    messagebox.showinfo("Rules", rules)

# Function to display types of bets
def show_bet_types():
    bet_types = (
        "Types of Bets:\n\n"
        "1. Straight up: Bet on a single number (0-36).\n"
        "2. Split: Bet on two adjacent numbers.\n"
        "   - Examples: (1, 2), (2, 3), (4, 5), (1, 4), (2, 5), (3, 6)\n"
        "3. Street: Bet on three consecutive numbers in a row.\n \n"
        "   - 0: Covers numbers 0, 1, 2\n"
        "   - 1: Covers numbers 1, 2, 3\n"
        "   - 4: Covers numbers 4, 5, 6\n"
        "   - 7: Covers numbers 7, 8, 9\n"
        "   - 10: Covers numbers 10, 11, 12\n"
        "   - 13: Covers numbers 13, 14, 15\n"
        "   - 16: Covers numbers 16, 17, 18\n"
        "   - 19: Covers numbers 19, 20, 21\n"
        "   - 22: Covers numbers 22, 23, 24\n"
        "   - 25: Covers numbers 25, 26, 27\n"
        "   - 28: Covers numbers 28, 29, 30\n"
        "   - 31: Covers numbers 31, 32, 33\n"
        "   - 34: Covers numbers 34, 35, 36\n \n"
        "4. Red/Black: Bet on the color of the number.\n"
        "5. Even/Odd: Bet on whether the number is even or odd.\n"
        "6. Column: Bet on one of the three columns.\n\n"
        "   - Column 1: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34\n"
        "   - Column 2: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35\n"
        "   - Column 3: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36\n\n"
        "7. High/Low: Bet on whether the number is high (19-36) or low (1-18).\n"
    )
    messagebox.showinfo("Types of Bets", bet_types)

# Function to show the roulette board
def show_roulette_board():
    clear_game_frame()
    numbers = [
        [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    ]

    colors = {
        0: "green", 1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black", 7: "red", 8: "black", 9: "red",
        10: "black", 11: "black", 12: "red", 13: "black", 14: "red", 15: "black", 16: "red", 17: "black", 18: "red",
        19: "red", 20: "black", 21: "red", 22: "black", 23: "red", 24: "black", 25: "red", 26: "black", 27: "red",
        28: "black", 29: "black", 30: "red", 31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red"
    }

    for row in numbers:
        frame = tk.Frame(game_frame)
        frame.pack()
        for num in row:
            label = tk.Label(frame, text=num, borderwidth=2, relief="solid", width=5, height=2, bg=colors[num], fg="white")
            label.pack(side="left")

    zero_label = tk.Label(game_frame, text="0", borderwidth=2, relief="solid", width=5, height=2, bg=colors[0], fg="white")
    zero_label.pack(pady=10)
    
    tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
    game_frame.pack(padx=20, pady=20)

# Function to start the game
def start_game():
    clear_game_frame()
    tk.Label(game_frame, text="Enter your starting amount of money:").pack(pady=10)
    initial_money_entry.pack(pady=10)
    tk.Button(game_frame, text="Submit", command=set_initial_money).pack(pady=10)
    tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
    game_frame.pack(padx=20, pady=20)

# Function to set the initial amount of money
def set_initial_money():
    global total_money
    try:
        total_money = int(initial_money_entry.get())
        if total_money <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount of money.")
        return
    update_money_label()
    ask_bet_amount()

# Function to ask for bet amount
def ask_bet_amount():
    clear_game_frame()
    tk.Label(game_frame, text="Place your bet amount ($10 per round):").pack(pady=10)
    bet_amount_entry.pack(pady=10)
    tk.Button(game_frame, text="Next", command=ask_bet_type).pack(pady=10)
    tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
    game_frame.pack(padx=20, pady=20)

# Function to ask for bet type
def ask_bet_type():
    global bet_amount
    if not validate_bet_amount():
        return
    if bet_amount > total_money:
        messagebox.showerror("Invalid Bet", "You don't have enough money to place this bet.")
        return

    clear_game_frame()
    tk.Label(game_frame, text="Choose the type of bet:").pack(pady=10)
    for text, value in [("Straight up", 1), ("Split", 2), ("Street", 3), ("Red/Black", 4), ("Even/Odd", 5), ("Column", 6), ("High/Low", 7)]:
        tk.Radiobutton(game_frame, text=text, variable=bet_type_var, value=value).pack()

    tk.Button(game_frame, text="Next", command=ask_bet_details).pack(pady=10)
    tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
    game_frame.pack(padx=20, pady=20)

# Function to validate bet amount input
def validate_bet_amount():
    try:
        global bet_amount
        bet_amount = int(bet_amount_entry.get())
        if bet_amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid bet amount.")
        return False
    return True

# Function to ask for bet details based on bet type
def ask_bet_details():
    clear_game_frame()
    bet_type = bet_type_var.get()
    entry_widgets = {
        1: [("Enter the number to bet on (0-36):", entry_bet_number)],
        2: [("Enter the first adjacent number to bet on (0-36):", entry_bet_number1), ("Enter the second adjacent number to bet on (0-36):", entry_bet_number2)],
        3: [("Enter the street number to bet on (0-34):", entry_bet_number)],
        4: [("Enter '0' for black or '1' for red:", entry_bet_color)],
        5: [("Enter '0' for even or '1' for odd:", entry_bet_even_odd)],
        6: [("Enter '1' for Column 1, '2' for Column 2, or '3' for Column 3:", entry_bet_column)],
        7: [("Enter '1' for high or '2' for low:", entry_bet_high_low)],
    }

    for label, entry in entry_widgets[bet_type]:
        tk.Label(game_frame, text=label).pack(pady=10)
        entry.pack(pady=10)

    tk.Button(game_frame, text="Place Bet", command=place_bet).pack(pady=10)
    tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
    game_frame.pack(padx=20, pady=20)

# Function to place the bet and calculate the result
def place_bet():
    global total_money
    total_money -= 10  # Cost per round
    bet_type = bet_type_var.get()

    try:
        bet_details = get_bet_details(bet_type)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid bet details.")
        return

    result = spin_wheel()
    color = generate_color()

    messagebox.showinfo("Result", f"The wheel spins... It lands on {result} ({color})!")

    outcome = "Loss"
    amount = -bet_details['amount']
    if bet_wins(bet_type, bet_details, result, color):
        winnings = calculate_winnings(bet_type, bet_details['amount'])
        total_money += winnings
        outcome = "Win"
        amount = winnings
        messagebox.showinfo("Congratulations", f"You win ${winnings}!")
    else:
        total_money -= bet_details['amount']
        messagebox.showinfo("Sorry", "You lose.")

    update_money_label()
    record_game_result(result, color, outcome, amount)
    update_games_table(outcome)

    if total_money <= 0:
        messagebox.showinfo("Game Over", "You have no more money. Game over!")
        game_frame.pack_forget()
        start_frame.pack(padx=20, pady=20)
    else:
        ask_bet_amount()

# Function to get bet details based on bet type
def get_bet_details(bet_type):
    bet_details = {'amount': int(bet_amount_entry.get())}
    if bet_type == 1:
        bet_details['number'] = int(entry_bet_number.get())
        if not (0 <= bet_details['number'] <= 36):
            throw_value_error()
    elif bet_type == 2:
        bet_details['number1'] = int(entry_bet_number1.get())
        bet_details['number2'] = int(entry_bet_number2.get())
        if not (0 <= bet_details['number1'] <= 36) or not (0 <= bet_details['number2'] <= 36) or abs(bet_details['number1'] - bet_details['number2']) != 1:
            throw_value_error()
    elif bet_type == 3:
        bet_details['number'] = int(entry_bet_number.get())
        if not is_valid_street(bet_details['number']):
            throw_value_error()
    elif bet_type == 4:
        bet_details['color'] = int(entry_bet_color.get())
        if bet_details['color'] not in [0, 1]:
            throw_value_error()
    elif bet_type == 5:
        bet_details['even_odd'] = int(entry_bet_even_odd.get())
        if bet_details['even_odd'] not in [0, 1]:
            throw_value_error()
    elif bet_type == 6:
        bet_details['column'] = int(entry_bet_column.get())
        if bet_details['column'] not in [1, 2, 3]:
            throw_value_error()
    elif bet_type == 7:
        bet_details['high_low'] = int(entry_bet_high_low.get())
        if bet_details['high_low'] not in [1, 2]:
            throw_value_error()
    return bet_details

# Function to raise ValueError
def throw_value_error():
    raise ValueError

# Function to check if the bet wins
def bet_wins(bet_type, bet_details, result, color):
    if bet_type == 1:
        return result == bet_details['number']
    elif bet_type == 2:
        return result in [bet_details['number1'], bet_details['number2']]
    elif bet_type == 3:
        return result in [bet_details['number'], bet_details['number'] + 1, bet_details['number'] + 2]
    elif bet_type == 4:
        return (color == "Black" and bet_details['color'] == 0) or (color == "Red" and bet_details['color'] == 1)
    elif bet_type == 5:
        return (result % 2 == 0 and bet_details['even_odd'] == 0) or (result % 2 != 0 and bet_details['even_odd'] == 1)
    elif bet_type == 6:
        return 1 + 12 * (bet_details['column'] - 1) <= result <= 12 * bet_details['column']
    elif bet_type == 7:
        return (1 <= result <= 18 and bet_details['high_low'] == 1) or (19 <= result <= 36 and bet_details['high_low'] == 2)

# Function to calculate winnings based on bet type and amount
def calculate_winnings(bet_type, amount):
    odds = {1: 35, 2: 17, 3: 11, 4: 1, 5: 1, 6: 2, 7: 1}
    return amount * odds[bet_type]

# Function to update the money label
def update_money_label():
    label_total_money.config(text=f"Your total money: ${total_money}")

# Function to clear the game frame
def clear_game_frame():
    for widget in game_frame.winfo_children():
        if widget != label_total_money:
            widget.pack_forget()

# Function to record the game result in the database
def record_game_result(result, color, outcome, amount):
    try:
        conn = sqlite3.connect("CasinoDB.db")
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = 'user1'  # Example user ID, should be dynamic
        game_id = 'Roulette'
        sql_command = """INSERT INTO HISTORY (TIMESTAMP, GAMEID, USERID, RESULT, AMOUNT)
                         VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sql_command, (timestamp, game_id, user_id, outcome, amount))
        conn.commit()
        print("Database updated successfully")
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        conn.close()

# Function to update the Roulette row in the GAMES table
def update_games_table(outcome):
    try:
        conn = sqlite3.connect("CasinoDB.db")
        cursor = conn.cursor()
        if outcome == "Win":
            sql_command = "UPDATE GAMES SET WINS = WINS + 1 WHERE GAMEID = 'Roulette'"
        else:
            sql_command = "UPDATE GAMES SET LOSSES = LOSSES + 1 WHERE GAMEID = 'Roulette'"
        cursor.execute(sql_command)
        conn.commit()
        print("GAMES table updated successfully")
    except Exception as e:
        print(f"Error updating GAMES table: {e}")
    finally:
        conn.close()

# Function to return to the main menu
def return_to_main_menu():
    game_frame.pack_forget()
    start_frame.pack(padx=20, pady=20)

# Initialize the main window
root = tk.Tk()
root.title("Roulette Game")

total_money = 0
bet_amount = 0

# Frame for starting the game and viewing rules and bet types
start_frame = tk.Frame(root, bg='green', padx=20, pady=20)
start_frame.pack(padx=20, pady=20)

# Add a big title for the game
title_label = tk.Label(start_frame, text="Roulette", font=("Helvetica", 24), bg='green')
title_label.grid(row=0, column=0, padx=10, pady=10)

button_rules = ttk.Button(start_frame, text="View Rules", command=show_rules)
button_rules.grid(row=1, column=0, padx=10, pady=10)

button_bet_types = ttk.Button(start_frame, text="View Types of Bets", command=show_bet_types)
button_bet_types.grid(row=2, column=0, padx=10, pady=10)

button_roulette_board = ttk.Button(start_frame, text="Roulette Board", command=show_roulette_board)
button_roulette_board.grid(row=3, column=0, padx=10, pady=10)

button_start = ttk.Button(start_frame, text="Start Game", command=start_game)
button_start.grid(row=4, column=0, padx=10, pady=10)

# Frame for the actual game
game_frame = tk.Frame(root, bg='darkred', padx=20, pady=20)

initial_money_entry = ttk.Entry(game_frame)
bet_amount_entry = ttk.Entry(game_frame)
entry_bet_number = ttk.Entry(game_frame)
entry_bet_number1 = ttk.Entry(game_frame)
entry_bet_number2 = ttk.Entry(game_frame)
entry_bet_color = ttk.Entry(game_frame)
entry_bet_even_odd = ttk.Entry(game_frame)
entry_bet_column = ttk.Entry(game_frame)
entry_bet_high_low = ttk.Entry(game_frame)

bet_type_var = tk.IntVar()

label_total_money = ttk.Label(game_frame, text="Your total money: $0", background='darkred', foreground='white')
label_total_money.pack(pady=10)

root.mainloop()
