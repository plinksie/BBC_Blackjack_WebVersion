from flask import Flask, render_template, request, jsonify
import requests
from blackjack import BlackjackGame

app = Flask(__name__)

# Global game instance and deck ID
game = None
deck_id = None


@app.route("/")
def home():
    """Landing page."""
    return render_template("home.html")


@app.route("/start", methods=["POST"])
def start_game():
    """Initialize a new game."""
    global game, deck_id
    # Fetch a new shuffled deck
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    deck_id = response.json().get("deck_id")

    # Initialize a new game
    game = BlackjackGame(deck_id)
    game.start_game()

    return render_template("game.html", player_cards=game.get_player_cards(), player_score=game.get_player_score())


@app.route("/draw", methods=["POST"])
def draw_card():
    """Handle player drawing a card."""
    global game
    if not game:
        return jsonify({"error": "Game not started"}), 400

    card = game.player_draw_card()
    return jsonify({"card": card, "score": game.get_player_score(), "is_bust": game.is_player_bust()})


@app.route("/stand", methods=["POST"])
def stand():
    """Handle player standing and calculate dealer's turn."""
    global game
    if not game:
        return jsonify({"error": "Game not started"}), 400

    dealer_result = game.dealer_play()
    return jsonify({
        "dealer_cards": dealer_result["dealer_cards"],
        "dealer_score": dealer_result["dealer_score"],
        "winner": dealer_result["winner"]
    })


if __name__ == "__main__":
    app.run(debug=True)