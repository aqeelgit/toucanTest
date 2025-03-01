class Card:
    """
    Represents a playing card with a suit and a rank.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

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