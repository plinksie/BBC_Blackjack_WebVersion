from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Global game instance and deck ID
deck_id = None
player_hand = []
dealer_hand = []

@app.route("/")
def home():
    """Landing page."""
    return render_template("home.html")


@app.route("/start", methods=["POST"])
def start_game():
    """Start a new game."""
    global deck_id, player_hand, dealer_hand
    # Fetch a new shuffled deck
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    deck_id = response.json()["deck_id"]

    # Deal two cards to player and dealer
    player_hand = draw_cards(2)
    dealer_hand = draw_cards(2)

    return render_template("game.html", player_hand=player_hand, dealer_hand=["Hidden"], player_score=calculate_score(player_hand))


@app.route("/draw", methods=["POST"])
def draw():
    """Draw a card for the player."""
    global player_hand
    card = draw_cards(1)[0]
    player_hand.append(card)
    player_score = calculate_score(player_hand)

    # Check if player busted
    is_bust = player_score > 21
    return jsonify({"card": card, "score": player_score, "is_bust": is_bust})


@app.route("/stand", methods=["POST"])
def stand():
    """Handle dealer's turn and determine winner."""
    global dealer_hand
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(draw_cards(1)[0])

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # Determine winner
    if dealer_score > 21 or player_score > dealer_score:
        winner = "You win!"
    elif player_score == dealer_score:
        winner = "It's a tie!"
    else:
        winner = "Dealer wins!"

    return jsonify({"dealer_cards": dealer_hand, "dealer_score": dealer_score, "winner": winner})


def draw_cards(count):
    """Draw cards from the API."""
    response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}")
    return response.json()["cards"]


def calculate_score(hand):
    """Calculate Blackjack score for a hand."""
    score = 0
    aces = 0

    for card in hand:
        value = card["value"]
        if value.isdigit():
            score += int(value)
        elif value in ["JACK", "QUEEN", "KING"]:
            score += 10
        elif value == "ACE":
            score += 11
            aces += 1

    # Adjust Aces if score exceeds 21
    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score


if __name__ == "__main__":
    app.run(debug=True)