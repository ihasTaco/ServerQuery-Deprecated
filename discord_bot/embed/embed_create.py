import discord
from discord.ext import commands
from discord import app_commands
import datetime
import logging

from modules import json_parser
import servers_query.query as query
import server_graph

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

def create_embed(file_path, uuid, server_info, player_info, server_rules, embed_type):
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Get the current time
    timestamp = datetime.datetime.now(datetime.datetime.utcnow().astimezone().tzinfo)

    # Load the JSON file
    data = json_parser.read_json_file(file_path)

    logger.info('JSON file loaded')

    # Get the embed configuration
    embed_config = data[uuid].get("Embed", {})
    fields_config = embed_config.get("Fields", {})
    if not embed_config:
        # Use default layout
        embed_config = {"Title": {"Type": "use_server_title"},"Description": {"Type": "show_steam_connection_link"},"Color": "#23272a","Thumbnail": {"Display": True, "URL": "https://royalproductions.xyz/images/logo/RP_Logo_Outline.png"},"Footer": {"Text": "ServerQuery by Royal Productions", "Icon URL": "https://cdn.discordapp.com/icons/360541835371741185/201c015115ff6e8352486a8ad6c39a1a.webp"}}
        fields_config = {'Status': {'Position': 0, 'Display': True}, 'Connection': {'Position': 1, 'Display': True}, 'Location': {'Position': 2, 'Display': True}, 'Game': {'Position': 3, 'Display': True}, 'Map': {'Position': 4, 'Display': True}, 'Players': {'Position': 5, 'Display': True}, 'Player Names': {'Display': True}, 'Player Graph': {'Display': True}}
    
    # Get the title configuration
    title_config = embed_config.get("Title", {})
    if title_config.get("Type", "") == "use_server_title":
        if embed_type == 'offline':
            title = "Server Offline"
        else:
            title = server_info['server_name']
        logger.info('Using server title')
    elif title_config.get("Type", "") == "use_config_title":
        title = data[uuid]["Server Name"]
        logger.info('Using config title')
    elif title_config.get("Type", "") == "use_custom_title":
        title = title_config.get("Custom", "")
        logger.info('Using custom title')
    else:
        title = None
        logger.warning('No title found')

    # Get the description configuration
    description_config = embed_config.get("Description", {})
    
    if description_config.get("Type", "") == "turn_off":
        description = None
        logger.info('Description turned off')
    elif description_config.get("Type", "") == 'show_steam_connection_link':
        description = f'Connect: steam://connect/{data[uuid]["IP"]}:{data[uuid]["Port"]}'
        logger.info('Using steam connection link')
    elif description_config.get("Type", "") == "custom_description":
        description = description_config.get("Custom", "")
        logger.info('Using custom description')
    else:
        description = None
        logger.warning('No description found')

    # Get the thumbnail configuration
    thumbnail_config = embed_config.get("Thumbnail", {})

    if thumbnail_config.get("Display", False):
        thumbnail_icon_url = thumbnail_config.get("URL", '')
    else:
        thumbnail_icon_url = ''

    # Get the footer configuration
    footer_config = embed_config.get("Footer", {})

    if footer_config.get("Display", False):
        footer_text = footer_config.get("Text", "")
    else:
        footer_config = embed_config.get("Footer", {})
        footer_text = footer_config.get("Text", "")
        footer_icon_url = footer_config.get("Icon URL", '')

    # Get the color configuration
    color_config = embed_config.get("Color", "")
    if not color_config:
        color_config = '#23272a'

    color = discord.Colour(int(color_config.lstrip("#"), 16))

    if embed_type == 'online':
        fields = []
        for field_name, field_info in fields_config.items():
            if field_info.get("Display", False):
                if field_name == "Status":
                    fields.append(["Status", ':green_circle: Online'])
                elif field_name == "Connection":
                    fields.append(["Connection", f'`{data[uuid]["IP"]}:{data[uuid]["Port"]}`'])
                elif field_name == "Location":
                    fields.append(["Location", f'{data[uuid]["Server Location"]}'])
                elif field_name == "Game":
                    fields.append(["Game", f'{data[uuid]["Game"]}'])
                elif field_name == "Map":
                    fields.append(["Map", f'`{server_info["map_name"]}`'])
                elif field_name == "Players":
                    fields.append(["Players", f'{server_info["player_count"]}/{server_info["max_players"]}'])

        # Sort fields based on their position
        fields.sort(key=lambda x: fields_config[x[0]]["Position"])

        embed = discord.Embed(title=title, description=description, color=color, timestamp=timestamp)
        embed.set_thumbnail(url=thumbnail_icon_url)

        for field in fields:
            embed.add_field(name=field[0], value=field[1])
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)

        if server_info["player_count"] != 0:
            if fields_config.get("Player Names", {}).get("Display", False):
                player_names = []
                player_names.insert(0, '')
                for player in player_info:
                    player_names.append(player[1])

                player_names_string = "\n".join(player_names)
                embed.add_field(name="Online Players", value=f'```{player_names_string}```', inline=False)
        
    elif embed_type == 'offline':
        fields = []
        for field_name, field_info in fields_config.items():
            if field_info.get("Display", False):
                if field_name == "Status":
                    fields.append(["Status", ':red_circle: Offline'])
                elif field_name == "Connection":
                    fields.append(["Connection", f'`{data[uuid]["IP"]}:{data[uuid]["Port"]}`'])
                elif field_name == "Location":
                    fields.append(["Location", f'{data[uuid]["Server Location"]}'])
                elif field_name == "Game":
                    fields.append(["Game", f'{data[uuid]["Game"]}'])
                elif field_name == "Map":
                    fields.append(["Map", '`N/A`'])
                elif field_name == "Players":
                    fields.append(["Players", '--/--'])

        # If server is offline set color to red
        color_config = '#e03f4f'
        color = discord.Colour(int(color_config.lstrip("#"), 16))

        # Sort fields based on their position
        fields.sort(key=lambda x: fields_config[x[0]]["Position"])

        if data[uuid]["Server Name"]:
            server_name = data[uuid]["Server Name"]
        else:
            server_name = 'Server is Offline'

        embed = discord.Embed(title=server_name, timestamp=timestamp, color=color)
        embed.set_thumbnail(url=thumbnail_icon_url)

        for field in fields:
            embed.add_field(name=field[0], value=field[1])

        embed.set_footer(text=footer_text, icon_url=footer_icon_url)

        # Log the creation of the embed
        logging.info(f"Created offline Discord embed for {server_name}")

    return embed