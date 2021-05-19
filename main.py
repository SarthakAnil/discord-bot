import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

#work around for package importing

import discord
from VB.data import mongoDB
#from VB.data import keep_alive
from discord.ext import commands

ignoredFiles = ['stringVars.py','__init__.py']

def get_prefix(client, message): 
	if message.guild == None :
		return '.'
	guild_info = mongoDB.dbCollection.find_one({"guild_id" : message.guild.id})
	return guild_info['Prefix'] 

def loadCogs(client):
	for fileName in os.listdir('./cogs') :
		if fileName.endswith('.py') and fileName not in ignoredFiles :
			client.load_extension(f'cogs.{fileName[:-3]}')

if __name__ == "__main__":
	client = commands.Bot(command_prefix= (get_prefix))
	loadCogs(client)
	#keep_alive.keep_alive()
	client.run(os.getenv('TOKEN'))