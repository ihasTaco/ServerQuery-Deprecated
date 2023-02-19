import json
import subprocess
import sys
import logging

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

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

def check_json_file(retries=0):
    """
    Check the JSON file for proper formatting and loadability.

    The function attempts to read the file up to 3 times in case of file not found or permission errors.
    If a file is found but not loadable, it will attempt to format it.

    Args:
        retries (int): The number of times the function has been called recursively.

    Returns:
        None
    """
    file_path = "data_management\server_info.json"
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

def remove_server_by_index(index):
    """
    Remove a server from the JSON file by index.

    Args:
        index (int): The index of the server to be removed.

    Returns:
        The server that was removed.
    """
    with open("data_management\server_info.json", "r") as file:
        server_info = json.load(file)

    server_to_remove = server_info.pop(list(server_info.keys())[index - 1])
    with open("data_management\server_info.json", "w") as file:
        json.dump(server_info, file, indent=4)
    return server_to_remove

def del_server_info():
    try:
        # Check JSON format
        check_json_file()

        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
        logging.info("Delete Server Info function called")

        with open("data_management\server_info.json", "r") as file:
            server_info = json.load(file)

        # Print all servers and their info
        print("\nServers\n")
        for i, server_id in enumerate(server_info, start=1):
            server = server_info[server_id]
            if "IP" in server and "Port" in server and "Server Name" in server:
                print(f"{i}) {server['IP']}:{server['Port']} | {server['Game']} | {server['Server Name']}")
            else:
                print(f"{i}) Server information missing")

        print("\n\nType 'exit' to go back")

        # Get the user's choice and remove the server if the input is valid
        choice = input("Enter server index to remove: ")
        if choice.lower() == 'exit':
            pass
        else:
            choice = int(choice)
            if choice > len(server_info) or choice < 1:
                print("Invalid option, try again.")
            else:
                remove_server_by_index(choice)
                print("Server removed successfully")
                logging.info("Server removed successfully")
                del_server_info()

    except Exception as e:
        logging.exception(f"Error in Delete Server Info function: {e}")
        print("An error occurred. Please check the logs for more information.")