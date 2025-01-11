from deck import Deck

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

    def calculate_score(self):
        """Calculate the Blackjack score of the hand."""
        score = 0
        aces = 0

        for card in self.cards:
            rank = card.split(" ")[0]  # Extract rank from card string
            if rank.isdigit():
                score += int(rank)
            elif rank in ["Jack", "Queen", "King"]:
                score += 10
            elif rank == "Ace":
                score += 11
                aces += 1

        # Adjust for Aces if score exceeds 21
        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score


def play():
    print("Welcome to Blackjack!")
    deck = Deck()
    deck.shuffle()

    # Player setup
    player_hand = Hand()
    for _ in range(2):  # Deal initial 2 cards to player
        player_hand.add_card(deck.deal_card())

    # Dealer setup
    dealer_hand = Hand()
    for _ in range(2):  # Deal initial 2 cards to dealer
        dealer_hand.add_card(deck.deal_card())

    # Player's turn
    while True:
        print(f"Your hand: {player_hand.cards}, Score: {player_hand.calculate_score()}")
        if player_hand.calculate_score() > 21:
            print("Bust! You lose.")
            return

        action = input("Do you want to 'hit' or 'stand'? ").lower()
        if action == 'hit':
            player_hand.add_card(deck.deal_card())
        elif action == 'stand':
            break
        else:
            print("Invalid input. Please type 'hit' or 'stand'.")

    # Dealer's turn
    print(f"\nDealer's hand: {dealer_hand.cards[0]}, [Hidden]")
    while dealer_hand.calculate_score() < 17:
        dealer_hand.add_card(deck.deal_card())

    print(f"Dealer's final hand: {dealer_hand.cards}, Score: {dealer_hand.calculate_score()}")

    # Determine the winner
    player_score = player_hand.calculate_score()
    dealer_score = dealer_hand.calculate_score()

    if dealer_score > 21:
        print("Dealer busts! You win!")
    elif player_score > dealer_score:
        print("You win!")
    elif player_score == dealer_score:
        print("It's a tie!")
    else:
        print("Dealer wins!")


if __name__ == "__main__":
    play()