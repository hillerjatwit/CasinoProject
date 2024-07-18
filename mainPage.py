import tkinter as tk
from tkinter import messagebox, ttk

# Initialize the user database (in a real application, use a secure database)
user_db = {}

# Function to handle user login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    
    if username in user_db and user_db[username]['password'] == password:
        messagebox.showinfo("Login Success", f"Welcome, {user_db[username]['name']}!")
        show_main_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

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

def play_slots():
    messagebox.showinfo("Slots", "Starting Slots game...")

def play_roulette():
    messagebox.showinfo("Roulette", "Starting Roulette game...")

def play_other_games():
    messagebox.showinfo("Other Games", "Starting other casino games...")

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

slots_button = ttk.Button(main_frame, text="Play Slots", command=play_slots)
slots_button.pack(pady=10)

roulette_button = ttk.Button(main_frame, text="Play Roulette", command=play_roulette)
roulette_button.pack(pady=10)

other_games_button = ttk.Button(main_frame, text="Play Other Games", command=play_other_games)
other_games_button.pack(pady=10)

logout_button = ttk.Button(main_frame, text="Logout", command=show_login_page)
logout_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
