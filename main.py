import discord
from discord.ext import commands
import json
import os
from core.classes import Cog_Extension
import keep_alive

#開啟json檔
with open('background_setting.json', "r", encoding="utf8") as jfile:
	jdata = json.load(jfile)

#前綴詞為[
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="[",intents = intents)

############to do: a-NS,b-WE NoTrump  
@bot.event
async def on_ready():
	print("bot is online")

@bot.command()
async def load(ctx, extension):
	bot.load_extension(F'cmds.{extension}')
	await ctx.send(F'{extension} loaded')

@bot.command()
async def reload(ctx, extension):
	bot.reload_extension(F'cmds.{extension}')
	await ctx.send(F'{extension} reloaded')

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(F'cmds.{extension}')
	await ctx.send(F'{extension} unloaded')


@bot.command()
async def message(ctx, id):
	user = ctx.author
	context = await user.fetch_message(id)
	print("message get")
	await context.delete()


for filename in os.listdir('cmds'):
	if filename.endswith(".py"):
		bot.load_extension(F"cmds.{filename[:-3]}")#去掉.py
		print('loaded')

if __name__ == "__main__":
	#keep_alive.keep_alive()
	bot.run("MTExMDU2NDAxMjcxMTc1MTY4MA.G014p8.FbWsEquJObyVSupZ9njVtGQR0_5hd_MdORGoLw")
