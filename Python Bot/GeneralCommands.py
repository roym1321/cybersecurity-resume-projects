import asyncio
from Init_Bot import bot
from discord import app_commands
from discord.ext.commands import command, cooldown
import discord
import os
import random


async def LeaveChannel(connection):
    if connection:
        if connection[0].is_playing():
            connection[0].stop()
        await connection[0].disconnect(force=True)
        return True
    return False


async def JoinChannel(interaction: discord.Interaction, channel_to_join, respond=True):
    print(f"Trying to join {channel_to_join}")
    connection = interaction.client.voice_clients
    if not channel_to_join:
        return None
    if connection:
        connection = interaction.client.voice_clients[0]
        if connection.channel != channel_to_join:
            # if cls:
            #     # connection.cls = wavelink.Player
            #     pass
            await connection.move_to(channel_to_join)
    else:
        try:
            connection = await channel_to_join.connect()
        except Exception as e:
            print(f"Unknown error: {e}")
            return
    if respond:
        await interaction.response.send_message(f"Joined {channel_to_join.name}", ephemeral=True)
    return connection


async def PlayAudioFile(voice_client, file_path, volume) -> bool:
    volume = 40 if volume is None else volume

    audio_source = discord.PCMVolumeTransformer(original=discord.FFmpegPCMAudio(file_path), volume=volume / 100)
    voice_client.play(source=audio_source)
    return True


async def StopAudio(interaction: discord.Interaction, voice_client):
    if not voice_client.is_playing():
        await interaction.response.send_message(f"No Sound", ephemeral=True)
    else:
        voice_client.stop()
        await interaction.response.send_message(f"Stopped", ephemeral=True)


async def is_roy(interaction: discord.Interaction) -> bool:
    if str(interaction.user) != 'roym':
        await interaction.response.send_message("For now only Roy can.")
        return False
    return True


# Slash Commands
@bot.tree.command(name="delete_bot_messages", description="Delete all messages on this channel")
@app_commands.describe(count='How many messages to check')
# @cooldown()
async def delete_bot_messages(interaction: discord.Interaction, count: int = None):
    if not await is_roy(interaction):
        return
    await interaction.response.send_message("Deleting messages...")
    print("Deleting messages...")
    try:
        deleted = await interaction.channel.purge(check=lambda m: m.author == bot.user,
                                                  bulk=True, limit=count)
    except:
        deleted = await interaction.channel.purge(check=lambda m: m.author == bot.user,
                                                  bulk=False, limit=count)
        print("Bulking is not enabled")
    await asyncio.sleep(1)
    await interaction.channel.send(f'Deleted {len(deleted)} message(s)', delete_after=60)


@bot.tree.command(name="stop_sound", description="Force stop the player")
async def stop_sound(interaction: discord.Interaction):
    if not await is_roy(interaction):
        return
    try:
        voice_client = interaction.client.voice_clients[0]
    except:
        await interaction.response.send_message(f"The bot is currently not connected to a voice channel.",
                                                ephemeral=True)
        return
    if not voice_client.is_playing():
        await interaction.response.send_message(f"No Sound", ephemeral=True)
    else:
        voice_client.stop()
        await interaction.response.send_message(f"Stopped", ephemeral=True)


@bot.tree.command(name="sound", description="sound")
async def sound(interaction: discord.Interaction, volume: app_commands.Range[int, 0, 100] = None):
    if not await is_roy(interaction):
        return
    channel_to_join = interaction.user.voice.channel

    if channel_to_join:
        voice_client = await JoinChannel(interaction, channel_to_join=channel_to_join, respond=False)
        if not voice_client:
            await interaction.response.send_message(f"Could not join your voice channel", ephemeral=True)
            return

        view = discord.ui.View()

        class Choose_mp3(discord.ui.Select):
            def __init__(self):
                self.voice_client = voice_client
                mp3_list = os.listdir(r"C:\Users\Roy\Music\Take One")
                mp3_files = [discord.SelectOption(label=file.split(".")[0], value=file)
                             for file in mp3_list]
                super(Choose_mp3, self).__init__(options=mp3_files)

            async def callback(self, interaction: discord.Interaction):
                song = self.values[0].split(".")[0]
                file_path = r"C:\Users\Roy\Music\Take One\\" + self.values[0]
                await PlayAudioFile(voice_client, file_path, volume)
                await interaction.response.send_message(content=f"Playing {song}")

        view.add_item(Choose_mp3())

        await interaction.response.send_message("Choose a sound:", view=view, ephemeral=True)
    else:
        await interaction.response.send_message(f"Be in a voice channel", ephemeral=True)


@bot.tree.command(name="leave", description="leaves the user's channel")
async def leave(interaction: discord.Interaction):
    if not await is_roy(interaction):
        return
    connection = interaction.client.voice_clients
    if await LeaveChannel(connection):
        await interaction.response.send_message(f"I Left jeez", ephemeral=True)
    else:
        await interaction.response.send_message(f"Im not connected to any voice channel ya cunt", ephemeral=True)


@bot.tree.command(name="join", description="joins the user's channel. Optionally can write a channel's name to join. ")
@app_commands.describe(channel='What channel should I join? (optional)')
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel = None):
    if not await is_roy(interaction):
        return
    if channel:
        channel_to_join = channel
    elif interaction.user.voice:
        try:
            channel = interaction.user.voice.channel
        except AttributeError:
            await interaction.response.send_message("Could not Connect", ephemeral=True)
            return
        channel_to_join = channel
    else:
        await interaction.followup.send(f"You need to be in a Voice Channel or provide its name", ephemeral=True)
        return
    voice_client = await JoinChannel(interaction, channel_to_join=channel_to_join, respond=True)
    if not voice_client:
        await interaction.response.send_message(f"Already in the requested voice channel", ephemeral=True)


@bot.tree.command(name="shutdown", description='Closes the bot')
async def shutdown(interaction: discord.Interaction):
    if not await is_roy(interaction):
        return
    connection = interaction.client.voice_clients
    if connection:
        await connection[0].disconnect(force=False)
    await interaction.response.send_message("Shutting down...")
    await bot.close()



