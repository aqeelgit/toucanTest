from game import Game
from menu import display_menu, handle_menu_choice

def main():
    game = Game()
    print("=== Welcome to Toucan Card Game ===")
    
    game_running = True
    while game_running:
        choice = display_menu(game)
        game_running = handle_menu_choice(game, choice)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred:", e)