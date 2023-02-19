import json
import logging

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.exception(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        logging.exception(f"Invalid JSON format: {e}")
    return None

# Write JSON data to the specified file path
def write_json_file(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.exception(f"Error while writing JSON file {file_path}: {e}")

# Update the player count of a server in the JSON file
def update_server_players(file_path, server_uuid, player_count):
    data = load_json_file(file_path)
    if data:
        server = data[server_uuid]
        player_counts = server["Player Count"]
        player_counts = player_counts[1:] + [player_count]
        server["Player Count"] = player_counts
        write_json_file(file_path, data)
        logging.info(f"Player count for server {server_uuid} updated to {player_count}")

# Update the message ID of a server in the JSON file
def update_message_id(file_path, server_uuid, message_id):
    data = load_json_file(file_path)

    data[server_uuid]["Message ID"] = message_id

    write_json_file(file_path, data)