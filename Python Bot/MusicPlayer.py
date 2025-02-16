import discord
from discord import app_commands
import datetime
from Init_Bot import bot
import yt_dlp
import asyncio
from GeneralCommands import JoinChannel, LeaveChannel, PlayAudioFile

FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

music_play_session = False
music_play_queue = dict()


class MusicPlayerButtons(discord.ui.View):
    def __init__(self, track, interaction):
        super(MusicPlayerButtons, self).__init__()
        self.track = track
        self.timeout = 600
        self.interaction = interaction
        # self.close_session_when_stopped_playing()

    # async def close_session_when_stopped_playing(self):
    #     connection = self.interaction.client.voice_clients
    #     while connection.is_playing():
    #         pass

    @discord.ui.button(label='Pause', style=discord.ButtonStyle.green)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            voice_client = interaction.client.voice_clients[0]
        except:
            await interaction.response.send_message(f"The bot is currently not connected to a voice channel.",
                                                    ephemeral=True)
            return
        if voice_client.is_paused():
            voice_client.resume()
            button.label = 'Pause'
            await interaction.response.edit_message(view=self)
        elif voice_client.is_playing():
            voice_client.pause()
            button.label = 'Resume'
            await interaction.response.edit_message(view=self)
        else:
            print('Music Player UI Error')

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            voice_client = interaction.client.voice_clients[0]
        except:
            await interaction.response.send_message(f"The bot is currently not connected to a voice channel.",
                                                    ephemeral=True)
            return
        if not voice_client.is_playing():
            source = await discord.FFmpegOpusAudio.from_probe(self.track, **FFMPEG_OPTIONS)
            voice_client.play(source)
            button.label = 'Stop'
            button.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
        else:
            voice_client.stop()
            button.label = 'Play'
            button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Stop session', style=discord.ButtonStyle.primary)
    async def Delete_Message(self, interaction: discord.Interaction, button: discord.ui.Button):
        global music_play_session
        music_play_session = False
        connection = interaction.client.voice_clients
        if connection:
            if connection[0].is_playing():
                connection[0].stop()
            # await connection[0].disconnect(force=False)
            await interaction.response.send_message(f"Session Closed", ephemeral=False)
        await interaction.message.delete()

    async def on_timeout(self) -> None:
        global music_play_session
        if music_play_session:
            await self.interaction.delete_original_response()
        music_play_session = False


@bot.tree.command(name="play", description="Play songs from YouTube")
@app_commands.describe(song='Song name')
async def play(interaction: discord.Interaction, song: str, volume: app_commands.Range[int, 0, 100] = None):
    global music_play_session
    if music_play_session:
        await interaction.response.send_message("A song is already playing.", ephemeral=True)
        return
    volume = 40 if volume is None else volume
    # Join Channel
    try:
        channel = interaction.user.voice.channel
    except AttributeError:
        await interaction.response.send_message("Could not Open", ephemeral=True)
        return

    await interaction.response.defer()
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{song}", download=False)
        if 'entries' in info:
            info = info['entries'][0]
        track = info['url']
        url = info['original_url']
        title = info['title']
        voice_client = await JoinChannel(interaction, channel_to_join=channel, respond=False)
        source = await discord.FFmpegOpusAudio.from_probe(track, **FFMPEG_OPTIONS)
        voice_client.play(source)

        await interaction.followup.send(f"Testing {song}", ephemeral=True)
    # Create PLayer

        view = MusicPlayerButtons(track=track, interaction=interaction)
        view.add_item(discord.ui.Button(label='Link', url=url, style=discord.ButtonStyle.link))
        # Create Embed
        embed = discord.Embed(
            title=" <:YouTube:1065217286518083666> YouTube Player",
            description=f'Playing: {title}',
            url=url,
            color=0xd02905
        )
        embed.add_field(name='Duration', value=f'{datetime.timedelta(seconds=info["duration"])}')
        embed.set_thumbnail(url=info['thumbnail'])
        embed.set_image(url=info.get('thumbnail'))
        await interaction.followup.send(embed=embed, view=view)
        # Update Interaction
        view.interaction = interaction
        music_play_session = True


async def on_ending_session(interaction: discord.Interaction, volume):
    global music_play_queue, music_play_session
    queue_length = len(music_play_queue.keys())
    await asyncio.sleep(1)
    while queue_length != 0:
        await asyncio.sleep(1)
        if not music_play_session:
            song_from_queue = list(music_play_queue.keys())[0]
            print(f'A Music session has stopped by {interaction.user.name}, trying to play {song_from_queue}')
            # setup player
            await play(interaction, song_from_queue, volume)


@bot.tree.command(name="queue", description="Queue a song from YouTube")
@app_commands.describe(song='Song name')
async def queue(interaction: discord.Interaction, song: str = None, volume: app_commands.Range[int, 0, 100] = None):
    global music_play_queue
    if not song:
        queue_length = len(music_play_queue.keys())
        if queue_length > 0:
            queue_list = "\n".join([f"{i + 1}. {song}" for i, song in enumerate(music_play_queue.keys())])
            embed = discord.Embed(
                title="Bot Queue",
                description=queue_list,
                color=0xd02905
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No songs on queue", ephemeral=True)
        return
    global music_play_session
    if not music_play_session:
        await interaction.response.send_message("Use /play to play the song", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    if song in music_play_queue.keys():
        await interaction.response.send_message("Song is already on queue.")
        return

    music_play_queue[song] = volume
    print(list(music_play_queue.keys()))
    await interaction.followup.send(f"Added {song} to the queue.")

    await asyncio.create_task(on_ending_session(interaction, volume))