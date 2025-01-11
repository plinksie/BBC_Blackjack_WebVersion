import unittest
from deck import Deck
from blackjack import Hand

class DeckTestCase(unittest.TestCase):
    def test_shuffle(self):
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        self.assertNotEqual(deck.cards, original_order, "Deck should be shuffled.")

    def test_deal_card(self):
        deck = Deck()
        initial_size = len(deck.cards)
        card = deck.deal_card()
        self.assertEqual(len(deck.cards), initial_size - 1, "Dealing a card should reduce deck size by 1.")
        self.assertNotIn(card, deck.cards, "Dealt card should be removed from the deck.")

    def test_empty_deck(self):
        deck = Deck()
        for _ in range(52):  # Exhaust the deck
            deck.deal_card()
        with self.assertRaises(ValueError):
            deck.deal_card()


class HandTestCase(unittest.TestCase):
    def test_hand_score(self):
        hand = Hand()
        hand.add_card("10 of Hearts")
        hand.add_card("Ace of Spades")
        self.assertEqual(hand.calculate_score(), 21, "Hand score should calculate correctly.")

    def test_ace_adjustment(self):
        hand = Hand()
        hand.add_card("Ace of Hearts")
        hand.add_card("Ace of Spades")
        hand.add_card("9 of Diamonds")
        self.assertEqual(hand.calculate_score(), 21, "Hand score should adjust for multiple Aces correctly.")


if __name__ == "__main__":
    unittest.main()