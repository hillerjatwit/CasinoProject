import Player
import Dealer
import Deck
from Deck import Deck
from Player import Player
from Dealer import Dealer

def eval( player, dealer, bet ):
    if player.totalCardVal()>21:
        print(f'You Went Over 21! Bust')
        bet=0
        return bet
    elif dealer.totalCardVal()>21:
        print(f'The Dealer Went Over 21! You Win')
        bet = bet*2
        return bet        
    elif (dealer.totalCardVal()>player.totalCardVal()) and dealer.totalCardVal()<22:
        print(f'The Dealer has {dealer.showHandVal()} which is more than your {player.showHandVal()}')
        bet = 0
        return bet
    elif dealer.totalCardVal()==player.totalCardVal():
        print(f'The Dealer has {dealer.showHandVal()} which is the same as your {player.showHandVal()}, Draw!')
        bet=bet
        return bet
    elif (dealer.totalCardVal() < player.totalCardVal()) and player.totalCardVal()<22: 
        print(f'The Dealer has {dealer.totalCardVal()} which is less than your {player.totalCardVal()}, You win')
        bet = bet*2
        return bet
def bust(player):
    for i in range(player.cardCount()):
        if player.returnCardName(i) == "A" and player.singleCardVal(i) == 11:
            player.replaceCardVal(i)
            print("Your total went over 21 while you had an ace acting as an eleven, it now has a value of 1")
            return 0
        else:
            return 1

def play(player, dealer, deck, bet):
    c = 2
    hitorstay = 1

    while hitorstay == 1:
        if player.totalCardVal() > 21:
            if bust(player) == 1:
                bet = eval(player, dealer, bet)
                hitorstay = 0
        else:
            print("You currently have: ")
            player.showHand()
            hitorstay = int(input("Would you like to hit(1) or stay(0): "))
            if hitorstay == 1:
                print("Dealing...")
                player.addHand(deck)
                
                print(f"You received a {player.showHandAt(c)}")
                c += 1
                if bust(player) == 1 and player.totalCardVal() > 21:
                    bet = eval(player, dealer, bet)
                    hitorstay = 0
            else:
                hitorstay = 0
                print("The dealer's hand was: ")
                dealer.showHand()
                print()
                while dealer.totalCardVal() < 17:
                    print("Dealing...")
                    dealer.addHand(deck)
                    print("The dealer's hand is now: ")
                    dealer.showHand()
                    print()
                bet = eval(player, dealer, bet)
    player.withdraw(-bet)

def insurance(player):
    insurance_val = 0
    has_insurance = int(input("Would you like insurance (1-yes)? "))
    
    if has_insurance == 1:
        valid_insur = 0
        while valid_insur == 0:
            insurance_val = float(input("How much would you like to put down? "))
            if insurance_val == 0:
                has_insurance = 0
                break
            if insurance_val > player.showBank():
                print(f"Sorry, you don't have that much money. Enter a valid number under ${player.showBank()} or enter 0 for none.")
                valid_insur = 0
            else:
                player.withdraw(insurance_val)
                valid_insur = True
                player.hasInsurance(True)


    return has_insurance, insurance_val

def main():
    
    deck = Deck()
    player = Player()
    dealer = Dealer()
    player.setBank(1000)
    while player.showBank()>0:
        player.clearHand()
        dealer.clearHand()
        deck.reset()
        validBet= False
        while validBet==False:
            print(f'You Have ${player.showBank()}')
            bet = int(input("How Much Would You Like to bet ") )
            if bet > player.showBank():
                print(f'You Dont Have That Much Money, Keep it Under {player.showBank()}')
            elif bet<1:
                print(f'Please Make sure the bet is over 0 dollars')
            else:
                validBet=True
                player.withdraw(bet)
        
        player.addHand(deck)
        dealer.addHand(deck)
        player.addHand(deck)
        dealer.addHand(deck)
        print("Player's hand:")
        player.showHand()

        print("Dealer's hand:")
        dealer.hideHand()

    # insurance if dealer deals a ace as a second card, offer insurance
        if dealer.singleCardVal(1) == 11:
            insurance(player)
    #if both blackjack
        if( dealer.showHandVal()==21 and dealer.cardCount()==2) and (player.showHandVal()==21 and player.cardCount()==2):
            print(f'You both have a blackjack')
            if player.checkInsurance()==True:
                print(f'You Had Insurance and Both Got BlackJack! You Get 2 x Insurance and Your Bet Value!')
                bet = player.insuranceVal()*2 + bet
            elif player.checkInsurance()==False:
                print(f'You Both Got BlackJack! Push!')
                bet = bet 
            player.withdraw(0-bet)

    #If dealer gets 21 
        elif dealer.showHandVal()==21 and dealer.cardCount()==2:
            print(f'Dealer Has BlackJack')
            #if the player has no insurance they lose
            if player.checkInsurance() == False:
                print('Sorry, You Lose')
                bet = 0
            #if the player has insurance then they get 2x their insurance bet back  
            elif player.checkInsurance() == True:
                print(f'Good Call! You Hvae Insurance, You get {player.returnInsuranceVal()*2} BacK! ')
                bet = player.returnInsuranceVal()*2
            #has insurance but doesnt hit
            else:
                print(f'Dealer did not have blackjack')
        
        
        #Player gets a blackjack
        elif player.showHandVal()==21 and player.cardCount()==2:
            print(f'Congrats! You got a BlackJack!')
            bet = bet*2.5
            player.withdraw(0-bet)

        else:

            doubledown = 0
            doubledown = int(input("Would you Like to double down?(1-Yes, 0-No)") )
            if doubledown==1:
                if player.showBank() < bet:
                    print(f'Sorry, You Dont Have Enough To Double Down')
                    play(player, dealer, deck, bet)
                else:
                    player.withdraw(bet)
                    bet=bet*2
                    player.addHand(deck)
                    player.showHand()
                    if player.totalCardVal()>21:
                        if bust(player)==1:
                            bet = eval(player,dealer,bet)
                    else:
                        print (f'The Dealers Hand Was')
                        dealer.showHand()
                        while dealer.totalCardVal()<17:
                            dealer.addHand(deck)
                            print(f'Dealer draws a card')
                            dealer.showHand()
                        bet =eval(player,dealer,bet)
                    player.withdraw(0-bet)

            else:
                play(player, dealer, deck, bet)


    print(f'')
print(f'')
print(f'')













if __name__ == "__main__":
    main()
