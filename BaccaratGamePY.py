import random
import sqlite3
from datetime import datetime
import time

class Game:
    def __init__(self, game_id, max_bet):
        self.game_id = game_id
        self.max_bet = max_bet
        self.times_played = 0
        self.wins = 0
        self.losses = 0

    def play(self, user, bet):
        raise NotImplementedError

    def record_win(self):
        self.times_played += 1
        self.wins += 1

    def record_loss(self):
        self.times_played += 1
        self.losses += 1

class Baccarat(Game):
    def __init__(self):
        super().__init__("Baccarat", 1000)

    def play(self, user, bet):
        player_hand = self.draw_hand()
        banker_hand = self.draw_hand()

        player_score = self.calculate_score(player_hand)
        banker_score = self.calculate_score(banker_hand)

        print(f"Initial Player's hand: {player_hand} with score {player_score}")
        print(f"Initial Banker's hand: {banker_hand} with score {banker_score}")

        if player_score < 8 and banker_score < 8:
            if player_score <= 5:
                player_hand.append(self.draw_card())
                player_score = self.calculate_score(player_hand)
                print(f"Player draws a third card: {player_hand[-1]}")
                print(f"Updated Player's hand: {player_hand} with score {player_score}")

            banker_hand = self.apply_banker_rules(banker_hand, player_hand)
            banker_score = self.calculate_score(banker_hand)
            print(f"Updated Banker's hand: {banker_hand} with score {banker_score}")

        if player_score > banker_score:
            print("Player wins!")
            winnings = bet
            result = "Win"
            self.record_win()
        elif banker_score > player_score:
            print("Banker wins!")
            winnings = -bet
            result = "Loss"
            self.record_loss()
        else:
            print("It's a tie!")
            winnings = 0
            result = "Tie"

        user.record_history(self.game_id, result, winnings)
        return winnings

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
        choice = input("Do you want to cheat? (yes/no): ").strip().lower()
        if choice == 'yes':
            if self.cheat_attempt():
                print("Cheater caught!")
                self.bankroll -= 2 * bet  # Lose double the bet
                self.hascheated += 1  # Increment number of times cheated
                casino.update_user_cheating(self.userid, self.hascheated)  # Update database
                print(f"You lose {2 * bet} due to cheating attempt!")
                return 0
            else:
                print("Cheating successful! You win the bet.")
        
        winnings = game.play(self, bet)
        self.bankroll += winnings
        self.netgain += winnings
        casino.update_winnings(winnings)

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
                    HASCHEATED INTEGER NOT NULL DEFAULT 0  -- Changed to integer for count of cheating attempts
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

    def add_game(self, game):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM GAMES WHERE GAMEID=?', (game.game_id,))
        existing_game = cursor.fetchone()
        if existing_game is None:
            with self.connection:
                self.connection.execute('''
                    INSERT INTO GAMES (GAMEID, NETGAIN, GAMESALLOWED, MAXBET, TIMESPLAYED, WINS, LOSSES)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (game.game_id, 0, 100, game.max_bet, game.times_played, game.wins, game.losses))
        else:
            print(f"Game {game.game_id} already exists in the database.")

    def update_winnings(self, winnings):
        pass

    def update_game_stats(self, game_id, times_played, wins, losses):
        retries = 3
        for attempt in range(retries):
            try:
                with self.connection:
                    self.connection.execute('''
                        UPDATE GAMES
                        SET TIMESPLAYED = TIMESPLAYED + ?,
                            WINS = WINS + ?,
                            LOSSES = LOSSES + ?
                        WHERE GAMEID = ?
                    ''', (times_played, wins, losses, game_id))
                break
            except sqlite3.OperationalError as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt+1}: Error updating game stats: {e}. Retrying...")
                    time.sleep(1)
                else:
                    print("Failed to update game stats after multiple attempts. Please try again later.")

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

# Main game loop
if __name__ == "__main__":
    db_path = 'CasinoDB.db'
    casino = Casino("My Casino", db_path)
    baccarat = Baccarat()
    casino.add_game(baccarat)

    choice = input("Do you want to (1) Register or (2) Login? ")

    if choice == '1':
        userid = input("Enter your username: ")
        password = input("Enter your password: ")
        initial_bankroll = float(input("Enter your initial bankroll: "))
        user = User(userid, initial_bankroll, password)
        casino.add_user(user)
        print("Registration successful!")
    elif choice == '2':
        userid = input("Enter your username: ")
        password = input("Enter your password: ")
        user = casino.login_user(userid, password)
        if not user:
            exit()

    while user.bankroll > 0:
        bet = float(input(f"Enter your bet (available bankroll: {user.bankroll}): "))
        if bet > user.bankroll:
            print("You cannot bet more than your available bankroll.")
            continue
        
        user.play_game(baccarat, casino, bet)
        print(f"{user.userid} now has {user.bankroll} after playing Baccarat.")

        if user.bankroll <= 0:
            print("You have run out of funds!")
            break

        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break

    # Update the game statistics in the database
    casino.update_game_stats("Baccarat", baccarat.times_played, baccarat.wins, baccarat.losses)

    print(f"Game over! {user.userid} ends with a bankroll of {user.bankroll}.")
