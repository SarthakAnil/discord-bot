import discord
import sys
import asyncio
from app.data import stringVars
from app.data.mongoDB import dbCollection
from discord.ext import commands
import traceback

class Messaging(commands.Cog) :
	def __init__(self,client):
		self.client = client

	@commands.command(help = stringVars.help_dm,description = stringVars.Des_help_dm)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	async def dm(self,ctx, member: discord.Member, *, message=None):
		def check(message):
				return message.author.id == ctx.message.author.id and message.content != ""
		
		Err_embed=discord.Embed(
				title="Opps You did a mistake!!!!",
				color=0xFF5733
			)
		MgsL_embed=discord.Embed(
				title="List of messages stored in DB",
				color=0xFF5733
			)
		mention_arr = [] 	#to send list of mentions as normal text
		try :
			if member == self.client.user :
				
				if message ==None :
					Err_embed.add_field(name = 'Hmm.. I got nothing!!',value=stringVars.dmErrNomsg,inline=False )
					await ctx.reply(embed = Err_embed)
				
				elif message == 'msglist' :
					guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
					
					for i in  range (len(guild_info['msgList'])) :
						MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i] ,inline=False ) 
					
					await ctx.send(embed = MgsL_embed)
				
				elif message == 'delete' :
					guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
					
					if len(guild_info['msgList']) == 1 :
						Err_embed.add_field(name = 'Not Allowed',value='You simply cannot delete every message in the DB',inline=False )
						await ctx.reply(embed = Err_embed)
						return
					
					for i in  range (len(guild_info['msgList'])) :
						MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i] ,inline=False ) 
					
					await ctx.send("Which one You wish to delete?", embed = MgsL_embed)
					reply_message = await self.client.wait_for("message", timeout=60, check=check)
					
					if (int(reply_message.content) <= len(guild_info['msgList'])) :
						guild_info['msgList'].pop(int(reply_message.content))
						dbCollection.update_one({"guild_id" : ctx.guild.id},{"$set": {"msgList" : guild_info['msgList']}})
						await ctx.reply("Message deleted from DB")
					
					else:
						Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrNotInDB,inline=False )
						await ctx.reply(embed = Err_embed)

				else :
					guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
					guild_info['msgList'].append(message)
					dbCollection.update_one({"guild_id" : ctx.guild.id},{"$set": {"msgList" : guild_info['msgList']}})
					guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
					
					for i in  range (len(guild_info['msgList'])) :
						MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i],inline=False  ) 
					
					await ctx.send(f"{message} added to Message List.",embed = MgsL_embed)
			
			elif message == None:
				guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
				
				for i in  range (len(guild_info['msgList'])) :
					MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i],inline=False ) 
				
				await ctx.send("Select a message to send:",embed = MgsL_embed)
				reply_message = await self.client.wait_for("message", timeout=60, check=check)
				
				if (int(reply_message.content) <= len(guild_info['msgList'])) :
					message_embed = discord.Embed(
						title=f"Message From {ctx.guild.name}",
						description = guild_info['msgList'][int(reply_message.content)],
						color=0xFF5733
					)
					message_embed.add_field(name= 'Initiated by :' ,value= ctx.message.author.mention)
					message_embed.set_author(
						name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
						icon_url=ctx.message.author.avatar_url
					)
					
					for word in guild_info['msgList'][int(reply_message.content)].split(" ")  :
						if word != '' :
							if word[0] =='<' :
								mention_arr.append(word)
					
					message_embed.set_footer(text=stringVars.dmFooter)
					await member.send(' '.join(mention_arr) , embed = message_embed)
					await ctx.reply(f"the folowing has been send to the member {member.mention}\n {' '.join(mention_arr)}\n\n",embed = message_embed)

				else:
					Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrNotInDB,inline=False )
					await ctx.reply(embed = Err_embed)

			else:
				for word in message.split(" ") :
					if word != '' :
						if word[0] =='<' :
							mention_arr.append(word)
				mention_arr.append(ctx.message.author.mention)
				message_embed = discord.Embed(
					title=f"Message From {ctx.guild.name}",
					description = message,
					color=0xFF5733
				)
				message_embed.add_field(name= 'Initiated by :' ,value= ctx.message.author.mention)
				message_embed.set_author(
					name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
					icon_url=ctx.message.author.avatar_url
				)
				message_embed.set_footer(text=stringVars.dmFooter)
				await member.send(f"{' '.join(mention_arr)}\n\n" , embed = message_embed)
				await ctx.reply(f"The folowing has been send to the member {member.mention}\n{' '.join(mention_arr)}",embed = message_embed)
		
		except asyncio.TimeoutError:
			Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrTimeout,inline=False )
			await ctx.reply(embed = Err_embed)
		
		except ValueError:
			Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrInvalidInput,inline=False )
			await ctx.reply(embed = Err_embed)
		
		except:
			Err_embed=discord.Embed(
				title="Run time error!!!!",
				description = 'This error was missed during beta test',
				color=0xFF5733
			)
			Err_embed.add_field(name ='Trace Back' ,value= traceback.format_exc() ,inline=False )
			Err_embed.add_field(name='Contact Bot owner',value=stringVars.errCriticalError)
			await ctx.reply(embed = Err_embed)

	@commands.command(help = stringVars.help_send,description = stringVars.Des_help_send)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True, manage_roles =True)
	async def send(self,ctx ,channel :discord.TextChannel , *, message=None):
		def check(message):
				return message.author.id == ctx.message.author.id and message.content != ""
		
		Err_embed=discord.Embed(
				title="Opps You did a mistake!!!!",
				color=0xFF5733
			)
		MgsL_embed=discord.Embed(
				title="List of messages stored in DB",
				color=0xFF5733
			)
		mention_arr = []
		try :
			if message ==None:
				guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
				
				for i in  range (len(guild_info['msgList'])) :
					MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i],inline=False ) 
				
				await ctx.send("Select a message to send:\n" , embed = MgsL_embed)
				reply_message = await self.client.wait_for("message", timeout=60, check=check)
				
				if (int(reply_message.content) <= len(guild_info['msgList'])) :
					message_embed = discord.Embed(
						title="Info",
						description = guild_info['msgList'][int(reply_message.content)],
						color=0xFF5733
					)
					message_embed.set_author(
						name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
						icon_url=ctx.message.author.avatar_url
					)
					
					for word in guild_info['msgList'][int(reply_message.content)].split(" ") :
						if word != '' :
							if word[0] =='<' :
								mention_arr.append(word)
					
					await channel.send(' '.join(mention_arr),embed = message_embed)
					await ctx.reply(f"The folowing has been send to the channel {channel.mention}\n {' '.join(mention_arr)}" ,embed = message_embed)

				else:
					Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrNotInDB,inline=False )
					await ctx.reply(embed = Err_embed)

			else:
				message_embed = discord.Embed(
					title=f"Info",
					description = message,
					color=0xFF5733
				)
				message_embed.set_author(
					name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
					icon_url=ctx.message.author.avatar_url
				)
				for word in guild_info['msgList'][int(reply_message.content)].split(" ") :
					if word != '' :
						if word[0] =='<' :
							mention_arr.append(word)
				await channel.send(' '.join(mention_arr),embed = message_embed)
				await ctx.reply(f"The folowing has been send to the channel {channel.mention}\n {' '.join(mention_arr)}" ,embed = message_embed)

		except asyncio.TimeoutError:
			Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrTimeout,inline=False )
			await ctx.reply(embed = Err_embed)
		
		except ValueError:
			Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrInvalidInput,inline=False )
			await ctx.reply(embed = Err_embed)
		
		except:
			Err_embed=discord.Embed(
				title="Run time error!!!!",
				description = 'This error was missed during beta test',
				color=0xFF5733
			)
			Err_embed.add_field(name ='Trace Back' ,value= traceback.format_exc() ,inline=False )
			Err_embed.add_field(name='Contact Bot owner',value=stringVars.errCriticalError)
			await ctx.reply(embed = Err_embed)	
		
def setup(client) :
	client.add_cog(Messaging(client))