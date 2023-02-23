import json
import logging

logging.basicConfig(filename='logs/console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

# Function to format an incorrectly formatted JSON file
def format_json_file(file_path):
    retries = 0
    formatted_data = None

    # Retry loading the file a maximum of 3 times in case of file not found or permission errors
    while retries < 3:
        try:
            # Will try to open the the file
            with open(file_path, "r") as file:
                data = file.read()
                # Will try to recorrect the formatting
                formatted_data = json.loads(data)
                logging.info(f"Successfully opened and formatted JSON file {file_path}.")
            break

        except (FileNotFoundError, PermissionError) as e:
            logging.warning(f"Error opening file {file_path}: {e}")
            print(f"Error opening file {file_path}: {e}")
            retries += 1

        except json.JSONDecodeError as e:
            logging.warning(f"Error decoding JSON data in {file_path}: {e}")
            print(f"Error decoding JSON data in {file_path}: {e}")
            formatted_data = None
            retries += 1

        if retries == 3:
            logging.error(f"Failed to open or format JSON file {file_path} after 3 attempts.")

    return formatted_data

def check_json_file(file_path, retries=0):
    logging.info("Checking JSON file")

    # The script will only try to read the file 3 times, in case of file being missing or permission issues.
    while retries < 3:
        try:
            with open(file_path, "r") as file:
                json.load(file)
                logging.info(f"File {file_path} loaded successfully!")
            break

        except FileNotFoundError as e:
            logging.warning(f"File {file_path} is missing!: {e}")
            break

        except PermissionError as e:
            logging.warning(f"Error opening file {file_path}: {e}")
            retries += 1

        except json.JSONDecodeError as e:
            logging.warning(f"Error decoding JSON data in {file_path}: {e}")
            formatted_data = format_json_file(file_path)

            if formatted_data is not None:
                with open(file_path, "w") as file:
                    json.dump(formatted_data, file, indent=4)
                    logging.info(f"Formatted JSON data written to {file_path}")
                break
            retries += 1
    if retries == 3:
        logging.error(f"Failed to open or format JSON file {file_path} after 3 attempts.")

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.exception(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        logging.exception(f"Invalid JSON format: {e}")
    return None

def write_json_file(file_path, data):
    logging.info(f"file path: \n{file_path} data: \n{data}")
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.exception(f"Error while writing JSON file {file_path}: {e}")

def update_server_players(file_path, server_uuid, player_count):
    data = read_json_file(file_path)
    if data:
        server = data[server_uuid]
        player_counts = server["Player Count"]
        player_counts = player_counts[1:] + [player_count]
        server["Player Count"] = player_counts
        write_json_file(file_path, data)
        logging.info(f"Player count for server {server_uuid} updated to {player_count}")

def update_message_id(file_path, server_uuid, message_id):
    data = read_json_file(file_path)

    if data:
        server = data.get(server_uuid, {})
        server["Message ID"] = message_id
        data[server_uuid] = server

        write_json_file(file_path, data)