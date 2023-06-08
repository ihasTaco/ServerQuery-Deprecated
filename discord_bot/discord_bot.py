import discord
from discord.ext import commands
from discord import app_commands
import sys
import subprocess
import time
import json
import datetime
import asyncio
import json_parser
from servers_queries import query
import server_graph
import logging
import configparser

# commands group
import commands.server_group as server_group

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')

def restart():
    subprocess.Popen(["python", "module_checker.py"])
    exit()

async def update_embed(client, embed, image_file):
    logger = logging.getLogger(__name__)
    logger.info(f"Updating embed with image: {image_file}")
    
    # send the embed and get the message object
    message = await client.send(embed=embed)

    # create a file object with the image file
    with open(image_file, 'rb') as f:
        file = discord.File(fp=f, filename='player_data.png')
        # set the image URL of the embed to the attachment URL of the file
        embed.set_image(url='attachment://player_data.png')
        # edit the message with the updated embed that includes the image
        await message.edit(embed=embed)
    
    logger.info("Embed updated successfully")

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
    data = json_parser.load_json_file(file_path)

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
    elif description_config.get("Type", 'show_steam_connection_link'):
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

async def send_image(client, channel, file_path):
    logger = logging.getLogger(__name__)
    print(channel)
    with open(file_path, "rb") as f:
        # Create a Discord file object with the image file
        file = discord.File(f)  
        # Send the file to the specified channel
        try:
            message = await channel.send(file=file) 
        except Exception as e:
            logger.exception(f"Error sending file {file_path}: {e}")
        else:
            logger.info(f"File {file_path} sent to channel {channel.id}")
            # Get the URL of the uploaded image 
            image_url = message.attachments[0].url 
            # Return the URL of the uploaded image 
            return image_url 

async def send_embed(client, embed, uuid, file_path, status):
    # Load the JSON file
    data = json_parser.load_json_file(file_path)

    # Get the channel and guild IDs from the JSON file using the provided UUID
    channel_id = data[uuid]['Channel ID']
    guild_id = data[uuid]['Guild ID']

    # Get the guild object using the guild ID
    guild = client.get_guild(int(guild_id))
    
    img_guild = client.get_guild(int(config.get('DEFAULT', 'graph_guild_id')))

    if guild is not None:
        # Get the channel object using the channel ID
        channel = guild.get_channel(int(channel_id))

        if channel is not None:
            # Get the embed and fields configuration from the JSON file using the provided UUID
            embed_config = data[uuid].get("Embed", {})
            fields_config = embed_config.get("Fields", {})

            # If status is True, check if the Player Graph field should be displayed
            if status == True:
                if fields_config.get("Player Graph", {}).get("Display", True):
                    # If the Player Graph field should be displayed, set the image URL to the URL of the player data graph
                    embed.set_image(url=await send_image(client, img_guild.get_channel(int(config.get('DEFAULT', 'graph_channel_id'))), 'discord_bot\images\player_data.png'))

            # Send the embed to the channel
            message = await channel.send(embed=embed)

            # Get the message ID of the sent message and update the JSON file with it
            message_id = message.id
            json_parser.update_message_id(file_path, uuid, message_id)

            logging.info(f"Embed sent to channel {channel.id} in guild {guild.id}")
        else:
            logging.error(f"Unable to find channel with id {channel_id} in guild {guild_id}")
            print(f"Unable to find channel with id {channel_id} in guild {guild_id}")
    else:
        logging.error(f"Unable to find guild with id {guild_id}")
        print(f"Unable to find guild with id {guild_id}")

async def edit_embed(client, embed, uuid, file_path, status):
    # Load the JSON file
    data = json_parser.load_json_file(file_path)

    # Get the message id, channel id, and guild id from the data
    message_id = data[uuid]['Message ID']
    channel_id = data[uuid]['Channel ID']
    guild_id = data[uuid]['Guild ID']

    # Get the guild object from the client using the guild id
    guild = client.get_guild(int(guild_id))
    img_guild = client.get_guild(int(config.get('DEFAULT', 'graph_guild_id')))
    if guild is not None:
        # Get the channel object from the guild using the channel id
        channel = guild.get_channel(int(channel_id))
        if channel is not None:
            try:
                # Try to fetch the message using the message id
                message = await channel.fetch_message(int(message_id))
            except discord.errors.NotFound:
                # If the message is not found, send a new embed instead
                await send_embed(client, embed, uuid, file_path, status)
                logging.warning(f"Message not found for UUID {uuid}. Sending a new embed.")
                return
            
            # Get the embed and fields configuration from the data
            embed_config = data[uuid].get("Embed", {})
            fields_config = embed_config.get("Fields", {})

            # If the status is true and the player graph is set to display, set the image URL for the graph
            if status == True:
                if fields_config.get("Player Graph", {}).get("Display", True):
                    embed.set_image(url=await send_image(client, img_guild.get_channel(int(config.get('DEFAULT', 'graph_channel_id'))), 'discord_bot\images\player_data.png'))
            
            # Edit the message with the updated embed
            await message.edit(embed=embed)
            logging.info(f"Embed with UUID {uuid} edited successfully.")
        else:
            logging.warning(f"Unable to find channel with id {channel_id} in guild {guild_id}")
    else:
        logging.warning(f"Unable to find guild with id {guild_id}")

async def get_uuid_by_index(file_path, index=None, uuid=None):
    # Load the JSON file
    servers = json_parser.load_json_file(file_path)

    # Get a list of server UUIDs
    server_uuid = list(servers.keys())

    # Create a map of UUIDs to their index positions
    uuid_index_map = {}
    if not uuid_index_map:
        uuid_index_map = {uuid: index for index, uuid in enumerate(server_uuid)}

    # Get the UUID by the index position
    def get_uuid_by_index(index):
        return server_uuid[index]

    # Get the index position by the UUID
    def get_index_by_uuid(uuid):
        return uuid_index_map.get(uuid, None)

    # Return either the UUID or index position
    if index is not None:
        result = get_uuid_by_index(index)
        logging.info(f"get_uuid_by_index: Returning UUID for index {index}: {result}")
        return result
    elif uuid is not None:
        result = get_index_by_uuid(uuid)
        logging.info(f"get_uuid_by_index: Returning index for UUID {uuid}: {result}")
        return result

def get_server_info(file_path, uuid, query_type):
    # Load the JSON file
    data = json_parser.load_json_file(file_path)

    if data:
        # Retrieve the necessary information from the JSON data
        ip = data[uuid]["IP"]
        port = data[uuid]["Query Port"]
        protocol = data[uuid]["Query API"]

        # Create an instance of the appropriate class in the protocol class
        if protocol == "Valve":
            protocol_instance = query.protocol.valve(ip, port, query_type)
        elif protocol == "Minecraft.Java":
            protocol_instance = query.protocol.minecraft.java(ip, port, query_type)
        elif protocol == "Minecraft.Bedrock":
            protocol_instance = query.protocol.minecraft.bedrock(ip, port, query_type)
        elif protocol == "FiveM":
            protocol_instance = query.protocol.fivem(ip, port, query_type)
        elif protocol == "SAMP":
            protocol_instance = query.protocol.samp(ip, port, query_type)
        else:
            # Log a warning if the protocol is not recognized
            logging.warning(f"Protocol '{protocol}' is not recognized.")

        # Return the result
        return protocol_instance
    else:
        # Log a warning if the data is empty
        logging.warning(f"JSON data is empty for uuid '{uuid}' in file '{file_path}'.")

    # If the JSON file is empty, return None
    return None

async def check_server_status(server_id, status, file_path):
    # Get the current time
    timestamp = datetime.datetime.now(datetime.datetime.utcnow().astimezone().tzinfo)
    # Load the JSON file
    data = json_parser.load_json_file(file_path)

    # Check if the server status has been recorded before
    if "Status" not in data[server_id]:
        data[server_id]["Status"] = status
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return
    
    # Check if the server status has changed
    if data[server_id]["Status"] != status:
        # Update the status in the JSON file
        data[server_id]["Status"] = status
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        # Get the embed configuration
        embed_config = data[server_id].get("Embed", {})

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

        server_name = ''
        if data[server_id]["Server Name"] == '':
            server_name = server_id
        else:
            server_name = data[server_id]["Server Name"]

        if status == True:
            # Create an embed to notify that the server is online
            embed = discord.Embed(title=f"Server {server_name} is now online", color=0x00FF00, timestamp=timestamp)
            embed.add_field(name="Server Status", value=":green_circle: Online", inline=True)
        elif status == False:
            # Create an embed to notify that the server is offline
            embed = discord.Embed(title=f"Server {server_id} is now offline", color=0xFF0000, timestamp=timestamp)
            embed.add_field(name="Server Status", value=":red_circle: Offline", inline=True)
            
        embed.set_thumbnail(url=thumbnail_icon_url)
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        
        # Get the guild and channel where the notification should be sent
        guild = client.get_guild(int(config.get('DEFAULT', 'status_guild_id')))
        if guild is not None:
            channel = guild.get_channel(int(config.get('DEFAULT', 'status_channel_id')))
            if channel is not None: 
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    logging.error(f"Error issued when trying to send status change message: {e}")

                if status == True:
                    logging.info(f"Server {server_name} is now online.")
                elif status == False:
                    logging.info(f"Server {server_name} is now offline.")

async def wait(seconds):
    await asyncio.sleep(seconds)

@client.event
async def on_ready():
    start_time = time.time()

    logging.info("ServerQuery is starting up")

    # Path to the server_info.json file
    file_path = "data_management\server_info.json"

    # Get the server uuid by index
    await get_uuid_by_index(file_path, index=None, uuid=None)

    # Clear the terminal screen
    subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)

    # Create a new server group command
    serverGroup = server_group.ServerGroup(name="server", description="Manage ServerQuery servers")
    client.tree.add_command(serverGroup)

    # Print the ServerQuery banner
    print("  _________                               ________                              \n /   _____/ ______________  __ ___________\_____  \  __ __   ___________ ___.__.\n \_____  \_/ __ \_  __ \  \/ // __ \_  __ \/  / \  \|  |  \_/ __ \_  __ <   |  |\n /        \  ___/|  | \/\   /\  ___/|  | \/   \_/.  \  |  /\  ___/|  | \/\___  |\n/_______  /\___  >__|    \_/  \___  >__|  \_____\ \_/____/  \___  >__|   / ____|\n        \/     \/                 \/             \__>           \/       \/     \n")
    print("________________________________________________________________________________")
    print("                             ServerQuery is ready!                              ")
    print("_______________________________ By: ihasTacoFML ________________________________\n")

    # Synchronize the command tree
    await client.tree.sync()
    # Initialize the server index to 0
    server_index = 0

    while True: 
        try:
            # Load the JSON file
            data = json_parser.load_json_file(file_path)

            # Get the server UUID by index
            server_uuid = await get_uuid_by_index(file_path, server_index)

            # Get server information, player information, and server rules information
            server_info = get_server_info(file_path, server_uuid, 'server_info')
            player_info = get_server_info(file_path, server_uuid, 'player_info')
            server_rules = get_server_info(file_path, server_uuid, 'server_rules')

            # Check if the server is online or offline
            if server_info == False or  player_info == False or server_rules == False:
                # If the server is offline, create an "offline" embed and update the server status
                embed = create_embed(file_path, server_uuid, server_info, player_info, server_rules, 'offline')
                status = False
                await check_server_status(server_uuid, status, file_path)
                logging.info(f"Server {server_uuid} is offline")
            else:
                # If the server is online, update the number of players, plot player data, create an "online" embed, and update the server status
                json_parser.update_server_players(file_path, server_uuid, server_info["player_count"])
                server_graph.plot_player_data(server_uuid)
                embed = create_embed(file_path, server_uuid, server_info, player_info, server_rules, 'online')
                status = True
                await check_server_status(server_uuid, status, file_path)

            # Send or edit the embed in Discord, depending on whether a message ID is present in the JSON file
            if not data[server_uuid]['Message ID']:
                await send_embed(client, embed, server_uuid, file_path, status)
            else:
                await edit_embed(client, embed, server_uuid, file_path, status)

            # Increment the server index and continue the loop
            server_index += 1

        except IndexError:
            # If all servers have been checked, wait for 5 minutes before starting again and reset the server index to 0
            await wait(300)
            server_index = 0
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 24 * 60 * 60:  # 24 hours
                restart()

client.run(str(config.get('DEFAULT', 'discord_token')))
