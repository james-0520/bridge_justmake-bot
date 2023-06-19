import discord
from discord.ext import commands

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.a_win_edition=0
        self.b_win_edition=0
        self.channel=0
        self.people=0



