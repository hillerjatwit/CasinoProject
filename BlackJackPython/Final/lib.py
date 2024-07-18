import random
import tkinter
from typing import List, Union

class Card:
    def __init__(self, label: str, suit: str):
        self.label = label
        self.suit = suit
        self.value = self._get_value()


    def _get_value(self) -> Union[int, tuple]:
        if self.label in ("2", "3", "4", "5", "6", "7", "8", "9", "10"):
            return int(self.label)
        if self.label in ("J", "Q", "K"):
            return 10
        if self.label == "A":
            return 11
        raise ValueError("Bad Label")
    def _get_name(self):
        return f"{self.label}_of_{self.suit}"
    
    
class Deck:
    def __init__ (self):
        self.cards = []
        self._build()
        
    def _build(self):
        for suit in ["spades", "clubs", "diamonds", "hearts"]:
            for v in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"):
                self.cards.append(Card(v,suit))