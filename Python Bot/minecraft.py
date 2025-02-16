import discord
from Init_Bot import bot
from mcstatus import JavaServer
from Tokens import MINECRAFT_IP


class Delete_Button(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.timeout = 180
        self.interaction = interaction
        self.is_deleted = False

    @discord.ui.button(label='Delete Messsage', style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        self.is_deleted = True

    async def on_timeout(self) -> None:
        if not self.is_deleted:
            self.delete.disabled = True
            await self.interaction.edit_original_response(embed=None, view=self)
            # await self.interaction.delete_original_response()


# class delete_button(discord.ui.Button):
#     def __init__(self):
#         super().__init__(label="Delete Messsage", style=discord.ButtonStyle.danger)
#
#     async def callback(self, interaction: discord.Interaction):
#         await interaction.message.delete()


@bot.tree.command(name="minecraft", description="Minecraft Server Status")
async def minecraft(interaction: discord.Interaction):
    try:
        server = JavaServer.lookup(MINECRAFT_IP)
        status = server.status()
    except:
        await interaction.response.send_message("Could not retrieve server information", ephemeral=True)
        return
    if status.players.sample:
        Online_players = "\n".join([f"{i + 1}. {player.name}" for i, player in enumerate(status.players.sample)])
    else:
        Online_players = "No Online Players"

    msg_ui = discord.Embed(
        title=f"Minecraft Server <a:PEPEMinecraft:1080590782181933168>",
        description=f"The server has {status.players.online} player(s) online",
        color=0x2DFA4D,
    )
    msg_ui.set_thumbnail(url="https://cdna.artstation.com/p/assets/images/images/027/406/726/large/ilya-vdovyuk-5.jpg?1591446999")
    msg_ui.add_field(name='Online Players', value=Online_players, inline=True)
    msg_ui.add_field(name="IP", value=f"{server.address.host}:{server.address.port}")
    msg_ui.set_image(url="https://i.ibb.co/tJ6RnNh/2023-03-01-23-21-48.png")
    msg_ui.set_footer(text=status.description, icon_url="https://cdn3.emoji.gg/emojis/7171-minecraft-sheep-spinning.gif")
    # view = discord.ui.View()
    # view.add_item(delete_button())
    await interaction.response.send_message(embed=msg_ui, view=Delete_Button(interaction), ephemeral=True)

"""

You can pass the same address you'd enter into the address field in minecraft into the 'lookup' function
If you know the host and port, you may skip this and use JavaServer("example.org", 1234)

'status' is supported by all Minecraft servers that are version 1.7 or higher.
Don't expect the player list to always be complete, because many servers run
plugins that hide this information or limit the number of players returned or even
alter this list to contain fake players for purposes of having a custom message here.


'ping' is supported by all Minecraft servers that are version 1.7 or higher.
It is included in a 'status' call, but is also exposed separate if you do not require the additional info.
latency = server.ping()
print(f"The server replied in {latency} ms")


'query' has to be enabled in a server's server.properties file!
It may give more information than a ping, such as a full player list or mod information.
query = server.query()
print(query.players)
print(f"The server has the following players online: {', '.join(query.players.names)}")

"""

