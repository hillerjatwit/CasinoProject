from tkinter import *
import random
from PIL import Image, ImageTk
import lib
from tkinter import messagebox


root = Tk()
root.title('Codemy.com - Card Deck')
#root.iconbitmap('c:/gui/codemy.ico')
root.geometry("1200x800")
root.configure(background="green")

def stand():
    global isShowing, dealer_image1
    
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
    split_button.config(state="disabled")
    
    if status["player"] != "bust":
        if status["dealer"] == "stand":
            if dealer_total > player_total:
                messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: {dealer_total}")
            elif dealer_total < player_total:
                messagebox.showinfo("Player Wins", f"Player: {player_total}  Dealer: {dealer_total}")
            else:
                messagebox.showinfo("Push", f"Player: {player_total}  Dealer: {dealer_total}")
        elif status["dealer"] == "hit":
            dealer_hit()
            stand()
        elif status["dealer"] == "win":
            messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: 21")
        elif status["dealer"] == "bust":
            messagebox.showinfo("Player Wins", f"Player: {player_total}  Dealer: {dealer_total}")
    else:
        messagebox.showinfo("Dealer Wins", f"Player: {player_total}  Dealer: {dealer_total}")
                        
def resize_cards(card):
	# Open the image
	our_card_img = Image.open(card)

	# Resize The Image
	our_card_resize_image = our_card_img.resize((150, 218))
	
	# output the card
	global our_card_image
	our_card_image = ImageTk.PhotoImage(our_card_resize_image)

	# Return that card
	return our_card_image

def generate_deck():
     D = lib.Deck()
     return D.cards
    
def shuffle():
    global status, player_wins, dealer_wins, isShowing
    player_wins = 0
    dealer_wins = 0
    isShowing = False
    
    status = {"dealer":"no", "player":"no"}
    
    card_button.config(state="normal")
    stand_button.config(state="normal")
    split_button.config(state="disabled")
    
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
    
    global Deck
    Deck = generate_deck()
    
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
    
    root.title(f'Blackjack')
    
def dealer_hit():
    global dealer_spot, dealer_total, player_total, player_score
    
    if dealer_spot <= 5:
        try:
            
            dealer_card = random.choice(Deck)
            Deck.remove(dealer_card)
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
            root.title("Exception")
            
        validateGame("dealer")
        
def player_hit():
    
    #Take card from Deck and Show on GUI, check blackjack else where
    
    global player_spot, player_total, dealer_total, player_score
    if player_spot <= 5:
        try:
            player_card = lib.Card
            player_card = random.choice(Deck)
            Deck.remove(player_card)
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
            root.title("Exception")
            
        validateGame("player")
        
def split():
    return 1

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
                split_button.config(state="disabled")
                dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                dealer_label_1.config(image=dealer_image1)
                
                messagebox.showinfo("Push", "Tie")
            elif status["dealer"] == "win":
                card_button.config(state="disabled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")
                dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                dealer_label_1.config(image=dealer_image1)
                
                messagebox.showinfo("Dealer Wins", "Blackjack, Dealer Wins")
            elif status["player"] == "win":
                card_button.config(state="disabled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")
                dealer_image1 = resize_cards(f'images/cards/{dealer[0]._get_name()}.png')
                dealer_label_1.config(image=dealer_image1)
                
                messagebox.showinfo("Player Wins", "Blackjack, Player Wins")
                
    elif len(dealer_score) < 2 or len(player_score) < 2:
        i = 0
    else:   
            if status["dealer"] == "yes" and status["player"] == "yes":
                messagebox.showinfo("Push", "Tie")
                card_button.conifg(state="disabled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")
            elif status["dealer"] == "yes":
                messagebox.showinfo("Dealer Wins", "21, Dealer Wins")
                card_button.config(state="disbaled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")
                
            elif status["player"] == "yes":
                messagebox.showinfo("Playewr Wins", "21, Player Wins")
                card_button.config(state="disbaled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")
            if status["player"] == "bust":
                messagebox.showinfo("Player Busts", f"Player Loses Player: {player_total}")
                card_button.config(state="disbaled")
                stand_button.config(state="disabled")
                split_button.config(state="disabled")     
    
    


my_frame = Frame(root, bg="green")
my_frame.pack(pady=20)

# Create Frames For Cards
dealer_frame = LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.pack(padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text="Player", bd=0)
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
button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

# Create a couple buttons
shuffle_button = Button(button_frame, text="Shuffle Deck", command=shuffle)
shuffle_button.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit Me", command=player_hit)
card_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand", command=stand)
stand_button.grid(row=0, column=2, padx=10)

split_button = Button(button_frame, text="Split", command=split)
split_button.grid(row=0, column=3)


shuffle()

root.mainloop()