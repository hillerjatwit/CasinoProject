import random
from Card import Card 

class Deck:
    def __init__(self):
        self.cards = [Card(cardID, suit) for cardID in range(1, 14) for suit in range(1, 5)]
        random.shuffle(self.cards)

    def deckSize(self):
        return len(self.cards)

    def add(self, card_index):
        return self.cards.pop(card_index)
    
    def reset(self):
        self.cards = [Card(cardID, suit) for cardID in range(1, 14) for suit in range(1, 5)]
