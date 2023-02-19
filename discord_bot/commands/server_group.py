import discord
from discord.ext import commands
from discord import app_commands

# Define a new subclass of the Group class in discord.py's app_commands module
class ServerGroup(app_commands.Group):
    # Define a new subcommand called 'add' with a description
    @app_commands.command(description = "Add a server to ServerQuery")
    async def add(self, interaction: discord.Interaction):
        # Send an ephemeral message in response to the command
        await interaction.response.send_message(
            f"ping!", ephemeral=True
        )
    # Define a new subcommand called 'delete' with a description
    @app_commands.command(description = "Remove a server from ServerQuery")
    async def delete(self, interaction: discord.Interaction):
        # Send an ephemeral message in response to the command
        await interaction.response.send_message(
            f"ping!", ephemeral=True
        )
    # Define a new subcommand called 'list' with a description
    @app_commands.command(description = "List all server in ServerQuery")
    async def list(self, interaction: discord.Interaction):
        # Send an ephemeral message in response to the command
        await interaction.response.send_message(
            f"ping!", ephemeral=True
        )
    # Define a new subcommand called 'edit' with a description
    async def edit(self, interaction: discord.Interaction):
        # Send an ephemeral message in response to the command
        await interaction.response.send_message(
            f"ping!", ephemeral=True
        )