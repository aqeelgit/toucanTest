import time
from game import clear_screen, print_header, animate_text, print_subheader

def display_menu(game):
    """
    Displays an improved context-aware menu based on the current game state.
    """
    clear_screen()
    
    # ASCII art title
    print("""
  _______                               ______                 _ 
 |__   __|                             / _____)               | |
    | | ___  _   _  ____ _____ ____   | /      _____ ___  ____| |
    | |/ _ \| | | |/ ___|____ |  _ \  | |     |____ | __)/ ___| |
    | | |_| | |_| ( (___/ ___ | | | | | \_____/ ___ | |  | |__| |
    |_|\___/ \____|\____)_____|_| |_|  \______)_____|_|   \____/
    """)
    
    # Display game status
    print("\n=== GAME STATUS ===")
    if game.player1.is_active or game.player2.is_active:
        print("\n◉ Current Players:")
        if game.player1.is_active:
            print(f"  ▶ Player 1: {game.player1.username} ({len(game.player1.hand)} cards)")
        else:
            print("  ▷ Player 1: Not registered")
            
        if game.player2.is_active:
            print(f"  ▶ Player 2: {game.player2.username} ({len(game.player2.hand)} cards)")
        else:
            print("  ▷ Player 2: Not registered")
            
        if hasattr(game, 'can') and game.can:
            print(f"\n◉ Cards in stock: {len(game.can.cards)}")
    else:
        print("\nNo players registered yet. Start by registering Player 1 and Player 2.")

    # Display current trick leader if applicable
    if hasattr(game, 'current_trick') and game.current_trick and 'leader' in game.current_trick:
        print(f"\n◉ Current trick leader: {game.current_trick['leader'].username}")
        
    # Victory conditions check
    for player in [game.player1, game.player2]:
        if player.is_active and len(player.hand) >= 27:  # Use 27 as per official rules
            print(f"\n⭐ {player.username} has {len(player.hand)} cards and can claim victory! ⭐")

    # Display menu options
    print("\n=== MENU OPTIONS ===")
    
    menu_options = []
    
    # Phase 1: Registration Phase
    if not (game.player1.is_active and game.player2.is_active):
        menu_options.append(("P", "Player Registration", "Register players"))
    
    # Phase 2: Game Setup Phase
    if game.player1.is_active or game.player2.is_active:
        menu_options.append(("N", "New Round", "Create deck, shuffle, and deal cards"))
    
    # Phase 3: Gameplay Phase
    if (game.player1.is_active and game.player2.is_active and 
            hasattr(game, 'can') and game.can and
            len(game.player1.hand) > 1 and len(game.player2.hand) > 1):
        menu_options.append(("T", "Play Trick", "Begin the next trick"))
        
    # Victory Phase
    for player in [game.player1, game.player2]:
        if player.is_active and len(player.hand) >= 27:  # Use 27 for official rules
            menu_options.append(("V", f"Claim Victory ({player.username})", f"{player.username} claims the win"))
            
            # Only show challenge option for the other player
            other_player = game.player2 if player == game.player1 else game.player1
            if other_player.is_active:
                menu_options.append(("C", f"Challenge Victory ({other_player.username})", 
                                   f"{other_player.username} challenges the claim"))
    
    # Always available options
    menu_options.append(("S", "Show Game Status", "Display detailed game state and hands"))
    menu_options.append(("H", "Help & Rules", "Game rules and instructions"))
    menu_options.append(("Q", "Quit Game", "Exit the application"))
    
    # Display formatted menu
    for key, title, description in menu_options:
        print(f"[{key}] {title.ljust(25)} - {description}")
    
    return input("\nSelect an option: ").strip().upper()

def handle_menu_choice(game, choice):
    """
    Handles the menu choice with improved user experience
    """
    if choice == 'P':
        # Player registration submenu
        clear_screen()
        print_header("Player Registration")
        
        reg_options = []
        if not game.player1.is_active:
            reg_options.append(("1", "Register as Player 1"))
        if not game.player2.is_active:
            reg_options.append(("2", "Register as Player 2"))
        reg_options.append(("B", "Back to main menu"))
        
        for key, desc in reg_options:
            print(f"[{key}] {desc}")
        
        reg_choice = input("\nSelect an option: ").strip()
        if reg_choice in ['1', '2']:
            result = game.register_player(reg_choice)
            animate_text(result, delay=0.01)
            input("\nPress Enter to continue...")
        return True
            
    elif choice == 'N':
        clear_screen()
        print_header("Starting New Round")
        animate_text("Initializing new game round...", delay=0.01)
        time.sleep(0.5)
        
        animate_text("Creating deck...", delay=0.01)
        game.create_deck()
        time.sleep(0.5)
        
        animate_text("Shuffling cards...", delay=0.01)
        game.shuffle_deck()
        time.sleep(0.5)
        
        animate_text("Dealing cards to players...", delay=0.01)
        game.deal_cards()
        
        print("\nNew round started successfully! Ready for trick-play phase.")
        input("\nPress Enter to continue...")
        return True
        
    elif choice == 'T':
        game.play_trick()
        return True
        
    elif choice == 'S':
        game.show_status()
        input("\nPress Enter to continue...")
        return True
        
    elif choice == 'V':
        clear_screen()
        print_header("Victory Claim")
        
        # Determine which player can claim victory
        claimant = None
        for player in [game.player1, game.player2]:
            if player.is_active and len(player.hand) >= 27:  # Use 27 for official rules
                claimant = player
                break
                
        if claimant:
            print(f"{claimant.username} is attempting to claim victory with {len(claimant.hand)} cards!")
            time.sleep(1)
            
            if game.claim_victory(claimant):
                animate_text(f"\n🏆 {claimant.username} WINS THE GAME! 🏆", delay=0.01)
                print("\nGame over!")
                input("\nPress Enter to continue...")
                return False  # End the game loop
        else:
            print("Error: No player has enough cards to claim victory (need 27+).")
        
        input("\nPress Enter to continue...")
        return True
        
    elif choice == 'C':
        clear_screen()
        print_header("Victory Challenge")
        
        # Determine which player can challenge
        challenger = None
        claimant = None
        
        for player in [game.player1, game.player2]:
            if player.is_active and len(player.hand) >= 27:  # Use 27 for official rules
                claimant = player
                challenger = game.player2 if player == game.player1 else game.player1
                break
                
        if challenger and claimant:
            print(f"{challenger.username} is challenging {claimant.username}'s victory claim!")
            time.sleep(1)
            
            if game.challenge_victory(challenger):
                animate_text(f"\n🏆 {challenger.username} SUCCESSFULLY CHALLENGED AND WINS THE GAME! 🏆", delay=0.01)
                print("\nGame over!")
                input("\nPress Enter to continue...")
                return False  # End the game loop
        else:
            print("Error: No valid challenger found.")
        
        input("\nPress Enter to continue...")
        return True
        
    elif choice == 'H':
        clear_screen()
        display_help()
        input("\nPress Enter to continue...")
        return True
        
    elif choice == 'Q':
        clear_screen()
        animate_text("Thank you for playing Toucan Card Game! Goodbye.", delay=0.01)
        return False  # End the game loop
        
    else:
        print("Invalid option. Please try again.")
        time.sleep(1)
        return True

def display_help():
    """
    Displays the game rules and help information with improved formatting
    """
    print_header("Toucan Card Game - Help & Rules")
    
    sections = [
        ("Overview", [
            "Toucan is a trick-taking card game for 2 players.",
            "The goal is to collect at least 27 cards in your hand to claim victory."
        ]),
        ("Card Rankings", [
            "Cards are ranked from highest to lowest: K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2, A"
        ]),
        ("Game Flow", [
            "1. Each player is dealt 7 cards initially.",
            "2. Players take turns being the leader and follower in tricks.",
            "3. The leader plays two cards and declares 'High' or 'Low'.",
            "4. The follower must match the leader's suit pattern with two cards:",
            "   - If leader plays two cards of the same suit, follower must do the same",
            "   - If leader plays two cards of the same color (but different suits), follower must do the same",
            "   - If leader plays two cards of different colors, follower must do the same",
            "5. If the follower fails to match the pattern, the leader wins the trick.",
            "6. If the follower matches the pattern, the higher or lower card (based on the declaration) wins.",
            "7. The winner of a trick leads the next trick.",
            "8. After each trick, both players draw cards from the stock to replenish their hands."
        ]),
        ("Winning", [
            "- When a player has at least 27 cards, they can claim victory.",
            "- The opponent can challenge this claim if they also have 27 or more cards."
        ]),
        ("Menu Options", [
            "[P] Player Registration - Register players",
            "[N] New Round - Start a new game round",
            "[T] Play Trick - Play a trick when a round is in progress",
            "[S] Show Status - Display detailed game state",
            "[V] Claim Victory - Claim victory when having enough cards",
            "[C] Challenge Victory - Challenge opponent's victory claim",
            "[H] Help & Rules - Show this help screen",
            "[Q] Quit Game - Exit the game"
        ])
    ]
    
    for title, content in sections:
        print_subheader(title)
        for line in content:
            print(line)
        print()