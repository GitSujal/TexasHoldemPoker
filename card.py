
class Card(object):

    suit_dict = {
        "C": "\u2663",
        "D": "\u2666",
        "H": "\u2665",
        "S": "\u2660"
        }

    rank_dict = {
        "A": 14,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13
    }

    def __init__(self, suit, rank):
        self.rank_string = rank
        self.suit = self.suit_dict[suit.upper()]
        self.rank = self.rank_dict[rank.upper()]
        self.suit_string = suit.upper()

    def __str__(self):
        return str(self.rank_string)  + self.suit_string
    
    def __repr__(self):
        return str(self.rank_string) + self.suit_string

    def isConsecutive(self, otherCard) -> bool:
        if abs(self.rank - otherCard.rank) == 1:
            return True
        elif self.rank == 14 and otherCard.rank == 2:
            return True
        else:
            return False

    def isSameSuit(self, otherCard) -> bool:
        if self.suit == otherCard.suit:
            return True
        else:
            return False
    
    def __eq__(self, __o: object) -> bool:
        if self.rank == __o.rank and self.suit == __o.suit:
            return True
        else:
            return False

    def __lt__(self, __o: object) -> bool:
        if self.rank < __o.rank:
            return True
        elif self.rank == __o.rank and self.suit < __o.suit:
            return True
        else:
            return False
    
    def __gt__(self, __o: object) -> bool:
        if self.rank > __o.rank:
            return True
        elif self.rank == __o.rank and self.suit > __o.suit:
            return True
        else:
            return False
    
    def __ne__(self, __o: object) -> bool:
        if self.rank != __o.rank or self.suit != __o.suit:
            return True
        else:
            return False
