import subprocess
import sys
import os
import json
import time
import msvcrt
import logging
import data_add
import data_del
import data_edit

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def display_menu():
    # Initialize variables
    choice = ''
    start_time = time.time()
    
    # Loop until a valid input is received or the timeout is reached
    while True:
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
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
                    display_menu()
                    logging.error("Invalid user input received: %s", user_input)
                
                # Check if input is valid, if not display error message and restart loop
                while choice not in [0, 1, 2, 3, 4]:
                    print("Invalid choice. Try again.")
                    choice = int(input("Input: "))
                    display_menu()
                    logging.error("Invalid user input received: %s", user_input)
                
                # Process user input
                if choice == 1:
                    data_add.prompt_add()
                    display_menu()
                    logging.info("User chose to add a server")
                elif choice == 2:
                    data_del.del_server_info()
                    display_menu()
                    logging.info("User chose to delete a server")
                elif choice == 3:
                    data_edit.prompt_edit()
                    display_menu()
                    logging.info("User chose to edit a server")
                    pass
                elif choice == 4:
                    # Edit server function
                    pass
                break
        # Check if timeout is reached
        elif elapsed_time > 10.0:
            # Timeout reached, automatically skip
            break
        else:
            # Clear screen and display menu
            subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
            print(" _________________________________________ ")
            print("|             SERVER MANAGER              |")
            print("| 1) Add Server                           |")
            print("| 2) Delete Server                        |")
            print("| 3) Edit Server                          |")
            print("| 0) Skip                                 |")
            print("|_________________________________________|")
            print("|_________ Skipping in {:.0f} seconds _________|".format(10.0 - elapsed_time))
            
            # Wait for a short amount of time before clearing the screen and showing the menu again
            time.sleep(0.5)
            
            # Log the display menu operation
            logging.info("Displaying server manager menu")
            

# clear the console screen
subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)

# specify the path to the server_info.json file
filename = "data_management\server_info.json"

# Create the file if it doesn't exist
if not os.path.exists(filename):
    print("Server Info doesn't exist! Creating now!")
    logging.warning("Server Info doesn't exist. Creating now.")
    with open(filename, "w") as f:
        f.write("{}")

# Load the contents of the server_info.json file into memory
with open(filename, "r") as f:
    data = json.load(f)

    # If the file is empty, ask the user if they want to add data
    if not data:
        response = input("Server info file is empty. Do you want to add data? \nYou can always add data later! (y/n): ")
        logging.info("Empty server info file, asking user if they want to add data")
    
        # Ensure that the user inputs 'y' or 'n'
        while response.lower() not in ["y", "n"]:
            response = input("Invalid input.\nServer info file is empty. Do you want to add data? \nYou can always add data later! (y/n): ")
            logging.warning("Invalid input for server info file")
    
        # If the user chooses to add data, prompt them to do so and display the menu
        if response.lower() == 'y':
            data_add.prompt_add()
            subprocess.call(["python", "data_management\data_add.py"])
            display_menu()
            logging.info("User chose to add data, displaying menu")
    
        # If the user chooses not to add data, display the menu
        else:
            display_menu()
            logging.info("User chose not to add data, displaying menu")
    
    # If the file is not empty, display the menu
    else:
        display_menu()
        logging.info("Non-empty server info file, displaying menu")