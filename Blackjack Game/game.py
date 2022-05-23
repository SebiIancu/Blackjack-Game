from deck import Deck
from hand import Hand


class Game:
    MINIMUM_BET = 1
    player_hand_value = 0
    dealer_hand_value = 0

    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.bet = None
        self.deck = Deck()

    def place_bet(self):
        while True:
            bet = float(input("Place your bet: "))
            if bet > self.player.balance:
                print("Insufficient funds")
            elif bet < self.MINIMUM_BET:
                print(f"Minimum bet is :{self.MINIMUM_BET}.")
            else:
                self.bet = bet
                self.player.balance -= bet
                break

    def player_hit_or_stay(self):

        while True:
            h_or_s = input("Hit or stay?").lower()

            if h_or_s in ["hit", "stay"]:
                break
            print("That is not a valid option")

        return h_or_s == "hit"

    def player_turn(self):
        while True:
            hit = self.player_hit_or_stay()
            if not hit:
                break

            card = self.deck.deal(1)[0]
            self.player.hit(card)
            print("You got:", card)
            print("You have:", self.player.get_str_hand())

            if self.player.hand.get_value() > 21:
                return True  # player Busts

        return False

    def dealer_turn(self):
        self.dealer.hand.cards_in_hand[1].hidden = False
        print("Dealer has", self.dealer.get_str_hand())

        while self.dealer.hand.get_value() < 16:
            card = self.deck.deal(1)[0]
            self.dealer.hit(card)
            print("Dealer hits:", card)
            print("Dealer has:", self.dealer.get_str_hand())

        if self.dealer.hand.get_value() > 21:
            return True

        return False

    def player_vs_dealer(self):
        if Game.player_hand_value > Game.dealer_hand_value:
            self.player.balance += 2 * self.bet
            print(f"Congratulations! You won {2 * self.bet}")
        else:
            print("Dealer Won!")

    def deal_start_hands(self):
        self.player.hand = Hand(self.deck.deal(2))
        self.dealer.hand = Hand(self.deck.deal(2))
        self.dealer.hand.cards_in_hand[1].hidden = True
        print("You have:", self.player.get_str_hand())
        print("Dealer has:", self.dealer.get_str_hand())

    def handle_blackjack(self):
        if self.player.hand.get_value() != 21:
            return False

        if self.dealer.hand.get_value() == 21:
            self.player.balance += self.bet
            print(
                "Both you and the dealer have Blackjack, you tie. Your bet has been returned.")
            return True

        self.player.balance += self.bet * 2.5
        print(f"Blackjack! You win {self.bet * 1.5} :)")
        return True

    def whos_the_winner(self):
        player_total = self.player.hand.get_value()
        dealer_total = self.dealer.hand.get_value()

        if dealer_total < player_total:
            self.player.balance += self.bet * 2
            print(f"You win ${self.bet}!")
        elif dealer_total > player_total:
            print(f"You lose ${self.bet}")
        else:
            self.player.balance += self.bet
            print("Its a tie. All bets returned.")

    def reset_round(self):
        self.deck = Deck()
        self.player.hand = None
        self.dealer.hand = None
        self.bet = None

    def start_round(self):
        self.place_bet()
        self.deal_start_hands()

        if self.handle_blackjack():
            self.reset_round()
            return  # round over.

        player_lost = self.player_turn()
        if player_lost:
            print(f"You bust, you lose ${self.bet}")
            return  # round over.

        dealer_lost = self.dealer_turn()
        if dealer_lost:
            self.player.balance += self.bet * 2
            print(f"Dealer busts, you win ${self.bet}")
            return  # round over.

        self.whos_the_winner()
        self.reset_round()

    def confirm_start(self):
        answer = input(f"Your balance is: ${self.player.balance}, wanna play?").lower()

        return answer in ["y", "yes", "start"]

    def start_game(self):
        while self.player.balance > 0:
            if not self.confirm_start():
                print(f"You left the game with ${self.player.balance}.")
                break

            self.start_round()
            print()

        else:
            print("No more money. Restart the game.")
