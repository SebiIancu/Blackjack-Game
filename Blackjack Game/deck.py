import random
from card import Card


class Deck:
    def __init__(self):
        self.deck = []
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        for suit in range(4):
            for value in range(1, 14):
                self.deck.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, num_cards): # this method will crash if the deck has fewer cards in it than the number of cards we
        # need to deal, but it should never happen in a blackjack game.
        dealt_cards = []

        for _ in range(num_cards):
            dealt_card = self.deck.pop()
            dealt_cards.append(dealt_card)

        return dealt_cards
