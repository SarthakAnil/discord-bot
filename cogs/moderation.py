import discord
import sys
import asyncio
from app.data import stringVars 
from app.data.mongoDB import dbCollection
from discord.ext import commands


class Moderation(commands.Cog) :
	
	def __init__(self,client):
		self.client = client
	
	class MemberRoles(commands.MemberConverter):
		async def convert(self, ctx, argument):
			member = await super().convert(ctx, argument)
			return [role.name for role in member.roles[1:]] 
	
	@commands.command(help = stringVars.help_roles,description = stringVars.Des_help_roles)
	@commands.guild_only()
	async def roles(self,ctx, *, member : MemberRoles) :
		await ctx.send('I see the following roles: ' + ', '.join(member))

	@commands.command(aliases = ['gr','giverole','GiveRole'],help = stringVars.help_gr,description = stringVars.Des_help_gr)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True, manage_roles =True)
	async def giveRole(self,ctx ,member :discord.Member ,role :discord.Role ) :
		await member.add_roles(role)
		await ctx.reply(f'{ctx.message.author.mention} gave  {member.mention} {role.mention} role')

	@commands.command(aliases = ['rr','removerole','RemoveRole'],help = stringVars.help_rr,description = stringVars.Des_help_rr)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True, manage_roles =True)
	async def removeRole(self,ctx ,member :discord.Member ,role :discord.Role ) :
		await member.remove_roles(role)
		await ctx.reply(f'{ctx.message.author.mention} removed  {role.mention} role from  {member.mention} ')
		
	@commands.command(aliases =['v'] ,help = stringVars.help_verify,description = stringVars.Des_help_verify)
	@commands.guild_only()
	@commands.has_permissions(manage_guild=True, manage_roles =True)
	async def verify(self,ctx ,member :discord.User, role :discord.Role ,channel :discord.TextChannel,*, message=None):
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
		mention_arr =[member.mention]
		if message ==None:
			try:
				guild_info = dbCollection.find_one({"guild_id" : ctx.guild.id})
				
				for i in  range (len(guild_info['msgList'])) :
					MgsL_embed.add_field(name= f'{i} :' ,value= guild_info['msgList'][i],inline=False ) 
				
				await ctx.send("Select a message to send:",embed = MgsL_embed)
				reply_message = await self.client.wait_for("message", timeout=60, check=check)
				
				if (int(reply_message.content) <= len(guild_info['msgList'])) :
					message_embed = discord.Embed(
					title="Congragulations You have been verified",
					description = f'{member.mention} you have been verified in {ctx.guild.name}',
					color=0xFF5733
					)
					message_embed.set_author(
						name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
						icon_url=ctx.message.author.avatar_url
					)
					if (int(reply_message.content) != -1) :
						message_embed.add_field(name = 'Important',value=guild_info['msgList'][int(reply_message.content)],inline=False )
					
					for word in guild_info['msgList'][int(reply_message.content)].split(" "):
						if word != '' :
							if word[0] =='<' :
								mention_arr.append(word)
					
					await channel.send(' '.join(mention_arr) ,embed = message_embed  )
					await ctx.reply(f"The folowing has been send to the channel {channel.mention} \n{' '.join(mention_arr)}" ,embed = message_embed)
					mention_arr.append(channel.mention)
					message_embed.set_footer(text=stringVars.dmFooter )
					await member.send(' '.join(mention_arr) ,embed = message_embed)

				else:
					Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrNotInDB,inline=False )
					await ctx.reply(embed = Err_embed)
			except asyncio.TimeoutError:
				Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrTimeout,inline=False )
				await ctx.reply(embed = Err_embed)
			except ValueError:
				Err_embed.add_field(name = stringVars.dmErrFail,value=stringVars.dmErrInvalidInput,inline=False )
				await ctx.reply(embed = Err_embed)
		else:
			message_embed = discord.Embed(
					title="Congragulations You have been verified",
					description = f'{member.mention} you have been verified in {ctx.guild.name}',
					color=0xFF5733
					)
			message_embed.set_author(
				name=(f'{ctx.message.author.display_name}#{ctx.message.author.discriminator}'), 
				icon_url=ctx.message.author.avatar_url
			)
			message_embed.add_field(name = 'Important',value=message,inline=False )
			
			for word in message.split(" "):
				if word != '' :
							if word[0] =='<' :
								mention_arr.append(word)
			
			message_embed.add_field(name = 'Important',value=f"Check out {channel.mention} in {ctx.guild.name}",inline=False )
			await channel.send(' '.join(mention_arr) , embed = message_embed)
			await ctx.reply(f"The folowing has been send to the channel {channel.mention} \n{' '.join(mention_arr)}" ,embed = message_embed)
			message_embed.set_footer(text=stringVars.dmFooter )
			mention_arr.append(channel.mention)
			await member.send(' '.join(mention_arr) ,embed = message_embed)
		await member.add_roles(role)



def setup(client) :
	client.add_cog(Moderation(client))















'''

#------------------------------------------------------------------------------------------------------------------
#To find the roles of a menber
@client.command(help = stringVars.help_roles)
@commands.guild_only()
async def roles(ctx, *, member : MemberRoles):
	await ctx.send('I see the following roles: ' + ', '.join(member))

'''