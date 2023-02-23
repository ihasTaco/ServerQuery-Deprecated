import os
import json
import subprocess
import sys

from modules import json_parser

def read_json(file_path):
    # Load the data from the JSON file
    with open(file_path) as f:
        data = json.load(f)
        return data

def import_customizations(server_UUID, import_embed_settings=True, import_graph_settings=True):
    # Get the path to the import_export folder
    import_export_folder_path = os.path.join(os.getcwd(), 'import_export')
    if not os.path.exists(import_export_folder_path):
        print(f'import_export folder does not exist: {import_export_folder_path}')
        return
    
    # Get the list of files in the import_export folder
    import_export_files = os.listdir(import_export_folder_path)
    if not import_export_files:
        print('No customization files found in folder.')
        return
    
    # Print the list of customization files
    print('Choose a customization file to import:')
    for i, file_name in enumerate(import_export_files):
        print(f'{i}) {file_name}')
    
    # Get the index of the file to import
    while True:
        index = input('Enter the index of the file to import: ')
        try:
            index = int(index)
        except ValueError:
            print('Invalid index. Please enter a number.')
            continue
        if index < 0 or index >= len(import_export_files):
            print(f'Index out of range. Please enter a number between 0 and {len(import_export_files) - 1}.')
            continue
        break
    
    # Load the selected import_export file
    file_name = import_export_files[index]
    file_path = os.path.join(import_export_folder_path, file_name)
    data = read_json(file_path)
    
    # Check if we need to import the embed settings
    if import_embed_settings:
        # Update the server embed settings
        embed_config = data.get('Embed')
        if embed_config:
            with open('server_info.json', 'r') as f:
                server_data = json.load(f)
            server_data[server_UUID]['Embed'].update(embed_config)
            with open('server_info.json', 'w') as f:
                json.dump(server_data, f, indent=4)
    
    # Check if we need to import the graph settings
    if import_graph_settings:
        # Update the server graph settings
        graph_config = data.get('Graph')
        if graph_config:
            with open('server_info.json', 'r') as f:
                server_data = json.load(f)
            server_data[server_UUID]['Graph'].update(graph_config)
            with open('server_info.json', 'w') as f:
                json.dump(server_data, f, indent=4)
    
    print('Customizations imported successfully.')

def export_customizations(server_uuid):
    # Load the server info from the JSON file
    with open("server_data/server_info.json") as f:
        data = json.load(f)

    if server_uuid not in data:
        print(f"Server with UUID {server_uuid} not found.")
        return

    server_data = data[server_uuid]
    server_name = server_data["Server Name"]

    # Prompt the user to enter the output file name
    filename = input(f"Enter a name for the output file (without extension) for server '{server_name}': ")

    # Create the output directory if it does not exist
    output_dir = "import_exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export the embed and graph customizations to a JSON file
    with open(os.path.join(output_dir, f"{filename}.json"), "w") as f:
        json.dump({
            "Embed": server_data["Embed"],
            "Graph": server_data["Graph"]
        }, f, indent=4)

    print(f"Customizations for server '{server_name}' exported to '{os.path.join(output_dir, filename)}.json'")

def prompt_export():
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
    # Prompt the user to select a server to export customizations for
    with open("server_data/server_info.json") as f:
        data = json.load(f)

    print("Select a server to export customizations for:\n")
    for i, server_uuid in enumerate(data, start=1):
        server_name = data[server_uuid]["Server Name"]
        print(f"{i}) {data[server_uuid]['IP']}:{data[server_uuid]['Port']} | {server_name}")
    
    choice = int(input("\nEnter the index of the server: ")) - 1
    server_uuid = list(data.keys())[choice]

    export_customizations(server_uuid)