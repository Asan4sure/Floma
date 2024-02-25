import discord
from discord.ext import commands
import json

class fun87(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway commands"""
  
    def help_custom(self):
		      emoji = '<a:giveaways:1208688340736409670> '
		      label = "Giveaway"
		      description = ""
		      return emoji, label, description
#')

    # now make a command where the server owner can change the channel for leveling.
    @commands.group()
    async def __Giveaway__(self, ctx: commands.Context):
        """• `gstart <time> <winners> <msg, prize>`, `greroll <msgid>`, `gend <msgid>` """
       # await ctx.send('leveling is under construction.')
    

    
    #@commands.command()
    ##async def level(self, ctx: commands.Context, user: discord.Member):
     #   with open('./data/databases/leveling.json', 'r') as f:
           # leveling = json.load(f)
       # await ctx.send(f'{user.mention} is currently level {leveling[str(user.id)]["level"]}.')

def setup(client):
    client.add_cog(fun87(client))