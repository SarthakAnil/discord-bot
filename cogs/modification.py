import discord 
from app.data import stringVars 
from discord.ext import commands
from app.data.mongoDB import dbCollection
import traceback
import asyncio

class Setups(commands.Cog) :
	def __init__(self,client):
		self.client = client
	
	@commands.command(name = 'setPrefix' ,aliases =['sp'] , help = stringVars.help_setPrefix,description = stringVars.Des_help_setPrefix)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def setPrefix(self,ctx,prefix='.app '):
		myquery = { "guild_id": ctx.guild.id }
		newvalues = { '$set': { "Prefix": prefix } }
		dbCollection.update_one(myquery, newvalues)
		await ctx.send (f'"{prefix}" is set as your new prefix')

	@commands.command(help = stringVars.help_delete,description = stringVars.Des_help_delete)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def delete(self,ctx,listeningC : discord.TextChannel):
		guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
		
		if	listeningC.id not in guild_info['Listening'] :
			Err_embed=discord.Embed(
				title="Opps You did a mistake!!!!",
				description = f'{listeningC.mention} is not listed as a listening channel in the DB',
				color=0xFF5733
			)
			await ctx.reply(embed = Err_embed)
			return
		
		for i in range (len(guild_info['Listening'])): 
			if guild_info['Listening'][i] == listeningC.id :
				guild_info['Listening'].pop(i)
				break
		
		forwardingC = guild_info['Listining_forwarding'].pop(str(listeningC.id)) 
		generalC = guild_info['Listining_general'].pop(str(listeningC.id),None) 
		verifiedC = guild_info['Listining_verified'].pop(str(listeningC.id),None) 
		dbCollection.update_many(
			{"guild_id" : ctx.guild.id},
				{"$set": {	"Listening" : guild_info['Listening'], 
							"Listining_forwarding" : guild_info['Listining_forwarding'], 
							"Listining_general" : guild_info['Listining_general'], 
							"Listining_verified" : guild_info['Listining_verified']
							}
				}
		)
		if verifiedC == None and generalC == None :
			await ctx.reply(stringVars.delSetupLFDelete.format(
														listeningC.mention,
														self.client.get_channel(forwardingC).mention,))
		else: 
			await ctx.reply(stringVars.delSetupDelete.format(
														listeningC.mention,
														self.client.get_channel(forwardingC).mention,
														self.client.get_channel(verifiedC).mention ,
														self.client.get_channel(generalC).mention )
														)



	@commands.command(help = stringVars.help_setup,description = stringVars.Des_help_setup)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def setup(self,ctx,listeningC : discord.TextChannel,
						forwardingC : discord.TextChannel,
						verifiedC : discord.TextChannel = None,
						generalC : discord.TextChannel = None
						):

		guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
		if	listeningC.id in guild_info['Listening'] :
			Err_embed=discord.Embed(
				title="Action Not permited",
				description = stringVars.setupLCexist.format(listeningC.mention),
				color=0xFF5733
			)
			await ctx.reply(embed = Err_embed)
			return
		
		guild_info['Listening'].append(listeningC.id)
		guild_info['Listining_forwarding'][str(listeningC.id)] = forwardingC.id
		guild_info['Listining_general'][str(listeningC.id)] = generalC.id 
		guild_info['Listining_verified'][str(listeningC.id)] = verifiedC.id 
		dbCollection.update_many(
		{"guild_id" : ctx.guild.id},
			{"$set": {"Listening" : guild_info['Listening'], 
			"Listining_forwarding" : guild_info['Listining_forwarding'], 
			"Listining_general" : guild_info['Listining_general'], 
			"Listining_verified" : guild_info['Listining_verified']
			}
		}
		)
		await ctx.reply(stringVars.setupDone.format(listeningC.mention,forwardingC.mention,verifiedC.mention,generalC.mention))

	@commands.command(aliases =['setuplf'] ,help = stringVars.help_setupLF,description = stringVars.Des_help_setupLF)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def setupLF(self,ctx,listeningC : discord.TextChannel,
						forwardingC : discord.TextChannel
						):

		guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
		if	listeningC.id in guild_info['Listening'] :
			Err_embed=discord.Embed(
				title="Action Not permited",
				description = stringVars.setupLCexist.format(listeningC.mention),
				color=0xFF5733
			)
			await ctx.reply(embed = Err_embed)
			return
		
		guild_info['Listening'].append(listeningC.id)
		guild_info['Listining_forwarding'][str(listeningC.id)] = forwardingC.id
		dbCollection.update_many(
		{"guild_id" : ctx.guild.id},
			{"$set": {"Listening" : guild_info['Listening'], 
			"Listining_forwarding" : guild_info['Listining_forwarding'], 
			}
		}
		)
		await ctx.reply(stringVars.setupLFDone.format(listeningC.mention,forwardingC.mention))



def setup(client) :
	client.add_cog(Setups(client))