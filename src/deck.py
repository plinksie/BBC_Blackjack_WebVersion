import random

class Deck:
    def __init__(self):
        self.cards = [
            f"{rank} of {suit}"
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        ]

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deal a card from the top of the deck."""
        if self.cards:
            return self.cards.pop()
        raise ValueError("No cards left in the deck!")