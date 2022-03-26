from itertools import combinations
class TexasPokerHand():

    hand_types_dict = {
        "High Card": 1,
        "Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }

    def __init__(self, *cards):
        self.cards = self._sort_cards(cards)
        self.hand_type = self._get_hand_type()
        self.hand_ranking = self.hand_types_dict[self.hand_type]*100 + sum([card.rank for card in self.cards])

    def _sort_cards(self, cards):
        return sorted(cards, key=lambda card: card.rank)

    def is_royal_flush(self):
        if self.is_straight_flush() and self.cards[0].rank == 10:
            return True
        else:
            return False
    
    def is_straight_flush(self):
        if self.is_flush() and self.is_straight():
            return True
        else:
            return False
    
    def is_four_of_a_kind(self):
        all_combs = combinations(self.cards, 4)
        is_four = False
        for comb in all_combs:
            if comb[0].rank == comb[1].rank == comb[2].rank == comb[3].rank:
                is_four = True
        return is_four
    
    def is_full_house(self):
        if self.is_three_of_a_kind() and self.is_pair():
            return True
        else:
            return False
    
    def is_flush(self):
        if self.cards[0].suit == self.cards[1].suit == self.cards[2].suit == self.cards[3].suit == self.cards[4].suit:
            return True
        else:
            return False
    
    def is_straight(self):
        if self.cards[0].isConsecutive(self.cards[1]) and self.cards[1].isConsecutive(self.cards[2]) and self.cards[2].isConsecutive(self.cards[3]) and self.cards[3].isConsecutive(self.cards[4]):
            return True
        elif self.cards[0].rank == 2 and self.cards[1].rank == 3 and self.cards[2].rank == 4 and self.cards[3].rank == 5 and self.cards[4].rank == 14:
            return True
        else:
            return False
    
    def is_three_of_a_kind(self):
        all_combs = combinations(self.cards, 3)
        is_toke = False
        for comb in all_combs:
            if comb[0].rank == comb[1].rank == comb[2].rank:
                is_toke = True
        return is_toke

    def is_two_pair(self):
        all_combs = combinations(self.cards, 2)
        tp_count = 0
        for comb in all_combs:
            if comb[0].rank == comb[1].rank:
                tp_count +=1
        return tp_count==2

    
    def is_pair(self):
        all_combs = combinations(self.cards, 2)
        tp_count = 0
        for comb in all_combs:
            if comb[0].rank == comb[1].rank:
                tp_count +=1
        return tp_count==1
    

    def _get_hand_type(self):
        if self.is_royal_flush():
            return "Royal Flush"
        elif self.is_straight_flush():
            return "Straight Flush"
        elif self.is_four_of_a_kind():
            return "Four of a Kind"
        elif self.is_full_house():
            return "Full House"
        elif self.is_flush():
            return "Flush"
        elif self.is_straight():
            return "Straight"
        elif self.is_three_of_a_kind():
            return "Three of a Kind"
        elif self.is_two_pair():
            return "Two Pair"
        elif self.is_pair():
            return "Pair"
        else:
            return "High Card"

    def get_hand_type(self):
        return self.hand_types_dict[self._get_hand_type()]

    def __eq__(self, __o: object) -> bool:
        if self.hand_type == __o.hand_type and self.cards[4] == __o.cards[4]:
            return True
        else:
            return False
    
    def __lt__(self, __o: object) -> bool:
        if self.hand_type < __o.hand_type:
            return True
        elif self.hand_type == __o.hand_type and self.cards[4] < __o.cards[4]:
            return True
        else:
            return False
    
    def __gt__(self, __o: object) -> bool:
        if self.hand_type > __o.hand_type:
            return True
        elif self.hand_type == __o.hand_type and self.cards[4] > __o.cards[4]:
            return True
        else:
            return False
    
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    
    def __str__(self) -> str:
        return_string = "{0:50}|{1:20}|{2:10}".format(str(self.cards),self.hand_type, self.hand_ranking)
        return return_string
    
    def __repr__(self) -> str:
        return self.__str__()