import random
import time
import os
from player import Player, Hand, Card, Can

# ASCII card visualization
class ASCIICard:
    """
    Provides ASCII visualization for cards in the terminal
    """
    # ASCII representations for each suit
    SUIT_SYMBOLS = {
        "Hearts": "♥",    # or use "<3" for better compatibility
        "Diamonds": "♦",  # or use "<>" for better compatibility
        "Clubs": "♣",     # or use "+" for better compatibility
        "Spades": "♠"     # or use "^" for better compatibility
    }
    
    # ASCII card frame
    CARD_TOP = ".-------."
    CARD_BOTTOM = "'-------'"
    CARD_EMPTY = "|       |"
    
    @staticmethod
    def get_card_ascii(card):
        """Returns a list of strings representing a card's ASCII appearance"""
        rank_display = card.rank.ljust(2)
        suit_symbol = ASCIICard.SUIT_SYMBOLS[card.suit]
        
        return [
            ASCIICard.CARD_TOP,
            f"| {rank_display}    |",
            f"|   {suit_symbol}   |",
            # f"|    {rank_display.rstrip()} |",
            #ASCIICard.CARD_BOTTOM
        ]
    
    @staticmethod
    def display_hand(hand):
        """Displays all cards in a hand as ASCII art with card numbers"""
        if not hand.cards:
            print("Empty hand")
            return
            
        # Create header with card numbers - adjusted spacing
        header = "    "
        for i in range(len(hand.cards)):
            # The 9 matches the width of the ASCII card (9 characters)
            card_num = str(i + 1).center(9)
            header += card_num + " "
        print(header)
        
        # Prepare all card visuals
        card_displays = [ASCIICard.get_card_ascii(card) for card in hand.cards]
        
        # Display cards in rows
        for line_idx in range(3):  # Only display 3 lines
            line = "    "
            for card_display in card_displays:
                line += card_display[line_idx] + " "
            print(line)

    @staticmethod
    def display_trick(leader_cards, follower_cards, leader_name, follower_name, declaration=None):
        """Displays current trick with leader and follower cards"""
        # Display trick header
        print("\n" + "=" * 50)
        header = f"Current Trick"
        if declaration:
            header += f" (Declaration: {declaration.upper()})"
        print(f"{header.center(50)}")
        print("=" * 50)
        
        # Leader cards
        leader_displays = [ASCIICard.get_card_ascii(card) for card in leader_cards]
        print(f"\n{leader_name}'s cards:")
        for line_idx in range(3):
            line = "    "
            for card_display in leader_displays:
                line += card_display[line_idx] + " "
            print(line)
            
        # Follower cards
        follower_displays = [ASCIICard.get_card_ascii(card) for card in follower_cards]
        print(f"\n{follower_name}'s cards:")
        for line_idx in range(3):
            line = "    "
            for card_display in follower_displays:
                line += card_display[line_idx] + " "
            print(line)

# Utility functions
def clear_screen():
    """Clear the console screen"""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')

def print_header(text, width=60):
    """Print a nicely formatted header"""
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width)

def print_subheader(text, width=60):
    """Print a nicely formatted subheader"""
    print("\n" + "-" * width)
    print(text.center(width))
    print("-" * width)

def animate_text(text, delay=0.01):
    """Print text with a typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def display_card_info():
    """Display info about card ranks and suits"""
    print_subheader("Card Information")
    print("Ranks: K (highest) > Q > J > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > A (lowest)")
    print("Suits: ♥ Hearts (red) | ♦ Diamonds (red) | ♣ Clubs (black) | ♠ Spades (black)")
    print("\nPattern Rules:")
    print("- Two cards of same suit → must play two of the same suit")
    print("- Two cards of same color but different suits → must play the same pattern")
    print("- Two cards of different colors → must play two cards of different colors")

# Mapping for card rank values (Ace is low)
RANK_VALUES = {
    "K": 13, "Q": 12, "J": 11, "10": 10,
    "9": 9, "8": 8, "7": 7, "6": 6,
    "5": 5, "4": 4, "3": 3, "2": 2, "A": 1
}

class Game:
    """
    Enhanced version of the Toucan card game with improved visuals and UX
    """
    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.deck = []   # Temporary deck used during setup
        self.can = Can() # Stock of remaining cards after dealing
        self.current_trick = {}  # Will hold trick data during trick play
        self.victory_threshold = 27
        self.played_tricks = []  # Store history of played tricks

    # --- Setup Phase ---
    def register_player(self, choice):
        """Register a player with improved input validation"""
        if choice == '1':
            if not self.player1.is_active:
                while True:
                    username = input("Enter username for Player 1: ").strip()
                    if not username:
                        print("Error: Username cannot be empty. Please try again.")
                    else:
                        break
                self.player1.username = username
                self.player1.is_active = True
                return f"Player 1 registered as {username}."
            return f"Player 1 is already registered as {self.player1.username}."
        elif choice == '2':
            if not self.player2.is_active:
                while True:
                    username = input("Enter username for Player 2: ").strip()
                    if not username:
                        print("Error: Username cannot be empty. Please try again.")
                    else:
                        break
                self.player2.username = username
                self.player2.is_active = True
                return f"Player 2 registered as {username}."
            return f"Player 2 is already registered as {self.player2.username}."
        else:
            return "Error: Invalid registration option."

    def create_deck(self):
        """Create a standard 52-card deck with visual feedback"""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        animate_text("Deck created: 52 cards.", delay=0.01)

    def shuffle_deck(self):
        """Shuffle the deck with visual feedback"""
        if not self.deck or len(self.deck) != 52:
            print("Error: Complete deck not found. Please create a deck first.")
            return
        random.shuffle(self.deck)
        animate_text("Deck shuffled. Cards are now in random order.", delay=0.01)

    def deal_cards(self):
        """Deal cards to players with visual feedback"""
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
            print(f"\nDealing 7 cards to {player.username}...")
            for _ in range(7):
                card = self.deck.pop()
                player.hand.add_card(card)
                time.sleep(0.05)  # Slight delay for effect
                
        self.can.set_cards(self.deck)
        self.deck = []  # Clear the temporary deck
        
        animate_text("\nDealing complete! Each player has 7 cards.", delay=0.01)
        animate_text(f"Stock has {len(self.can.cards)} remaining cards.", delay=0.01)

    def start_new_round(self):
        """Start a new game round with enhanced visual feedback"""
        active_players = [p for p in (self.player1, self.player2) if p.is_active]
        if not active_players:
            print("Error: No registered players. Please register before starting a new round.")
            return
            
        # Reset trick history
        self.played_tricks = []
        
        # Reset current trick data
        self.current_trick = {}
        
        self.create_deck()
        time.sleep(0.5)
        self.shuffle_deck()
        time.sleep(0.5)
        self.deal_cards()
        
        print("\nNew round started. Ready for trick-play phase!")

    def show_status(self):
        """Enhanced status display with ASCII visualization"""
        clear_screen()
        print_header("Game Status")
        
        # Display player information
        print(f"Player 1: {self.player1.username if self.player1.is_active else 'Not registered'}")
        if self.player1.is_active:
            print(f"Cards in hand: {len(self.player1.hand)}")
        
        print(f"\nPlayer 2: {self.player2.username if self.player2.is_active else 'Not registered'}")
        if self.player2.is_active:
            print(f"Cards in hand: {len(self.player2.hand)}")
        
        # Display Can (stock) information
        print(f"\nCards in stock: {len(self.can.cards)}")
        
        # Display card information
        display_card_info()
        
        # Show hands if both players are active
        if self.player1.is_active:
            print_subheader(f"{self.player1.username}'s Hand")
            ASCIICard.display_hand(self.player1.hand)
        
        if self.player2.is_active:
            print_subheader(f"{self.player2.username}'s Hand")
            ASCIICard.display_hand(self.player2.hand)

    # --- Trick-Play Phase ---
    def leader_move(self):
        """Enhanced leader move with better visuals and input validation"""
        # Determine leader
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

        clear_screen()
        print_header(f"{leader.username}'s Turn (Leader)")
        
        # Display leader's hand
        print(f"Your hand:")
        ASCIICard.display_hand(leader.hand)
        
        # Card selection with validation
        while True:
            try:
                indices_input = input("\nSelect two card numbers to play (separated by a space): ")
                indices = indices_input.split()
                
                if len(indices) != 2:
                    print("Error: Exactly two cards must be selected.")
                    continue
                    
                indices = [int(i) - 1 for i in indices]
                
                if any(i < 0 or i >= len(leader.hand.cards) for i in indices):
                    print("Error: One or more selected card indices are out of range.")
                    continue
                    
                if indices[0] == indices[1]:
                    print("Error: You must select two different cards.")
                    continue
                    
                break
            except ValueError:
                print("Error: Invalid input. Please enter numeric values.")
        
        # Get the selected cards
        selected_cards = [leader.hand.cards[i] for i in sorted(indices, reverse=True)]
        
        # Display selected cards
        print("\nYou selected:")
        leader_displays = [ASCIICard.get_card_ascii(card) for card in selected_cards]
        for line_idx in range(3):
            line = "    "
            for card_display in leader_displays:
                line += card_display[line_idx] + " "
            print(line)
        
        # Remove the cards from hand
        for i in sorted(indices, reverse=True):
            del leader.hand.cards[i]
        
        # Get declaration with validation
        while True:
            declaration = input("\nDeclare 'High' or 'Low': ").strip().lower()
            if declaration in ['high', 'low']:
                break
            print("Error: Declaration must be 'High' or 'Low'.")
        
        self.current_trick['leader'] = leader
        self.current_trick['leader_cards'] = selected_cards
        self.current_trick['declaration'] = declaration
        
        animate_text(f"\n{leader.username} played two cards with declaration '{declaration}'.")
        time.sleep(1)
        return True

    def follower_move(self):
        """Enhanced follower move with better visuals and input validation"""
        # Identify follower
        if self.player1.is_active and self.player2.is_active:
            follower = self.player2 if self.current_trick.get('leader') == self.player1 else self.player1
        else:
            print("Error: Both players must be registered for a trick.")
            return False

        if len(follower.hand) < 2:
            print(f"Error: {follower.username} does not have enough cards to play a trick.")
            return False
        
        # Display trick information
        clear_screen()
        print_header(f"{follower.username}'s Turn (Follower)")
        
        leader = self.current_trick['leader']
        leader_cards = self.current_trick['leader_cards']
        declaration = self.current_trick['declaration']
        
        print(f"{leader.username} played:")
        leader_displays = [ASCIICard.get_card_ascii(card) for card in leader_cards]
        for line_idx in range(3):
            line = "    "
            for card_display in leader_displays:
                line += card_display[line_idx] + " "
            print(line)
        
        print(f"\nDeclaration: {declaration.upper()}")
        
        # Show pattern information
        pattern_type = ""
        if leader_cards[0].suit == leader_cards[1].suit:
            pattern_type = f"Two cards of the SAME SUIT ({leader_cards[0].suit})"
        elif (leader_cards[0].suit in ["Hearts", "Diamonds"] and 
              leader_cards[1].suit in ["Hearts", "Diamonds"]):
            pattern_type = "Two RED cards of DIFFERENT SUITS"
        elif (leader_cards[0].suit in ["Clubs", "Spades"] and 
              leader_cards[1].suit in ["Clubs", "Spades"]):
            pattern_type = "Two BLACK cards of DIFFERENT SUITS"
        else:
            pattern_type = "One RED and one BLACK card"
        
        print(f"\nPattern: {pattern_type}")
        print("You must follow this pattern with your two cards.")
        
        # Display follower's hand
        print(f"\nYour hand:")
        ASCIICard.display_hand(follower.hand)
        
        # Card selection with validation
        while True:
            try:
                indices_input = input("\nSelect two card numbers to play (separated by a space): ")
                indices = indices_input.split()
                
                if len(indices) != 2:
                    print("Error: Exactly two cards must be selected.")
                    continue
                    
                indices = [int(i) - 1 for i in indices]
                
                if any(i < 0 or i >= len(follower.hand.cards) for i in indices):
                    print("Error: One or more selected card indices are out of range.")
                    continue
                    
                if indices[0] == indices[1]:
                    print("Error: You must select two different cards.")
                    continue
                    
                # Preview if the pattern matches
                preview_cards = [follower.hand.cards[i] for i in indices]
                if not self.validate_suit_pattern(leader_cards, preview_cards):
                    print(f"Warning: Your selected cards don't match the required pattern: {pattern_type}")
                    confirm = input("Do you still want to play these cards? (y/n): ").lower()
                    if confirm != 'y':
                        continue
                
                break
            except ValueError:
                print("Error: Invalid input. Please enter numeric values.")
        
        # Get the selected cards
        selected_cards = [follower.hand.cards[i] for i in sorted(indices, reverse=True)]
        
        # Display selected cards
        print("\nYou selected:")
        follower_displays = [ASCIICard.get_card_ascii(card) for card in selected_cards]
        for line_idx in range(3):
            line = "    "
            for card_display in follower_displays:
                line += card_display[line_idx] + " "
            print(line)
        
        # Remove the cards from hand
        for i in sorted(indices, reverse=True):
            del follower.hand.cards[i]
        
        self.current_trick['follower'] = follower
        self.current_trick['follower_cards'] = selected_cards
        
        animate_text(f"\n{follower.username} played two cards.")
        time.sleep(1)
        return True

    def validate_suit_pattern(self, leader_cards, follower_cards):
        """
        Validates if the follower's cards match the leader's suit pattern.
        Returns True if valid, False otherwise.
        """
        leader_suit1, leader_suit2 = leader_cards[0].suit, leader_cards[1].suit
        follower_suit1, follower_suit2 = follower_cards[0].suit, follower_cards[1].suit

        # Check for flush (same suit)
        if leader_suit1 == leader_suit2:
            return follower_suit1 == follower_suit2 and follower_suit1 == leader_suit1

        # Check for color (same color, different suits)
        leader_color1 = "red" if leader_suit1 in ["Hearts", "Diamonds"] else "black"
        leader_color2 = "red" if leader_suit2 in ["Hearts", "Diamonds"] else "black"
        follower_color1 = "red" if follower_suit1 in ["Hearts", "Diamonds"] else "black"
        follower_color2 = "red" if follower_suit2 in ["Hearts", "Diamonds"] else "black"

        if leader_color1 == leader_color2:
            return (follower_color1 == follower_color2 and
                    follower_color1 == leader_color1 and
                    follower_suit1 != follower_suit2)

        # Check for mix (different colors)
        return (follower_color1 != follower_color2)

    def evaluate_trick(self):
        """Enhanced trick evaluation with visual display"""
        if not self.current_trick.get('leader') or not self.current_trick.get('follower'):
            print("Error: Incomplete trick data.")
            return

        clear_screen()
        print_header("Trick Evaluation")
        
        declaration = self.current_trick.get('declaration')
        leader = self.current_trick.get('leader')
        follower = self.current_trick.get('follower')
        leader_cards = self.current_trick.get('leader_cards')
        follower_cards = self.current_trick.get('follower_cards')
        
        # Display both players' cards
        ASCIICard.display_trick(leader_cards, follower_cards, 
                              leader.username, follower.username, declaration)
        
        print(f"\nDeclaration: {declaration.upper()}")
        
        # Validate suit pattern
        if not self.validate_suit_pattern(leader_cards, follower_cards):
            animate_text(f"\n{follower.username} failed to match the suit pattern.")
            winner = leader
        else:
            # Evaluate based on declaration
            animate_text("\nSuit pattern matched correctly. Evaluating based on declaration...")
            time.sleep(1)
            
            if declaration == 'high':
                leader_value = RANK_VALUES.get(leader_cards[0].rank, 0)
                follower_value = RANK_VALUES.get(follower_cards[0].rank, 0)
                
                print(f"\nComparing highest cards: {leader_cards[0]} vs {follower_cards[0]}")
                
                if leader_value > follower_value:
                    winner = leader
                    print(f"{leader.username}'s card is higher")
                elif leader_value < follower_value:
                    winner = follower
                    print(f"{follower.username}'s card is higher")
                else:
                    print("Highest cards are tied! Comparing second cards...")
                    leader_value = RANK_VALUES.get(leader_cards[1].rank, 0)
                    follower_value = RANK_VALUES.get(follower_cards[1].rank, 0)
                    print(f"Comparing second cards: {leader_cards[1]} vs {follower_cards[1]}")
                    
                    winner = leader if leader_value >= follower_value else follower
                    print(f"{winner.username}'s second card is {'higher or equal' if winner == leader else 'higher'}")
            elif declaration == 'low':
                leader_value = RANK_VALUES.get(leader_cards[1].rank, 0)
                follower_value = RANK_VALUES.get(follower_cards[1].rank, 0)
                
                print(f"\nComparing lowest cards: {leader_cards[1]} vs {follower_cards[1]}")
                
                if leader_value < follower_value:
                    winner = leader
                    print(f"{leader.username}'s card is lower")
                elif leader_value > follower_value:
                    winner = follower
                    print(f"{follower.username}'s card is lower")
                else:
                    print("Lowest cards are tied! Comparing second cards...")
                    leader_value = RANK_VALUES.get(leader_cards[0].rank, 0)
                    follower_value = RANK_VALUES.get(follower_cards[0].rank, 0)
                    print(f"Comparing second cards: {leader_cards[0]} vs {follower_cards[0]}")
                    
                    winner = leader if leader_value <= follower_value else follower
                    print(f"{winner.username}'s second card is {'lower or equal' if winner == leader else 'lower'}")
            else:
                print("Error: Unknown declaration.")
                return

        # Announce winner with animation
        print("\n" + "-" * 40)
        animate_text(f"Result: {winner.username} wins the trick!", delay=0.01)
        print("-" * 40)
        
        # Add to trick history
        self.played_tricks.append({
            'leader': leader.username,
            'follower': follower.username,
            'declaration': declaration,
            'winner': winner.username,
            'leader_cards': [str(card) for card in leader_cards],
            'follower_cards': [str(card) for card in follower_cards]
        })
        
        # Store the winner before clearing the trick data
        next_leader = winner
        self.current_trick.clear()  # Clear the trick data
        self.current_trick['leader'] = next_leader  # Set the winner as the leader for the next trick

    def replenish_hands(self):
        """Enhanced visual representation of drawing cards from the stock"""
        print_subheader("Replenishing Hands")
        
        for player in [self.player1, self.player2]:
            if player.is_active:
                cards_to_draw = min(2, len(self.can.cards))
                if cards_to_draw > 0:
                    animate_text(f"{player.username} draws {cards_to_draw} card(s) from the stock...", delay=0.01)
                    
                    drawn_cards = []
                    for _ in range(cards_to_draw):
                        card = self.can.cards.pop()
                        player.hand.add_card(card)
                        drawn_cards.append(card)
                    
                    # Display drawn cards
                    drawn_displays = [ASCIICard.get_card_ascii(card) for card in drawn_cards]
                    for line_idx in range(3):
                        line = "    "
                        for card_display in drawn_displays:
                            line += card_display[line_idx] + " "
                        print(line)
                else:
                    print(f"No more cards in stock for {player.username} to draw!")
        
        # Show updated card counts
        print(f"\nUpdated hand sizes:")
        print(f"{self.player1.username}: {len(self.player1.hand)} cards")
        print(f"{self.player2.username}: {len(self.player2.hand)} cards")
        print(f"Stock: {len(self.can.cards)} cards")
        
        # Set next trick leader
        if 'leader' in self.current_trick:
            animate_text(f"\n{self.current_trick['leader'].username} will lead the next trick.")
        else:
            print("Error: No leader set for the next trick.")

    def play_trick(self):
        """Coordinates the leader's and follower's moves with improved visuals"""
        if not self.leader_move():
            input("\nPress Enter to continue...")
            return
        if not self.follower_move():
            input("\nPress Enter to continue...")
            return
        self.evaluate_trick()
        input("\nPress Enter to continue to card replenishment...")
        self.replenish_hands()
        input("\nPress Enter to continue...")

    def claim_victory(self, player):
        """Enhanced victory claim with visual feedback"""
        animate_text(f"Checking if {player.username} has enough cards for victory...", delay=0.01)
        time.sleep(1)
        
        if len(player.hand) >= self.victory_threshold:
            print_header(f"{player.username} CLAIMS VICTORY!")
            print(f"\n{player.username} has {len(player.hand)} cards, which is at least {self.victory_threshold}!")
            animate_text("\nVictory claim is valid!", delay=0.01)
            return True
        else:
            print(f"\n{player.username} has only {len(player.hand)} cards, " 
                 f"which is less than the required {self.victory_threshold}.")
            animate_text("Victory claim is invalid!", delay=0.01)
            return False

    def challenge_victory(self, challenger):
        """Enhanced victory challenge with visual feedback"""
        animate_text(f"Checking if {challenger.username} has enough cards to challenge...", delay=0.01)
        time.sleep(1)
        
        if len(challenger.hand) >= self.victory_threshold:
            print_header(f"{challenger.username} SUCCESSFULLY CHALLENGES!")
            print(f"\n{challenger.username} has {len(challenger.hand)} cards, which is at least {self.victory_threshold}!")
            animate_text("\nChallenge is successful! The challenger wins!", delay=0.01)
            return True
        else:
            print(f"\n{challenger.username} has only {len(challenger.hand)} cards, " 
                 f"which is less than the required {self.victory_threshold}.")
            animate_text("Challenge fails! The original claimant wins!", delay=0.01)
            return False
