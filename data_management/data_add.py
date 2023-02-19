import json
import uuid
import sys
import subprocess
import check_api
import logging
import embed_customization
import graph_customization

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

def prompt_add():
    # Check JSON format
    check_json_file()

    # Clear the console screen
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)

    # Display a prompt to add server information
    print(" _______________________________")
    print("|        Add Server Info        |")
    print("|_______________________________|\n\n")

    logging.info("Prompting user to add server information")

    # Set the path for the server info JSON file
    filename = "data_management\server_info.json"

    # Read the server info from the JSON file, or create an empty dictionary if the file is empty or doesn't exist
    server_info = {}
    with open(filename, "r") as f:
        try:
            server_info = json.load(f)
        except json.JSONDecodeError:
            server_info = {}

    # Initialize a new server dictionary with a random UUID as the ID
    new_server = {}
    new_server["ID"] = str(uuid.uuid4())
    print(f"Server UUID: {new_server['ID']}")
    logging.info(f"Created new server with ID: {new_server['ID']}")

    # Prompt the user to enter the server IP address, port, and query port
    while True:
        new_server["IP"] = input("Enter server IP Address: ")
        if new_server["IP"]:
            break
        else:
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print("Creating new server")
            print(f"Server UUID: {new_server['ID']}")

    while True:
        new_server["Port"] = input("Enter server Port: ")
        if new_server["Port"]:
            break
        else:
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print("Creating new server")
            print(f"Server UUID: {new_server['ID']}")
            print(f"Enter server IP Address: {new_server['IP']}")

    while True:
        new_server["Query Port"] = input("Enter server Query Port: ")
        if new_server["Query Port"]:
            break
        else:
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print("Creating new server")
            print(f"Server UUID: {new_server['ID']}")
            print(f"Enter server IP Address: {new_server['IP']}")
            print(f"Enter server Port: {new_server['Port']}")

    results = check_api.search()
    if results:
        new_server["Game"] = results[0]
        new_server["Query API"] = results[1]
    new_server["Server Name"] = input("Enter server name (optional, but recommended): ")
    
    while True:
        new_server["Guild ID"] = input("Enter your Discord Guild (Server) ID: ")
        if new_server["Guild ID"]:
            break
        else:
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print("Creating new server")
            print(f"Server UUID: {new_server['ID']}")
            print(f"Enter server IP Address: {new_server['IP']}")
            print(f"Enter server Port: {new_server['PORT']}")
            print(f"Enter server Query Port: {new_server['Query Port']}")
            print(f"Selected Game: {new_server['Server Name']}")
            print(f"Query API: {new_server['Query API']}")
            print(f"Enter server name (optional): {new_server['Server Name']}")
    
    while True:
        new_server["Channel ID"] = input("Enter the Discord Channel ID that you want to send server info to: ")
        if new_server["Channel ID"]:
            break
        else:
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print("Creating new server")
            print(f"Server UUID: {new_server['ID']}")
            print(f"Enter server IP Address: {new_server['IP']}")
            print(f"Enter server Port: {new_server['PORT']}")
            print(f"Enter server Query Port: {new_server['Query Port']}")
            print(f"Selected Game: {new_server['Server Name']}")
            print(f"Query API: {new_server['Query API']}")
            print(f"Enter server name (optional): {new_server['Server Name']}")
            print(f"Enter your Discord Guild (Server) ID: {new_server['Guild ID']}")
    
    new_server["Message ID"] = "" # This will be set later

    new_server["Server Location"] = input("Enter Server Location (example: :flag_us: US) (optional): ")
    
    new_server["Player Count"] = [0 for i in range(288 * 7)]
    new_server["Embed"] = {}
    new_server["Graph"] = {}
    server_info[new_server["ID"]] = new_server
    
    with open(filename, "w") as f:
        json.dump(server_info, f)
        print(server_info)
        logging.info(f"Server info has been added: {server_info[new_server['ID']]}")
    
    print("Server info has been added.")
    logging.info(f"Added server: {server_info[new_server['ID']]}")

    answer = input("Do you want to customize the server embed? (y/n): ")
    while answer.lower() not in ["y", "n"]:
        answer = input("Invalid input.\nDo you want to customize the server embed? (y/n): ")

    if answer == 'y':
        embed_customization.customize_title(server_info, new_server['ID'], filename)

    answer = input("Do you want to customize the server embed graph? (y/n): ")
    while answer.lower() not in ["y", "n"]:
        answer = input("Invalid input.\nDo you want to customize the server embed graph? (y/n): ")

    if answer == 'y':
        graph_customization.prompt_graph_customization(new_server['ID'])

    answer = input("Do you want to add another server? (y/n): ")
    while answer.lower() not in ["y", "n"]:
        answer = input("Invalid input.\nDo you want to add another server? (y/n): ")
    if answer.lower() == "y":
        prompt_add()
    else:
        return