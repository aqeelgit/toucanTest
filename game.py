"""
Game Module: A minimal console-based introduction for the "Toucan" card game.

This script demonstrates:
  - A Player class representing a game participant.
  - A Game class that manages two players' states.
  - A main function that provides a console menu, letting players "Take a Seat"
    with friendly, encouraging messages (including error feedback).

Usage:
  python game.py

Dependencies:
  - A standard Python 3.x installation
"""

class Player:
    """
    Represents a single player in the Toucan game.
    Each player has:
      - player_id (int): Unique identifier (e.g., 1 or 2).
      - is_active (bool): Whether the player is 'seated' in the game.
    """

    def __init__(self, player_id):
        """
        Initializes the Player with a given player_id.
        By default, a new player is not active (is_active = False).
        """
        self.player_id = player_id
        self.is_active = False

    def __str__(self):
        """
        Returns a user-friendly string describing the player's status.
        """
        status = "ready to play" if self.is_active else "not yet seated"
        return f"Player {self.player_id} is currently {status}"

class Game:
    """
    Manages the overall state for a two-player Toucan game.
    It holds two Player objects and provides methods to let them 'take a seat'
    with positive, user-friendly messages.
    """

    def __init__(self):
        """
        Creates two Player objects (player1 and player2).
        Each starts inactive, awaiting a call to 'enter_game'.
        """
        self.player1 = Player(player_id=1)
        self.player2 = Player(player_id=2)

    def enter_game(self, choice):
        """
        Allows the user to become Player 1 or Player 2 if they are not active already.
        Parameters:
            choice (str): '1' to become Player 1, '2' to become Player 2.
        Returns:
            str: A friendly message indicating success or reason for failure.
        """
        if choice == '1':
            if not self.player1.is_active:
                self.player1.is_active = True
                return "Awesome! Player 1 is now seated at the table."
            else:
                return "Friendly reminder: Player 1 is already seated. Let's get the action rolling!"
        elif choice == '2':
            if not self.player2.is_active:
                self.player2.is_active = True
                return "Fantastic! Player 2 has joined the table. Let the fun begin!"
            else:
                return "Heads up: Player 2 is already seated, no worries—we're all set!" 
        else:
            # Normally shouldn't happen if caller ensures valid inputs
            return "Something went wrong. Please enter '1' or '2' only."

    def get_active_players(self):
        """
        Gathers a human-readable list of all currently seated players.
        Returns:
            list of str: e.g., ["Player 1"] or ["Player 1", "Player 2"].
        """
        active = []
        if self.player1.is_active:
            active.append("Player 1")
        if self.player2.is_active:
            active.append("Player 2")
        return active

def main():
    """
    Main entry point: Displays a console menu allowing the user(s) to 'take a seat' in the game.
    Prevents duplicate seats and handles invalid inputs in a friendly, encouraging manner.
    """
    game = Game()

    print("Welcome to Toucan (Console Version)!")
    print("Get ready for a lighthearted, card-flinging adventure!\n")

    # Loop until the user quits or both players have entered
    while True:
        print("\nMain Menu:")
        print("  [1] Take a Seat as Player 1")
        print("  [2] Take a Seat as Player 2")
        print("  [Q] Quit (Hope you can join us another time!)")
        user_input = input("Your choice: ").strip()

        # If user decides to quit
        if user_input.lower() == 'q':
            print("\nNo worries—thanks for stopping by! See you next time!")
            break

        # Validate user_input is either '1' or '2'
        if user_input not in ('1', '2'):
            # Show an encouraging error message, then continue
            print("\nThat choice doesn't ring a bell.")
            print("Try '1', '2', or 'Q' to quit. You'll get the hang of it!")
            continue

        # Attempt to seat the chosen player
        result_message = game.enter_game(user_input)
        print(f"\n{result_message}")

        # Display which players are currently seated
        active_players = game.get_active_players()
        if active_players:
            print("Currently seated player(s):", ", ".join(active_players))
        else:
            print("No one is seated at the table yet... but there's always time!")

        # Optional stopping condition: if both are active, we can move on
        if game.player1.is_active and game.player2.is_active:
            print("\nGreat news, both players are now seated!")
            print("Stay tuned: card-dealing and more awaits in our next phase. Enjoy!")
            break  # End this "Enter the Game" loop

# Standard Python convention to protect the main logic
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Catch any unforeseen errors to prevent crashes
        print("\nOops! An unexpected error just happened.")
        print("But don't worry—we'll fix it soon. Here are some details:")
        print(str(e))
