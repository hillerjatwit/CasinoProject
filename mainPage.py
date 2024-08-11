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
from tkinter import messagebox, simpledialog
from typing import Union
from datetime import datetime
from PIL import Image, ImageTk

# Initialize the user database (in a real application, use a secure database)
user_db = {}

class dbConnection:
    # FOR EASE OF USE
    DatabaseURI = "CasinoDB.db"
    cur = None
    db = None

    def __init__(self):
        self.db = sqlite3.connect(self.DatabaseURI)
        self.cur = self.db.cursor()

    def query(self, query):
        # IF YOU WANT TO RUN A QUERY
        self.cur.execute(query)
        return self.cur.fetchone()

    def queryall(self, query):
        # IF YOU WANT TO RUN A QUERY
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQLite error: {e}")
            return []

    def queryExecute(self, query):
        # IF YOU WANT TO RUN AN EXECUTABLE
        self.cur.execute(query)
        self.db.commit()

#Poker Classes and definitions:
# Player class definition
class Player:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand.clear()

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.value)

    def display_hand(self):
        return ", ".join([f"{card.name} of {card.suit}" for card in self.hand])

# Card class definition
# Mapping suits to symbols
suit_symbols = {
    "HEARTS": "♥",
    "DIAMONDS": "♦",
    "CLUBS": "♣",
    "SPADES": "♠"
}

class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value
        self.image = None

    def get_image(self, card_images):
        return card_images[f"{self.name} of {self.suit}", None]

# Deck class definition
# class Deck:
#     def __init__(self):
#         self.cards = [Card(name, suit, value) for suit in ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
#                       for value, name in enumerate(["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"], 1)]

#     def shuffle_deck(self):
#         random.shuffle(self.cards)

#     def deal_card(self):
#         return self.cards.pop() if self.cards else None
class Deck:
    def __init__(self):
        self.cards = []
        self.make_deck()

    def make_deck(self):
        suits = ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
        names = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        # Create a list of Card objects for each suit and name
        self.cards = [Card(names[i], suit, values[i]) for suit in suits for i in range(13)]
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() 
    
    

# PokerGame class definition
class PokerGame:
    def __init__(self):
        print("Initializing PokerGame")
        self.connect_to_database()  # Connect to the database first
        self.create_tables()  # Create necessary tables if they don't exist
        self.deck = Deck()  # Create a deck of cards
        self.players = [Player("Player 1", 150), Player("Computer 1", 150), Player("Computer 2", 150)]  # Create 1 human player and 2 computer players with initial wallet amount
        self.pot = 0  # Initialize the pot
        self.player_winnings = {}  # Dictionary to track player winnings
        self.root = tk.Tk()  # Create the main window
        self.root.title("Poker Game")  # Set the title of the main window
        self.card_images = self.load_card_images()  # Load card images
        self.image_references = []
        self.back_of_card_image = self.load_back_of_card_image()  # Load the back of card image
        self.hand_windows = []  # List to keep track of hand windows
        self.create_menu()  # Create the menu

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect('CasinoDB.db')
            self.cursor = self.conn.cursor()
            print("Database connection established")
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS HISTORY (
                                   TIMESTAMP TEXT,
                                   GAMEID INTEGER,
                                   USERID TEXT,
                                   RESULT TEXT,
                                   AMOUNT INTEGER
                                   )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS USER (
                                   USERID TEXT PRIMARY KEY,
                                   PASSWORD TEXT,
                                   NETGAIN INTEGER,
                                   BALANCE INTEGER,
                                   HASCHEATED BOOLEAN
                                   )''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Table creation failed: {e}")

    def save_game_result(self, game_id, user_id, result, amount):
        try:
            print(f"Saving game result for user {user_id}")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("INSERT INTO HISTORY (TIMESTAMP, GAMEID, USERID, RESULT, AMOUNT) VALUES (?, ?, ?, ?, ?)",
                                (timestamp, game_id, user_id, result, amount))
            self.conn.commit()
            print(f"Game result saved for user {user_id}: {result} with amount {amount}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_user_balance_and_netgain(self, user_id, netgain, balance):
        try:
            print(f"Updating user balance and net gain for user {user_id}")
            self.cursor.execute("UPDATE USER SET NETGAIN = NETGAIN + ?, BALANCE = BALANCE + ? WHERE USERID = ?",
                                (netgain, balance, user_id))
            self.conn.commit()
            print(f"User balance and net gain updated for user {user_id}: Net Gain {netgain}, Balance {balance}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")


    def load_card_images(self):
        card_images = {}
        # Path to the directory containing card images
        
        card_name_mapping = {
            "ACE": "ace",
            "TWO": "2",
            "THREE": "3",
            "FOUR": "4",
            "FIVE": "5",
            "SIX": "6",
            "SEVEN": "7",
            "EIGHT": "8",
            "NINE": "9",
            "TEN": "10",
            "JACK": "jack",
            "QUEEN": "queen",
            "KING": "king"
        }
        image_dir = r"C:\Users\penacruzn\OneDrive - Wentworth Institute of Technology\Desktop\DECK OF CARDS"
        for suit in ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]:
            for name in ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING"]:
                filename = f"{card_name_mapping[name]}_of_{suit.lower()}.png"
                path = os.path.join(image_dir, filename)
                if os.path.exists(path):
                    image = Image.open(path)
                    image = image.resize((100, 150), Image.LANCZOS)  # Resize the image
                    card_images[f"{name} of {suit}"] = ImageTk.PhotoImage(image)
                else:
                    print(f"Image not found: {path}")
        return card_images

    def load_back_of_card_image(self):
        path = r"C:\Users\penacruzn\OneDrive - Wentworth Institute of Technology\Desktop\POKER_GAME\DECK OF CARDS\Back_of_card.png"
        image = Image.open(path)
        image = image.resize((100, 150), Image.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(image)

    def create_menu(self):
        self.root.geometry("600x400")  # Set the window size
        menu_frame = tk.Frame(self.root, bg="green")  # Create a frame for the menu
        menu_frame.pack(expand=True, fill="both")  # Pack the frame to fill the window

        # Create and pack the welcome label
        welcome_label = tk.Label(menu_frame, text="Welcome to Poker", font=("Comic Sans MS", 24, "bold"), bg="green", fg="white")
        welcome_label.pack(pady=20)

        # Create and pack the "Go to Table" button
        btn_go_to_table = tk.Button(menu_frame, text="Go to Table", command=self.start_game, bg="blue", fg="white", font=("Arial", 16))
        btn_go_to_table.pack(pady=10)

        # Create and pack the "See Rules" button
        btn_see_rules = tk.Button(menu_frame, text="See Rules", command=self.display_rules, bg="blue", fg="white", font=("Arial", 16))
        btn_see_rules.pack(pady=10)

        # Create and pack the "See Poker Hands and Rules" button
        btn_see_hands_rules = tk.Button(menu_frame, text="See Poker Hands and Rules", command=self.display_hands_and_rules, bg="blue", fg="white", font=("Arial", 16))
        btn_see_hands_rules.pack(pady=10)

        # Create and pack the "Quit Game" button
        btn_quit = tk.Button(menu_frame, text="Quit Game", command=self.root.quit, bg="blue", fg="white", font=("Arial", 16))
        btn_quit.pack(pady=10)

        self.root.mainloop()  # Start the Tkinter main loop

    def start_game(self):
        rounds = simpledialog.askinteger("Rounds", "Enter the number of rounds to play:", minvalue=1, maxvalue=100)
        for round_number in range(1, rounds + 1):
            messagebox.showinfo("Round", f"Round {round_number}")
            self.play_round()
            if self.check_winner():
                break
        self.display_final_winner()

    def play_round(self):
        ante = 10  # Ante amount for each player
        for player in self.players:
            player.wallet -= ante  # Deduct ante from each player's wallet
            self.pot += ante  # Add ante to the pot
        self.deck.shuffle_deck()  # Shuffle the deck before dealing new cards
        self.deal_cards()  # Deal cards to players
        self.betting_cycle()  # Start the first betting cycle
        self.discard_phase()  # Allow players to discard and draw new cards
        self.betting_cycle()  # Start the second betting cycle
        self.determine_winner()  # Determine the winner of the game
        self.print_wallets()  # Display the updated wallets

    def deal_cards(self):
        self.close_all_hand_windows()  # Close all open hand windows
        for player in self.players:
            player.hand.clear()  # Clear the player's hand before dealing new cards
        for _ in range(5):
            for player in self.players:
                if len(self.deck.cards) == 0:
                    messagebox.showinfo("Reshuffle", "Deck is empty. Reshuffling deck.")
                    self.deck = Deck()
                    self.deck.shuffle_deck()
                card = self.deck.deal_card()  # Deal a card to the player
                player.add_card_to_hand(card)  # Add the card to the player's hand
                card.image = card.get_image(self.card_images)  # Assign the image to the card

        for player in self.players:
            player.sort_hand()  # Sort the player's hand
            self.display_hand(player)  # Display the player's hand

    def display_hand(self, player):
        hand_window = tk.Toplevel(self.root)  # Create a new window for the player's hand
        self.hand_windows.append(hand_window)  # Keep track of the hand window
        hand_window.title(f"{player.name}'s Hand")  # Set the title of the hand window
        
        hand_frame = tk.Frame(hand_window)  # Create a frame for the hand
        hand_frame.pack(pady=20)  # Pack the frame

        # Display each card in the player's hand
        for card in player.hand:
            if player.name.startswith("Player"):
                card_label = tk.Label(hand_frame, image=card.image, padx=10, pady=5)
            else:
                card_label = tk.Label(hand_frame, image=self.back_of_card_image, padx=10, pady=5)
            card_label.pack(side="left")
            self.image_references.append(card.image)

    def update_hand_display(self, player, window):
        for widget in window.winfo_children():  # Clear existing widgets in the window
            widget.destroy()
        # Display each card in the player's hand
        for card in player.hand:
            if player.name.startswith("Player"):
                card_label = tk.Label(window, image=card.image, padx=10, pady=5)
            else:
                card_label = tk.Label(window, image=self.back_of_card_image, padx=10, pady=5)
            card_label.pack(side="left")

    def close_all_hand_windows(self):
        for window in self.hand_windows:  # Close all hand windows
            window.destroy()
        self.hand_windows.clear()  # Clear the list of hand windows

    def betting_cycle(self):
        current_bet = 0  # Initialize the current bet
        for player in self.players:
            if player.hand:  # If the player has not folded
                if player.name.startswith("Player"):
                    # Human player
                    bet = simpledialog.askinteger("Betting", f"{player.name}'s turn. Current bet is {current_bet}. Your wallet: {player.wallet}\nEnter your bet (0 to fold): ")
                else:
                    # Computer player makes a random bet
                    bet = random.randint(0, min(player.wallet, current_bet + 20))
                    messagebox.showinfo("Betting", f"{player.name} bets {bet}")  # Show the computer player's bet in a message box

                if bet == 0:
                    player.hand.clear()  # Clear the player's hand if they fold
                else:
                    current_bet = max(current_bet, bet)  # Update the current bet
                    player.wallet -= bet  # Deduct the bet from the player's wallet
                    self.pot += bet  # Add the bet to the pot

    def discard_phase(self):
        for player in self.players:
            if player.hand:  # If the player has not folded
                self.close_all_hand_windows()  # Close all hand windows before showing the current player's hand
                hand_window = tk.Toplevel(self.root)  # Create a new window for the player's hand
                self.hand_windows.append(hand_window)  # Keep track of the hand window
                hand_window.title(f"{player.name}'s Hand")

                hand_frame = tk.Frame(hand_window)  # Create a frame for the hand
                hand_frame.pack(pady=20)

                self.update_hand_display(player, hand_frame)  # Display the player's hand

                if player.name.startswith("Player"):
                    # Human player discards
                    discard_indexes = simpledialog.askstring("Discard Phase", f"{player.name}, choose the cards to discard (enter indexes separated by spaces):\n{player.display_hand()}")
                    discard_indexes = [int(x)-1 for x in discard_indexes.split() if x.isdigit()]
                else:
                    # Computer player randomly chooses cards to discard
                    discard_indexes = random.sample(range(5), random.randint(0, 5))
                    messagebox.showinfo("Discarding", f"{player.name} discards {discard_indexes}")  # Show the computer player's discards in a message box

                for idx in sorted(discard_indexes, reverse=True):
                    if 0 <= idx < len(player.hand):
                        player.hand.pop(idx)  # Remove the discarded card from the player's hand
                        if len(self.deck.cards) == 0:
                            messagebox.showinfo("Reshuffle", "Deck is empty. Reshuffling deck.")
                            self.deck = Deck()
                            self.deck.shuffle_deck()
                        card = self.deck.deal_card()  # Deal a new card to the player
                        card.image = card.get_image(self.card_images)  # Assign the image to the card
                        player.add_card_to_hand(card)  # Add the card to the player's hand

                player.sort_hand()  # Sort the player's hand
                self.update_hand_display(player, hand_frame)  # Update the display of the player's hand
    
                # Close the current player's hand window after they finish discarding
                hand_window.destroy()

    def determine_winner(self):
        player_hands = []
        player_cards = {}

        for player in self.players:
            if player.hand:
                hand_type = self.evaluate_hand(player.hand)  # Evaluate the player's hand
                player_hands.append((player.name, hand_type))  # Add the player's hand type to the list
                player_cards[player.name] = player.hand  # Store the player's hand

        if not player_hands:  # If all players folded
            messagebox.showinfo("Result", "All players folded. No winner.")
            return

        # Rank the hands and determine the winner
        hand_rank = {
            "High Card": 1, "One Pair": 2, "Two Pair": 3,
            "Three of a Kind": 4, "Straight": 5, "Flush": 6,
            "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10
        }

        player_hands.sort(key=lambda pair: hand_rank[pair[1]], reverse=True)

        winner_name = player_hands[0][0]
        winner_hand_type = player_hands[0][1]
        messagebox.showinfo("Winner", f"Congratulations {winner_name} wins with a {winner_hand_type}!")
        winning_hand = ", ".join([f"{card.name} of {card.suit}" for card in player_cards[winner_name]])
        messagebox.showinfo("Winning Hand", f"Winning hand: {winning_hand}")

        # Display the hands of the losers
        losers_hands = []
        for name, hand in player_cards.items():
            if name != winner_name:
                hand_str = ", ".join([f"{card.name} of {card.suit}" for card in hand])
                losers_hands.append(f"{name}'s hand: {hand_str}")
        messagebox.showinfo("Losers' Hands", "\n".join(losers_hands))

        # Update the player's winnings
        self.player_winnings[winner_name] = self.player_winnings.get(winner_name, 0) + self.pot

        self.pot = 0

    def print_wallets(self):
        wallets_display = ""
        for player in self.players:
            wallets_display += f"{player.name}'s Wallet: {player.wallet + self.player_winnings.get(player.name, 0)}\n"
        messagebox.showinfo("Wallets", wallets_display)

    def check_winner(self):
        active_players = [player for player in self.players if player.wallet > 0]
        if len(active_players) == 1:
            messagebox.showinfo("Game Over", f"{active_players[0].name} is the last player remaining and wins the game!")
            return True
        return False

    def display_final_winner(self):
        winner = max(self.players, key=lambda player: player.wallet)
        messagebox.showinfo("Game Over", f"{winner.name} has the most chips and wins the game!")

    def evaluate_hand(self, hand):
        # Evaluate the hand and return the hand type
        if self.is_royal_flush(hand):
            return "Royal Flush"
        if self.is_straight_flush(hand):
            return "Straight Flush"
        if self.is_four_of_a_kind(hand):
            return "Four of a Kind"
        if self.is_full_house(hand):
            return "Full House"
        if self.is_flush(hand):
            return "Flush"
        if self.is_straight(hand):
            return "Straight"
        if self.is_three_of_a_kind(hand):
            return "Three of a Kind"
        if self.is_two_pair(hand):
            return "Two Pair"
        if self.is_one_pair(hand):
            return "One Pair"
        return "High Card"

    def is_royal_flush(self, hand):
        return self.is_straight_flush(hand) and hand[0].value == 10

    def is_straight_flush(self, hand):
        return self.is_straight(hand) and self.is_flush(hand)

    def is_four_of_a_kind(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 4 in counts.values()

    def is_full_house(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 3 in counts.values() and 2 in counts.values()

    def is_flush(self, hand):
        return all(card.suit == hand[0].suit for card in hand)

    def is_straight(self, hand):
        return all(hand[i].value == hand[i - 1].value + 1 for i in range(1, len(hand)))

    def is_three_of_a_kind(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 3 in counts.values()

    def is_two_pair(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return list(counts.values()).count(2) == 2

    def is_one_pair(self, hand):
        counts = {card.value: sum(1 for c in hand if c.value == card.value) for card in hand}
        return 2 in counts.values()

    def display_rules(self):
        # Display the rules of the poker game
        rules = (
            "Poker Rules:\n"
            "1. The game is 5-card draw poker.\n"
            "2. Each player is dealt 5 cards.\n"
            "3. Players bet, discard, and draw new cards.\n"
            "4. Best hand wins the pot.\n"
            "5. $10 to play each round.\n\n"
            "Betting Rules:\n"
            "During each betting cycle, players have three options:\n"
            "  a. Fold (Enter 0): If you think your hand is weak, you can fold by entering 0.\n"
            "     This means you will not participate further in this round, and your cards will be discarded.\n"
            "  b. Call (Enter the current bet amount): If you want to match the current highest bet placed by other players,\n"
            "     you enter an amount equal to the current bet. This means you are staying in the game by matching the current bet.\n"
            "  c. Raise (Enter an amount greater than the current bet): If you believe your hand is strong or you want to bluff,\n"
            "     you can enter an amount greater than the current bet to raise. This forces other players to either match your new bet or fold.\n\n"
            "Example:\n"
            "  - Assume the current bet is 10.\n"
            "  - If you think your hand is weak and you don't want to continue, enter 0 to fold.\n"
            "  - If you think your hand is decent and you want to stay in the game without raising the stakes, enter 10 to call the current bet.\n"
            "  - If you think your hand is strong or want to bluff, enter 20 or any higher amount to raise the bet.\n"
            "    This means other players will now have to match 20 to stay in the game.\n"
        )
        messagebox.showinfo("Poker Rules", rules)

    def display_hands_and_rules(self):
        # Display the poker hands and rules
        hands_rules = (
            "Poker Hands and Rules:\n"
            "1. Royal Flush: A, K, Q, J, 10, all the same suit.\n"
            "2. Straight Flush: Five cards in a sequence, all the same suit.\n"
            "3. Four of a Kind: All four cards of the same rank.\n"
            "4. Full House: Three of a kind with a pair.\n"
            "5. Flush: Any five cards of the same suit, but not in a sequence.\n"
            "6. Straight: Five cards in a sequence, but not of the same suit.\n"
            "7. Three of a Kind: Three cards of the same rank.\n"
            "8. Two Pair: Two different pairs.\n"
            "9. One Pair: Two cards of the same rank.\n"
            "10. High Card: When you haven't made any of the hands above, the highest card plays.\n"
        )
        messagebox.showinfo("Poker Hands and Rules", hands_rules)

# Function to handle user login
def login():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()

    username = login_username_entry.get()
    password = login_password_entry.get()
    global user_db
    user_db = conn.queryall(
        f"""SELECT USERID, PASSWORD
        FROM USER
        WHERE USERID = '{username}' 
        AND PASSWORD = '{password}'"""
    )
    isadmin = 0
    if user_db == []:  # If admin login
        user_db = conn.queryall(
            f"""SELECT USERID, PASSWORD
            FROM ADMIN
            WHERE USERID = '{username}'
            AND PASSWORD = '{password}'"""
        )
        isadmin = 1

    if user_db != []:
        messagebox.showinfo("Login Success", f"Welcome, {user_db[0][0]}!")
        user_db = user_db[0]
        if isadmin == 0:
            show_main_page()
        elif isadmin == 1:
            show_admin_main_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")



    # if username in user_db and user_db[0] == password:
    #     messagebox.showinfo("Login Success", f"Welcome, {user_db[1]}!")
    #     show_main_page()
    # else:
        # messagebox.showerror("Login Failed", "Invalid username or password")

# Function to handle user signup
def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = signup_confirm_password_entry.get()
    db = sqlite3.connect("CasinoDB.db")
    cursor = db.cursor()
    conn = dbConnection()
    if not username or not password or not confirm_password:
        messagebox.showerror("Signup Failed", "All fields are required")
    elif password != confirm_password:
        messagebox.showerror("Signup Failed", "Passwords do not match")
    elif username in user_db:
        messagebox.showerror("Signup Failed", "Username already exists")
    else:
        conn.queryExecute(f"""INSERT INTO USER VALUES('{username}', '{password}', 0, 1000, 0)""")

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
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()
    conn = dbConnection()
    login_frame.pack_forget()
    admin_main_frame.pack_forget()
    signup_frame.pack_forget()
    ischeat=conn.query(f"SELECT HASCHEATED FROM USER WHERE USERID = '{user_db[0]}'")
    if ischeat[0]=='1':
        main_frame.forget()
        cheaterpage=tk.Frame(root, padx=20, pady=20)
        cheaterpage = tk.Frame(root, padx=20, pady=20)
        messagebox.showinfo("CHEAT", "CHEATER DETECTED!! LOGGING OUT!")
        main_frame.pack_forget()
        signup_frame.pack_forget()
        show_login_page()
        main_frame.pack_forget()
    else:
        main_frame.pack(fill="both", expand=True)




def show_admin_main_page():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    balance_frame.pack_forget()
    admin_main_frame.pack_forget()
    admin_main_frame.pack(fill="both", expand=True)

# Function to show the login page
def show_login_page():
    admin_main_frame.pack_forget()
    signup_frame.pack_forget()
    main_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Function to show the signup page
def show_signup_page():
    login_frame.pack_forget()
    main_frame.pack_forget()
    admin_main_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)

def show_add_balance_page():
    login_frame.pack_forget()
    main_frame.pack_forget()
    admin_main_frame.pack_forget()
    balance_frame.pack(fill="both", expand=True)



# Placeholder functions for games
def play_blackjack():
    messagebox.showinfo("Blackjack", "Starting Blackjack game...")
    
    root.withdraw()
    
    root_bj = Tk()
    root_bj.title('Blackjack')
    root_bj.geometry('1500x1000')
    root_bj.configure(background="green")
    
    
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

    class Card_BJ:
        def __init__(self, label: str, suit: str):
            self.label = label
            self.suit = suit
            self.value = self._get_value()
        
        def _get_value(self) -> Union[int, tuple]:
            if self.label in ("2", "3", "4", "5", "6", "7", "8", "9", "10"):
                return int(self.label)
            if self.label in ("J", "Q", "K"):
                return 10
            if self.label == "A":
                return 11
            raise ValueError("Bad Label")
    
        def _get_name(self):
            return f"{self.label}_of_{self.suit}"
        
    class Deck_BJ:
        def __init__ (self):
            self.cards = []
            self._build()
            
        def _build(self):
            for suit in ["spades", "clubs", "diamonds", "hearts"]:
                for v in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"):
                    self.cards.append(Card_BJ(v,suit))
        
    def getUserInfo():
        global username
        
        username = "user3"
        conn = dbConnection()
        return conn.queryall(
            f"SELECT BALANCE FROM USER WHERE USERID = '{username}'"
        )
        
    def place_bet():
        global userMoney, Bet, Betplaced, username
        try:
            bet_amount = int(bet_entry.get())
            userMoney = int(userMoney)
            if int(bet_amount) > userMoney:
                messagebox.showwarning("Insufficient Funds", "You do not have enough money to place this bet.")
                return False
            else:
                Bet = bet_amount
                newBalance = userMoney - bet_amount
                conn = dbConnection()
                conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                )
                userMoney = newBalance
                updateLabels()
                return True
        except ValueError:
            messagebox.showwarning("Invalid Bet", "Please enter a valid number for the bet amount.")
            
    def updateLabels():
        money_label.config(text=f"Money: ${userMoney}")
        bet_label.config(text=f"Current Bet: ${Bet}")
        
    def stand():
        global isShowing, dealer_image1, userMoney
        
        if (not isShowing):
            isShowing = True
            dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
            dealer_label_1.config(image=dealer_image1)
            
        
        player_total = 0
        dealer_total = 0
        
        
        for score in dealer_score:
            dealer_total += score
            
        for score in player_score:
            player_total += score
            
        
        card_button.config(state="disabled")
        stand_button.config(state="disabled")
        
        if status["player"] != "bust":
            if status["dealer"] == "stand":
                if dealer_total > player_total:
                    messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: {dealer_total}")
                    return
                elif dealer_total < player_total:
                    newBalance = userMoney + (2 * Bet)
                    userMoney = newBalance
                    conn = dbConnection()
                    conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                    )
                    messagebox.showinfo("Player Wins", f"Player: {player_total}  Dealer: {dealer_total}")
                    return
                else:
                    newBalance = userMoney + Bet
                    userMoney = newBalance
                    conn = dbConnection()
                    conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                    )
                    messagebox.showinfo("Push", f"Player: {player_total}  Dealer: {dealer_total}")
                    return
            elif status["dealer"] == "hit":
                dealer_hit()
                stand()
            elif status["dealer"] == "win":
                if dealer_total == player_total:
                    newBalance = userMoney + Bet
                    userMoney = newBalance
                    conn = dbConnection()
                    conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                    )
                    messagebox.showinfo("Push", f"Player: {player_total}  Dealer: {dealer_total}")
                    return
                messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: 21")
                return
            elif status["dealer"] == "bust":
                newBalance = userMoney + (2 * Bet)
                userMoney = newBalance
                conn = dbConnection()
                conn.queryExecute(
                f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                )
                messagebox.showinfo("Player Wins", f"Player: {player_total}  Dealer: {dealer_total}")
                return
        else:
            status["dealer"] = "win"
            messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: {dealer_total}")
            return
            
        updateLabels()
            
    def resize_cards(card):
        # Open the image
        our_card_img = Image.open(card)

        # Resize The Image
        our_card_resize_image = our_card_img.resize((150, 218))
        
        # output the card
        global our_card_image
        our_card_image = ImageTk.PhotoImage(our_card_resize_image, master=root_bj)

        # Return that card
        return our_card_image

    def generate_deck():
        D = Deck_BJ()
        return D.cards
    
    def startGame():
        
        card_button.config(state="disabled")
        stand_button.config(state="disabled")

        isBetPlaced = place_bet()
        
        if isBetPlaced:
            shuffle()
        else:
            return
        
    def shuffle():
        global status, player_wins, dealer_wins, isShowing, Bet, Betplaced, count, first
        player_wins = 0
        dealer_wins = 0
        isShowing = False
        
        
        
            #reset images
        dealer_label_1.config(image='')
        dealer_label_2.config(image='')
        dealer_label_3.config(image='')
        dealer_label_4.config(image='')
        dealer_label_5.config(image='')
        player_label_1.config(image='')
        player_label_2.config(image='')
        player_label_3.config(image='')
        player_label_4.config(image='')
        player_label_5.config(image='')
        
        status = {"dealer":"no", "player":"no"}
        
        
        card_button.config(state="normal")
        stand_button.config(state="normal")
        
        global D
        D = generate_deck()
        
        global dealer, player, dealer_spot, dealer_score, player_spot, player_score
        dealer = []
        player = []
        dealer_score = []
        player_score = []
        dealer_spot = 0
        player_spot = 0
        
        dealer_hit()
        dealer_hit()
        
        player_hit()
        player_hit()
        
        
    def dealer_hit():
        global dealer_spot, dealer_total, player_total, player_score, D
        
        if dealer_spot <= 5:
            try:
                
                dealer_card = random.choice(D)
                D.remove(dealer_card)
                dealer.append(dealer_card)
                dealer_score.append(dealer_card._get_value())
                
                global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5
                
                if dealer_spot == 0:
                    # Resize Card
                    dealer_image1 = resize_cards(f'images/cards/BackOfCard.png')
                    # Output Card To Screen
                    dealer_label_1.config(image=dealer_image1)
                    # Increment our player spot counter
                    dealer_spot += 1
                elif dealer_spot == 1:
                    # Resize Card
                    dealer_image2 = resize_cards(f'images/cards/{dealer_card._get_name()}.png')
                    # Output Card To Screen
                    dealer_label_2.config(image=dealer_image2)
                    # Increment our player spot counter
                    dealer_spot += 1
                elif dealer_spot == 2:
                    # Resize Card
                    dealer_image3 = resize_cards(f'images/cards/{dealer_card._get_name()}.png')
                    # Output Card To Screen
                    dealer_label_3.config(image=dealer_image3)
                    # Increment our player spot counter
                    dealer_spot += 1
                elif dealer_spot == 3:
                    # Resize Card
                    dealer_image4 = resize_cards(f'images/cards/{dealer_card._get_name()}.png')
                    # Output Card To Screen
                    dealer_label_4.config(image=dealer_image4)
                    # Increment our player spot counter
                    dealer_spot += 1
                elif dealer_spot == 4:
                    # Resize Card
                    dealer_image5 = resize_cards(f'images/cards/{dealer_card._get_name()}.png')
                    # Output Card To Screen
                    dealer_label_5.config(image=dealer_image5)
                    # Increment our player spot counter
                    dealer_spot += 1
                    
            except:
                root_bj.title("Exception")
                
            validateGame("dealer")
            
    def player_hit():
        
        #Take card from Deck and Show on GUI, check blackjack else where
        
        global player_spot, player_total, dealer_total, player_score, D
        if player_spot <= 5:
            try:
                player_card = random.choice(D)
                D.remove(player_card)
                player.append(player_card)
                player_score.append(player_card._get_value())
                
                global player_image1, player_image2, player_image3, player_image4, player_image5
                
                
                if player_spot == 0:
                    # Resize Card
                    player_image1 = resize_cards(f'images/cards/{player_card._get_name()}.png')
                    # Output Card To Screen
                    player_label_1.config(image=player_image1)
                    # Increment our player spot counter
                    player_spot += 1
                elif player_spot == 1:
                    # Resize Card
                    player_image2 = resize_cards(f'images/cards/{player_card._get_name()}.png')
                    # Output Card To Screen
                    player_label_2.config(image=player_image2)
                    # Increment our player spot counter
                    player_spot += 1
                elif player_spot == 2:
                    # Resize Card
                    player_image3 = resize_cards(f'images/cards/{player_card._get_name()}.png')
                    # Output Card To Screen
                    player_label_3.config(image=player_image3)
                    # Increment our player spot counter
                    player_spot += 1
                elif player_spot == 3:
                    # Resize Card
                    player_image4 = resize_cards(f'images/cards/{player_card._get_name()}.png')
                    # Output Card To Screen
                    player_label_4.config(image=player_image4)
                    # Increment our player spot counter
                    player_spot += 1
                elif player_spot == 4:
                    # Resize Card
                    player_image5 = resize_cards(f'images/cards/{player_card._get_name()}.png')
                    # Output Card To Screen
                    player_label_5.config(image=player_image5)
                    # Increment our player spot counter
                    player_spot += 1
                
            except:
                #Add new deck to old deck
                root_bj.title("Exception")
                
            validateGame("player")
            
    def validateGame(player):
        
        global dealer_total, player_total, dealer_score, player_score, aceChanged

        dealer_total = 0
        player_total = 0
        aceChanged = False
        
        if player == "dealer":
            
            #Calculate total
            for score in dealer_score:
                dealer_total += score
                
            if dealer_total > 21:
                for i in range(0, len(dealer_score), 1):
                    #Check for ace if one change it
                    if dealer_score[i] == 11:
                        dealer_score[i] = 1
                        aceChanged = True
                        continue
                #If Ace was changed recalc total
                if aceChanged:
                    dealer_total = 0
                    for score in dealer_score:
                        dealer_total += score
                    #Check if bust again    
                    if dealer_total > 21:
                        #Check for another ace
                        for i in range(0, len(dealer_score), 1):
                            if dealer_score[i] == 11:
                                dealer_score[i] = 1
                                
                                dealer_total = 0
                                for score in dealer_score:
                                    dealer_total += score
                                if dealer_score == 21:
                                    status[player] = "win"
                                elif dealer_score >= 17:
                                    status[player] = "stand"
                                else:
                                    status[player] = "hit"
                                continue
                    elif dealer_total == 21:
                        status[player] = "win"
                
                    elif dealer_total >= 17:
                        status[player] = "stand"
                
                    else:
                        status[player] = "hit"
                        
                else:
                    status[player] = "bust"
                
            elif dealer_total == 21:
                status[player] = "win"
                
            elif dealer_total >= 17:
                status[player] = "stand"
                
            else:
                status[player] = "hit"
                
        elif player == "player":
            
            for score in player_score:
                player_total += score
            for score in dealer_score:
                dealer_total += score
                
            if player_total > 21:
                for i in range(0, len(player_score), 1):
                    if player_score[i] == 11:
                        player_score[i] = 1
                        aceChanged = True
                        continue
                        
                
                if aceChanged:
                    player_total = 0
                    for score in player_score:
                        player_total += score
                    
                    if player_total > 21:
                        for i in range(0, len(player_score), 1):
                            if player_score[i] == 11:
                                player_score[i] = 1
                                
                                player_total = 0
                                for score in player_score:
                                    player_total += score
                                    
                                if player_total == 21:
                                    status[player] = "win"
                                else:
                                    status[player] = "no"
                                continue
                    elif player_total == 21:
                        status[player] = "win"
                    else:
                        status[player] = "no"  
                else:
                    status[player] = "bust"          
            
            elif player_total == 21:
                status[player] = "win"
            else:
                status[player] = "no"

        
        blackjack()
            
    def blackjack():
        
        global dealer_label_1, dealer_image1
        
        #Logic for first Cards
        if len(dealer_score) == 2 and len(player_score) == 2:
                if status["dealer"] == "win" and status["player"] == "win":
                    card_button.conifg(state="disabled")
                    stand_button.config(state="disabled")
                    dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                    dealer_label_1.config(image=dealer_image1)
                    
                    newBalance = userMoney + Bet
                    conn = dbConnection()
                    conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                    )
                    
                    messagebox.showinfo("Push", "Tie")
                elif status["dealer"] == "win":
                    card_button.config(state="disabled")
                    stand_button.config(state="disabled")
                    dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                    dealer_label_1.config(image=dealer_image1)
                    
                    messagebox.showinfo("Dealer Wins", "Blackjack, Dealer Wins")
                elif status["player"] == "win":
                    card_button.config(state="disabled")
                    stand_button.config(state="disabled")
                    dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                    dealer_label_1.config(image=dealer_image1)
                    
                    newBalance = userMoney + (3 * Bet)
                    userMoney = newBalance
                    conn = dbConnection()
                    conn.queryExecute(
                    f"UPDATE USER SET BALANCE = {newBalance} WHERE USERID = '{username}'"
                    )
                    
                    messagebox.showinfo("Player Wins", "Blackjack, Player Wins")   
                    
        else:
            if status["player"] == "bust":
                messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: {dealer_total}")
                
        updateLabels()

    def Close():
        root_bj.destroy()
        root.deiconify()
        show_main_page()

        
        
        
    
    global userMoney, Bet
    
    userMoney = str(getUserInfo())
    userMoney = ''.join(e for e in userMoney if e.isalnum())
    
    Bet = 0
    
    bj_frame = Frame(root_bj, bg="green")
    bj_frame.pack(pady=20)    
    
    dealer_frame = LabelFrame(bj_frame, text="Dealer", bd=0)
    dealer_frame.pack(padx=20, ipadx=20)

    player_frame = LabelFrame(bj_frame, text="Player", bd=0)
    player_frame.pack(ipadx=20, pady=10)

    # Put Dealer cards in frames
    dealer_label_1 = Label(dealer_frame, text='')
    dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

    dealer_label_2 = Label(dealer_frame, text='')
    dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

    dealer_label_3 = Label(dealer_frame, text='')
    dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

    dealer_label_4 = Label(dealer_frame, text='')
    dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

    dealer_label_5 = Label(dealer_frame, text='')
    dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

    # Put Player cards in frames
    player_label_1 = Label(player_frame, text='')
    player_label_1.grid(row=1, column=0, pady=20, padx=20)

    player_label_2 = Label(player_frame, text='')
    player_label_2.grid(row=1, column=1, pady=20, padx=20)

    player_label_3 = Label(player_frame, text='')
    player_label_3.grid(row=1, column=2, pady=20, padx=20)

    player_label_4 = Label(player_frame, text='')
    player_label_4.grid(row=1, column=3, pady=20, padx=20)

    player_label_5 = Label(player_frame, text='')
    player_label_5.grid(row=1, column=4, pady=20, padx=20)

    # Create Button Frame
    button_frame = Frame(root_bj, bg="green")
    button_frame.pack(pady=20)

    # Create a couple buttons
    shuffle_button = Button(button_frame, text="Start", command=startGame)
    shuffle_button.grid(row=0, column=0)

    card_button = Button(button_frame, text="Hit Me", command=player_hit)
    card_button.grid(row=0, column=1, padx=10)

    stand_button = Button(button_frame, text="Stand", command=stand)
    stand_button.grid(row=0, column=2, padx=10)

    money_label = Label(root_bj, text=f"Money: ${userMoney}", font=("Helvetica", 18), bg="green", fg="white")
    money_label.pack(pady=20)

    bet_label = Label(root_bj, text=f"Current Bet: ${Bet}", font=("Helvetica", 18), bg="green", fg="white")
    bet_label.pack(pady=20)

    bet_entry = Entry(root_bj, font=("Helvetica", 18), width=10)
    bet_entry.pack(pady=20)
    
    close_button = Button(button_frame, text="Close", command=Close)
    close_button.grid(row=0, column=3, padx=20)
    
    root_bj.mainloop()
    

#FUNCTION TO PLAY ROULETTE GAME
#============================================================================
def play_roulette():
    db = sqlite3.connect("CasinoDB.db")
    cursor = db.cursor()
    conn = dbConnection()
    global total_money
    user = user_db[0]
    oldestbank = total_money = int(conn.query(f"SELECT BALANCE FROM USER WHERE USERID = '{user}'")[0])

    def spin_wheel():
        return random.randint(0, 36)

    def generate_color():
        return "Black" if random.randint(0, 1) == 0 else "Red"

    def is_valid_street(number):
        return 0 <= number <= 34

    def show_rules():
        rules = (
            "Roulette Rules:\n\n"
            "1. The game starts by placing a bet on a specific type of bet.\n"
            "2. The wheel is spun and a ball lands on a number (0-36).\n"
            "3. The color of the number can be either black or red.\n"
            "4. Based on the outcome, the winnings are calculated and added to or subtracted from the total money.\n"
        )
        messagebox.showinfo("Rules", rules)
        return_to_main_menu()

    def show_bet_types():
        bet_types = (
            "Types of Bets:\n\n"
            "1. Straight up: Bet on a single number (0-36).\n"
            "2. Split: Bet on two adjacent numbers.\n"
            "3. Street: Bet on three consecutive numbers in a row.\n"
            "4. Red/Black: Bet on the color of the number.\n"
            "5. Even/Odd: Bet on whether the number is even or odd.\n"
            "6. Column: Bet on one of the three columns.\n"
            "7. High/Low: Bet on whether the number is high (19-36) or low (1-18).\n"
        )
        messagebox.showinfo("Types of Bets", bet_types)
        return_to_main_menu()

    def show_roulette_board():
        board_window = Toplevel(root)
        board_window.title("Roulette Board")
        board_window.geometry("400x300")
        
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
            frame = tk.Frame(board_window)
            frame.pack()
            for num in row:
                label = tk.Label(frame, text=num, borderwidth=2, relief="solid", width=5, height=2, bg=colors[num], fg="white")
                label.pack(side="left")

        zero_label = tk.Label(board_window, text="0", borderwidth=2, relief="solid", width=5, height=2, bg=colors[0], fg="white")
        zero_label.pack(pady=10)
        
        tk.Button(board_window, text="Close", command=board_window.destroy).pack(pady=10)

    def start_game():
        ask_bet_amount()

    def ask_bet_amount():
        clear_game_frame()
        tk.Label(game_frame, text="Place your bet amount ($10 per round):").pack(pady=10)
        bet_amount_entry = ttk.Entry(game_frame)
        bet_amount_entry.pack(pady=10)
        tk.Button(game_frame, text="Next", command=lambda: ask_bet_type(bet_amount_entry)).pack(pady=10)
        tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
        game_frame.pack(padx=20, pady=20)

    def ask_bet_type(bet_amount_entry):
        global bet_amount
        if not validate_bet_amount(bet_amount_entry):
            return
        if bet_amount > total_money:
            messagebox.showerror("Invalid Bet", "You don't have enough money to place this bet.")
            return

        clear_game_frame()
        tk.Label(game_frame, text="Enter the type of bet (1-7):").pack(pady=10)
        bet_type_entry = ttk.Entry(game_frame)
        bet_type_entry.pack(pady=10)
        tk.Button(game_frame, text="Next", command=lambda: ask_bet_details(bet_type_entry)).pack(pady=10)
        tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
        game_frame.pack(padx=20, pady=20)

    def validate_bet_amount(bet_amount_entry):
        try:
            global bet_amount
            bet_amount = int(bet_amount_entry.get())
            if bet_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid bet amount.")
            return False
        return True

    def ask_bet_details(bet_type_entry):
        clear_game_frame()
        try:
            bet_type = int(bet_type_entry.get())
            if not (1 <= bet_type <= 7):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid bet type (1-7).")
            return

        entry_widgets = {
            1: [("Enter the number to bet on (0-36):", ttk.Entry(game_frame))],
            2: [("Enter the first adjacent number to bet on (0-36):", ttk.Entry(game_frame)), ("Enter the second adjacent number to bet on (0-36):", ttk.Entry(game_frame))],
            3: [("Enter the street number to bet on (0-34):", ttk.Entry(game_frame))],
            4: [("Enter '0' for black or '1' for red:", ttk.Entry(game_frame))],
            5: [("Enter '0' for even or '1' for odd:", ttk.Entry(game_frame))],
            6: [("Enter '1' for Column 1, '2' for Column 2, or '3' for Column 3:", ttk.Entry(game_frame))],
            7: [("Enter '1' for high or '2' for low:", ttk.Entry(game_frame))],
        }

        for label, entry in entry_widgets[bet_type]:
            tk.Label(game_frame, text=label).pack(pady=10)
            entry.pack(pady=10)

        tk.Button(game_frame, text="Place Bet", command=lambda: place_bet(entry_widgets[bet_type], bet_type)).pack(pady=10)
        tk.Button(game_frame, text="Return to Main Menu", command=return_to_main_menu).pack(pady=10)
        game_frame.pack(padx=20, pady=20)
#========#=====================================================================================
    def place_bet(entry_widgets, bet_type):
        global total_money

        try:
            bet_details = get_bet_details(bet_type, entry_widgets)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid bet details.")
            return

        # Deduct $10 for placing the bet
        if total_money < bet_details['amount'] + 10:
            messagebox.showerror("Insufficient Funds", "You do not have enough money to place this bet.")
            return

        total_money -= 10

        # Deduct the bet amount from the user's total money
        total_money -= bet_details['amount']

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
            messagebox.showinfo("Sorry", "You lose.")

        update_money_label()
        update_database(outcome, amount)

        if total_money <= 0:
            messagebox.showinfo("Game Over", "You have no more money. Game over!")
            game_frame.pack_forget()
            start_frame.pack(padx=20, pady=20)
        else:
            show_continue_options()  # Give the player an option to continue or quit


#======================================================================================
    def get_bet_details(bet_type, entry_widgets):
        bet_details = {'amount': bet_amount}
        entries = [entry.get() for label, entry in entry_widgets]

        if bet_type == 1:
            bet_details['number'] = int(entries[0])
            if not (0 <= bet_details['number'] <= 36):
                throw_value_error()
        elif bet_type == 2:
            bet_details['number1'] = int(entries[0])
            bet_details['number2'] = int(entries[1])
            if not (0 <= bet_details['number1'] <= 36) or not (0 <= bet_details['number2'] <= 36) or abs(bet_details['number1'] - bet_details['number2']) != 1:
                throw_value_error()
        elif bet_type == 3:
            bet_details['number'] = int(entries[0])
            if not is_valid_street(bet_details['number']):
                throw_value_error()
        elif bet_type == 4:
            bet_details['color'] = int(entries[0])
            if bet_details['color'] not in [0, 1]:
                throw_value_error()
        elif bet_type == 5:
            bet_details['even_odd'] = int(entries[0])
            if bet_details['even_odd'] not in [0, 1]:
                throw_value_error()
        elif bet_type == 6:
            bet_details['column'] = int(entries[0])
            if bet_details['column'] not in [1, 2, 3]:
                throw_value_error()
        elif bet_type == 7:
            bet_details['high_low'] = int(entries[0])
            if bet_details['high_low'] not in [1, 2]:
                throw_value_error()
        return bet_details

    def throw_value_error():
        raise ValueError

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

    def calculate_winnings(bet_type, amount):
        odds = {1: 35, 2: 17, 3: 11, 4: 1, 5: 1, 6: 2, 7: 1}
        return amount * odds[bet_type]

    def update_money_label():
        label_total_money.config(text=f"Your total money: ${total_money}")

    def clear_game_frame():
        for widget in game_frame.winfo_children():
            if widget != label_total_money:
                widget.pack_forget()

    def return_to_main_menu():
        clear_game_frame()
        start_frame.pack(padx=20, pady=20)

    def show_continue_options():
        clear_game_frame()
        tk.Label(game_frame, text="Would you like to continue playing or quit?", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(game_frame, text="Next", command=ask_bet_amount).pack(pady=10)
        tk.Button(game_frame, text="Quit", command=return_to_main_menu).pack(pady=10)
        game_frame.pack(padx=20, pady=20)

    def update_database(outcome, amount):
        conn.queryExecute(f"UPDATE USER SET BALANCE = {total_money} WHERE USERID = '{user}'")

        if outcome == "Win":
            wins = conn.query(f"SELECT WINS FROM GAMES WHERE GAMEID = 'Roulette'")[0]
            conn.queryExecute(f"UPDATE GAMES SET WINS = {int(wins) + 1} WHERE GAMEID = 'Roulette'")
        else:
            losses = conn.query(f"SELECT LOSSES FROM GAMES WHERE GAMEID = 'Roulette'")[0]
            conn.queryExecute(f"UPDATE GAMES SET LOSSES = {int(losses) + 1} WHERE GAMEID = 'Roulette'")

        timeplayed = conn.query(f"SELECT TIMESPLAYED FROM GAMES WHERE GAMEID = 'Roulette'")[0]
        conn.queryExecute(f"UPDATE GAMES SET TIMESPLAYED = {int(timeplayed) + 1} WHERE GAMEID = 'Roulette'")

        CasinoNet = conn.query(f"SELECT NETGAIN FROM GAMES WHERE GAMEID = 'Roulette'")[0]
        conn.queryExecute(f"UPDATE GAMES SET NETGAIN = {int(CasinoNet) + (total_money - oldestbank)} WHERE GAMEID = 'Roulette'")

        dt_string = datetime.now().strftime(f"%Y-%m-%d-%H:%M:%S")
        conn.queryExecute(f"INSERT INTO HISTORY VALUES ('{dt_string}', 'Roulette', '{user}', '{outcome}', {abs(total_money - oldestbank)})")
        netgain = conn.query(f"SELECT NETGAIN FROM USER WHERE USERID = '{user}'")[0]
        conn.queryExecute(f"UPDATE USER SET NETGAIN = {int(netgain) + (total_money - oldestbank)} WHERE USERID = '{user}'")

    # Initialize the main window
    root = tk.Tk()
    root.title("Roulette Game")

    start_frame = tk.Frame(root, bg='green', padx=20, pady=20)
    start_frame.pack(padx=20, pady=20)

    title_label = tk.Label(start_frame, text="Roulette", font=("Helvetica", 24), bg='green')
    title_label.grid(row=0, column=0, padx=10, pady=10)

    label_total_money = tk.Label(start_frame, text=f"Your total money: ${total_money}", font=("Helvetica", 16), bg='green')
    label_total_money.grid(row=1, column=0, padx=10, pady=10)

    button_rules = ttk.Button(start_frame, text="View Rules", command=show_rules)
    button_rules.grid(row=2, column=0, padx=10, pady=10)

    button_bet_types = ttk.Button(start_frame, text="View Types of Bets", command=show_bet_types)
    button_bet_types.grid(row=3, column=0, padx=10, pady=10)

    button_roulette_board = ttk.Button(start_frame, text="Roulette Board", command=show_roulette_board)
    button_roulette_board.grid(row=4, column=0, padx=10, pady=10)

    button_start = ttk.Button(start_frame, text="Start Game", command=start_game)
    button_start.grid(row=5, column=0, padx=10, pady=10)

    game_frame = tk.Frame(root, bg='darkred', padx=20, pady=20)

    bet_type_var = tk.IntVar()

    root.mainloop()

 

def play_poker():
    messagebox.showinfo("Poker", "Starting Poker game...")


def play_craps():
    db = sqlite3.connect("CasinoDB.db")
    cursor = db.cursor()
    conn = dbConnection()
    global bank
    global result
    global cont
    global oldestbank
    user = user_db[0]
    print(user)
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

        main_menu = ttk.Button(r, text='Go To Menu', width=25,command=lambda:[r.pack_forget(),show_main_page()] ).grid(row=7,column =2)

        dpassbutton = ttk.Button()

        def play_game(type):
            max_roll = int((conn.query("SELECT GAMESALLOWED FROM GAMES WHERE GAMEID = 'Craps'"))[0])
            #global roll_cnt
            roll_cnt = max_roll #temporary variable to count down reroll attempts
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
                dice1 = Label(f, text = dice, font = ('Arial',100), width = 4).grid(row = 1, column = pos)
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
                    win = Label(f, text = f'You Won ${userbet}!').grid(row = 2, column = 1)
                    bank += userbet
                elif roll in (losecon):
                    lose = Label(f, text = f'You Lost ${userbet}!').grid(row = 2, column = 1)
                    bank -= userbet
                else:
                    while rolltotal not in (roll, 7, 13):#13 is a special case to break the while loop
                        time.sleep(1)
                        rroll = Label(f, text = f'Rerolling for {roll}...').grid(row = 2, column = 1)

                        if (roll_cnt < 1):
                            rolltotal = 13
                            roll_stop = Label(f, text = f'You ran out of reroll attempts!').grid(row = 3, column = 2)
                            f.update_idletasks
                            time.sleep(1)
                        else:   
                            for i in range(max_roll):
                                roll_cnt = roll_cnt - 1
                                rrolls_left = Label(f, text = f'Reroll attempts left: {roll_cnt}').grid(row = 2, column = 2)
                                f.update_idletasks
                                time.sleep(1)
                                rolltotal = roll_dice()
                                print(f"({rolltotal})")
                                continue
                    if rolltotal not in (7,13):
                        win = Label(f, text = f'You Won ${userbet}!').grid(row = 3, column = 1)
                        bank += userbet
                    else:
                        lose = Label(f, text = f'You Lost ${userbet}!').grid(row = 3, column = 1)
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

                time.sleep(1.5)#shows the results to the user for a time
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

    user = user_db[0]
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

   
        def shake_machine():    
            p = tk.Frame(root,padx=20,pady=20, width= 700, height=300)
            root.minsize(700, 300)
            p.pack(fill="both", expand=True)
            space1=Label(p,text="",width=18).grid(row=0,column=0)
            space2=Label(p,text="",width=18).grid(row=1,column=1)
            space3=Label(p,text="",width=18).grid(row=2,column=2)
            space4=Label(p,text="",width=18).grid(row=3,column=3)
            space5=Label(p,text="",width=18).grid(row=4,column=4)
            space6=Label(p,text="").grid(row=5,column=0)
            space7=Label(p,text="").grid(row=6,column=0)
            space8=Label(p,text="").grid(row=7,column=0)
            space9=Label(p,text="").grid(row=8,column=0)
            
            
            lab=Label(p,text="SHAKING").grid(row=9,column=2)
            def shake():
                x = root.winfo_x()
                y = root.winfo_y()
                #SHAKE THE MACHINE
                for _ in range(10):

                    root.geometry(f"+{x + 5}+{y}")
                    root.update_idletasks()
                    root.after(50)

                    root.geometry(f"+{x + 10}+{y}")
                    root.update_idletasks()
                    root.after(50)
                    
                    root.geometry(f"+{x + 5}+{y}")
                    root.update_idletasks()
                    root.after(50)

                    root.geometry(f"+{x}+{y}")
                    root.update_idletasks()
                    root.after(50)
                    
                    root.geometry(f"+{x - 5}+{y}")
                    root.update_idletasks()
                    root.after(50)
                    
                    root.geometry(f"+{x - 10}+{y}")
                    root.update_idletasks()
                    root.after(50)
                    
                    root.geometry(f"+{x - 5}+{y}")
                    root.update_idletasks()
                    root.after(50)
                    
                    root.geometry(f"+{x}+{y}")
                    root.update_idletasks()
                    root.after(50)

                root.geometry(f"+{x}+{y}")  # Restore original position
            def check_caught():
                if caught_cheating==1:
                    conn.queryExecute(f"Update USER SET HASCHEATED = 1 WHERE USERID ='{user}'")
                    outcomelabel=Label(p,text="You got caught cheating").grid(row=9,column=2)
                    p.update_idletasks()
                    time.sleep(2)
                    p.pack_forget()
                    show_main_page()


                else:
                    conn.queryExecute(f"UPDATE USER SET BALANCE = {bank+shakeResult} WHERE USERID = '{user}'")
                    outcomelabel=Label(p,text=f"You got away with it and got ${shakeResult}").grid(row=9,column=2)
                    p.update_idletasks()
                    return_button = ttk.Button(p, text='Return', width=25,command=lambda:[p.pack_forget(),play_slots()] ).grid(row=10,column =2)


            shake()  # Start shaking after 1 millisecond
            time.sleep(1)
            droppings = random.randint(0, 9)
            shakeResult = [0,0,0,1,1,1,500,1000,2000,5000][droppings]
            cheating = random.randint(0, 9)# 1 means caught
            caught_cheating = [0,0,0,0,0,0,0,1,1,1][cheating]
            check_caught()
            root.mainloop()




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
                slot1 = random.randint(0, 6)
                slotRes1 = [Apple, Cherry, Grape, Orange, HorseShoe, Bar][slot1]
            
                slot2 = random.randint(0, 6)
                slotRes2 = [Apple, Cherry, Grape, Orange, HorseShoe, Bar][slot2]

                slot3 = random.randint(0, 6)
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
        hidden14 = Label(r, text='', width=5).grid(row=11, column=4)
        hidden15 = Label(r, text='', width=5).grid(row=12, column=4)
        hidden16 = Label(r, text='', width=5).grid(row=13, column=4)
        hidden17 = Label(r, text='', width=5).grid(row=14, column=5)
        hidden18 = Label(r, text='', width=5).grid(row=15, column=6)
        hidden19 = Label(r, text='', width=5).grid(row=16, column=4)                    
        hidden20 = Label(r, text='', width=5).grid(row=17, column=4)                    
        hidden21 = Label(r, text='', width=5).grid(row=18, column=4)                    


        #CREATING BUTTONS FOR THE USER TO INTERACT WITH ALONG WITH COMMANDS AND ATTRIBUTES
        button = ttk.Button(r, text='10$ Spins ',width=25,command=lambda:[r.pack_forget(),slotChoiceis1(),playgame()] ).grid(row=9,column = 1)
        button2 = ttk.Button(r, text='50$ Spins', width=25,command=lambda:[r.pack_forget(),slotChoiceis2(),playgame()] ).grid(row=9, column =2)
        button3 = ttk.Button(r, text='100$ Spins', width=25,command=lambda:[r.pack_forget(),slotChoiceis3(),playgame()] ).grid(row=9,column =3)
        manual = ttk.Button(r, text='Game Manual', width=25,command=lambda:[r.pack_forget(),openmanual()] ).grid(row=10,column =1)
        shakemachine = ttk.Button(r, text='Shake Machine', width=15,command=lambda:[r.pack_forget(),shake_machine()]).grid(row=19,column =5)
        main_menu = ttk.Button(r, text='Go To Menu', width=25,command=lambda:[r.pack_forget(),show_main_page()] ).grid(row=10,column =3)


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
        x.append(add)	 
        y.append(i[0])	
        add=add+1
    plt.plot(x,y, marker = 'x', linestyle = '-', color = 'b') 
    plt.title("Casino Profit/Loss Per Play")
    plt.title("HOUSE WINS/LOSSES")
    plt.show() 
            
def check_profit():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()

    cursor.execute("SELECT RESULT, AMOUNT FROM HISTORY")
    data = cursor.fetchall()

    x = []  
    y = []  
    
    for index, (result, amount) in enumerate(data):
        if result == "Win":
            y.append(amount)  #win
        elif result == "Loss":
            y.append(-amount)  # loss
        
        x.append(index + 1) 
    

    plt.plot(x, y, marker='x', linestyle='-', color='b')
    plt.axhline(0, color='red', linewidth=0.8) 
    plt.title("Casino Profit/Loss Per Play")
    plt.xlabel("Number of Plays")
    plt.ylabel("Profit/Loss")
    plt.show()

def check_players():
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()

    cursor.execute("SELECT USERID, NETGAIN FROM USER")
    data = cursor.fetchall()

    users = [row[0] for row in data]
    net_gains = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    positions = np.arange(len(users))

    plt.bar(positions, net_gains, color='blue', alpha=0.7)  

    plt.axhline(0, color='red', linewidth=0.8)  
    plt.title("Total Net Gain/Loss per User")
    plt.xlabel("Users")
    plt.ylabel("Net Gain/Loss")
    plt.xticks(positions, users)  
    plt.show()


def add_balance():
    
    db = sqlite3.connect("CasinoDB.db") 
    cursor = db.cursor()

    usern = balance_user_entry.get()
    balancen = balance_money_entry.get()

    cursor.execute("SELECT USERID FROM USER")
    data = cursor.fetchall()

    user_exists = False
    for row in data:
        if row[0] == usern:
            user_exists = True
            break

    if (user_exists == False):
        messagebox.showwarning("INVALID USER",f"User {usern} Does Not Exist")
    else:
        cursor.execute(f"SELECT BALANCE FROM USER WHERE USERID = '{usern}'")
        data = cursor.fetchone()
        balance = int(data[0])+int(balancen)
        cursor.execute(f"UPDATE USER SET BALANCE = {balance} WHERE USERID = '{usern}'")
        db.commit()

class Baccarat:
    def __init__(self):
        self.max_bet = 1000
        self.times_played = 0
        self.wins = 0
        self.losses = 0

    def play(self, user, bet):
        player_hand = self.draw_hand()
        banker_hand = self.draw_hand()

        player_score = self.calculate_score(player_hand)
        banker_score = self.calculate_score(banker_hand)

        if player_score < 8 and banker_score < 8:
            if player_score <= 5:
                player_hand.append(self.draw_card())

            banker_hand = self.apply_banker_rules(banker_hand, player_hand)

        if player_score > banker_score:
            result = "Player wins!"
            user.record_history("Baccarat", "Win", bet)
            self.wins += 1
            winnings = bet
        elif banker_score > player_score:
            result = "Banker wins!"
            user.record_history("Baccarat", "Loss", -bet)
            self.losses += 1
            winnings = -bet
        else:
            result = "It's a tie!"
            user.record_history("Baccarat", "Tie", 0)
            winnings = 0

        user.bankroll += winnings
        self.times_played += 1

        return player_hand, banker_hand, result

    def draw_hand(self):
        return [self.draw_card(), self.draw_card()]

    def draw_card(self):
        return random.randint(1, 13)

    def calculate_score(self, hand):
        score = sum(min(card, 10) for card in hand)
        return score % 10

    def apply_banker_rules(self, banker_hand, player_hand):
        banker_score = self.calculate_score(banker_hand)
        player_third_card = player_hand[2] if len(player_hand) > 2 else None

        if banker_score <= 2:
            banker_hand.append(self.draw_card())
        elif banker_score == 3:
            if player_third_card is None or player_third_card != 8:
                banker_hand.append(self.draw_card())
        elif banker_score == 4:
            if player_third_card is not None and player_third_card in [2, 3, 4, 5, 6, 7]:
                banker_hand.append(self.draw_card())
        elif banker_score == 5:
            if player_third_card is not None and player_third_card in [4, 5, 6, 7]:
                banker_hand.append(self.draw_card())
        elif banker_score == 6:
            if player_third_card is not None and player_third_card in [6, 7]:
                banker_hand.append(self.draw_card())

        return banker_hand

class User:
    def __init__(self, userid, bankroll, password):
        self.userid = userid
        self.bankroll = bankroll
        self.password = password
        self.netgain = 0
        self.hascheated = 0  # 0 = not a cheater, 1 = cheater

    def play_game(self, game, casino, bet, baccarat_window, bet_choice):
        choice = messagebox.askquestion("Cheating Attempt", "Do you want to cheat?")
        if choice == 'yes':
            self.hascheated = 1
            casino.update_user_cheating(self.userid, self.hascheated)

            if self.cheat_attempt():
                messagebox.showinfo("Cheating Attempt", "Cheater caught! Logging you out.")
                baccarat_window.destroy()  # Close the Baccarat game window
                show_login_page()  # Log out the user by showing the login page
                return [], [], "Cheater caught!"  # Return default values

        player_hand, banker_hand, result = game.play(self, bet)

        # If the user tried to cheat and was not caught, force a win
        if self.hascheated == 1:
            if bet_choice.get() == "Player":
                result = "Player wins!"
                player_hand, banker_hand = game.draw_hand(), game.draw_hand()
            elif bet_choice.get() == "Banker":
                result = "Banker wins!"
                player_hand, banker_hand = game.draw_hand(), game.draw_hand()
            elif bet_choice.get() == "Tie":
                result = "It's a tie!"
                player_hand = game.draw_hand()
                banker_hand = player_hand[:]  # Ensure both hands are identical for a tie

        messagebox.showinfo("Game Result", result)
        return player_hand, banker_hand, result

    def record_history(self, game_id, result, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        retries = 3
        for attempt in range(retries):
            try:
                with casino.connection:
                    casino.connection.execute('''
                        INSERT INTO HISTORY (TIMESTAMP, GAMEID, USERID, RESULT, AMOUNT) VALUES (?, ?, ?, ?, ?)
                    ''', (timestamp, game_id, self.userid, result, amount))
                break
            except sqlite3.OperationalError as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1}: Error recording history: {e}. Retrying...")
                    time.sleep(1)
                else:
                    print("Failed to record history after multiple attempts. Please try again later.")

    def cheat_attempt(self):
        return random.random() < 0.5  # 50% chance of being caught

class Casino:
    def __init__(self, name, db_path):
        self.name = name
        self.connection = sqlite3.connect(db_path, timeout=10)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS USER (
                    USERID TEXT PRIMARY KEY NOT NULL,
                    PASSWORD TEXT NOT NULL,
                    NETGAIN INTEGER NOT NULL,
                    BALANCE INTEGER NOT NULL,
                    HASCHEATED TEXT NOT NULL DEFAULT 'NO'
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS GAMES (
                    GAMEID TEXT PRIMARY KEY NOT NULL,
                    NETGAIN INTEGER NOT NULL,
                    GAMESALLOWED INTEGER NOT NULL,
                    MAXBET INTEGER NOT NULL,
                    TIMESPLAYED INTEGER NOT NULL,
                    WINS INT NOT NULL DEFAULT 0,
                    LOSSES INT NOT NULL DEFAULT 0
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS HISTORY (
                    TIMESTAMP DATE NOT NULL,
                    GAMEID TEXT NOT NULL,
                    USERID TEXT NOT NULL,
                    RESULT TEXT NOT NULL,
                    AMOUNT INTEGER NOT NULL,
                    PRIMARY KEY(TIMESTAMP)
                )
            ''')

    def add_user(self, user):
        retries = 3
        for attempt in range(retries):
            try:
                with self.connection:
                    self.connection.execute('''
                        INSERT INTO USER (USERID, PASSWORD, NETGAIN, BALANCE, HASCHEATED) VALUES (?, ?, ?, ?, ?)
                    ''', (user.userid, user.password, user.netgain, user.bankroll, user.hascheated))
                break
            except sqlite3.OperationalError as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1}: Error adding user: {e}. Retrying...")
                    time.sleep(1)
                else:
                    print("Failed to add user after multiple attempts. Please try again later.")

    def login_user(self, userid, password):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM USER WHERE USERID=? AND PASSWORD=?', (userid, password))
        user_record = cursor.fetchone()
        if user_record:
            print("Login successful!")
            return User(user_record[0], user_record[3], password)
        else:
            print("Login failed!")
            return None

    def update_user_cheating(self, userid, hascheated):
        retries = 3
        for attempt in range(retries):
            try:
                with self.connection:
                    self.connection.execute('''
                        UPDATE USER
                        SET HASCHEATED = ?
                        WHERE USERID = ?
                    ''', (hascheated, userid))
                break
            except sqlite3.OperationalError as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1}: Error updating user cheating stats: {e}. Retrying...")
                    time.sleep(1)
                else:
                    print("Failed to update user cheating stats after multiple attempts. Please try again later.")



def play_baccarat():
    if not user_db:
        messagebox.showerror("Error", "No user is currently logged in.")
        return

    baccarat_game = Baccarat()

    # Define the baccarat_window here
    baccarat_window = tk.Toplevel(root)
    baccarat_window.title("Baccarat Game")

    game_frame = tk.Frame(baccarat_window, padx=20, pady=20)
    game_frame.pack(padx=20, pady=20)

    # Use user_db for the logged-in user's information
    welcome_label = tk.Label(game_frame, text=f"Welcome, {user_db[0]}!", font=("Arial", 24))
    welcome_label.pack(pady=20)

    # Retrieve the user's bankroll from the database
    conn = dbConnection()
    user_bankroll = int(conn.query(f"SELECT BALANCE FROM USER WHERE USERID = '{user_db[0]}'")[0])

    bankroll_label = tk.Label(game_frame, text=f"Bankroll: ${user_bankroll}", font=("Arial", 16))
    bankroll_label.pack()

    bet_label = tk.Label(game_frame, text="Enter your bet:", font=("Arial", 16))
    bet_label.pack(pady=10)

    bet_entry = tk.Entry(game_frame, font=("Arial", 16))
    bet_entry.pack()

    # Define bet_choice variable here
    bet_choice = tk.StringVar(value="Player")

    # Betting options
    player_bet_button = tk.Radiobutton(game_frame, text="Bet on Player", variable=bet_choice, value="Player", font=("Arial", 16))
    player_bet_button.pack(pady=5)

    banker_bet_button = tk.Radiobutton(game_frame, text="Bet on Banker", variable=bet_choice, value="Banker", font=("Arial", 16))
    banker_bet_button.pack(pady=5)

    tie_bet_button = tk.Radiobutton(game_frame, text="Bet on Tie", variable=bet_choice, value="Tie", font=("Arial", 16))
    tie_bet_button.pack(pady=5)

    def play_baccarat_game():
        nonlocal user_bankroll
        bet = int(bet_entry.get())
        if bet > user_bankroll:
            messagebox.showerror("Error", "Bet exceeds current bankroll.")
            return

        user = User(user_db[0], user_bankroll, user_db[1])
        player_hand, banker_hand, result = user.play_game(baccarat_game, casino, bet, baccarat_window, bet_choice)

        if result == "Player wins!" and bet_choice.get() == "Player":
            winnings = 2 * bet
            messagebox.showinfo("Result", f"You bet on Player and won ${winnings}!")
        elif result == "Banker wins!" and bet_choice.get() == "Banker":
            winnings = 2 * bet
            messagebox.showinfo("Result", f"You bet on Banker and won ${winnings}!")
        elif result == "It's a tie!" and bet_choice.get() == "Tie":
            winnings = 2 * bet
            messagebox.showinfo("Result", f"You bet on a Tie and won ${winnings}!")
        else:
            if result == "It's a tie!":
                winnings = 0
                messagebox.showinfo("Result", "It's a tie and you didn't bet on a Tie, no change to your bankroll.")
            else:
                winnings = -bet
                messagebox.showinfo("Result", f"You lost your bet of ${bet}.")

        # Update the bankroll in the database
        user_bankroll += winnings
        conn.queryExecute(f"UPDATE USER SET BALANCE = {user_bankroll} WHERE USERID = '{user_db[0]}'")

        # Update the bankroll label
        bankroll_label.config(text=f"Bankroll: ${user_bankroll}")
        player_hand_label.config(text=f"Player Hand: {player_hand}")
        banker_hand_label.config(text=f"Banker Hand: {banker_hand}")

    play_button = tk.Button(game_frame, text="Play Baccarat", command=play_baccarat_game, font=("Arial", 16))
    play_button.pack(pady=20)

    hands_frame = tk.Frame(game_frame)
    hands_frame.pack(pady=10)

    player_hand_label = tk.Label(hands_frame, text="Player Hand: ", font=("Arial", 16))
    player_hand_label.pack()

    banker_hand_label = tk.Label(hands_frame, text="Banker Hand: ", font=("Arial", 16))
    banker_hand_label.pack()

    # Back button to return to the main menu
    back_button = tk.Button(game_frame, text="Back to Main Menu", command=lambda: baccarat_window.destroy(), font=("Arial", 16))
    back_button.pack(pady=20)


def play_poker():
    game = PokerGame()
  

# Initialize the Casino object at the start of your script
casino = Casino("My Casino", "CasinoDB.db")




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
admin_main_frame = tk.Frame(root, padx=20, pady=20)

welcome_label = tk.Label(main_frame, text="Welcome to the Main Page!", font=("Arial", 16))
welcome_label.pack(pady=20)

blackjack_button = ttk.Button(main_frame, text="Play Blackjack", command=play_blackjack)
blackjack_button.pack(pady=10)

slots_button = ttk.Button(main_frame, text="Play Slots", command=lambda:[main_frame.pack_forget(),login_frame.pack_forget(), admin_main_frame.pack_forget(),signup_frame.pack_forget(),play_slots()])
slots_button.pack(pady=10)

slots_button = ttk.Button(main_frame, text="Play Craps", command=lambda:[main_frame.pack_forget(),login_frame.pack_forget(), signup_frame.pack_forget(),play_craps()])
slots_button.pack(pady=10)

roulette_button = ttk.Button(main_frame, text="Play Roulette", command=play_roulette)
roulette_button.pack(pady=10)

baccarat_button = ttk.Button(main_frame, text="Play Baccarat", command=play_baccarat)
baccarat_button.pack(pady=10)             

poker_button = ttk.Button(main_frame, text="Play Poker", command=play_poker)
poker_button.pack(pady=10)

logout_button = ttk.Button(main_frame, text="Logout", command=show_login_page)
logout_button.pack(pady=10)

#Create Admins Page 
statistics_button = ttk.Button(admin_main_frame, text="Wins Vs Losses", command=check_stats)
statistics_button.pack(pady=10)


statistics_button = ttk.Button(admin_main_frame, text="Profit Per Play", command=check_profit)
statistics_button.pack(pady=10)


statistics_button = ttk.Button(admin_main_frame, text="Different Users Net Gains", command=check_players)
statistics_button.pack(pady=10)

add_bal_button = ttk.Button(admin_main_frame, text="Add Balance", command=show_add_balance_page)
add_bal_button.pack(pady=10)

admin_logout_button = ttk.Button(admin_main_frame, text="Logout", command=show_login_page)
admin_logout_button.pack(pady=10)


balance_frame = tk.Frame(root, padx=20, pady=10)

balance_user_entry_label = tk.Label(balance_frame, text="Enter User: ", font=("Arial", 12)).grid(pady=10)
balance_user_entry = tk.Entry(balance_frame, font=("Arial", 12))
balance_user_entry.grid(pady=10)

balance_money_entry_label =tk.Label(balance_frame, text="Enter The Balance You Want To Add: ", font=("Arial", 12)).grid(pady=10)
balance_money_entry = tk.Entry(balance_frame, font=("Arial", 12))
balance_money_entry.grid(pady=10)
add_balance_to_user = ttk.Button(balance_frame, text="Add Balance", command=add_balance).grid(pady=10)

return_to_admin_frame= ttk.Button(balance_frame, text="Return", command=show_admin_main_page).grid(pady=10)

# Start the Tkinter main loop
root.mainloop()