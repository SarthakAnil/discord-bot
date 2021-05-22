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
	async def delete(self,ctx,listeningC : discord.TextChannel = None):
		guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
		
		if listeningC != None:
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
		else:
			def check(message):
				return message.author.id == ctx.message.author.id and message.content != ""

			Err_embed=discord.Embed(
				title="Opps You did a mistake!!!!",
				color=0xFF5733
			)
			MgsL_embed=discord.Embed(
				title="List of Listening channels stored in DB",
				color=0xFF5733
			)
			try :	
				for i in range (len(guild_info['Listening'])): 
					MgsL_embed.add_field(name= f'{i} :' ,value= self.client.get_channel(guild_info['Listening'][i]).mention ,inline=False )
				
				await ctx.send("Which one You wish to delete?", embed = MgsL_embed)
				reply_message = await self.client.wait_for("message", timeout=60, check=check)
				
				if (int(reply_message.content) <= len(guild_info['Listening'])) :
						listeningC = guild_info['Listening'].pop(int(reply_message.content))
						forwardingC = guild_info['Listining_forwarding'].pop(str(listeningC)) 
						generalC = guild_info['Listining_general'].pop(str(listeningC),None) 
						verifiedC = guild_info['Listining_verified'].pop(str(listeningC),None) 
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
																		self.client.get_channel(listeningC).mention,
																		self.client.get_channel(forwardingC).mention,))
						else: 
							await ctx.reply(stringVars.delSetupDelete.format(
																		self.client.get_channel(listeningC).mention,
																		self.client.get_channel(forwardingC).mention,
																		self.client.get_channel(verifiedC).mention ,
																		self.client.get_channel(generalC).mention )
																		)
								
				else:
					Err_embed.add_field(name = stringVars.delFail,value=stringVars.delFailNotinDB,inline=False )
					await ctx.reply(embed = Err_embed)
			
			except asyncio.TimeoutError:
				Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrTimeout,inline=False )
				await ctx.reply(embed = Err_embed)
			
			except ValueError:
				Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrInvalidInput,inline=False )
				await ctx.reply(embed = Err_embed)


	@commands.command(help = stringVars.help_setup,description = stringVars.Des_help_setup)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def setup(self,ctx,listeningC : discord.TextChannel,
						forwardingC : discord.TextChannel,
						verifiedC : discord.TextChannel ,
						generalC : discord.TextChannel 
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