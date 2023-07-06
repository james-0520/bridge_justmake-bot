import discord
from discord.ext import commands

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.EW_win_edition=0
        self.NS_win_edition=0
        self.channel=0
        self.bridge_people=0
        self.jm_people=0 
        self.king_color=""
        self.set_people = 0
        self.trickcount = 0



