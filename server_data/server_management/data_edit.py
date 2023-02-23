import subprocess
import sys
import logging

import server_customization.embed_customization as embed_customization
import server_customization.graph_customization as graph_customization
from modules import json_parser

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def display_server_info(server_info, file_path):
    try:
        for i, server in enumerate(server_info.values(), start=1):
            if all(key in server for key in ["IP", "Port", "Server Name"]):
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

        json_parser.write_json_file(file_path, server_info)
        logging.info("Formatted server_info.json and wrote to file")


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
    server_info = json_parser.read_json_file(file_path)

    # Get the server by index
    server = get_server_by_index(server_info, index)
    if server is None:
        logging.warning(f"Server with index {index} does not exist")
        return None
    server_id, server = server

    # If key is 13 (i.e., Embed), run customize_title function from server_embed_customization.py and break
    if key == 13:
        embed_customization.customize_title(server_info, server_id, file_path)
        return

    # If key is 14 (i.e., Graph), run prompt_graph_customization function from server_graph_customization.py and break
    if key == 14:
        graph_customization.prompt_graph_customization(server_id)
        return

    # Otherwise, update the key/value pair
    server_key = list(server.keys())[int(key)]
    if server_key in server:
        server[server_key] = value
        logging.info(f"Server {server_id} updated key {server_key} to {value}")
    else:
        logging.warning(f"Server {server_id} does not have a key named {server_key}")

    # Update the server in the server_info dictionary
    server_info[server_id] = server

    # Write the updated server_info to file
    json_parser.write_json_file(file_path, server_info)
    return server_info
    
def prompt_edit():
    file_path = "server_data\server_info.json"

    server_info = json_parser.read_json_file(file_path)

    while True:
        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
        logging.info('Edit server info prompt cleared')
        print(" _______________________________")
        print("|        Edit Server Info       |")
        print("|_______________________________|\n\n")
        display_server_info(server_info, file_path)
        print("\n\nType 'q' to go back")
        choice = input("Enter the number of the server you want to edit: ")
        if choice == 'q':
            break
        try:
            choice = int(choice)
            if choice > len(server_info) or choice < 1:
                print("Invalid input, try again.")
                continue

            server_id, server = get_server_by_index(server_info, choice)

            if server is None:
                continue

            display_edit_options(server)

            key = input("Enter the key you want to edit: ")
            edited_server = edit_server(server_info, server_id, key, file_path)

            if edited_server is not None:
                print("Server edited successfully")

        except ValueError:
            print("Invalid input, try again.")
            continue

def display_edit_options(server):
    allowed_keys = ["IP", "Port", "Query Port", "Server Name", "Guild ID", "Channel ID", "Server Location", "Embed", "Graph"]

    print("\nCurrent server information:")
    for i, (key, value) in enumerate(server.items()):
        if key not in allowed_keys:
            if key == "Player Count":
                print(f"X) {key}: []")
            else:
                print(f"X) {key}: {value}")
        elif key == "Embed":
            print(f"{i+1}) Embed")
        elif key == "Graph":
            print(f"{i+1}) Graph")
        else:
            print(f"{i+1}) {key}: {value}")

def edit_server(server_info, server_id, key, file_path):
    allowed_keys = ["IP", "Port", "Query Port", "Server Name", "Guild ID", "Channel ID", "Server Location", "Embed", "Graph"]

    index = int(key) - 1
    if list(server_info[server_id].keys())[index] not in allowed_keys:
        print("Error: Key not allowed for editing. Allowed keys:", allowed_keys)
        return None

    if list(server_info[server_id].keys())[index] == "Embed":
        embed_customization.customize_title(server_info, server_id, file_path)
        return None

    if list(server_info[server_id].keys())[index] == "Graph":
        graph_customization.prompt_graph_customization(server_id)
        return None

    value = input(f"Enter the new value for the {list(server_info[server_id].keys())[index]}: ")

    server_info[server_id][list(server_info[server_id].keys())[index]] = value
    json_parser.write_json_file(file_path, server_info)
    return server_info

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