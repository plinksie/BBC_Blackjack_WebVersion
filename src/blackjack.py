from deck import Deck

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = []
        self.dealer_hand = []

    def start_game(self):
        """Start a new game by dealing initial cards to player and dealer."""
        self.player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]

    def get_player_cards(self):
        """Return the player's cards."""
        return self.player_hand

    def get_player_score(self):
        """Calculate and return the player's score."""
        return self.calculate_score(self.player_hand)

    def player_draw_card(self):
        """Add a card to the player's hand."""
        card = self.deck.deal_card()
        self.player_hand.append(card)
        return card

    def is_player_bust(self):
        """Check if the player is bust."""
        return self.calculate_score(self.player_hand) > 21

    def get_dealer_hand(self, reveal=False):
        """Return the dealer's cards. Hide the second card if not revealed."""
        if reveal:
            return self.dealer_hand
        return [self.dealer_hand[0], "[Hidden]"]

    def dealer_play(self):
        """Simulate the dealer's turn."""
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.deal_card())
        dealer_score = self.calculate_score(self.dealer_hand)
        player_score = self.calculate_score(self.player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            winner = "You win!"
        elif player_score == dealer_score:
            winner = "It's a tie!"
        else:
            winner = "Dealer wins."

        return {"dealer_cards": self.dealer_hand, "dealer_score": dealer_score, "winner": winner}

    @staticmethod
    def calculate_score(hand):
        """Calculate the Blackjack score of a hand."""
        score = 0
        aces = 0

        for card in hand:
            rank = card.split(" ")[0]
            if rank.isdigit():
                score += int(rank)
            elif rank in ["Jack", "Queen", "King"]:
                score += 10
            elif rank == "Ace":
                score += 11
                aces += 1

        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score