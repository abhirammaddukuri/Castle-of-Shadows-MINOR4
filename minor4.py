import random
import json

# Initial Game State
player_stats = {
    'health': 100,
    'strength': 10,
    'intelligence': 8,
    'dexterity': 8,
    'charisma': 8,
    'wealth': 50,
    'experience': 0
}

inventory = {
    'items': {
        'torch': {
            'description': 'A lit torch to see in the dark.',
            'usable': True
        }
    },
    'gold': 50
}

knowledge = {
    'castle_layout': False,
    'book_of_secrets': False
}

game_world = {
    'village_status': 'peaceful',
    'npc_reputation': {}
}

# Game Functions

def intro():
    print("Welcome to the Advanced Adventure Game!")
    print("You find yourself in a dark forest, on the outskirts of an ancient castle.")
    create_character()
    main_hall()

def create_character():
    print("\nCharacter Creation:")
    name = input("Enter your character's name: ").strip()
    print(f"Hello, {name}. Choose your background:")
    background = input("Options: Noble, Thief, Scholar: ").strip().lower()
    
    if background == 'noble':
        player_stats['charisma'] = 15
        player_stats['wealth'] = 100
    elif background == 'thief':
        player_stats['dexterity'] = 15
        player_stats['wealth'] = 20
    elif background == 'scholar':
        player_stats['intelligence'] = 15
        player_stats['wealth'] = 50
    else:
        print("Invalid choice, defaulting to Scholar.")
        player_stats['intelligence'] = 15
        player_stats['wealth'] = 50
    
    print(f"{name}, you have chosen the path of a {background.capitalize()}.")

def main_hall():
    print("\nYou are in the main hall of a dark, abandoned castle.")
    print("There are three doors: left, right, and straight ahead.")
    choice = input("Which door do you choose? (left/right/straight) ").strip().lower()
    
    if choice == 'left':
        library()
    elif choice == 'right':
        armory()
    elif choice == 'straight':
        throne_room()
    else:
        print("Invalid choice, try again.")
        main_hall()

def library():
    print("\nYou enter a dusty old library filled with ancient books.")
    if not knowledge['book_of_secrets']:
        print("There is a mysterious book on a pedestal in the center of the room.")
        choice = input("Do you take the book? (yes/no) ").strip().lower()
        
        if choice == 'yes':
            print("The book glows and disappears! You've gained knowledge of the castle's secrets.")
            knowledge['book_of_secrets'] = True
        elif choice == 'no':
            print("You leave the book and exit the library.")
        else:
            print("Invalid choice, try again.")
            library()
    else:
        print("You have already explored this room.")
    
    main_hall()

def armory():
    print("\nYou enter the armory. Weapons and armor line the walls.")
    if 'sword' not in inventory['items']:
        print("A sword catches your eye.")
        choice = input("Do you take the sword? (yes/no) ").strip().lower()
        
        if choice == 'yes':
            print("You take the sword. It feels balanced and strong.")
            inventory['items']['sword'] = {
                'description': 'A sharp steel sword, perfect for combat.',
                'usable': True
            }
        elif choice == 'no':
            print("You leave the sword and exit the armory.")
        else:
            print("Invalid choice, try again.")
            armory()
    else:
        print("You have already taken the sword.")
    
    main_hall()

def throne_room():
    print("\nYou enter the grand throne room. An imposing figure sits on the throne.")
    print("It's the Dark King, and he doesn't look pleased to see you.")
    choice = input("Do you fight the Dark King or try to talk to him? (fight/talk) ").strip().lower()
    
    if choice == 'fight':
        combat({'name': 'Dark King', 'health': 100, 'strength': 20})
    elif choice == 'talk':
        if knowledge['book_of_secrets']:
            print("Using the knowledge from the book, you negotiate with the Dark King.")
            print("He reveals his tragic backstory and decides to leave the castle peacefully.")
            print("Congratulations, you've won the game through diplomacy!")
        else:
            print("The Dark King is not interested in talking and attacks you.")
            combat({'name': 'Dark King', 'health': 100, 'strength': 20})
    else:
        print("Invalid choice, try again.")
        throne_room()

def combat(enemy):
    print(f"You encounter a {enemy['name']}!")
    while player_stats['health'] > 0 and enemy['health'] > 0:
        print(f"Player Health: {player_stats['health']}, {enemy['name']} Health: {enemy['health']}")
        action = input("Choose your action (attack/defend/use item): ").strip().lower()
        if action == 'attack':
            damage = player_stats['strength']
            enemy['health'] -= damage
            print(f"You deal {damage} damage to the {enemy['name']}.")
        elif action == 'defend':
            print("You brace for the enemy's attack.")
            player_stats['health'] += 5  # Reduced damage or heal slightly
        elif action == 'use item':
            item = input("Which item do you want to use? ").strip().lower()
            use_item(item)
        else:
            print("Invalid action, try again.")
        
        if enemy['health'] > 0:
            enemy_attack(enemy)
        else:
            print(f"You have defeated the {enemy['name']}!")
            if enemy['name'] == 'Dark King':
                print("Congratulations! You have saved the kingdom!")
            break

def enemy_attack(enemy):
    damage = enemy['strength']
    player_stats['health'] -= damage
    print(f"The {enemy['name']} attacks you for {damage} damage.")
    if player_stats['health'] <= 0:
        print("You have been defeated. Game Over.")

def use_item(item_name):
    if item_name in inventory['items'] and inventory['items'][item_name]['usable']:
        print(f"You use the {item_name}.")
        if item_name == 'torch':
            print("You use the torch to light up the dark room.")
        elif item_name == 'potion':
            player_stats['health'] += 20
            print("You drink a health potion and restore 20 health.")
            del inventory['items']['potion']
    else:
        print(f"You can't use the {item_name} or it doesn't exist.")

def check_inventory():
    print("Inventory:")
    for item, details in inventory['items'].items():
        print(f"{item.capitalize()}: {details['description']}")
    print(f"Gold: {inventory['gold']}")

def save_game(filename="savegame.json"):
    game_state = {
        'player_stats': player_stats,
        'inventory': inventory,
        'knowledge': knowledge,
        'game_world': game_world
    }
    with open(filename, 'w') as file:
        json.dump(game_state, file)
    print("Game saved successfully.")

def load_game(filename="savegame.json"):
    global player_stats, inventory, knowledge, game_world
    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
            player_stats = game_state['player_stats']
            inventory = game_state['inventory']
            knowledge = game_state['knowledge']
            game_world = game_state['game_world']
            print("Game loaded successfully.")
    except FileNotFoundError:
        print("Save file not found.")

# Start Game
intro()
