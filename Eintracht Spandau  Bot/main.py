import time
import discord
from discord.ext import commands


UiButtonBot = commands.Bot(command_prefix="<", intents=discord.Intents.all())

client = discord.Client

@UiButtonBot.event
async def on_ready():
    print("UI ist startklar")

async def on_message(message):
    if message.author == client.user:
        return

    member_name = "Vollkartoffel"
    if message.author.name == member_name:
        await message.delete()



#----------------------------------
class Menu(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.value = None
        self.bot = bot

    async def start(self, interaction: discord.Interaction):
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Begrüßung", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Heeeyyy, was willst du denn???, ne Beratung oder waass?', file=discord.File("D:/Users/Maurice Töpfer/Pictures/Programmierung/Projekte/Discord Bot/Eintracht Spandau  Bot/Knabe böse.jpg"))
       # await interaction.followup.send("Hey, ich bin Kevin, Sportlicher-Leiter von EINS, wie kann ich dir helfen? ---#Knabe Raus#---")
        time.sleep(5)
        await interaction.delete_original_response()

    @discord.ui.button(label="Hymne", style=discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_author(name=f"Wo die Havel kreuzt die Spree ... Von Berlin aus jwd ... Wo die Zitadelle rockt Und die Altstadt uns lockt ... Da ist Spandau, da sind wir ... Spandau, Spandau, wir lieben dir")
        #embed.add_field(name=f"Momo", value="is dabei")
        await interaction.response.send_message(embed=embed, delete_after=30)

        view = MusicView(self.bot)
        await view.start(interaction=interaction)

    @discord.ui.button(label="Menu Schließen", style=discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


        #self.value = False
        #self.stop()           ---das sorg dafür das man es nur einmal benutzen kann, sprich nach den buttonsdurchlauf endet es


#----------------------------------
class Menu2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="löschen", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Wird gelöscht")


#-----------------------------------
class MusicButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode, bot):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        #await interaction.response.send_message("Song wird abgespielt", delete_after=5)
        voice_channel = discord.utils.get(interaction.guild.voice_channels, name="Lobby")
        await interaction.response.defer()

        voice_client = discord.utils.get(self.bot.voice_clients, channel= voice_channel)
        if voice_client == None:
            voice_client = await voice_channel.connect()

        if self.mode == 0:
            voice_client.play(discord.FFmpegPCMAudio(source="D:/Users/Maurice Töpfer/Pictures/Programmierung/Projekte/Discord Bot/Eintracht Spandau  Bot/Eintracht Spandau Hymne.wav", executable="ffmpeg.exe"))
        elif self.mode == 1:
            voice_client.pause()
        elif self.mode == 2:
            voice_client.resume()
        elif self.mode == 3:
            voice_client.stop()
        else:
            await voice_client.disconnect()
            view = Menu(self.bot)
            await view.start(interaction=interaction)

class MusicView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(MusicButton("Starten", discord.ButtonStyle.green, 0, bot))
        self.add_item(MusicButton("Pausieren", discord.ButtonStyle.blurple, 1, bot))
        self.add_item(MusicButton("Fortsetzen", discord.ButtonStyle.blurple,2, bot))
        self.add_item(MusicButton("Beenden", discord.ButtonStyle.red, 3, bot))
        self.add_item(MusicButton("Menü Schließen", discord.ButtonStyle.red, 4, bot))


    async def start(self, interaction: discord.Interaction):
        await interaction.message.edit(view=self)
#-----------------------------------




@UiButtonBot.command()
async def menu(ctx):
    view = Menu(bot=UiButtonBot)
    view.add_item(discord.ui.Button(label="Eintracht Spandau Twitch Stream", style=discord.ButtonStyle.link, url="https://www.twitch.tv/eintrachtspandau?lang=de"))
    view.add_item(discord.ui.Button(label="Prime League Tabelle", style=discord.ButtonStyle.red, url="https://www.primeleague.gg/coverages/30730-division-1-spring-split-2023"))
    await ctx.reply("Menuübersicht", file=discord.File("D:/Users/Maurice Töpfer/Pictures/Programmierung/Projekte/Discord Bot/Eintracht Spandau  Bot/Eintracht Spandau.png"), view=view)


@UiButtonBot.command()
async def delete(ctx):
    view = Menu2()
    await ctx.channel.purge(limit=None)
    await ctx.reply("Der ganze Chat wird gelöscht", view=view)


@UiButtonBot.command()
async def music(ctx):
    view = MusicView(bot=UiButtonBot)
    await ctx.reply("Musik", view=view)




UiButtonBot.run("MTA4NDA5MjQzODMyMDI1NDk3Ng.G2xL7L.dfU77PicEF1vwqx-f8lZ8J96wzRtpdpMBP_wqU")
