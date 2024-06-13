import Player 
import random
import Card
import Deck
class Dealer(Player.Player):
    def __init__(self, in_bank=100, start_card=None):
        super().__init__(in_bank, start_card)

    
    def hideHand(self):
       if self.hand:
        print(f"Hidden", end=" ")
        for card in self.hand[1:]:
            print(f"{card.showCardName()}{card.showCardSuit()}", end=" ")
        print()