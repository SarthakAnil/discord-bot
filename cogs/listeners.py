import discord 
from app.data import stringVars
from app.data.mongoDB import dbCollection
from discord.ext import commands

class Listeners(commands.Cog) :
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self) :
		print("cog bot ready !!")

	@commands.Cog.listener()
	async def on_guild_join(self,guild):
		guild_info ={
			"guild_id"  : guild.id,
			"Prefix"	: '.discord-bot ',
			"Listening" : [],
			"Listining_forwarding" :{},
			"Listining_general" :{},
			"Listining_verified" :{},
			"msgList" : [f'Please contact the moderators of {guild.name}']
		}
		dbCollection.insert_one(guild_info)
	
	@commands.Cog.listener()
	async def on_guild_remove(self,guild):
		dbCollection.delete_one({"guild_id" : guild.id})
	
	
	
	@commands.Cog.listener()
	async def on_command_error(self,ctx,error):

		if isinstance(error,commands.CommandNotFound) :
			Err_embed=discord.Embed(
				title="Invalid Command",
				description = stringVars.errCmdNotFound,
				color=0xFF5733
			)
			await ctx.reply(embed = Err_embed)
			
		
		elif isinstance(error, commands.MemberNotFound) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			Err_embed.add_field(name='What Happened:',value=stringVars.errMemberNotFound)
			Err_embed.add_field(name='FiX:',value=stringVars.errFixValue)
			await ctx.reply(embed = Err_embed)
		
		elif isinstance(error, commands.UserNotFound) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			Err_embed.add_field(name='What Happened:',value=stringVars.errUserNotFound)
			Err_embed.add_field(name='FiX:',value=stringVars.errFixValue)
			await ctx.reply(embed = Err_embed)					

		elif isinstance(error, commands.RoleNotFound) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			Err_embed.add_field(name='What Happened:',value=stringVars.errRoleNotFound)
			Err_embed.add_field(name='FiX:',value=stringVars.errFixValue)
			await ctx.reply(embed = Err_embed)
					
		elif isinstance(error, commands.ChannelNotFound) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			await ctx.reply(embed = Err_embed)

		elif isinstance(error, commands.TooManyArguments) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			Err_embed.add_field(name='What Happened:',value=stringVars.errTooManyArguments)
			Err_embed.add_field(name='FiX:',value=stringVars.errFixValue)
			await ctx.reply(embed = Err_embed)

		elif isinstance(error, commands.MissingRequiredArgument) :
			Err_embed=discord.Embed(
				title=stringVars.oops,
				description = error,
				color=0xFF5733
			)
			Err_embed.add_field(name='What Happened:',value=stringVars.errMissingArguments)
			Err_embed.add_field(name='FiX:',value=stringVars.errFixValue)
			await ctx.reply(embed = Err_embed)
		
		elif isinstance(error, commands.MissingPermissions) :
			await ctx.reply(stringVars.errMissingPerms.format(ctx.message.author.mention))

		else :
			Err_embed=discord.Embed(
				title="Run time error!!!!",
				description = 'This error was missed during beta test',
				color=0xFF5733
			)
			Err_embed.add_field(name='Error message',value=error)
			Err_embed.add_field(name='Contact Bot owner',value=stringVars.errCriticalError)
			await ctx.reply(embed = Err_embed)

	@commands.Cog.listener()
	@commands.guild_only()
	async def on_message(self,message):
		if not message.guild:
			return
		
		if message.author == self.client.user:
			return
		
		guild_info = dbCollection.find_one({"guild_id" : message.guild.id})
		listening_list = [] if guild_info.get('Listening') is None else guild_info.get('Listening')
		
		if message.channel.id in listening_list :
			frwdc = self.client.get_channel(guild_info['Listining_forwarding'][str(message.channel.id)])
			generalC = guild_info.get('Listining_general', {}).get(str(message.channel.id))
			verifiedC = guild_info.get('Listining_general', {}).get(str(message.channel.id))
			
			
			if generalC != None and verifiedC != None :
				embed=discord.Embed(
					title="Verification request",
					description=message.author.mention,
					color=0xFF5733
				) 
				embed.set_author(
					name=(f'{message.author.display_name}#{message.author.discriminator}'), 
					icon_url=message.author.avatar_url
				)
				embed.set_footer(text= message.content)
				
				if len(message.attachments) > 0 :
					embed.set_image(
						url = message.attachments[0].url
					)
					await frwdc.send(message.author.mention,embed=embed)
					await message.channel.send(stringVars.onMsg.format(self.client.get_channel(generalC).mention,
																		self.client.get_channel(verifiedC).mention,
																		message.author.mention))
					await message.author.send(stringVars.onMsg.format(self.client.get_channel(generalC).mention,
																		self.client.get_channel(verifiedC).mention,
																		message.author.mention))
				else:
					await frwdc.send(embed=embed)
					await message.channel.send(stringVars.onMsgNoAttachment.format(message.author.mention))
				
				await message.delete()

			else :
				if len(message.attachments) >0 :
					msg =[message.content]
					
					for ele in message.attachments :
						msg.append(ele.url)
					
					await frwdc.send('\n'.join(msg))
				else :
					msg =[message.content]
					await frwdc.send('\n'.join(msg))
				
				await message.delete()	
		
		#await self.client.process_commands(message) no need in case of cogs

def setup(client) :
	client.add_cog(Listeners(client))


	