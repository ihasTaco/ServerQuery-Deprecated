import discord
from discord.ext import commands
from discord import app_commands
import os
import sys
import subprocess
import json
import datetime
import asyncio
import logging
import configparser

# Get the absolute path to the ServerQuery directory
serverquery_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the ServerQuery directory to the Python module search path
sys.path.append(serverquery_dir)

import server_graph
from modules import json_parser
import servers_query.query as query
import embed.embed_create as embed_create
import embed.embed_send as embed_send

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

async def get_uuid_by_index(file_path, index=None, uuid=None):
    # Load the JSON file
    servers = json_parser.read_json_file(file_path)

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
    data = json_parser.read_json_file(file_path)
    
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
    data = json_parser.read_json_file(file_path)

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
    logging.info("ServerQuery is starting up")

    # Path to the server_info.json file
    file_path = "server_data\server_info.json"

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

    # Copy the global tree to the specified guild
    #client.tree.copy_global_to(guild=discord.Object(id=1071243907121295420))
    #client.tree.copy_global_to()
    # Synchronize the command tree for the specified guild
    #await client.tree.sync(guild=discord.Object(id=1071243907121295420))
    await client.tree.sync()
    # Initialize the server index to 0
    server_index = 0

    while True: 
        try:
            # Load the JSON file
            data = json_parser.read_json_file(file_path)

            # Get the server UUID by index
            server_uuid = await get_uuid_by_index(file_path, server_index)

            # Get server information, player information, and server rules information
            server_info = get_server_info(file_path, server_uuid, 'server_info')
            player_info = get_server_info(file_path, server_uuid, 'player_info')
            server_rules = get_server_info(file_path, server_uuid, 'server_rules')

            # Check if the server is online or offline
            if server_info == False or  player_info == False or server_rules == False:
                # If the server is offline, create an "offline" embed and update the server status
                embed = embed_create.create_embed(file_path, server_uuid, server_info, player_info, server_rules, 'offline')
                status = False
                await check_server_status(server_uuid, status, file_path)
                logging.info(f"Server {server_uuid} is offline")
            else:
                # If the server is online, update the number of players, plot player data, create an "online" embed, and update the server status
                json_parser.update_server_players(file_path, server_uuid, server_info["player_count"])
                server_graph.plot_player_data(server_uuid)
                embed = embed_create.create_embed(file_path, server_uuid, server_info, player_info, server_rules, 'online')
                status = True
                await check_server_status(server_uuid, status, file_path)

            # Send or edit the embed in Discord, depending on whether a message ID is present in the JSON file
            if not data[server_uuid]['Message ID']:
                await embed_send.send_embed(client, embed, server_uuid, file_path, status)
            else:
                await embed_send.edit_embed(client, embed, server_uuid, file_path, status)

            # Increment the server index and continue the loop
            server_index += 1
        except IndexError:
            # If all servers have been checked, wait for 5 minutes before starting again and reset the server index to 0
            await wait(300)
            server_index = 0
            
client.run(str(config.get('DEFAULT', 'discord_token')))