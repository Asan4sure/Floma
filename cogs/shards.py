import discord
import logging
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class ready(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = discord.Colour.green()

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        logging.info("Shard #%s is ready" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        logging.info("Shard #%s has connected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        logging.info("Shard #%s has disconnected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_resume(self, shard_id):
        logging.info("Shard #%s has resumed" % (shard_id))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        missing = " | ".join(error.args)
        await ctx.send(f"{missing}", delete_after=10)
      elif isinstance(error, commands.MissingPermissions):
        missing_perms = " | ".join(error.missing_perms)
        await ctx.send(f"You don't have the {missing_perms} permisisons to run the **{ctx.command.name}** command!", delete_after=10)
      elif isinstance(error, commands.MemberNotFound):
          await ctx.send(f"Please provide a member!", delete_after=10)
      elif isinstance(error, commands.NSFWChannelRequired):
        em6 = discord.Embed(description=f"Please first enable NSFW Channel in this channel!", color = discord.Colour.dark_red(), timestamp=ctx.message.created_at)
        em6.set_image(url=f"https://i.imgur.com/oe4iK5i.gif")

        await ctx.send(embed=em6, delete_after=10)
      elif isinstance(error, commands.BotMissingPermissions):
        missing = " | ".join(error.missing_perms)
        await ctx.send(f'I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
      elif isinstance(error, commands.CommandNotFound):
        print(" ")
      else:
        raise error

def setup(client):
  client.add_cog(ready(client))