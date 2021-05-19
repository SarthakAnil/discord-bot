import discord 
from app.data import stringVars 
from discord.ext import commands
from app.data.mongoDB import dbCollection
import traceback
import asyncio

class Test(commands.Cog) :
	def __init__(self,client):
		self.client = client
	
	@commands.command( help = stringVars.help_ping,description = stringVars.Des_help_ping)
	async def ping(self,ctx):
		await ctx.send (f'Pong! {round(self.client.latency * 1000)}ms')

	








def setup(client) :
	client.add_cog(Test(client))