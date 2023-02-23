from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import logging

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

# A dictionary of game names and their corresponding query APIs
# I've added all A2S, minecraft (java & bedrock), and fivem servers from this repo:
# https://github.com/Austinb/GameQ/wiki/Supported-servers-list-v3
# These are using pretty much the same API's that this bot is using so everything there, should work here.

games = {
    "7 Days to Die": "Valve",
    "Age of Chivalry": "Valve",
    "Alien Swarm": "Valve",
    "America's Army 3": "Valve",
    "America's Army: Proving Grounds": "Valve",
    "ARK: Survival Evolved": "Valve",
    "Armed Assualt 2: Operation Arrowhead": "Valve",
    "Armed Assault 2: DayZ Mod": "Valve",
    "Armed Assualt 3": "Valve",
    "Battalion 1944": "Valve",
    "Brink": "Valve",
    "Call of Duty: Modern Warfare 3": "Valve",
    "Conan Exiles": "Valve",
    "Conter-Strike 1.5": "Valve",
    "Counter Strike 1.6": "Valve",
    "Counter-Strike 2D": "Valve",
    "Counter-Strike: Condition Zero": "Valve",
    "Counter-Strike: Global Offense": "Valve",
    "Counter-Strike: Source": "Valve",
    "Dark and Light": "Valve",
    "DayZ Standalone": "Valve",
    "Day of Defeat": "Valve",
    "Day of Defeat: Source": "Valve",
    "Days of War": "Valve",
    "Empyrion - Galactic Survival": "Valve",
    "Fortress Forever": "Valve",
    "Garry's Mod": "Valve",
    "GRAV Online": "Valve",
    "Grand Theft Auto V (FiveM)": "FiveM",
    "Grand Theft Auto San Andreas (SAMP)": "SAMP",
    "Half-Life: Deathmatch": "Valve",
    "Half-Life 2: Deathmatch": "Valve",
    "Half Life 2: Synergy Mod": "Valve",
    "Homefront": "Valve",
    "Insurgency": "Valve",
    "Just Cause 2 Multiplayer": "Valve",
    "Killing Floor 2": "Valve",
    "Left 4 Dead": "Valve",
    "Left 4 Dead 2": "Valve",
    "Minecraft (Java)": "Minecraft.Java",
    "Minecraft (Bedrock)": "Minecraft.Bedrock",
    "Natural Selection": "Valve",
    "Natural Selection 2": "Valve",
    "PixARK": "Valve",
    "Quake Live": "Valve",
    "Red Dead Redemption 2 (RedM)": "FiveM",
    "Red Orchestra 2: Heroes of Stalingrad": "Valve",
    "Rising Storm": "Valve",
    "Rust": "Valve",
    "Shattered Horizon": "Valve",
    "Starbound": "Valve",
    "Space Engineers": "Valve",
    "Squad": "Valve",
    "Team Fortress Classic": "Valve",
    "Team Fortress 2": "Valve",
    "The Forest": "Valve",
    "The Ship": "Valve",
    "Unturned": "Valve",
    "Wurm Unlimited": "Valve",
    "Zombie Master": "Valve",
    "Zombie Panic: Source": "Valve",
}

# A function to search for games based on a query string
# Uses fuzzy matching to return a list of possible matches
def search_game(game_name):
    logging.info(f'Searching for: {game_name}')
    results = process.extract(game_name, games.keys(), limit=8, scorer=fuzz.token_set_ratio)
    matches = [(match[0], games[match[0]]) for match in results]
    logging.info(f'Found {len(matches)} possible results: {matches}')
    return matches

# A function to prompt the user to search for a game
# Returns the selected game and its corresponding query API
def search():
    logging.info("Starting game search function")
    while True:
        while True:
            search_query = input("Enter the Server Game: ")
            if search_query:
                break
        search_query = search_query.lower()
        search_results = search_game(search_query)
        if not search_results:
            print("No matches found, retrying search...")
            continue
        for i, game in enumerate(search_results, start=1):
            print(f"({i}) {game[0]}")
        print(f"\n({len(search_results) + 1}) Retry search")
        while True:
            try:
                choice = int(input("Input: "))
                if choice == len(search_results) + 1:
                    continue
                selected_game = search_results[choice - 1]
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except IndexError:
                print("The number you have entered exceeds the maximum allowed value. Please try again with a smaller number.")
            except Exception as e:
                logging.error(f"Error selecting game: {e}")
                print("Something fucked up...\nand it wasn't me this time...\nwho am I kidding, I put this thing together with duct tape, im surprised it's still standing\n\nSubmit this as an issue on my github.\nhttps://github.com/ihasTaco/RP-Discord-Server-Status\nError:", e)
        logging.info(f"Selected Game: {selected_game[0]}\nQuery API: {selected_game[1]}")
        print(f"Selected Game: {selected_game[0]}\nQuery API: {selected_game[1]}")
        break
    
    return selected_game