import discord 
from app.data import stringVars # VB is the name of the root directory
from discord.ext import commands

class Owneronly(commands.Cog) :
	def __init__(self,client):
		self.client = client

	@commands.command(aliases = ['LoadCog','LC','lc'],description = stringVars.Des_help_ping)
	@commands.is_owner()
	async def loadcog(self,ctx,extension) :
		try :
			self.client.load_extension(f'cogs.{extension}')
			await ctx.reply(f'Loaded {extension}')
		except Exception as error :
			Err_embed=discord.Embed(
				title="Run time error!!!!",
				description = 'This error occured when you invoked a command',
				color=0xFF5733
			)
			Err_embed.add_field(name='Error message',value=error)
			Err_embed.add_field(name='Contact Bot owner',value=stringVars.errCriticalError)
			await ctx.reply(embed = Err_embed)

	@commands.command(aliases = ['UnLoadCog','ULC','ulc'],description = stringVars.Des_help_ping)
	@commands.is_owner()
	async def unloadcog(self,ctx,extension) :
		try :
			self.client.unload_extension(f'cogs.{extension}')
			await ctx.reply(f'Unloaded {extension}')
		except Exception as error :
			Err_embed=discord.Embed(
				title="Run time error!!!!",
				description = 'This error occured when you invoked a command',
				color=0xFF5733
			)
			Err_embed.add_field(name='Error message',value=error)
			Err_embed.add_field(name='Contact Bot owner',value=stringVars.errCriticalError)
			await ctx.reply(embed = Err_embed)

def setup(client) :
	client.add_cog(Owneronly(client))