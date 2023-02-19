import asyncio
import a2s
from mcstatus import JavaServer
from mcstatus import BedrockServer
import fivempy
from samp_client.client import SampClient

class protocol:
    # Class containing methods to query various game servers
    def valve(ip, port, query_type):
        # Valve server query method
        address = (str(ip), int(port))

        try:
            if query_type == "server_info":
                info = a2s.info(address)
                info_dict = dict(info)

                return info_dict

            elif query_type == "player_info":
                players = a2s.players(address)

                player_array = []
                for player in players:
                    player_info = [player.index, player.name, player.score, player.duration]
                    player_array.append(player_info)

                return player_array

            elif query_type == "server_rules":
                rules = a2s.rules(address)

                rule_dict = {}
                for rule in rules:
                    rule_dict[rule] = rules[rule]

                return rule_dict

            else:
                print("Error: Incorrect Query Type!\nSet Query Type to:\nserver_info")
                return None

        except TimeoutError:
            print("The server took too long to respond.\nThis may be because the server isn't online, or the query was denied!")
            return False
    
    class minecraft:
        # Minecraft server query methods
        def java(ip, port, query_type):
            address = f"{ip}:{port}"

            try:
                if query_type == "server_info":
                    server = JavaServer.lookup(address)
                    status = server.status()
                    query = server.query()

                    info_dict = {
                                 'protocol': status.version.protocol, 
                                 'server_name': query.motd,
                                 'map_name': query.map, 
                                 'folder': None, 
                                 'game': 'Minecraft', 
                                 'app_id': None,
                                 'player_count': status.players.online, 
                                 'max_players': status.players.max, 
                                 'bot_count': None,
                                 'server_type': None,
                                 'platform': 'Java',
                                 'password_protected': None,
                                 'vac_enabled': None,
                                 'version': status.version.name,
                                 'edf': None,
                                 'port': port,
                                 'steam_id': None,
                                 'stv_port': None,
                                 'stv_name': None,
                                 'keywords': None,
                                 'game_id': None,
                                 'ping': status.latency
                                 }

                    return info_dict

                elif query_type == "player_info":
                    server = JavaServer.lookup(address)
                    query = server.query()

                    return query.players.names

                elif query_type == "server_rules":
                    return None

                else:
                    return "Error: Incorrect Query Type!\nSet Query Type to:\nserver_info\nplayer_info"
            
            except TimeoutError:
                print("The server took too long to respond.\nThis may be because the server isn't online, or the query was denied!")
                return False

        def bedrock(ip, port, query_type):
            address = f"{ip}:{port}"

            try:
                if query_type == "server_info":
                    # Lookup the server by IP and port
                    server = BedrockServer.lookup(address)
                    # Get the server status
                    status = server.status()

                    # Create a dictionary with server info
                    info_dict = {
                                 'protocol': status.version.protocol, 
                                 'server_name': status.motd,
                                 'map_name': status.map, 
                                 'folder': None, 
                                 'game': 'Minecraft', 
                                 'app_id': None,
                                 'player_count': status.players_online, 
                                 'max_players': status.players_max, 
                                 'bot_count': None,
                                 'server_type': None,
                                 'platform': 'Bedrock',
                                 'password_protected': None,
                                 'vac_enabled': None,
                                 'version': status.version.brand,
                                 'edf': None,
                                 'port': port,
                                 'steam_id': None,
                                 'stv_port': None,
                                 'stv_name': None,
                                 'keywords': None,
                                 'game_id': None,
                                 'ping': status.latency
                                 }

                    return info_dict

                elif query_type == "player_info":
                    # TODO: Implement player_info query for Bedrock servers
                    return None

                elif query_type == "server_rules":
                    # TODO: Implement server_rules query for Bedrock servers
                    return None

                else:
                    # Invalid query_type parameter
                    return "Error: Incorrect Query Type!\nSet Query Type to:\nserver_info"

            except TimeoutError:
                # Handle TimeoutError exceptions
                print("The server took too long to respond.\nThis may be because the server isn't online, or the query was denied!")
                return False
            
    def fivem(ip, port, query_type):
        address = f"{ip}:{port}"

        try:
            if query_type == "server_info":
                server = fivempy.Server(address)
                info, dynamic = server.get_info(), server.get_dynamic()

                # Create a dictionary of server information
                info_dict = {
                             'protocol': None, 
                             'server_name': info['vars']['sv_projectName'], 
                             'map_name': dynamic['mapname'],
                             'folder': None, 
                             'game': info['vars']['gamename'], 
                             'app_id': None,
                             'player_count': server.get_player_count(), 
                             'max_players': server.get_max_player(), 
                             'bot_count': None,
                             'server_type': info['server'],
                             'platform': 'FiveM',
                             'password_protected': None,
                             'vac_enabled': None,
                             'version': info['version'],
                             'edf': None,
                             'port': port,
                             'steam_id': None,
                             'stv_port': None,
                             'stv_name': None,
                             'keywords': info['vars']['tags'],
                             'game_id': None,
                             'ping': None
                             }
    
                return info_dict

            elif query_type == "player_info":
                server = fivempy.Server(address)

                # Get the list of players on the server and create an array of player data
                players = server.get_players()
                player_array = []
                for player in players:
                    player_info = [player['id'], player['name'], None, None]
                    player_array.append(player_info)

                return player_array

            elif query_type == "server_rules":
                return None

            else:
                print("Error: Incorrect Query Type!\nSet Query Type to:\nserver_info")
                return None

        except TimeoutError or TypeError:
            print("The server took too long to respond.\nThis may be because the server isn't online, or the query was denied!")
            return False

    def samp(ip, port, query_type):
        address = (str(ip), int(port))
    
        try:
            if query_type == "server_info":
                with SampClient(ip, port) as client:
                    # Get server information, rules, and clients
                    info = client.get_server_info()
                    rules = client.get_server_rules_dict()
                    clients = client.get_server_clients()
                
                # Build a dictionary containing the server information
                info_dict = {
                             'protocol': None, 
                             'server_name': info.hostname, 
                             'map_name': rules['mapname'],
                             'folder': None, 
                             'game': 'samp', 
                             'app_id': None,
                             'player_count': info.players, 
                             'max_players': info.max_players, 
                             'bot_count': None,
                             'server_type': None,
                             'platform': 'samp',
                             'password_protected': info.password,
                             'vac_enabled': None,
                             'version': rules['version'],
                             'edf': None,
                             'port': port,
                             'steam_id': None,
                             'stv_port': None,
                             'stv_name': None,
                             'keywords': None,
                             'game_id': None,
                             'ping': None
                             }
    
                return info_dict
    
            elif query_type == "player_info":
                return None
    
            elif query_type == "server_rules":
                return None
    
            else:
                print("Error: Incorrect Query Type!\nSet Query Type to:\nserver_info")
                return None
    
        except TimeoutError:
            print("The server took too long to respond.\nThis may be because the server isn't online, or the query was denied!")
            return False
        
#####################################
#               TODO                #
#-----------------------------------#
# Terraria                          #
# Roblox                            #
# TeamSpeak                         #
# RageM                             #
#####################################

# testing use only
#info = protocol.valve("147.135.105.231", "27036", "player_info")
#print(info)