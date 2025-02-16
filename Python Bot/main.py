import discord
from Tokens import *
from Init_Bot import bot
import openai
import AI
import IdosSoundBoard
import MusicPlayer
import GeneralCommands
import minecraft
import pkg_resources
import anonynous


async def internal_command_prompt():
    test = ''
    while test != 'stop':
        test = input()
        print(test)
    print('stopped')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="A Game",
                                                         game='Some Game',
                                                         url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    await bot.user.edit(username='RoyBot')
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    print(f"{bot.user} is ready")
    # bot.loop.create_task(internal_command_prompt())


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
