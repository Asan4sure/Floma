import discord
import json
from discord.ext import commands
import datetime


IGNORE = [844924055361945620,844924055361945620]

antiSpam = False
antiLink = False
antiWord = True
punishment = "ban"

class Antinuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def ban(self, guild, user, *, reason: str = None):
        try:
            return await self.ban(guild, user, reason=reason)
        except Exception:
            return


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            if entry.user.id in IGNORE:
              return

            elif entry.user.id == guild.owner.id:
              return 

            else:
                await guild.ban(entry.user,
                                   reason="Anti Ban")

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild,
                              user: discord.User) -> None:
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.unban):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await guild.kick(entry.user,
                                   reason="Anti Unban | Not Whitelisted")                                          

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.bot_add):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            if member.bot:
                await member.ban(reason="Floma | Not Whitelisted")
                await guild.ban(entry.user,
                                   reason="Floma | Not Whitelisted")               

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        guild = channel.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.channel_create):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await channel.delete()
                await guild.ban(entry.user,
                                   reason="Anti Channel Create | Not Whitelisted")                       

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)      
        guild = channel.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.channel_delete):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await channel.clone()
                await guild.ban(entry.user,
                               reason="Anti Channel Delete | Not Whitelisted")                  

    @commands.Cog.listener()
    async def on_guild_channel_update(
            self, after: discord.abc.GuildChannel,
            before: discord.abc.GuildChannel) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)              
        name = before.name
        guild = after.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.channel_update):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await after.edit(name=f"{name}", reason=f"Recovery")
                await guild.ban(entry.user,
                                   reason="Anti Channel Update | Not Whitelisted")                     

    @commands.Cog.listener()
    async def on_guild_update(self, after: discord.Guild,
                              before: discord.Guild) -> None:
        guild = after
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.guild_update):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await after.edit(name=f"{before.name}",
                                 reason=f"Recovery")
                await guild.ban(entry.user,
                                  reason="Anti Guild Update")                       

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)      
        guild = channel.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.webhook_create):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await guild.ban(entry.user,
                               reason="Anti Webhook ")
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.id == entry.target.id:
                            await webhook.delete()
                            break                

    @commands.Cog.listener()
    async def on_guild_role_create(self, role) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        guild = role.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_create):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await role.delete()
                await guild.ban(entry.user,
                                   reason="Anti Role Create")                         

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)      
        guild = role.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_delete):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await role.clone()
                await guild.ban(entry.user,
                                   reason="Anti Role Delete")                   

    @commands.Cog.listener()
    async def on_guild_role_update(self, after: discord.Role,
                                   before: discord.Role) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)                                     
        guild = after.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_update):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                permissions = before.permissions
                await after.edit(name=f"{before.name}",permissions=permissions)
                await guild.ban(entry.user,
                                   reason="Anti Role Update")                       

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after) -> None:
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        guild = after.guild
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_update):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await guild.ban(entry.user,
                                   reason="Anti Emoji ")                      


    @commands.Cog.listener()
    async def on_member_remove(self, member, guild):
          with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick).flatten()      
            logs = logs[0]
            if logs.user.id == 844924055361945620 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
             await logs.user.ban(reason=f"Anti Kick")
            prunelogs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick).flatten()
            prunelogs = prunelogs[0]
            if logs.user.id == 844924055361945620 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
             await logs.user.ban(reason=f"Anti Prune")


    @commands.Cog.listener()
    async def on_guild_vanity(self, before, after)-> None:
          guild = after
          before_vanity = await before.vanity_invite()
          after_vanity = await after.vanity_invite()
          if before_vanity != after_vanity:
            async for entry in after.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(seconds=10), action=discord.AuditLogDiff.vanity_url_code):
               if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:  
                   await guild.ban(entry.user,
                                   reason="Anti Vanity")



    @commands.Cog.listener()
    async def on_guild_update_recovery(ctx, guild, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await channel.delete()

          return   

    @commands.Cog.listener()
    async def on_guild_update_recover(before, after, guild):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await guild.ban(i.user, reason="Anti Guild Recover")
          await guild.edit(name=f"{before.name}")

          return          

    @commands.Cog.listener()
    async def on_guild_role_update_recovery(before, after):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      role = after.guild  
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.role_update):
          if str(i.user.id) in whitelisted[str(role.guild.id)]:
            return
          await after.edit(name=f"{before.name}")  
          await role.guild.ban(i.user, reason="Updating roles as Non-Whitelist User")       


def setup(client):
    client.add_cog(Antinuke(client))
