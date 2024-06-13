import random

   
class Card:
    SPADE = '\u2660'
    CLUB = '\u2663'
    HEART = '\u2665'
    DIAMOND = '\u2666'
   
    def __init__(self, cardID=None, in_suit=None):
        if cardID is None or in_suit is None:
            cardID = random.randint(1, 13)
            in_suit = random.randint(1, 4)
        self.cardName = self.getCardName(cardID)
        self.cardVal = self.getCardVal(cardID)
        self.cardSuit = self.getCardSuit(in_suit)

    def getCardName (self,card):
        cardName={
            1:"A",
            2:"2",
            3:"3",
            4:"4",
            5:"5",
            6:"6",
            7:"7",
            8:"8",
            9:"9",
            10:"10",
            11:"J",
            12:"Q",
            13:"K"
        }
        return cardName[card]
    def getCardVal(self,card):
        if card == 1:
            return 11
        elif 2<=card<=10:
            return card
        else:
            return 10
        
    def getCardSuit(self, suit):
        suits = {
            1: self.SPADE,
            2: self.CLUB,
            3: self.HEART,
            4: self.DIAMOND
        }
        return suits[suit]
    
    def showCardName(self):

        self.cardName
        return self.cardName
    
    def showCardVal(self):
        self.cardVal
        return self.cardVal
        

    def showCardSuit(self):
        self.cardSuit
        return self.cardSuit

    def changeCardVal(self,updatedCardVal):
        self.cardVal=updatedCardVal