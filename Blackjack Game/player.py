
class Player():
    def __init__(self, balance):
        self.balance = balance

    def get_str_hand(self):
        return str(self.hand)

    def hit(self, card):
        self.hand.add_to_hand(card)

