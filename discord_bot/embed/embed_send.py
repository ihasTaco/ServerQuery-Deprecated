import discord
import logging
import configparser

from modules import json_parser

config = configparser.ConfigParser()
config.read('config.ini')

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

async def send_image(client, channel, file_path):
    logger = logging.getLogger(__name__)
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
    data = json_parser.read_json_file(file_path)

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
    data = json_parser.read_json_file(file_path)

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