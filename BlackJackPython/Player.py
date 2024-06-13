import random
import Card
import Deck

class Player:
    def __init__(self, in_bank=100, start_card=None):
        self.bank = in_bank
        self.hand = []
        self.insured= False
        self.insuranceVal= 0
        if start_card is not None:
            self.hand.append(start_card)
        self.name = "User"

    def returnName(self):
        return self.name

    def addHand(self, deck):
        rand_card = random.randint(0, deck.deckSize() - 1)
        self.hand.append(deck.add(rand_card))

    def showHand(self):
        for card in self.hand:
            print(f"{card.showCardName()}{card.showCardSuit()}", end=" ")
        print()

    def showBank(self):
        return self.bank

    def withdraw(self, amount):
        self.bank -= amount

    def deposit(self, amount):
        self.bank += amount

    def showHandAt(self, num):
        return self.hand[num].showCardName()+self.hand[num].showCardSuit()

    def returnCard(self, num):
        return self.hand[num]

    def totalCardVal(self):
        return sum(card.showCardVal() for card in self.hand)

    def showHandVal(self):
        return self.totalCardVal()
    
    def returnCardName(self, num):
        return self.hand[num].showCardName()

    def removeCard(self, num):
        del self.hand[num]

    def cardCount(self):
        return len(self.hand)

    def replaceCardVal(self, num):
        self.hand[num].changeCardVal(1)

    def singleCardVal(self, num):
        return self.hand[num].showCardVal()

    def setBank(self, val):
        self.bank = val

    def clearHand(self):
        self.hand.clear()
    
    def hasInsurance(self,val):
        if val==True:
            self.insured=True
        else:
            False

    def updateInsuranceVal(self,insurance):
        self.insuranceVal= insurance
    
    def returnInsuranceVal(self):
        return self.insuranceVal

    def checkInsurance(self):
        return self.insured
