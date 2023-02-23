import json
import uuid
import sys
import subprocess
import logging

import search.check_api as check_api
import server_customization.embed_customization as embed_customization
import server_customization.graph_customization as graph_customization
from modules import json_parser

def prompt_for_input(prompt_message, required=False):
    while True:
        user_input = input(prompt_message + ": ")
        if user_input:
            return user_input
        elif not required:
            return None
        else:
            print("Invalid input. Please try again.")

def prompt_add():
    # Set the path for the server info JSON file
    file_path = "server_data\server_info.json"

    # Check JSON format
    json_parser.check_json_file(file_path)

    # Clear the console screen
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)

    # Display a prompt to add server information
    print(" _______________________________")
    print("|        Add Server Info        |")
    print("|_______________________________|\n\n")

    logging.info("Prompting user to add server information")

    # Read the server info from the JSON file, or create an empty dictionary if the file is empty or doesn't exist
    server_info = {}
    try:
        server_info = json_parser.read_json_file(file_path)
    except json.JSONDecodeError:
        server_info = {}

    # Initialize a new server dictionary with a random UUID as the ID
    new_server = {}
    new_server["ID"] = str(uuid.uuid4())
    print(f"Server UUID: {new_server['ID']}")
    logging.info(f"Created new server with ID: {new_server['ID']}")

    # Prompt the user to enter the server IP address, port, and query port
    fields = {
        "IP": {"message": "Enter server IP Address", "required": True},
        "Port": {"message": "Enter server Port", "required": True},
        "Query Port": {"message": "Enter server Query Port", "required": True},
        "Server Name": {"message": "Enter server name (optional, but recommended)"},
        "Guild ID": {"message": "Enter your Discord Guild (Server) ID", "required": True},
        "Channel ID": {"message": "Enter the Discord Channel ID that you want to send server info to", "required": True},
        "Server Location": {"message": "Enter Server Location (example: :flag_us: US) (optional)"}
    }

    for field, data in fields.items():
        while True:
            prompt_message = data["message"]
            required = data.get("required", False)
            user_input = prompt_for_input(prompt_message, required=required)
            if user_input:
                new_server[field] = user_input
                break
            elif not required:
                break

    game = check_api.search()
    new_server["Game"] = game[0]
    new_server["Query API"] = game[1]
    new_server["Message ID"] = ''

    new_server["ID"] = str(uuid.uuid4())
    print(f"Server UUID: {new_server['ID']}")
    logging.info(f"Created new server with ID: {new_server['ID']}")
    new_server["Embed"] = {}
    new_server["Graph"] = {}
    new_server["Player Count"] = [0 for i in range(288 * 7)]
    server_info[new_server["ID"]] = new_server

    # Write the new server information to the JSON file
    json_parser.write_json_file(file_path, server_info)
    logging.info(f"Server info has been added: {server_info[new_server['ID']]}")
    
    print("Server info has been added.")
    logging.info(f"Added server: {server_info[new_server['ID']]}")

    answer = prompt_for_input("Do you want to customize the server embed? (y/n)")
    while answer.lower() not in ["y", "n"]:
        answer = prompt_for_input("Invalid input. Please try again.\nDo you want to customize the server embed? (y/n)")
    if answer.lower() == 'y':
        embed_customization.customize_title(server_info, new_server['ID'], file_path)

    answer = prompt_for_input("Do you want to customize the server embed graph? (y/n)")
    while answer.lower() not in ["y", "n"]:
        answer = prompt_for_input("Invalid input. Please try again.\nDo you want to customize the server embed graph? (y/n)")
    if answer.lower() == 'y':
        graph_customization.prompt_graph_customization(new_server['ID'])

    answer = prompt_for_input("Do you want to add another server? (y/n)")
    while answer.lower() not in ["y", "n"]:
        answer = prompt_for_input("Invalid input. Please try again.\nDo you want to add another server? (y/n)")
    if answer.lower() == "y":
        prompt_add()
    else:
        return