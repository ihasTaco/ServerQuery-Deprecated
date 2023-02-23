import json
import subprocess
import sys
import logging

from modules import json_parser

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def customize_title(server_info, server_id, file_path):
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    server_info[server_id]["Embed"]["Title"] = {}
    # Clear the console screen
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    # Get the title configuration from the server info
    title_config = server_info[server_id]["Embed"].get("Title", {})
    # Set up options for choosing the title type
    options = ["Use Server Title", "Use Config Title", "Use Custom Title"]
    # Get the server name and the config title from the server info
    server_name = server_info[server_id].get("Server Name", None)
    config_title = title_config.get("Config", None)

    # Print the available title options
    print("\nTitle Options:")
    for i, option in enumerate(options):
        if option == "Use Config Title" and server_name == '':
            print(f"{i+1}. {option} (Disabled)")
        else:
            print(f"{i+1}. {option}")

    # Get the user's choice for the title type
    while True:
        choice = input("\nEnter the number of your choice: ")
        try:
            if int(choice) == 2 and server_name == '':
                print("This option is disabled! To enable this option, add a server name!")
            else:
                choice = int(choice) - 1
                if choice < 0 or choice >= len(options):
                    raise ValueError
                break
        except ValueError:
            print("Invalid input. Please try again.")
    logging.info("Title type chosen: %s", options[choice])

    # Set the chosen title type
    title_type = options[choice].lower().replace(" ", "_")
    # If the user chose "Use Custom Title", get the custom title
    if title_type == "use_custom_title":
        custom_title = input("Enter a custom title: ")
        title_config["Custom"] = custom_title
        logging.info("Custom title added: %s", custom_title)
    # Set the title type in the title configuration
    title_config["Type"] = title_type
    # Update the title configuration in the server info
    server_info[server_id]["Embed"]["Title"] = title_config
    # Go to the next customization step
    customize_description(server_info, server_id, file_path)

def customize_description(server_info, server_id, file_path):
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    description_config = server_info[server_id]["Embed"].get("Description", {})
    options = ["Turn Off", "Show Steam Connection Link", "Custom Description"]
    steam_link = f"steam://connect/{server_info[server_id]['IP']}:{server_info[server_id]['Port']}"

    print("\nDescription Options:")
    for i, option in enumerate(options):
        if option == "Show Steam Connection Link":
            print(f"{i+1}. {option} ({steam_link})")
        else:
            print(f"{i+1}. {option}")

    while True:
        choice = input("\nEnter the number of your choice: ")
        try:
            choice = int(choice) - 1
            if choice < 0 or choice >= len(options):
                raise ValueError
            break
        except ValueError:
            logging.error("Invalid input. Please try again.")
            print("Invalid input. Please try again.")

    description_type = options[choice].lower().replace(" ", "_")
    if description_type == "custom_description":
        custom_description = input("Enter a custom description: ")
        description_config["Custom"] = custom_description

    description_config["Type"] = description_type
    server_info[server_id]["Embed"]["Description"] = description_config
    customize_color(server_info, server_id, file_path)

def customize_color(server_info, server_id, file_path):
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    color_config = server_info[server_id]["Embed"].get("Color", None)
    predefined_colors = {
        "red": "#ff0000",
        "green": "#00ff00",
        "blue": "#0000ff",
        "purple": "#800080",
        "orange": "#ffa500",
        "yellow": "#ffff00",
        "pink": "#ffc0cb",
        "cyan": "#00ffff",
        "magenta": "#ff00ff",
        "black": "#000000",
        "white": "#ffffff",
    }

    logging.info(f"Customize color for server {server_id}.")

    print("\nColor Options:")
    for i, (color_name, color_code) in enumerate(predefined_colors.items()):
        print(f"{i+1}. {color_name} ({color_code})")
    print("Enter a hexadecimal color code (e.g. #ff0000)")

    while True:
        choice = input("\nEnter the number or hexadecimal code of your choice: ")
        try:
            choice = int(choice) - 1
            if choice < 0 or choice >= len(predefined_colors):
                raise ValueError
            color = predefined_colors[list(predefined_colors.keys())[choice]]
            break
        except ValueError:
            try:
                color = int(choice.replace('#', ''), 16)
                if color < 0 or color > 0xFFFFFF:
                    raise ValueError
                color = hex(color).replace('0x', '#')
                break
            except ValueError:
                logging.warning(f"Invalid input for color for server {server_id}: {choice}")
                print("Invalid input. Please try again.")

    server_info[server_id]["Embed"]["Color"] = color
    logging.info(f"Color customised for server {server_id} with value {color}.")

    # Call the next function to customize the thumbnail
    customize_thumbnail(server_info, server_id, file_path)

def customize_thumbnail(server_info, server_id, file_path):
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    logging.info("Customizing thumbnail...")
    thumbnail_config = server_info[server_id]["Embed"].get("Thumbnail", {})
    
    print("\nEmbed Thumbnail:")
    answer = input("Do you want to add a thumbnail? (y/n): ")
    while answer.lower() not in ["y", "n"]:
        answer = input("Invalid input.\nDo you want to add a thumbnail? (y/n): ")

    if answer == 'y':
        thumbnail_url = input("Enter the URL for the thumbnail: ")
        thumbnail_config["Display"] = True
        thumbnail_config["URL"] = thumbnail_url
        server_info[server_id]["Embed"]["Thumbnail"] = thumbnail_config
        logging.info("Added thumbnail: %s", thumbnail_url)
    if answer == 'n':
        thumbnail_config["Display"] = False
        server_info[server_id]["Embed"]["Thumbnail"] = thumbnail_config
        logging.info("Thumbnail not added")

    customize_footer(server_info, server_id, file_path)

def customize_footer(server_info, server_id, file_path):
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    logging.info("Customizing embed footer")

    print("\nEmbed Footer:")
    footer_config = server_info[server_id]["Embed"].get("Footer", {})
    
    answer = input("Do you want to customize the footer of the embed? (y/n): ")
    while answer.lower() not in ["y", "n"]:
        answer = input("Invalid input.\nDo you want to customize the footer of the embed? (y/n): ")

    if answer == 'y':
        footer_text = input("Enter the text for the footer: ")
        footer_icon_url = input("Enter the URL for the footer icon: ")
        footer_config["Text"] = footer_text
        footer_config["Icon URL"] = footer_icon_url
        server_info[server_id]["Embed"]["Footer"] = footer_config
        logging.info(f"Updated footer text to {footer_text} and footer icon URL to {footer_icon_url}")
    else:
        logging.info("Footer customization cancelled")

    customize_fields(server_info, server_id, file_path)

def display_field_choice(option: str) -> bool:
    while True:
        choice = input(f"\nDo you want to display {option}? (y/n): ")
        if choice.lower() not in ["y", "n"]:
            print("Invalid input. Please try again.")
        else:
            break
    return choice == 'y'

def get_field_position(option, positions):
    while True:
        position = input(f"\nEnter the position (1-6) you want to display {option}: ")
        try:
            position = int(position) - 1
            if position < 0 or position >= 6 or positions[position] is not None:
                raise ValueError
            positions[position] = option
            break
        except ValueError:
            print("Invalid input. Please try again.")
    return position

def customize_fields(server_info, server_id, file_path):
    fields_config = server_info[server_id]["Embed"].get("Fields", {})
    options = ["Status", "Connection", "Location", "Game", "Map", "Players"]
    positions = [None] * 6

    logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

    print("\nField Options:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    for i, option in enumerate(options[:6]):
        print("\nCurrent Field Positions:")
        for i, position in enumerate(positions):
            if position is None:
                print(f"{i + 1}. None")
            else:
                print(f"{i + 1}. {position}")

        if display_field_choice(option):
            position = get_field_position(option, positions)
            fields_config[option] = {"Position": position, "Display": True}
        else:
            fields_config[option] = {"Display": False}

    fields_config["Player Names"] = {"Display": display_field_choice("Player Names")}
    fields_config["Player Graph"] = {"Display": display_field_choice("Player Graph")}
    server_info[server_id]["Embed"]["Fields"] = fields_config

    json_parser.write_json_file(file_path, server_info)

    logging.info('Fields customization completed')