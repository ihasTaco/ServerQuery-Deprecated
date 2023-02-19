import json
import subprocess
import sys
import logging
import embed_customization
import graph_customization

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def display_server_info(server_info, file_path):
    try:
        for i, server in enumerate(server_info.values(), start=1):
            if "IP" in server and "Port" in server and "Server Name" in server:
                print(f"{i}) {server['IP']}:{server['Port']} | {server['Server Name']}")
            else:
                print(f"{i}) Server information missing")
        return

    except KeyError as e:
        logging.error(f"KeyError in server_info.json: {e}")
        formatted_server_info = {}

        for i, server in enumerate(server_info, start=1):
            formatted_server_info[f"server{i}"] = {"IP": "", "Port": "", "Server Name": ""}
            for key, value in server.items():
                if key in formatted_server_info[f"server{i}"]:
                    formatted_server_info[f"server{i}"][key] = value
            print(f"{i}) {formatted_server_info[f'server{i}']['IP']}:{formatted_server_info[f'server{i}']['Port']} | {formatted_server_info[f'server{i}']['Server Name']}")

        write_server_info_to_file(server_info, file_path)
        logging.info("Formatted server_info.json and wrote to file")

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
    
def read_server_info_from_file(file_path, retries=0):
    server_info = None

    # The script will only try to read the file 3 times, in case of file being missing or permission issues.
    while retries < 3:
        try:
            with open(file_path, "r") as file:
                server_info = json.load(file)
            break
        except FileNotFoundError as e:
            logging.error(f"File 'server_info.json' is missing!: {e}")
            # Instead of trying to create the file, it will just send user back to data_manager which will handle creating and adding info to the file
            subprocess.call(["python", "data_management\data_manager.py"])
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
                break
            retries += 1
    if server_info is None:
        logging.critical("Exiting the program due to repeated permission errors while accessing the file.")
        exit()
    logging.info(f"Successfully read server information from file: {file_path}")
    return server_info

def write_server_info_to_file(server_info, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(server_info, file, indent=4)
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        return None
    logging.info(f"Server info written to file {file_path}")
    return server_info


def get_server_by_index(server_info, index):
    try:
        if index - 1 >= len(server_info):
            error_message = f"Index out of range. There are not that many servers. Index: {index}"
            logging.error(error_message)
            print(error_message)
            return None
        server_id = list(server_info.keys())[index - 1]
        return server_id, server_info[server_id]
    except Exception as e:
        error_message = f"An error occurred while trying to get the server by index. Error message: {str(e)}"
        logging.error(error_message)
        print(error_message)
        return None

def edit_server_by_index(file_path, index, key, value):
    # Read server info from file
    server_info = read_server_info_from_file(file_path, 0)
    # Get the server by index
    server_id, server = get_server_by_index(server_info, index)
    # If server doesn't exist, return None
    if server is None:
        logging.warning(f"Server with index {index} does not exist")
        return None
    # If key is 13 (i.e., Embed), run customize_title function from server_embed_customization.py and break
    if key == 13:
        server_id, server = get_server_by_index(server_info, index)
        embed_customization.customize_title(server_info, server_id, file_path)
    # If key is 14 (i.e., Graph), run customize_title function from server_embed_customization.py and break
    if key == 14:
        server_id, server = get_server_by_index(server_info, index)
        graph_customization.prompt_graph_customization(server_id)
    # Otherwise, update the key/value pair
    else:
        server_key = list(server.keys())[int(key)]
        if server_key in server:
            server[server_key] = value
            logging.info(f"Server {server_id} updated key {server_key} to {value}")
        else:
            logging.warning(f"Server {server_id} does not have a key named {server_key}")
    # Update the server in the server_info dictionary
    server_info[server_id] = server
    # Write the updated server_info to file
    return write_server_info_to_file(server_info, file_path)
    
def prompt_edit():
    file_path = "data_management\server_info.json"

    # Check JSON format
    read_server_info_from_file(file_path)

    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    logging.info('Edit server info prompt cleared')

    print(" _______________________________")
    print("|        Edit Server Info       |")
    print("|_______________________________|\n\n")

    server_info = read_server_info_from_file(file_path, 0)
    display_server_info(server_info, file_path)
    
    while True:
        choice = input("Enter the number of the server you want to edit: ")
        try:
            if choice == 'q':
                break
            # if the user put in a string, it will raise an exception that will be caught below
            choice = int(choice)

            # Check if the user entered a valid index
            if choice > len(server_info) or choice < 1:
                print("Invalid input, try again.")
            else:
                # allowed_keys are the fields that are editable
                allowed_keys = ["IP", "Port", "Query Port", "Server Name", "Guild ID", "Channel ID", "Server Location", "Embed", "Graph"]

                print("\nCurrent server information:")
                current_server = list(server_info.values())[choice - 1]
                
                # Print all keys for the server if they are allowed, they will be displayed like index) key name: value
                # Otherwise the will be displayed like X) key name: value
                for i, (key, value) in enumerate(current_server.items()):
                    if key not in allowed_keys:
                        # If the key is not in allowed_keys, display index (ex. X) ID: "value")
                        if key == "Player Count":
                            print(f"X) {key}: []")
                        else:
                            print(f"X) {key}: {value}")
                    elif key == "Embed":
                        # If the key is "Embed", display index (ex. 13) Embed: "Embed"
                        print(f"{i+1}) Embed")
                    elif key == "Graph":
                        # If the key is "Embed", display index (ex. 13) Embed: "Embed"
                        print(f"{i+1}) Graph")
                    else:
                        # If the key is in allowed_keys, display index (ex. 2) IP: "value")
                        print(f"{i+1}) {key}: {value}")

                while True:
                    try:
                        key = input("\nEnter the key you want to edit: ")

                        # key that aren't in the 'allowed_keys' arent editable
                        if list(current_server.keys())[int(key) - 1] not in allowed_keys:
                            print("Error: Key not allowed for editing. Allowed keys:", allowed_keys)

                        else:
                            print(f"Editing Key: {list(current_server.keys())[int(key) - 1]}")
                            index = int(key) - 1
                            
                            if list(current_server.keys())[int(key) - 1] == "Embed":
                                server_id, server = get_server_by_index(server_info, choice)
                                embed_customization.customize_title(server_info, server_id, file_path)
                                break
                            
                            if list(current_server.keys())[int(key) - 1] == "Graph":
                                server_id, server = get_server_by_index(server_info, choice)
                                graph_customization.prompt_graph_customization(server_id)
                                break
                            
                            # Prompt the user for the new information
                            value = input(f"Enter the new value for the {list(current_server.keys())[int(key) - 1]}: ")
                            
                            edited_server = edit_server_by_index(file_path, choice, index, value)
                            if edited_server is None:
                                return
                            
                            print("\nServer edited successfully")

                            break

                    except Exception as e:
                        print(f"Error: {e}")

                        # Log the error that occurred
                        logging.exception(e)

                        break

        except ValueError:
            print("Invalid input, try again.")
        
        break

    prompt_edit_another_server()

def prompt_edit_another_server():
    while True:
        another_edit = input("Do you want to edit another server? (y/n): ")
        if another_edit == "y":
            prompt_edit()
        elif another_edit == "n":
            print("Returning to main menu.")
            break
        else:
            print("Invalid input, try again.")