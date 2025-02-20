"""
Toucan Card Game - Sprint #1 Consolidated
User Stories Implemented:
  1) Seat Players
  2) Create & Shuffle Deck
  3) Deal Cards

Features:
  - Two players can be 'seated' (is_active = True).
  - A fresh deck of 52 cards can be created and shuffled.
  - 7 cards are dealt to each active player, with leftover cards forming the 'Can' (stock).
  - Friendly messages guide the user and handle errors (e.g., not enough cards).

Note: Future sprints can streamline these steps or add GUI, AI, trick logic, scoring, etc.
"""

import random

class Card:
    """
    Represents a single playing card with a suit and rank.
    For Toucan, K is highest, A is lowest.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Player:
    """
    Holds:
      - player_id (1 or 2)
      - is_active (bool): whether the player has 'taken a seat'
      - hand (list of Card): 7 cards after dealing
    """
    def __init__(self, player_id):
        self.player_id = player_id
        self.is_active = False
        self.hand = []

    def __str__(self):
        status = "ready to play" if self.is_active else "not yet seated"
        return f"Player {self.player_id} is {status} with {len(self.hand)} card(s)."

class Game:
    """
    Manages:
      - Two players (player1, player2)
      - A deck (list of Card) which becomes the Can/stock after dealing
      - Seating players, creating/shuffling deck, dealing cards
    """

    def __init__(self):
        self.player1 = Player(player_id=1)
        self.player2 = Player(player_id=2)
        self.deck = []  # Will store 52 Card objects after creation

    def seat_player(self, choice):
        """
        Seats Player 1 or Player 2 if not active. Returns a user-friendly message.
        """
        if choice == '1':
            if not self.player1.is_active:
                self.player1.is_active = True
                return "Player 1 is now seated at the table."
            else:
                return "Player 1 is already seated."
        elif choice == '2':
            if not self.player2.is_active:
                self.player2.is_active = True
                return "Player 2 has joined the table."
            else:
                return "Player 2 is already seated."
        else:
            return "Invalid choice for seating."

    def create_deck(self):
        """
        Builds a fresh 52-card deck, K..A in each suit, stored in self.deck.
        """
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        print("\nA fresh deck of 52 cards has been created (K down to A).")

    def shuffle_deck(self):
        """
        Randomly shuffles self.deck, if it exists.
        """
        if not self.deck:
            print("\nOops! There's no deck to shuffle. Please create one first.")
            return
        random.shuffle(self.deck)
        print("\nShuffle complete! The deck is ready for dealing.")

    def deal_cards(self):
        """
        Deals 7 cards to each active player, if enough cards are present.
        Updates self.deck to become the stock ('Can') after dealing.
        """
        # Gather active players
        active_players = []
        if self.player1.is_active:
            active_players.append(self.player1)
        if self.player2.is_active:
            active_players.append(self.player2)

        if not active_players:
            print("\nNo players to deal to! Please seat at least one player first.")
            return

        needed = 7 * len(active_players)
        if len(self.deck) < needed:
            print(f"\nNot enough cards to deal. Need {needed}, have {len(self.deck)}.")
            print("Please create & shuffle a proper deck first.")
            return

        # Clear old hands (in case of multiple rounds)
        for player in active_players:
            player.hand.clear()

        # Deal 7 cards each
        for player in active_players:
            for _ in range(7):
                card = self.deck.pop()
                player.hand.append(card)

        print(f"\nDealing complete! Each active player received 7 cards.")
        print(f"{len(self.deck)} cards remain in the 'Can' (stock).")
        print("The game is now ready to proceed to the play phase!")

    def show_player_status(self):
        """
        Displays current status of Player 1 and Player 2 (hand size, seating).
        """
        print("\n---- Current Player Status ----")
        print(self.player1)
        print(self.player2)
        print("--------------------------------")

def main():
    game = Game()

    print("=== Welcome to Toucan (Sprint #1) ===")
    print("This console-based version demonstrates seating players, creating/shuffling a deck, and dealing cards.")

    while True:
        print("\nMain Menu:")
        print("  [1] Seat Player 1")
        print("  [2] Seat Player 2")
        print("  [3] Create a Fresh Deck (52 cards)")
        print("  [4] Shuffle the Deck")
        print("  [5] Deal Cards (7 each to active players)")
        print("  [6] Show Player Status")
        print("  [Q] Quit")

        choice = input("Please select an option: ").strip().lower()

        if choice == 'q':
            print("\nThanks for playing! Goodbye.")
            break
        elif choice == '1':
            result = game.seat_player(choice='1')
            print("\n" + result)
        elif choice == '2':
            result = game.seat_player(choice='2')
            print("\n" + result)
        elif choice == '3':
            game.create_deck()
        elif choice == '4':
            game.shuffle_deck()
        elif choice == '5':
            game.deal_cards()
        elif choice == '6':
            game.show_player_status()
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nAn unexpected error occurred. Please report the following:")
        print(str(e))
