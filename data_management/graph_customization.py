import json
import matplotlib.pyplot as plt
from matplotlib import colors
import subprocess
import sys
import logging

def read_json(file_path):
    # Load the data from the JSON file
    with open(file_path) as f:
        data = json.load(f)
        return data

def write_to_json(file_path, data):
    # Save the modified data to the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f)

def color_input(server_id, text):
    # Validate the input
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
    print(text)
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
    return color

def prompt_graph_customization(server_UUID):
    # Clear the console screen
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    file_path = "data_management\server_info.json"
    data = read_json(file_path)

    # Get the graph settings
    graph_config = data[server_UUID]['Graph']

    # Prompt the user for customizations
    print('Enter customizations for the graph:')

    data[server_UUID]['Graph']['Title'] = {}
    data[server_UUID]['Graph']['Title']['Text'] = input('Title text: ')
    data[server_UUID]['Graph']['Title']['Color'] = color_input(server_UUID, 'Title Text Color')

    data[server_UUID]['Graph']['Labels'] = {}
    data[server_UUID]['Graph']['Labels']['X Label Text'] = input('X label text: ')
    data[server_UUID]['Graph']['Labels']['Y Label Text'] = input('Y label text: ')
    data[server_UUID]['Graph']['Labels']['Color'] = color_input(server_UUID, 'Label Color')

    data[server_UUID]['Graph']['Tick Color'] = color_input(server_UUID, 'Tick Color')

    data[server_UUID]['Graph']['Online Players'] = {}
    data[server_UUID]['Graph']['Online Players']['Label'] = input('Online players label: ') 
    data[server_UUID]['Graph']['Online Players']['Line Color'] = color_input(server_UUID, 'Online Player Line Color')
    data[server_UUID]['Graph']['Online Players']['Fill Color'] = color_input(server_UUID, 'Online Player Fill Color')
    online_fill_opacity = input('Online players fill opacity (0 to 1): ')  
    if online_fill_opacity:
        online_fill_opacity = float(online_fill_opacity)
        if online_fill_opacity < 0 or online_fill_opacity > 1:
            print('Invalid online players fill opacity. Defaulting to 0.125.')
            online_fill_opacity = 0.125
        data[server_UUID]['Graph']['Online Players']['Fill Opacity'] = online_fill_opacity

    data[server_UUID]['Graph']['Trend'] = {}
    trend_display = input('Display trend line? (y/n): ')
    trend_line_color = color_input(server_UUID, 'Trend Line Color')
    if trend_display.lower() == 'y':
        trend_label = input('Trend line label: ')
        data[server_UUID]['Graph']['Trend']['Display'] = True
        data[server_UUID]['Graph']['Trend']['Label'] = trend_label
        data[server_UUID]['Graph']['Trend']['Line Color'] = trend_line_color
    else:
        data[server_UUID]['Graph']['Trend']['Display'] = False

    data[server_UUID]['Graph']['Grid'] = {}
    grid_display = input('Display grid? (y/n): ')
    if grid_display.lower() == 'y':
        grid_color = color_input(server_UUID, 'Grid Color')
        grid_opacity = input('Grid opacity (0 to 1): ')
        if grid_opacity:
            grid_opacity = float(grid_opacity)
            if grid_opacity < 0 or grid_opacity > 1:
                print('Invalid grid opacity. Defaulting to 0.125.')
                grid_opacity = 0.125
        data[server_UUID]['Graph']['Grid']['Display'] = True
        data[server_UUID]['Graph']['Grid']['Color'] = grid_color
        data[server_UUID]['Graph']['Grid']['Opacity'] = grid_opacity
    else:
        data[server_UUID]['Graph']['Grid']['Display'] = False

    data[server_UUID]['Graph']['Legend'] = {}
    legend_display = input('Display legend? (y/n): ')
    if legend_display.lower() == 'y':
        legend_color = color_input(server_UUID, 'Legend Color')
        legend_edge_color = color_input(server_UUID, 'Legend Edge Color')
        legend_opacity = input('Legend opacity (0 to 1): ')
        if legend_opacity:
            legend_opacity = float(legend_opacity)
            if legend_opacity < 0 or legend_opacity > 1:
                print('Invalid legend opacity. Defaulting to 0.')
                legend_opacity = 0
        data[server_UUID]['Graph']['Legend']['Display'] = True
        data[server_UUID]['Graph']['Legend']['Color'] = legend_color
        data[server_UUID]['Graph']['Legend']['Edge Color'] = legend_edge_color
        data[server_UUID]['Graph']['Legend']['Opacity'] = legend_opacity
    else:
        data[server_UUID]['Graph']['Legend']['Display'] = False

    write_to_json(file_path, data)