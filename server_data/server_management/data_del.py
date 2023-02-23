import json
import subprocess
import sys
import logging

from modules import json_parser
import server_management.data_add as data_add

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def remove_server_by_index(file_path, index):
    server_info = json_parser.read_json_file(file_path)

    server_to_remove = server_info.pop(list(server_info.keys())[index - 1])

    json_parser.write_json_file(file_path, server_info)

    return server_to_remove

def del_server_info():
    # Set the path for the server info JSON file
    file_path = "server_data\server_info.json"
    try:
        # Check JSON format
        json_parser.check_json_file(file_path)

        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
        logging.info("Delete Server Info function called")

        with open("server_data/server_info.json", "r") as file:
            server_info = json.load(file)

        # Print all servers and their info
        print("\nServers\n")
        if server_info == {}:
            while True:
                print("No servers added!\nAdd servers by typing 'a' or 'q' to go back!\n\n")
                response = input("What would you like to do? (a/q):")
                if response == 'a':
                    data_add.prompt_add()
                elif response == 'q':
                    return
                else:
                    print("Invalide Response")

        for i, server_id in enumerate(server_info, start=1):
            server = server_info[server_id]
            if all(key in server for key in ["IP", "Port", "Game", "Server Name"]):
                print(f"{i}) {server['IP']}:{server['Port']} | {server['Game']} | {server['Server Name']}")
            else:
                print(f"{i}) Server information missing")

        print("\n\nType 'q' to go back")

        # Get the user's choice and remove the server if the input is valid
        choice = input("Enter server index to remove: ")
        if choice.lower() == 'q':
            pass
        else:
            choice = int(choice)
            if choice > len(server_info) or choice < 1:
                print("Invalid option, try again.")
            else:
                remove_server_by_index(file_path, choice)
                print("Server removed successfully")
                logging.info("Server removed successfully")
                del_server_info()

    except Exception as e:
        logging.exception(f"Error in Delete Server Info function: {e}")
        print("An error occurred. Please check the logs for more information.")