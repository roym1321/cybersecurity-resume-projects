from Init_Bot import bot
import discord


@bot.tree.command(name="anonymous", description="Send anonymous messages")
async def anonymous(interaction: discord.Interaction, user: discord.User, message: str):
    if user == bot.user:
        await interaction.response.send_message(f"I cannot send a message to myself you silly goose",
                                                ephemeral=True)
        return

    try:
        if not user.dm_channel:
            await user.create_dm()
        embed = discord.Embed(title='Hey! Someone wanted me to send you this message:', description=message)
        await user.dm_channel.send(embed=embed)
        await interaction.response.send_message(f"The message has been sent to {user}!", ephemeral=True)
        print(f'{interaction.user.name} sent an anonymous message to {user}')
    except discord.Forbidden:
        await interaction.response.send_message(f"Could not send to {user}, probably because he blocked DMs from "
                                                f"server members.",
                                                ephemeral=True)
        return
    except Exception as e:
        if str(e).endswith("Cannot send messages to this user"):
            print(e)
            await interaction.response.send_message(f"Cannot send messages to this user",
                                                    ephemeral=True)
        else:
            print(f"An error has occurred while {interaction.user.name} tried to send an anonymous message to {user.name}")
            print(e)
            await interaction.response.send_message(f"An error has occurred",
                                                    ephemeral=True)
