import random

class Card:
    """
    Represents a playing card with a suit and a rank.
    In Toucan, cards are ranked from King (highest) to Ace (lowest).
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Hand:
    """
    Represents a collection of cards held by a player.
    """
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards.clear()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        if self.cards:
            return ', '.join(str(card) for card in self.cards)
        else:
            return "Empty"


class Can:
    """
    Represents the stock of remaining cards after dealing.
    """
    def __init__(self):
        self.cards = []

    def set_cards(self, cards):
        self.cards = cards.copy()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Can: {len(self.cards)} card(s)"


class Player:
    """
    Represents a player with an ID, username, active status, and a hand.
    """
    def __init__(self, player_id):
        self.player_id = player_id
        self.username = None
        self.is_active = False
        self.hand = Hand()

    def __str__(self):
        if self.is_active and self.username:
            return f"Player {self.player_id} ({self.username}) - {len(self.hand)} card(s) in hand"
        else:
            return f"Player {self.player_id} (Not registered)"


class Game:
    """
    Manages player registration, deck setup, and dealing cards.
    The integrated 'Start New Round' action creates a deck, shuffles it,
    deals 7 cards to each active player, and sets aside the remaining cards as the stock (Can).
    """
    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.deck = []  # Temporary deck used for creation and shuffling
        self.can = Can()  # Stock of remaining cards

    def register_player(self, choice):
        """
        Registers a player based on the choice.
        Prompts for a username if the player is not yet registered.
        """
        if choice == '1':
            if not self.player1.is_active:
                username = input("Enter username for Player 1: ").strip()
                if not username:
                    return "Error: Username cannot be empty."
                self.player1.username = username
                self.player1.is_active = True
                return f"Player 1 registered as {username}."
            else:
                return f"Player 1 is already registered as {self.player1.username}."
        elif choice == '2':
            if not self.player2.is_active:
                username = input("Enter username for Player 2: ").strip()
                if not username:
                    return "Error: Username cannot be empty."
                self.player2.username = username
                self.player2.is_active = True
                return f"Player 2 registered as {username}."
            else:
                return f"Player 2 is already registered as {self.player2.username}."
        else:
            return "Error: Invalid registration option."

    def create_deck(self):
        """
        Creates a fresh deck of 52 cards.
        """
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        print("Deck created: 52 cards.")

    def shuffle_deck(self):
        """
        Shuffles the deck if it exists.
        """
        if not self.deck or len(self.deck) != 52:
            print("Error: Complete deck not found. Please create a deck first.")
            return
        random.shuffle(self.deck)
        print("Deck shuffled successfully.")

    def deal_cards(self):
        """
        Deals 7 cards to each active player.
        The remaining cards become the stock (Can).
        """
        active_players = [p for p in (self.player1, self.player2) if p.is_active]
        if not active_players:
            print("Error: No registered players. Please register at least one player.")
            return

        cards_needed = 7 * len(active_players)
        if len(self.deck) < cards_needed:
            print(f"Error: Not enough cards to deal. Required: {cards_needed}, available: {len(self.deck)}.")
            return

        for player in active_players:
            player.hand.clear()
            for _ in range(7):
                try:
                    card = self.deck.pop()
                    player.hand.add_card(card)
                except Exception as e:
                    print("Error while dealing cards:", e)
                    return

        self.can.set_cards(self.deck)
        self.deck = []  # Clear the temporary deck
        print("Cards dealt: 7 cards per active player.")
        print(f"Stock (Can) now has {len(self.can)} card(s).")

    def start_new_round(self):
        """
        Integrates deck creation, shuffling, and dealing into one action.
        """
        active_players = [p for p in (self.player1, self.player2) if p.is_active]
        if not active_players:
            print("Error: No registered players. Please register before starting a new round.")
            return
        self.create_deck()
        self.shuffle_deck()
        self.deal_cards()
        print("New round started successfully. Ready for trick-play phase.")

    def show_status(self):
        """
        Displays the registration status and current hands for both players,
        as well as the remaining stock (Can).
        """
        print("\n--- Game Status ---")
        print(self.player1)
        print(self.player2)
        print(self.can)
        print("-------------------")


def main():
    game = Game()
    print("=== Welcome to Toucan Card Game ===")
    while True:
        print("\nMenu:")
        print("[1] Register as Player 1")
        print("[2] Register as Player 2")
        print("[3] Start New Round")
        print("[4] Show Game Status")
        print("[Q] Quit")
        choice = input("Select an option: ").strip().lower()
        if choice == 'q':
            print("Thank you for playing! Goodbye.")
            break
        elif choice in ['1', '2']:
            result = game.register_player(choice)
            print(result)
        elif choice == '3':
            game.start_new_round()
        elif choice == '4':
            game.show_status()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred:", e)
