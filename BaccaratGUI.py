import tkinter as tk
from tkinter import messagebox
import random
import sqlite3
from datetime import datetime
import time

# Define the Baccarat and User classes
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
        self.hascheated = 0  # Number of times cheated

    def play_game(self, game, casino, bet):
        choice = messagebox.askquestion("Cheating Attempt", "Do you want to cheat?")
        if choice == 'yes':
            if self.cheat_attempt():
                messagebox.showinfo("Cheating Attempt", "Cheater caught!")
                self.bankroll -= 2 * bet  # Lose double the bet
                self.hascheated += 1  # Increment number of times cheated
                casino.update_user_cheating(self.userid, self.hascheated)  # Update database
                return

        player_hand, banker_hand, result = game.play(self, bet)
        messagebox.showinfo("Game Result", result)

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
                    print(f"Attempt {attempt+1}: Error recording history: {e}. Retrying...")
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
                    HASCHEATED INTEGER NOT NULL DEFAULT 0
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
                    print(f"Attempt {attempt+1}: Error adding user: {e}. Retrying...")
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
                    print(f"Attempt {attempt+1}: Error updating user cheating stats: {e}. Retrying...")
                    time.sleep(1)
                else:
                    print("Failed to update user cheating stats after multiple attempts. Please try again later.")

# Casino GUI class
class CasinoGUI:
    def __init__(self, root, casino):
        self.root = root
        self.casino = casino
        self.baccarat = Baccarat()
        self.user = None  # Initialize user as None

        self.create_login_screen()

    def create_login_screen(self):
        # Create login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        # Login label and entries
        self.login_label = tk.Label(self.login_frame, text="Login to My Casino", font=("Arial", 24))
        self.login_label.pack(pady=20)

        self.userid_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 16))
        self.userid_label.pack()

        self.userid_entry = tk.Entry(self.login_frame, font=("Arial", 16))
        self.userid_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 16))
        self.password_label.pack()

        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 16))
        self.password_entry.pack()

        # Login and Register buttons
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login_user, font=("Arial", 16))
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register_user, font=("Arial", 16))
        self.register_button.pack()

    def login_user(self):
        userid = self.userid_entry.get()
        password = self.password_entry.get()

        self.user = self.casino.login_user(userid, password)
        if self.user:
            messagebox.showinfo("Login", "Login successful!")
            self.create_game_screen()
        else:
            messagebox.showerror("Login", "Login failed. Please check your username and password.")

    def register_user(self):
        userid = self.userid_entry.get()
        password = self.password_entry.get()

        if not userid or not password:
            messagebox.showerror("Register", "Please enter both username and password.")
            return

        # Check if user already exists
        cursor = self.casino.connection.cursor()
        cursor.execute('SELECT * FROM USER WHERE USERID=?', (userid,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Register", "User already exists. Please try a different username.")
        else:
            # Register new user
            new_user = User(userid, 1000, password)  # Initial bankroll set to 1000
            self.casino.add_user(new_user)
            messagebox.showinfo("Register", "Registration successful! You can now login.")
            self.userid_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def create_game_screen(self):
        # Destroy login or register frame and create game frame
        if hasattr(self, 'login_frame'):
            self.login_frame.destroy()
        elif hasattr(self, 'register_frame'):
            self.register_frame.destroy()

        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Welcome label
        self.welcome_label = tk.Label(self.main_frame, text=f"Welcome back, {self.user.userid}!", font=("Arial", 24))
        self.welcome_label.pack(pady=20)

        # Bankroll display
        self.bankroll_label = tk.Label(self.main_frame, text=f"Bankroll: {self.user.bankroll}", font=("Arial", 16))
        self.bankroll_label.pack()

        # Bet entry
        self.bet_label = tk.Label(self.main_frame, text="Enter your bet:", font=("Arial", 16))
        self.bet_label.pack(pady=10)

        self.bet_entry = tk.Entry(self.main_frame, font=("Arial", 16))
        self.bet_entry.pack()

        # Play button
        self.play_button = tk.Button(self.main_frame, text="Play Baccarat", command=self.play_baccarat, font=("Arial", 16))
        self.play_button.pack(pady=20)

        # Quit button
        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.root.quit, font=("Arial", 16))
        self.quit_button.pack(pady=20)

    def play_baccarat(self):
        try:
            bet = float(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")
            return

        if bet > self.baccarat.max_bet:
            messagebox.showerror("Invalid Bet", f"Maximum bet amount exceeded. Max bet: {self.baccarat.max_bet}.")
            return

        if bet > self.user.bankroll:
            messagebox.showerror("Invalid Bet", "You cannot bet more than your available bankroll.")
            return

        self.user.play_game(self.baccarat, self.casino, bet)

        # Update bankroll display
        self.bankroll_label.config(text=f"Bankroll: {self.user.bankroll}")

        if self.user.bankroll <= 0:
            messagebox.showinfo("Game Over", "You have run out of funds!")
            self.root.quit()

# Initialize casino and database
db_path = 'CasinoDB.db'
casino = Casino("My Casino", db_path)

# Create main application window
root = tk.Tk()
root.title("Casino Game")

# Create GUI instance
casino_gui = CasinoGUI(root, casino)

# Start GUI main loop
root.mainloop()
