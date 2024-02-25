from __future__ import annotations

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import motor.motor_asyncio as mongodb

SUCCESS = discord.PartialEmoji(name='sucess', id=961833947417944135)
TICK = discord.PartialEmoji(name='Tick', id=958955009855336558)
CANCEL = discord.PartialEmoji(name='cancel', id=961830994648911872)

def clean_code(content):
    if content.startswith('```') and content.endswith('```'):
        return "\n".join(content.split("\n")[1:][:-3])
    else:
        return content

class Pag():
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass
class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/Flame?retryWrites=true&w=majority")
        self.db = self.connection["Zeon"]["servers"]

    """Autorole commands"""  

    def help_custom(self):
		      emoji = '<a:uw_white_heart:958722698228412486>'
		      label = "Autorole"
		      description = "Shows all Autorole Commands"
		      return emoji, label, description   

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            if not member._roles.has(role):
                await member.add_roles(role, reason="Auto Role")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if data := await self.db.find_one(
            {"guild": member.guild.id}
        ):
            for role in data.get("autorole", []):
                await self.add_role(role=role, member=member)

            if member.bot:
                for role in data.get("bots", []):
                    await self.add_role(role=role, member=member)
            else:
                for role in data.get("humans", []):
                    await self.add_role(role=role, member=member)

# Schema: {"guild": INT, "bots": LIST, "humans": LIST, "autorole": []}

    @commands.group(invoke_without_command=True)
    async def autorole(self, ctx: commands.Context):
        ...

    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def humans(self, ctx, *, r: discord.Role):
        if data := await self.db.find_one(
            {"guild": ctx.guild.id,}, 
        ):
            if len(data.get("humans", [])) > 2:
                return await ctx.send(f"{CANCEL} | Autorole Humans Limit Reached")

            await self.db.update_one(
                {"guild": ctx.guild.id}, {"-addToSet": {"humans": r.id}}, upsert=True
            )
            await ctx.send(f"{SUCCESS} | Autorole Humans Updated to `{r.name}`")
    
    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, r: discord.Role):

        if data := await self.db.find_one(
            {"guild": ctx.guild.id,}, 
        ):
            if len(data.get("autorole", [])) > 2:
                return await ctx.send(f"{CANCEL} | Autorole Limit Reached")

            await self.db.update_one(
                {"guild": ctx.guild.id}, {"-addToSet": {"autorole": r.id}}, upsert=True
            )
            await ctx.send(f"{SUCCESS} | Autorole Updated to `{r.name}`")

    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def bots(self, ctx, *, r: discord.Role):
        if data := await self.db.find_one(
            {"guild": ctx.guild.id,}, 
        ):
            if len(data.get("bots", [])) > 2:
                return await ctx.send(f"{CANCEL} | Autorole Bots Limit Reached")

            await self.db.update_one(
                {"guild": ctx.guild.id}, {"-addToSet": {"bots": r.id}}, upsert=True
            )
            await ctx.send(f"{SUCCESS} | Autorole Bots Updated to `{r.name}`")

    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: commands.Context):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "-set": {
                    "autorole": []
                }
            }
        )
        await ctx.send(f"{TICK} | Successfully Deleted All Autorole")

    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def botsdelete(self, ctx: commands.Context):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "-set": {
                    "bots": []
                }
            }
        )    
        await ctx.send(f'{TICK} | Successfully Deleted All Bots Autorole')
  
    @autorole.command()
    @commands.has_permissions(administrator=True)
    async def humansdelete(self, ctx: commands.Context):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "-set": {
                    "humans": []
                }
            }
        )
        await ctx.send(f'{TICK} | Successfully Deleted All Humans Autorole')


def setup(bot):
    bot.add_cog(Welcomer(bot))