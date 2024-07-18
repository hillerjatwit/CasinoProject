import tkinter as tk
from BaccaratGUI import BaccaratGUI, Casino, User

if __name__ == "__main__":
    root = tk.Tk()
    casino = Casino()
    user = User(bankroll=1000)  # Example bankroll
    app = BaccaratGUI(root, casino, user)
    root.mainloop()

