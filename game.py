import random

# Mapping for card rank values (Ace is low)
RANK_VALUES = {
    "K": 13, "Q": 12, "J": 11, "10": 10,
    "9": 9, "8": 8, "7": 7, "6": 6,
    "5": 5, "4": 4, "3": 3, "2": 2, "A": 1
}

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
    Represents the collection of cards held by a player.
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
            return ', '.join(f"{i+1}:{str(card)}" for i, card in enumerate(self.cards))
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
        return f"Stock (Can) with {len(self.cards)} card(s)"

class Player:
    """
    Represents a player with an ID, username, active status, and a hand.
    """
    def __init__(self, player_id):
        self.player_id = player_id
        self.username = None
        self.is_active = False
        self.hand = Hand()
        self.role = None  # Future use: leader or follower

    def __str__(self):
        if self.is_active and self.username:
            return f"Player {self.player_id} ({self.username}) - {len(self.hand)} card(s) in hand"
        return f"Player {self.player_id} (Not registered)"

class Game:
    """
    Manages player registration, game setup (deck creation, shuffling, dealing),
    and the trick-play phase.
    """
    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.deck = []   # Temporary deck used during setup
        self.can = Can() # Stock of remaining cards after dealing
        self.current_trick = {}  # Will hold trick data during trick play

    # --- Setup Phase ---
    def register_player(self, choice):
        if choice == '1':
            if not self.player1.is_active:
                username = input("Enter username for Player 1: ").strip()
                if not username:
                    return "Error: Username cannot be empty."
                self.player1.username = username
                self.player1.is_active = True
                return f"Player 1 registered as {username}."
            return f"Player 1 is already registered as {self.player1.username}."
        elif choice == '2':
            if not self.player2.is_active:
                username = input("Enter username for Player 2: ").strip()
                if not username:
                    return "Error: Username cannot be empty."
                self.player2.username = username
                self.player2.is_active = True
                return f"Player 2 registered as {username}."
            return f"Player 2 is already registered as {self.player2.username}."
        else:
            return "Error: Invalid registration option."

    def create_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        print("Deck created: 52 cards.")

    def shuffle_deck(self):
        if not self.deck or len(self.deck) != 52:
            print("Error: Complete deck not found. Please create a deck first.")
            return
        random.shuffle(self.deck)
        print("Deck shuffled.")

    def deal_cards(self):
        active_players = [p for p in (self.player1, self.player2) if p.is_active]
        if not active_players:
            print("Error: No registered players. Register at least one player.")
            return
        cards_needed = 7 * len(active_players)
        if len(self.deck) < cards_needed:
            print(f"Error: Not enough cards to deal. Need {cards_needed}, available {len(self.deck)}.")
            return
        for player in active_players:
            player.hand.clear()
            for _ in range(7):
                player.hand.add_card(self.deck.pop())
        self.can.set_cards(self.deck)
        self.deck = []  # Clear the temporary deck
        print("Dealing complete: 7 cards each. Stock updated.")

    def start_new_round(self):
        active_players = [p for p in (self.player1, self.player2) if p.is_active]
        if not active_players:
            print("Error: No registered players. Please register before starting a new round.")
            return
        self.create_deck()
        self.shuffle_deck()
        self.deal_cards()
        print("New round started. Ready for trick-play phase.")

    def show_status(self):
        print("\n--- Game Status ---")
        print(self.player1)
        print(self.player2)
        print(self.can)
        print("-------------------")

    # --- Trick-Play Phase ---
    def leader_move(self):
        # Determine leader: for simplicity, choose first registered player.
        leader = None
        if self.player1.is_active:
            leader = self.player1
        elif self.player2.is_active:
            leader = self.player2
        if not leader:
            print("Error: No registered players.")
            return False
        if len(leader.hand) < 2:
            print(f"Error: {leader.username} does not have enough cards to play a trick.")
            return False

        print(f"\n{leader.username}'s hand:")
        print(leader.hand)
        try:
            indices = input("Select two card numbers to play (separated by a space): ").split()
            if len(indices) != 2:
                print("Error: Exactly two cards must be selected.")
                return False
            indices = [int(i) - 1 for i in indices]
            if any(i < 0 or i >= len(leader.hand.cards) for i in indices):
                print("Error: One or more selected card indices are out of range.")
                return False
            # Get the selected cards (remove them from hand in reverse order)
            selected_cards = [leader.hand.cards[i] for i in sorted(indices, reverse=True)]
            for i in sorted(indices, reverse=True):
                del leader.hand.cards[i]
        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")
            return False
        except Exception as e:
            print("Error during card selection:", e)
            return False

        declaration = input("Declare 'High' or 'Low': ").strip().lower()
        if declaration not in ['high', 'low']:
            print("Error: Declaration must be 'High' or 'Low'.")
            return False

        self.current_trick['leader'] = leader
        self.current_trick['leader_cards'] = selected_cards
        self.current_trick['declaration'] = declaration
        print(f"{leader.username} played: {selected_cards[0]} and {selected_cards[1]} with declaration '{declaration}'.")
        return True

    def follower_move(self):
        # Identify follower: the other registered player.
        if self.player1.is_active and self.player2.is_active:
            follower = self.player2 if self.current_trick.get('leader') == self.player1 else self.player1
        else:
            print("Error: Both players must be registered for a trick.")
            return False

        if len(follower.hand) < 2:
            print(f"Error: {follower.username} does not have enough cards to play a trick.")
            return False

        print(f"\n{follower.username}'s hand:")
        print(follower.hand)
        try:
            indices = input("Select two card numbers to play (separated by a space): ").split()
            if len(indices) != 2:
                print("Error: Exactly two cards must be selected.")
                return False
            indices = [int(i) - 1 for i in indices]
            if any(i < 0 or i >= len(follower.hand.cards) for i in indices):
                print("Error: One or more selected card indices are out of range.")
                return False
            selected_cards = [follower.hand.cards[i] for i in sorted(indices, reverse=True)]
            for i in sorted(indices, reverse=True):
                del follower.hand.cards[i]
        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")
            return False
        except Exception as e:
            print("Error during card selection:", e)
            return False

        self.current_trick['follower'] = follower
        self.current_trick['follower_cards'] = selected_cards
        print(f"{follower.username} played: {selected_cards[0]} and {selected_cards[1]}.")
        return True

    def evaluate_trick(self):
        """
        Evaluates the trick based on the leader's declaration.
        For 'high', compares the first card of each pair;
        for 'low', compares the second card.
        In case of tie, the other card is used.
        """
        if not self.current_trick.get('leader') or not self.current_trick.get('follower'):
            print("Error: Incomplete trick data.")
            return

        declaration = self.current_trick.get('declaration')
        leader_cards = self.current_trick.get('leader_cards')
        follower_cards = self.current_trick.get('follower_cards')

        if declaration == 'high':
            leader_value = RANK_VALUES.get(leader_cards[0].rank, 0)
            follower_value = RANK_VALUES.get(follower_cards[0].rank, 0)
            if leader_value > follower_value:
                winner = self.current_trick['leader']
            elif leader_value < follower_value:
                winner = self.current_trick['follower']
            else:
                leader_value = RANK_VALUES.get(leader_cards[1].rank, 0)
                follower_value = RANK_VALUES.get(follower_cards[1].rank, 0)
                winner = self.current_trick['leader'] if leader_value >= follower_value else self.current_trick['follower']
        elif declaration == 'low':
            leader_value = RANK_VALUES.get(leader_cards[1].rank, 0)
            follower_value = RANK_VALUES.get(follower_cards[1].rank, 0)
            if leader_value < follower_value:
                winner = self.current_trick['leader']
            elif leader_value > follower_value:
                winner = self.current_trick['follower']
            else:
                leader_value = RANK_VALUES.get(leader_cards[0].rank, 0)
                follower_value = RANK_VALUES.get(follower_cards[0].rank, 0)
                winner = self.current_trick['leader'] if leader_value <= follower_value else self.current_trick['follower']
        else:
            print("Error: Unknown declaration.")
            return

        print(f"\nTrick evaluated. Winner: {winner.username} wins the trick!")
        self.current_trick.clear()

    def play_trick(self):
        """
        Coordinates the leader's and follower's moves and evaluates the trick.
        """
        print("\n--- Trick Play Phase ---")
        if not self.leader_move():
            return
        if not self.follower_move():
            return
        self.evaluate_trick()

def main():
    game = Game()
    print("=== Welcome to Toucan Card Game ===")
    while True:
        print("\nMenu:")
        print("[1] Register as Player 1")
        print("[2] Register as Player 2")
        print("[3] Start New Round")
        print("[4] Play Trick")
        print("[5] Show Game Status")
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
            game.play_trick()
        elif choice == '5':
            game.show_status()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred:", e)
