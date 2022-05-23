from deck import Deck
from card import Card


class Hand:
    def __init__(self, cards):
        self.cards_in_hand = cards

    def get_value(self):
        value = 0
        aces = 0

        for card in self.cards_in_hand:
            val = card.value
            if val == 1:
                aces += 1
            else:
                value += min(val, 10)

        if aces == 0:
            return value

        if value + 11 > 21:
            return value + aces
        elif aces == 1:
            return value + 11
        elif value + 11 + (aces - 1) <= 21:
            return value + 11 + (aces - 1)
        else:
            return value + aces

    def add_to_hand(self, card):
        self.cards_in_hand.append(card)

    def __str__(self):
        string_cards = [str(card) for card in self.cards_in_hand]
        return ", ".join(string_cards)