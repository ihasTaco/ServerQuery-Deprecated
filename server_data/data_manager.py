import subprocess
import sys
import os
import json
import time
import msvcrt
import logging

# Get the absolute path to the ServerQuery directory
serverquery_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the ServerQuery directory to the Python module search path
sys.path.append(serverquery_dir)

from modules import json_parser
import server_management.data_add as data_add
import server_management.data_del as data_del
import server_management.data_edit as data_edit
import server_customization.manage_customizations as manage_customizations

logging.basicConfig(file_path='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def display_menu(elapsed_time):
    print(" _________________________________________ ")
    print("|             SERVER MANAGER              |")
    print("| 1) Add Server                           |")
    print("| 2) Edit Server                          |")
    print("| 3) Delete Server                        |")
    print("| 4) Export Server Customization          |")
    print("| 0) Skip                                 |")
    print("|_________________________________________|")
    print("|_________ Skipping in {:.0f} seconds _________|".format(10.0 - elapsed_time))


def manage_servers():
    start_time = time.time()

    while True:
        # Clear screen and display menu
        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Check if timeout is reached
        if elapsed_time > 10.0:
            break

        # Display the menu
        display_menu(elapsed_time)

        # Wait for a short amount of time before clearing the screen and showing the menu again
        time.sleep(0.5)

        # Check if user input is received
        if msvcrt.kbhit():
            # Get user input
            user_input = sys.stdin.readline().strip()

            # Validate input
            if user_input:
                try:
                    choice = int(user_input)
                except ValueError:
                    # Invalid input, display error message and restart loop
                    print("Invalid choice. Try again.")
                    logging.error("Invalid user input received: %s", user_input)
                    continue

                # Check if input is valid
                if choice not in [0, 1, 2, 3, 4]:
                    print("Invalid choice. Try again.")
                    logging.error("Invalid user input received: %s", user_input)
                    continue

                # Process user input
                if choice == 0:
                    break
                elif choice == 1:
                    data_add.prompt_add()
                    logging.info("User chose to add a server")
                    manage_servers()
                elif choice == 2:
                    data_edit.prompt_edit()
                    logging.info("User chose to edit a server")
                    manage_servers()
                elif choice == 3:
                    data_del.del_server_info()
                    logging.info("User chose to delete a server")
                    manage_servers()
                elif choice == 4:
                    manage_customizations.prompt_export()
                    logging.info("User chose to export a server")
                    manage_servers()

        # clear the console screen
        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)

    # Log the display menu operation
    logging.info("Displaying server manager menu")

# Specify the path to the server_info.json file
file_path = "server_data/server_info.json"

# Create the file if it doesn't exist
if not os.path.exists(file_path):
    print("Server info file does not exist. Creating now.")
    logging.warning("Server info file does not exist. Creating now.")
    json_parser.write_json_file(file_path, {})

# Load the contents of the server_info.json file into memory
with open(file_path, "r") as f:
    data = json.load(f)
    # If the file is empty, prompt the user to add data
    if data == {}:
        print("Server info file is empty.")
        response = ""
        while response.lower() not in ["y", "n"]:
            response = input("Do you want to add data? (y/n): ").strip()
            if response.lower() not in ["y", "n"]:
                print("Invalid input. Please enter 'y' or 'n'.")
                logging.warning("Invalid input for server info file")
            if response.lower() == "y":
                data_add.prompt_add()
                print("Data added successfully.")
                logging.info("User added data to server info file.")
                manage_servers()
            else:
                print("You can always add data later.")
                logging.info("User chose not to add data to server info file.")
                manage_servers()
    # If the file is not empty, display the menu
    else:
        manage_servers()
        logging.info("Server info file is not empty. Displaying menu.")