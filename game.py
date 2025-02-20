"""
Toucan Card Game (Partial Implementation)
Combines:
  - User Story #001: "Enter the Game"
  - User Story #002: "Shuffle the Deck"

Features so far:
  1. Players can 'take a seat' (become active).
  2. We can create a standard 52-card deck (K..A).
  3. We can shuffle the deck and confirm it's ready.
  4. The program handles input errors politely and won't crash.

Note: Future stories (like dealing cards, trick-taking, scoring) can be added later.
"""

import random

class Card:
    """
    Represents a single playing card with a suit and rank.
    K is highest, A is lowest for this game’s logic.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """
        Returns a user-friendly string, like "K of Hearts".
        """
        return f"{self.rank} of {self.suit}"

class Player:
    """
    Represents a single player in the Toucan card game.
    Each player has:
      - player_id (int): Unique identifier (e.g., 1 or 2).
      - is_active (bool): Whether the player is 'seated' in the game.
    """

    def __init__(self, player_id):
        self.player_id = player_id
        self.is_active = False

    def __str__(self):
        """
        Returns a user-friendly status of the player.
        """
        status = "ready to play" if self.is_active else "not yet seated"
        return f"Player {self.player_id} is currently {status}"

class Game:
    """
    Manages:
      - Two Player objects (player1, player2)
      - A deck of cards (list of Card objects)
      - Logic to seat players, create a deck, and shuffle it.
    """

    def __init__(self):
        self.player1 = Player(player_id=1)
        self.player2 = Player(player_id=2)
        self.deck = []  # Will store Card objects once created

    def seat_player(self, choice):
        """
        Lets the user become Player 1 or Player 2 if not active already.
        Returns a friendly message about the result.
        """
        if choice == '1':
            if not self.player1.is_active:
                self.player1.is_active = True
                return "Awesome! Player 1 is now seated at the table."
            else:
                return "Friendly reminder: Player 1 is already seated. Let's keep things rolling!"
        elif choice == '2':
            if not self.player2.is_active:
                self.player2.is_active = True
                return "Fantastic! Player 2 has joined the table. Let the fun begin!"
            else:
                return "Heads up: Player 2 is already seated. No worries, we're set!"
        else:
            # Shouldn't happen if we validate the input.
            return "Something went wrong. Please choose '1' or '2'."

    def get_active_players(self):
        """
        Returns a list of strings representing all players currently seated.
        """
        active = []
        if self.player1.is_active:
            active.append("Player 1")
        if self.player2.is_active:
            active.append("Player 2")
        return active

    def create_deck(self):
        """
        Creates a fresh 52-card deck.
        K is highest, A is lowest in rank order for this game.
        """
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        # Ranks: K down to A, with A as the lowest
        ranks = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]

        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle_deck(self):
        """
        Randomly shuffles the deck if it exists. 
        Prints a friendly confirmation or warns if no deck is created.
        """
        if not self.deck:
            print("\nOops! There's no deck to shuffle. Create one first (option 3).")
            return

        random.shuffle(self.deck)
        print("\nShuffling complete! The deck is now ready for dealing (in a future step).")

def main():
    """
    Main program flow (console-based):
      1. Players can seat themselves (User Story #001).
      2. We can create a deck and shuffle it (User Story #002).
      3. Error handling for invalid inputs, duplicates, etc.
    """
    game = Game()

    print("Welcome to Toucan (Console Version)!")
    print("Get ready for a lighthearted card-flinging adventure!\n")

    while True:
        print("\nMain Menu:")
        print("  [1] Take a Seat as Player 1")
        print("  [2] Take a Seat as Player 2")
        print("  [3] Create a Fresh Deck")
        print("  [4] Shuffle the Deck")
        print("  [Q] Quit (Hope you can join us another time!)")

        user_input = input("Your choice: ").strip()

        # Quit the program
        if user_input.lower() == 'q':
            print("\nNo worries—thanks for stopping by! See you next time!")
            break

        # Seat players
        elif user_input in ('1', '2'):
            result = game.seat_player(user_input)
            print(f"\n{result}")

            active_players = game.get_active_players()
            if active_players:
                print("Currently seated player(s):", ", ".join(active_players))
            else:
                print("No one is seated at the table yet.")

        # Create deck
        elif user_input == '3':
            game.create_deck()
            print("\nA fresh deck of 52 cards has been created! Ranks K..A, suits Hearts/Diamonds/Clubs/Spades.")  

        # Shuffle deck
        elif user_input == '4':
            game.shuffle_deck()

        # Handle invalid menu input
        else:
            print("\nThat choice doesn't ring a bell.")
            print("Try '1', '2', '3', '4', or 'Q' to quit. You'll get the hang of it!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nOh no! An unexpected error occurred.")
        print("Please let the developer know or try again.")
        print("Error details:", str(e))
