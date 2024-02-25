import os
import discord
import sys
import psutil
import asyncio
import random
import urllib
import json
import re
import requests
from time import strftime
from jishaku.cog import Jishaku
from discord.utils import find
from discord.ext import commands, tasks
import time
import aiohttp
from discord_buttons_plugin import *
from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_components import *
from typing import Union
from discord.gateway import DiscordWebSocket
import datetime
from discord.ext.commands import Greedy
from typing import Union

start_time = datetime.datetime.utcnow()


def guildowner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620


def clientowner(ctx):
    return ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620


#chat pe aaa
def is_allowed(ctx):
    return ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620 or ctx.message.author.id == 844924055361945620


async def get_prefix(client, message):
    with open('np.json', 'r') as f:
        p = json.load(f)
    if message.author.id in p["np"]:
        return ""
    else:
        return "-"


token = os.getenv("token")
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

prefix = "-"
client = commands.Bot(command_prefix=('-'),
                      intents=intents,
                      everyone_ping=False,
                      replied_user=False,
                      here_ping=False)

client = commands.AutoShardedBot(shard_count=1,
                                 command_prefix=get_prefix,
                                 case_insensitive=True,
                                 intents=intents,
                                help_command=None)
client.remove_command("help")
client.owner_ids = [844924055361945620]

headers = {"Authorization": f"{token}"}
ddb = DiscordComponents(client)
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('_'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.load_extension("jishaku")

with open('whitelisted.json') as f:
    whitelisted = json.load(f)


@client.event
async def on_guild_join():
    for x in client.guilds:
        if x.member_count < 30:
            await x.leave()


@client.listen("on_guild_join")
async def update_json(guild):
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    with open('whitelisted.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)


@commands.check(guildowner)
@client.command()
async def gsetup(ctx):
    for guild in client.guilds:
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(guild.id) not in whitelisted:
            whitelisted[str(guild.id)] = []

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)


@gsetup.error
async def gsetup_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("You Cant Use This Command")


@client.command()
async def g(ctx):
    for guild in list(client.guilds):
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(guild.id) not in whitelisted:
            whitelisted[str(guild.id)] = []

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)


@commands.check(is_server_owner)
@client.command(aliases=['wld'])
async def whitelisted(ctx):

    embed = discord.Embed(title=f"{ctx.guild.name} Whitelisted Users",
                          description="")

    with open('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
    try:
        for u in whitelisted[str(ctx.guild.id)]:
            embed.description += f"<@{(u)}> - {u} | "
        await ctx.reply(embed=embed)
    except KeyError:
        await ctx.reply(embed=discord.Embed(
            description="Nothing found for this guild!"))


@client.command(aliases=['wl'])
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.reply(embed=discord.Embed(
            description="Mention User To Whitelist"))
        return
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(ctx.guild.id) not in whitelisted:
        whitelisted[str(ctx.guild.id)] = []
    else:
        if str(user.id) not in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].append(str(user.id))
        else:
            await ctx.reply(embed=discord.Embed(
                description="User is Already In Whitelist"))
            return

    with open('whitelisted.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)

    await ctx.reply(embed=discord.Embed(
        description=f"{user} Has Been Whitelisted"))


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Only Guild Owner Can Use")


@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Only Guild Owner Can Use")


@client.command(aliases=['uwl'])
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
    if user is None:
        await ctx.reply("Only Guild Owner Can Use")
        return
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)
    try:
        if str(user.id) in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].remove(str(user.id))

            with open('whitelisted.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)

            await ctx.reply(embed=discord.Embed(
                description=f"{user} Removed From Whitelist"))
    except KeyError:
        await ctx.reply("Wont Whitelisted At All Till Now")


#cls()


@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Only Guild Owner Can Use")





async def status_task():
    while True:
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name="-help"))


@client.event
async def on_ready():
    print(f"Sucessfully logged in {client.user}")
    client.loop.create_task(status_task())


def restart_client():
    os.execv(sys.executable, ['python'] + sys.argv)


@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send(f"**{tick} | Successfully Restarted The Bot**")
    restart_client()

    @commands.command(aliases=['blacklist'])
    @commands.has_permissions(administrator=True)
    async def block(self, ctx, user: discord.Member = None):
        if not user:
            await ctx.send("Please specify a Member")
            return
        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.send(
            f"`{user.name}#{user.discriminator}` was blocked by `{ctx.author}`."
        )

    @block.error
    async def block_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You are not allowed to block people!")

    @commands.command(aliases=['removeblacklist', 'rb'])
    @commands.has_permissions(administrator=True)
    async def unblock(self, ctx, user: discord.Member = None):
        if not user:
            await ctx.send("Please specify a member")
            return
        await ctx.channel.set_permissions(user, send_messages=None)
        await ctx.send(
            f"`{user.name}#{user.discriminator}` was unblocked by `{ctx.author}`."
        )

    @block.error
    async def unblock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You are not allowed to unblock people!")

### ANTI SPAMM COMMANDS ###
spam_words = ['spam', 'bot', 'advertisement', 'promo', 'buy now', 'limited time offer']
link_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

def is_spam(message):
    if any(word in message.content.lower() for word in spam_words):
        return True
    if link_pattern.search(message.content):
        return True
    return False

# Initialize a dictionary to keep track of messages and their frequencies
last_messages = {}

@client.event
async def on_message(message):
    # Check if message is spam
    if not message.author.guild_permissions.administrator and is_spam(message):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please refrain from spamming or posting links.")
    else:
        # Check for repeated messages containing the same word
        content = message.content.lower()
        if content in last_messages and last_messages[content][0] == message.author.id:
            # If the same user repeats the same message, increment the frequency counter
            last_messages[content][1] += 1
            if last_messages[content][1] >= 3:
                # If the frequency counter exceeds the threshold, delete the message and notify the user
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please refrain from spamming the same word.")
        else:
            # If the message is not a repeat, add it to the dictionary with frequency 1
            last_messages[content] = [message.author.id, 1]
    await bot.process_commands(message)

  ################### ANTI SPAM ########################


@client.command()
async def baninfo(ctx):
    bra = ctx.message.author
    brasex = bra.avatar.url
    embed = discord.Embed(title="Floma",
                          description=f"""`
- [] optional argument\n- <> = required argument\n- Do not type these when using commands!`
        
**Aliases**\n`hackban | fuckban | fuckoff | jana | getlost`

**Usage**\n`!ban <member> <reason=reason>`\n""",
                          color=0x2f3136)
    embed.set_footer(text=f"", icon_url=brasex)
    await ctx.reply(embed=embed)


@client.event
async def on_guild_update(before, after):
    if "VANITY_URL" in after.features:
        with open("vanity.json") as f:
            vanity = json.load(f)
            stored_vanity = vanity[str(after.id)]
        return await after.edit(vanity_code=stored_vanity)


@client.command(aliases=['vanity'])
@commands.guild_only()
async def setvanity(ctx, vanity_code):
    if ctx.message.author.id != ctx.guild.owner_id:
        return
    with open('vanity.json', 'r') as f:
        vanity = json.load(f)
        vanity[str(ctx.guild.id)] = vanity_code
    with open('vanity.json', 'w') as f:
        json.dump(vanity, f, indent=4)
    await ctx.send("Successfully Set Vanity To {}".format(vanity_code))


cd = commands.CooldownMapping.from_cooldown(6, 7, commands.BucketType.user)


@client.event
async def on_member_update(before, after):
    with open("vanityroles.json", "r") as f:
        jnl = json.load(f)
    if str(before.guild.id) not in jnl:
        return
    elif str(before.guild.id) in jnl:
        vanity = jnl[str(before.guild.id)]["vanity"]
        role = jnl[str(before.guild.id)]["role"]
        channel = jnl[str(before.guild.id)]["channel"]
        if str(before.raw_status) == "offline":
            return
        else:
            aft = after.activities[0].name
            bef = before.activities[0].name
            if vanity in aft:
                try:
                    if vanity not in bef:
                        gchannel = client.get_channel(channel)
                        grole = after.guild.get_role(role)
                        await after.add_roles(
                            grole, reason="- added vanity in status")
                        await gchannel.send(
                            f"> {after.mention}, Thanks for repping {vanity} in your status <3"
                        )
                    elif vanity in bef:
                        return
                except:
                    pass
            elif vanity not in aft:
                if vanity in bef:
                    try:
                        gchannel = client.get_channel(channel)
                        grole = after.guild.get_role(role)
                        await after.remove_roles(
                            grole, reason="- removed vanity from status")
                        await gchannel.send(
                            f"> {after.mention} removed vanity from status.")
                    except:
                        pass


@client.command(aliases=["vantyrolessetup"])
@commands.has_permissions(administrator=True)
async def vrsetup(ctx, vanity, role: discord.Role,
                  channel: discord.TextChannel):
    with open("vanityroles.json", "r") as f:
        idk = json.load(f)
    if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members:
        await ctx.send(
            f'You cant use roles with administrator/ban/kick members permission.'
        )
    else:
        pop = {"vanity": vanity, "role": role.id, "channel": channel.id}
        idk[str(ctx.guild.id)] = pop
        embed = discord.Embed(
            color=discord.Colour(0x2f3136),
            description=
            f"Vanity: {vanity}\nRole: {role.mention}\nChannel: {channel.mention}"
        )
        #embed.set_thumbnail(url=bot.user.avatar_url)
        # embed.set_author(name="Vanity Roles Setup!", icon_url=bot.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
    with open('vanityroles.json', 'w') as f:
        json.dump(idk, f, indent=4)


@client.command(aliases=["vantyrolesshow"])
@commands.has_permissions(administrator=True)
async def vrshow(ctx):
    with open("vanityroles.json", "r") as f:
        jnl = json.load(f)
    if str(ctx.guild.id) not in jnl:
        await ctx.reply(f"Setup vanity roles using `,vrsetup`",
                        mention_author=False)
    elif str(ctx.guild.id) in jnl:
        vanity = jnl[str(ctx.guild.id)]["vanity"]
        role = jnl[str(ctx.guild.id)]["role"]
        channel = jnl[str(ctx.guild.id)]["channel"]
        gchannel = client.get_channel(channel)
        grole = ctx.guild.get_role(role)
        embed = discord.Embed(
            color=discord.Colour(0x2f3136),
            description=
            f"Vanity: {vanity}\nRole: {grole.mention}\nChannel: {gchannel.mention}"
        )
        #embed.set_thumbnail(url=bot.user.avatar_url)
        #embed.set_author(name="Vanity Roles!", icon_url=bot.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)


@client.command(aliases=["vantyrolesremove"])
@commands.has_permissions(administrator=True)
async def vrremove(ctx):
    with open("vanityroles.json", "r") as f:
        jnl = json.load(f)
        if str(ctx.guild.id) not in jnl:
            await ctx.reply(f"Setup vanity roles using `,vrsetup`",
                            mention_author=False)
        else:
            jnl.pop(str(ctx.guild.id))
            await ctx.reply(
                f"Removed the vanity roles system from this server.",
                mention_author=False)
    with open('vanityroles.json', 'w') as f:
        json.dump(jnl, f, indent=4)


@client.command()
@commands.is_owner()
async def leaveg(ctx, *, guild: discord.Guild = None):
    #if ctx.author.id in is_bot_owner:
    if guild is None:
        print("Please enter the guild ID!")  # No guild found
        return
    await guild.leave()  # Guild found
    await ctx.send(f"{tick} Successfully left: {guild.name}!")


######## ERROR ###########

################ HELP ##################


@commands.has_permissions(administrator=True)
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def roleall(ctx, *, role: discord.Role):
    num = 0
    failed = 0
    await ctx.send("Adding roles to all humans & bots")
    for user in list(ctx.guild.members):
        try:
            await user.add_roles(role)
            num += 1
        except Exception:
            failed += 1
    await ctx.reply('Added roles to all humans & bots')


@client.command()
@commands.has_permissions(administrator=True)
async def embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Waiting for a title')
    title = await client.wait_for('message', check=check)

    await ctx.send('Waiting for a description')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content,
                          description=desc.content,
                          color=0x2f3136)
    await ctx.send(embed=embed)


@client.command()
async def urban(ctx, *, search_terms: str, definition_number: int = 1):
    search_terms = search_terms.split(" ")
    try:
        if len(search_terms) > 1:
            pos = int(search_terms[-1]) - 1
            search_terms = search_terms[:-1]
        else:
            pos = 0
        if pos not in range(0, 11):
            pos = 0
    except ValueError:
        pos = 0
    search_terms = "+".join(search_terms)
    url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            result = json.loads(await r.text())
            if result["list"]:
                definition = result['list'][pos]['definition']
                example = result['list'][pos]['example']
                defs = len(result['list'])
                embed = discord.Embed(color=0x2f3136)
                embed.add_field(name="Defintion",
                                value=f"{definition}",
                                inline=True)
                embed.add_field(name="Example",
                                value=f"{example}",
                                inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0x2f3136)
                embed.add_field(name="Error",
                                value=f"No results found",
                                inline=True)
                await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def timer(ctx, want: int):
    brasex = ctx.message.author
    # radhe = brasex.avatar_url
    em = discord.Embed(description=f"Timer started for {want} seconds.")
    #  em.set_thumbnail(url=radhe)
    await ctx.send(embed=em, mention_author=True)
    await asyncio.sleep(want)
    await ctx.reply(f"Your timer for {want}s has been ended!")


@client.command()
async def Developer(ctx):
    await ctx.send("<@844924055361945620>")


@client.command(aliases=["voicekick"])
@commands.has_permissions(manage_messages=True)
async def vckick(ctx, member: discord.Member, reason="No reason provided"):
    await member.move_to(None)
    await ctx.reply(f'{member} has been disconnected from vc.',
                    mention_author=False)


@client.command()
@commands.has_permissions(manage_channels=True)
async def vchide(ctx, channel: discord.VoiceChannel = None):
    ch = channel or ctx.author.voice.channel
    if ch == None:
        await ctx.reply(
            f'You must be in a vc for hiding it or providing the channel id.',
            mention_author=False)
    else:
        overwrite = ch.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        overwrite.connect = False
        await ch.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.reply(f'{ch.mention} is now hidden from the default role.',
                        mention_author=False)


@client.command()
@commands.has_permissions(administrator=True)
async def moveall(ctx, channel: discord.VoiceChannel = None):
    if channel == None:
        await ctx.reply('Mention a channel to move users to!')
    if ctx.author.voice:
        channell = ctx.author.voice.channel
        members = channell.members
        for m in members:
            await m.move_to(channel)
        await ctx.reply(f"Moved all users to {channel.mention}")
    if ctx.author.voice is None:
        await ctx.reply(
            'You need to be connected to the channel from where you want to move everyone.'
        )


@client.group(invoke_without_command=True, aliases=["jahsd"])
async def hajja(ctx):
    embed = discord.Embed(
        color=0x2f3136,
        timestamp=ctx.message.created_at,
        title="",
        description=
        f"Hey, I am  Floma  a Multi Purpose bot And My Prefix is `{prefix}`or More Info Join My [Support Server](https://discord.gg/floma)\n**<:stolen_emoji:1028622104075178075> Public Commands\n`afk`, `userinfo`, `membercount`, `serverinfo`, `roleinfo`, `av`, `banner`, `invite`, `stats`, `invites`, `servericon`, `serverbanner`, `ping`,**\n\n**<:day:1028622633417314384> Moderation Commands\n`kick`, `hide`, `unhide`, `setnick`, `warn`, `unbanall`, `fuckban`, `ban`, `auditlogs [amount]`, `steal`, `mute`, `unmute`, `purge`, `addrole`, `removerole`, `revokeall`, `revokeinvites`, `channelnuke`, `unlockall`, `lockall`**\n\n**<:zzlogging:1036564590391214141> Logging Commands\n`setlog`, `removelog`, `showlog`**\n\n**<a:gxp_music:1036564752303923240> Music Commands\n`play`, `leave`, `connect`, `skip`, `pause`, `resume`, `volume`, `loop`**\n\n**<:cc_black_card:1028904495134027776> Fun Commands\n`Truth`, `Dare`, `maths`, `meme`, `coinflip`**\n\n**<:spy_config:1028903455852593182> Extra Commands\n`report`, `about`**"
    )
    embed.set_thumbnail(url="")
    embed.set_footer(text=".gg/flomas", icon_url="")
    embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
    await buttons.send(
        content=None,
        embed=embed,
        channel=ctx.channel.id,
        components=[
            ActionRow([
                Button(
                    style=ButtonType().Link,
                    label="Invite Me",
                    url=
                    f"https://discord.com/api/oauth2/authorize?client_id=1029406213764558928{client.user.id}&permissions=8&scope=bot"
                ),
                Button(style=ButtonType().Link,
                       label="Support Server",
                       url=f"https://discord.gg/floma")
            ])
        ])


@client.command()
async def ping(ctx):
    embed = discord.Embed(color=0x2f3136,
                          title="Ping!",
                          description=f"**`{int(client.latency * 1000)}ms`**")
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)


@client.command(aliases=["mc"])
async def membercount(ctx):
    scembed = discord.Embed(colour=discord.Colour(0x2f3136))
    scembed.add_field(name='**__Members__**',
                      value=f"{ctx.guild.member_count}")
    await ctx.send(embed=scembed, mention_author=False)


@client.command(aliases=["si", "serverinfo"])
async def serverinfos(ctx):
    guild_roles = len(ctx.guild.roles)
    guild_categories = len(ctx.guild.categories)
    guild_members = len(ctx.guild.members)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    channels = text_channels + voice_channels
    serverinfo = discord.Embed(colour=0x2f3136)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> Server Name",
                         value=f"{ctx.guild.name}",
                         inline=True)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> Server Id",
                         value=f"```{ctx.guild.id}```",
                         inline=False)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> Server Owner",
                         value=f"```{ctx.guild.owner}```",
                         inline=False)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> Boosts",
                         value=f"```{ctx.guild.premium_subscription_count}```",
                         inline=False)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> All Channel",
                         value=f"```{channels}```",
                         inline=False)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> All Roles",
                         value=f"```{guild_roles}```",
                         inline=False)
    serverinfo.add_field(
        name="<:furo_correct:1208687672047042671> All Categories",
        value=f"```{guild_categories} Categories```",
        inline=False)
    serverinfo.add_field(name="<:furo_correct:1208687672047042671> All Members",
                         value=f"```{guild_members}```",
                         inline=False)
    serverinfo.set_thumbnail(url=ctx.guild.icon_url)
    serverinfo.set_image(url=ctx.guild.banner_url)
    await ctx.send(embed=serverinfo)


@client.command()
@commands.has_permissions(administrator=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      view_channel=False)
    await ctx.send(
        '<:furo_correct:1208687672047042671>| **This Channel is Now Hidden From Everyone**'
    )


@client.command()
@commands.has_permissions(administrator=True)
async def unhide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      view_channel=True)
    await ctx.send(
        '<:furo_correct:1208687672047042671> | **This Channel is Now Visible To Everyone**'
    )


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(
        f'{tick} | Successfully Kicked {member.mention} Reason: {reason}')


@client.command(aliases=["ri"])
async def roleinfo(ctx, role: discord.Role = None):
    riembed = discord.Embed(title=f"**{role.name}'s Information**",
                            colour=discord.Colour(0x2f3136))
    riembed.add_field(
        name='__General info__',
        value=
        f"Name: {role.name}\nId: {role.id}\nPosition: {role.position}\nHex: {role.color}\nMentionable: {role.mentionable}\nCreated At: {role.created_at}"
    )
    await ctx.send(embed=riembed, mention_author=False)


@client.command("joke")
async def joke(ctx):
    import pyjokes
    embed = discord.Embed(title="Joke!",
                          description=pyjokes.get_joke(),
                          color=discord.Color.random())
    await ctx.send(embed=embed)


@client.command()
async def setnick(ctx, member: discord.Member, *, nick=None):
    if ctx.author.guild_permissions.manage_nicknames:

        old_nick = member.display_name

        await member.edit(nick=nick)

        new_nick = member.display_name

        await ctx.send(
            f'{tick} | Changed nickname from *{old_nick}* to *{new_nick}*')


@client.command(aliases=["av"])
async def pfp(ctx, member: discord.Member = None):
    member = ctx.author if not member else member

    embed = discord.Embed(title=f"**{member.name}'s Avatar**", color=0x2f3136)
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)


@client.command()
async def enlarge(ctx, emoji: discord.PartialEmoji = None):
    embed = discord.Embed(title=f"Emoji Name | {emoji.name}", color=0x2f3136)
    embed.set_image(url=f'{emoji.url}')
    embed.set_author(name=f"Requested by{ctx.author.name}",
                     icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text="Team Floma", icon_url="{}")
    await ctx.send(embed=embed)


@client.command()
async def warn(ctx, member: discord.Member, *, reason="`No Reason Provided`"):
    await ctx.send(
        f"**{tick} | `{member.display_name}` Has Been Warned For :`{reason}`**"
    )
    await member.send(
        f"**You Have Been Warned In `{ctx.guild.name}` for: `{reason}`**")


@commands.cooldown(3, 300, commands.BucketType.user)
@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.send(
        '**<:furo_correct:1208687672047042671>| Unbanning  {} Members**'.format(
            len(banlist)))
    for users in banlist:
        await ctx.guild.unban(user=users.user, reason=f"By {ctx.author}")


@client.command(aliases=["fban"])
@commands.has_permissions(ban_members=True)
async def fuckban(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.ban(reason=f"Banned by {ctx.author.name} reason: {reason}.")
    await ctx.send(
        f"**<:furo_correct:1208687672047042671>| Successfully FuckBanned {user.name}, Responsible:{ctx.author.name}.**",
        mention_author=False)


@client.command(name="unban",
                description="Unbans a user",
                usage="unban [user id]",
                aliases=["uban"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 15, commands.BucketType.member)
async def unban(ctx, user):

    try:

        await ctx.guild.unban(discord.Object(id=user))

        await ctx.send(embed=discord.Embed(
            title="unban",
            description=
            "<:furo_correct:1208687672047042671>| Successfully unbanned **`%s`**"
            % (user),
            color=discord.Colour.green()))

    except Exception:

        await ctx.send(embed=discord.Embed(
            title="unban",
            description=
            "<a:1603_Animated_Cross:1040660750483603496>| Failed to unban **`%s`**"
            % (user),
            color=0x00DEFF))


@client.command(name='',
                description='Bans mentioned user.',
                usage="ban <user> [reason]",
                inline=True)
@commands.has_guild_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def ban(ctx, member: discord.Member, *, reason=None):

    await ctx.message.delete()

    guild = ctx.guild

    if ctx.author == member:

        await ctx.send(
            (f'{ctx.author.mention}, Do you really want me to ban you?'),
            delete_after=20)

    elif ctx.author.top_role <= member.top_role:

        await ctx.send((
            f"**<a:1603_Animated_Cross:1040660750483603496>| You can't ban a member above you.**"
        ),
                       delete_after=20)

    elif ctx.author.top_role == member.top_role:

        await ctx.send((
            f"**<a:1603_Animated_Cross:1040660750483603496>| You can't ban member having same role as you**"
        ))

    elif ctx.guild.owner == member:

        await ctx.send((
            '<a:1603_Animated_Cross:1040660750483603496> | Server owners can\'t be banned!!'
        ),
                       delete_after=20)

    else:

        if reason == None:

            try:

                try:

                    #   await member.send(embed=create_embed(f"**You have been banned from, {guild.name}**"))

                    await member.ban(reason=f"Responsible: {ctx.author}")

                    banembed = discord.Embed(
                        description=
                        f'**<:furo_correct:1208687672047042671>| {member} Has Been Banned**',
                        colour=0x2f3136)

                    banembed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=banembed)

                except:

                    await member.ban(reason=f"Responsible: {ctx.author}")

                    ban2embed = discord.Embed(
                        description=
                        f'<:furo_correct:1208687672047042671>| {member} Has Been Banned**',
                        colour=0x2f3136)

                    ban2embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban2embed)

            except Exception as e:

                await ctx.send(
                    f"**<:furo_correct:1208687672047042671>| {member} Has Been Banned**"
                )

        else:

            try:

                try:

                    #    await member.send(embed=create_embed(f"**You have been banned from {guild.name} for *{reason}***"))

                    await member.ban(reason=reason)

                    ban3embed = discord.Embed(
                        description=
                        f'**<:furo_correct:1208687672047042671>| {member} Has Been Banned**\nReason: `{reason}`',
                        colour=0x2f3136)

                    ban3embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban3embed)

                except:

                    await member.ban(reason=reason)

                    ban4embed = discord.Embed(
                        description=
                        f'**<:furo_correct:1208687672047042671>| {member} Has Been Banned**\nReason: `{reason}`',
                        colour=0x2f3136)

                    ban4embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban4embed)

            except Exception as e:

                await ctx.send(
                    f"**<:furo_correct:1208687672047042671>| Failed To Ban, {member}**"
                )


@commands.has_permissions(view_audit_log=True)
@client.command(
    aliases=["log", "logs", "audit", "audit-logs", "audit-log", "auditlogs"])
async def auditlog(ctx, lmt: int):
    idk = []
    str = ""
    async for entry in ctx.guild.audit_logs(limit=lmt):
        idk.append(f'''User: `{entry.user}`
Action: `{entry.action}`
Target: `{entry.target}`
Reason: `{entry.reason}`\n\n''')
    for n in idk:
        str += n
    str = str.replace("AuditLogAction.", "")
    embed = discord.Embed(title=f" {ctx.guild} | Audit Logs",
                          description=f">>> {str}",
                          color=0x2f3136)
    await ctx.send(embed=embed)


@client.command()
async def banner(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    bid = await client.http.request(
        discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = bid["banner"]

    if banner_id:
        embed = discord.Embed(color=0x2f3136)
        embed.set_author(name=f"{user.name}'s Banner")
        embed.set_image(
            url=
            f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Floma',
                              color=0x2f3136,
                              description=f"**`User has no banner`**")
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, emotes: Greedy[Union[discord.Emoji,
                                          discord.PartialEmoji]]):
    if not emotes:
        return await ctx.send('**You Didnt Specify Any Emote/Emoji**')
    in_server, added = [], []
    for emote in emotes:
        if isinstance(emote, discord.Emoji) and emote.guild == ctx.guild:
            in_server.append(emote)
        else:
            added.append(await ctx.guild.create_custom_emoji(
                name=emote.name,
                image=await emote.url.read(),
                reason=f'**Added by {ctx.author} ({ctx.author.id})**'))

    if not added:
        return await ctx.send(
            f'**Specified emote{"s" if len(emotes) != 1 else ""} Is Already In This Server**'
        )
    if in_server:
        return await ctx.send(
            f'**{" ".join(map(str, added))} Have Been Added To This Server, While**'
            f'**{" ".join(map(str, in_server))} wasn\'t because they are already added!**'
        )
    await ctx.send(
        f'**{" ".join(map(str, added))} has been added to this server!**')


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(
                mutedRole, speak=False, send_messages=False
            )  #, read_message_history=True, read_messages=False , view_channels = True

    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(color=0x2F3136, title="Floma")
    embed.set_thumbnail(url="")
    embed.add_field(name="<:furo_correct:1208687672047042671>Muted",
                    value=f"{member.mention}",
                    inline=False)
    embed.set_footer(text="Floma", icon_url="")

    await ctx.send(embed=embed, mention_author=False)


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    embed = discord.Embed(color=0x2F3136, title="Floma")
    embed.add_field(name="<:furo_correct:1208687672047042671>Unmuted",
                    value=f"{member.mention}",
                    inline=False)
    embed.set_footer(text="Floma", icon_url="")
    embed.set_thumbnail(url="")
    await ctx.send(embed=embed, mention_author=False)


@client.command("purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send((f"** {tick} Successfully Purged {amount} Messages**"),
                   delete_after=5)


@client.command(aliases=["Roleremove", "rr"])
@commands.has_permissions(administrator=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(
        f"**{tick} | SuccessFully Removed {role} from {member.mention}**")


@client.command(aliases=["addrole", "role"])
@commands.has_permissions(administrator=True)
async def ar(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(
        f"**{tick} | SuccessFully Added {role} to {member.mention}**")


@client.command(aliases=["i"])
async def invite(ctx):
    embed = discord.Embed(
        color=0x2f3136,
        description=
        f"**<:floma:1068497357127295066>__Floma__\n\n<:furo_correct:1208687672047042671>[Invite Me](https://discord.com/api/oauth2/authorize?client_id=1057948119674925196&permissions=8&scope=bot) \n<:furo_correct:1208687672047042671>[Support Server](https://discord.gg/g5Q6pzhUfU)**"
    )
    embed.set_thumbnail(url="")
    await ctx.send(embed=embed, mention_author=True)


@client.command(aliases=["stats"])
async def botinfo(ctx):
    embed = discord.Embed(
        color=0x2f3136,
        title=
        f"<:floma:1068497357127295066> **__Floma__** <:floma:1068497357127295066>",
        description=
        f"**__Bot Information__**\n```\n・CPU Usage - {psutil.cpu_percent(1)}%\n・Total Ram - 15.6GB\n・Latency - {int(client.latency * 1000)}```\n<:furo_correct:1208687672047042671>**__Statistics__** \n```\n・Servers - {len(client.guilds)}\n・Users - {len(set(client.get_all_members()))}\n```"
    )
    embed.set_thumbnail(url="")
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@commands.cooldown(3, 30, commands.BucketType.user)
@client.command(aliases=['deletechannel'])
@commands.has_permissions(manage_channels=True)
async def delchannel(ctx, *channels: discord.TextChannel):
    for ch in channels:
        await ch.delete()
        await ctx.send(f'{ch.name} has been deleted')


@commands.cooldown(3, 30, commands.BucketType.user)
@client.command()
@commands.has_permissions(manage_channels=True)
async def addchannel(ctx, *names):
    for name in names:
        await ctx.guild.create_text_channel(name)
        await ctx.send(f'{name} has been created')


@client.command()
async def showguildsid(ctx):
    if ctx.author.id == 844924055361945620 or 844924055361945620:
        for guild in client.guilds:
            channel = guild.text_channels[0]
            rope = guild.id
            await ctx.send(f"{rope}")


@client.command()
async def showguilds(ctx):
    if ctx.author.id == 844924055361945620 or 844924055361945620:
        for guild in client.guilds:
            channel = guild.text_channels[0]
            rope = await channel.create_invite(unique=True)
            await ctx.send(f"`{guild.name}`\n {rope}")


@client.command()
async def createinvite(ctx, guildid: int):
    if ctx.author.id == 844924055361945620 or 844924055361945620:
        # try:
        guild = client.get_guild(guildid)
        invitelink = ""
        i = 0
        while invitelink == "":
            channel = guild.text_channels[i]
            link = await channel.create_invite(max_age=300, max_uses=1)
            invitelink = str(link)
            i += 1
        await ctx.send(invitelink)
    else:
        # except Exception:
        await ctx.send("Something went wrong")


@client.command(aliases=["prefix"])
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefixx):
    with open("prefixes.json", "r") as f:
        idk = json.load(f)
    if len(prefixx) > 5:
        await ctx.reply(embed=discord.Embed(
            color=discord.Colour(0x2f3136),
            description=f'Prefix Cannot Exceed More Than 5 Letters'))
    elif len(prefixx) <= 5:
        idk[str(ctx.guild.id)] = prefixx
        await ctx.reply(embed=discord.Embed(
            color=discord.Colour(0x2f3136),
            description=f'Updated Server Prefix To `{prefixx}`'))
    with open("prefixes.json", "w") as f:
        json.dump(idk, f, indent=4)


@client.command()
async def invites(ctx):
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(
        f"**You've invited** ``{totalInvites}`` **Members**{'' if totalInvites == 1 else ''} **to the server!**"
    )


@client.command(aliases=['icon', 'sicon'])
async def servericon(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0x2f3136)
    embed.set_image(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


############### ON MENTION #########


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith(f'<@{client.user.id}>'):
        embed = discord.Embed(
            color=0x2f3136,
            title=f"Floma",
            description=
            f"- **Hey, I'm Floma**\n**- My Prefix is `{prefix}`**\n**Type {prefix}help To Get Commands List**"
        )

        await message.reply(embed=embed)


truth_msg = [
    "How would you rate your looks on a scale from 1-10?",
    "What is one thing that brings a smile to your face, no matter the time of day?",
    "What’s is one thing that you’re proud of?",
    "Have you ever broken anything of someone else's and not told the person?",
    "Who is your boyfriend/girlfriend/partner?",
    "When was the last time you lied?", "When was the last time you cried?",
    "What's your biggest fear?", "What's your biggest fantasy?",
    "Do you have any fetishes?",
    "What's something you're glad your mum doesn't know about you?",
    "Have you ever cheated on someone?",
    "What was the most embarrassing thing you’ve ever done on a date?",
    "Have you ever accidentally hit something (or someone!) with your car?",
    "Name someone you’ve pretended to like but actually couldn’t stand.",
    "What’s your most bizarre nickname?",
    "What’s been your most physically painful experience?",
    "What bridges are you glad that you burned?",
    "What’s the craziest thing you’ve done on public transportation?",
    "If you met a genie, what would your three wishes be?",
    "If you could write anyone on Earth in for President of the United States, who would it be and why?",
    "What’s the meanest thing you’ve ever said to someone else?",
    "Who was your worst kiss ever?",
    "What’s one thing you’d do if you knew there no consequences?",
    "What’s the craziest thing you’ve done in front of a mirror?",
    "What’s the meanest thing you’ve ever said about someone else?",
    "What’s something you love to do with your friends that you’d never do in front of your partner?",
    "Who are you most jealous of?", "What do your favorite pajamas look like?",
    "Have you ever faked sick to get out of a party?",
    "Who’s the oldest person you’ve dated?",
    "How many selfies do you take a day?",
    "How many times a week do you wear the same pants?",
    "Would you date your high school crush today?", "Where are you ticklish?",
    "Do you believe in any superstitions? If so, which ones?",
    "What’s one movie you’re embarrassed to admit you enjoy?",
    "What’s your most embarrassing grooming habit?",
    "When’s the last time you apologized? What for?",
    "How do you really feel about the Twilight saga?",
    "Where do most of your embarrassing odors come from?",
    "Have you ever considered cheating on a partner?", "Boxers or briefs?",
    "Have you ever peed in a pool?",
    "What’s the weirdest place you’ve ever grown hair?",
    "If you were guaranteed to never get caught, who on Earth would you murder?",
    "What’s the cheapest gift you’ve ever gotten for someone else?",
    "What app do you waste the most time on?",
    "What’s the weirdest thing you’ve done on a plane?",
    "Have you ever been nude in public?",
    "How many gossip blogs do you read a day?",
    "What is the youngest age partner you’d date?",
    "Have you ever lied about your age?", "Have you ever used a fake ID?",
    "Who’s your hall pass?", "What is your greatest fear in a relationship?",
    "Have you ever lied to your boss?", "Who would you hate to see naked?",
    "Have you ever regifted a present?",
    "Have you ever had a crush on a coworker?",
    "Have you ever ghosted a friend?", "Have you ever ghosted a partner?",
    "What’s the most scandalous photo in your cloud?",
    "When’s the last time you dumped someone?",
    "What’s one useless skill you’d love to learn anyway?",
    "If I went through your cabinets, what’s the weirdest thing I’d find?",
    "Have you ever farted and blamed it on someone else?"
]


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def truth(ctx):
    await ctx.send(f"`{random.choice(truth_msg)}`", mention_author=False)


dare_msg = [
    "Let the person on your right take an ugly picture of you and your double chin and post it on IG with the caption, “I don’t leave the house without my double chin",
    " Eat a raw potato",
    "Order a pizza and pay the delivery guy in all small coins",
    "Open the window and scream to the top of our lungs how much you love your mother",
    "Kiss the person who is sitting beside you",
    "Beg for a cent on the streets",
    "Go into the other room, take your clothes off and put them on backward",
    "Show everyone your search history for the past week",
    "Set your crush’s picture as your FB profile picture",
    "Take a walk down the street alone and talk to yourself",
    "Do whatever someone wants for the rest of the day",
    " Continuously talk for 3 minutes without stopping",
    " Draw something on the face with a permanent marker",
    " Peel a banana with your feet",
    " Lay on the floor for the rest of the game",
    " Drink 3 big cups of water without stopping",
    "Go back and forth under the table until it’s your turn again",
    " Close your mouth and your nose: try to pronounce the letter ‘“A” for 10 seconds",
    "Ask someone random for a hug",
    "Call one of your parents and then tell them they are grounded for a week",
    "Have everyone here list something they like about you",
    "Wear a clothing item often associated with a different gender tomorrow",
    "Prank call your crush",
    "Tweet 'insert popular band name here fans are the worst' and don't reply to any of the angry comments.",
    "List everyone as the kind on animal you see them as.",
    "Talk in an accent for the next 3 rounds",
    "Let someone here do your makeup.", "Spin around for 30 seconds",
    "Share your phone's wallpaper",
    "Ask the first person in your DMs to marry you.",
    "Show the last DM you sent without context",
    "Show everyone here your screen time.", "Try to lick your elbow",
    "Tie your shoe strings together and try to walk to the door and back",
    "Everything you say for the next 5 rounds has to rhyme.",
    "Text your crush about how much you like them, but don't reply to them after that.",
    "Ask a friend for their mom's phone number",
    "Tell the last person you texted that you're pregnant/got someone pregnant.",
    "Do an impression of your favorite celebrity",
    "Show everyone the last YouTube video you watched.",
    "Ask someone in this server out on a date.",
    "Kiss the player you think looks the cutest."
]


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def dare(ctx):
    await ctx.send(f"`{random.choice(dare_msg)}`", mention_author=False)


@client.command()
async def coinflip(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(
            title="**COINFLIP**",
            description=f"{ctx.author.mention} Flipped coin, and got **Heads**!"
        )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="**COINFLIP**",
            description=f"{ctx.author.mention} Flipped coin, and got **Tails**!"
        )
        await ctx.send(embed=embed)


@client.command()
async def meme(ctx):
    memeAPI = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")

    memeData = json.load(memeAPI)

    memeUrl = memeData["url"]
    memeName = memeData["title"]
    memePoster = memeData["author"]
    memeSub = memeData["subreddit"]
    memeLink = memeData["postLink"]

    embed = discord.Embed(title=memeName, color=0x2f3136)
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def revokeall(ctx):
    for i in await ctx.guild.invites():
        await i.delete()
    await ctx.send(
        f"**{tick} | SuccessFully Removed All Of Invites Of The Guild**")


@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def revokeinvites(ctx, member: discord.Member = None):
    mem = member or ctx.author
    for i in await ctx.guild.invites():
        if i.inviter == mem:
            await i.delete()
    await ctx.send(
        f"**{tick} | SuccessFully Cleared Invites of {mem.mention}**")


@client.command()
async def math(ctx, *, expression: str):
    calculation = eval(expression)
    await ctx.send('Expression: {}\nAnswer: {}'.format(expression,
                                                       calculation))


@client.command(aliases=["cnuke"])
@commands.has_permissions(administrator=True)
async def channelnuke(ctx):
    channelthings = [ctx.channel.category, ctx.channel.position]
    await ctx.channel.clone()
    await ctx.channel.delete()
    embed = discord.Embed(
        title=f'Nuked Channel!',
        description=f'**Channel was nuked by {ctx.author.name}**',
        color=0x2f3136,
        timestamp=ctx.message.created_at)
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/990083771787247707/993747223017951302/Lynx_1.gif"
    )
    nukedchannel = channelthings[0].text_channels[-1]
    await nukedchannel.edit(position=channelthings[1])
    await nukedchannel.send(embed=embed)


@client.command(
    name="unlockall",
    description=
    "Unlocks the server. | Warning: this unlocks every channel for the everyone role.",
    usage="unlockall")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def unlockall(ctx, server: discord.Guild = None, *, reason=None):

    await ctx.message.delete()

    if server is None: server = ctx.guild

    try:

        for channel in server.channels:

            await channel.set_permissions(
                ctx.guild.default_role,
                overwrite=discord.PermissionOverwrite(send_messages=True),
                reason=reason)

        await ctx.send(
            f"{tick} | **{server}** Has Been Unlocked\nReason: `{reason}`")

    except:

        await ctx.send(f"{cross} | **Failed to unlock, {server}**")

    else:

        pass


@client.command(name="lockall",
                description="Locks down the server.",
                usage="lockall")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def lockall(ctx, server: discord.Guild = None, *, reason=None):

    await ctx.message.delete()

    if server is None: server = ctx.guild

    try:

        for channel in server.channels:

            await channel.set_permissions(
                ctx.guild.default_role,
                overwrite=discord.PermissionOverwrite(send_messages=False),
                reason=reason)

        await ctx.send(
            f"{tick} | **{server}** Has Been Locked\nReason: `{reason}`")

    except:

        await ctx.send(f"{cross} | **Failed To Lockdown, {server}**```")

    else:

        pass


#create a yes/no poll
@client.command()
@commands.has_permissions(administrator=True)
#the content will contain the question, which must be answerable with yes or no in order to make sense
async def poll(ctx, *, content: str):
    print("Creating yes/no poll...")
    #create the embed file
    embed = discord.Embed(
        title=f"{content}",
        description=
        "React to this message with <a:JKtick:1045972372701847612> for yes, <:furo_Wrong:1208687798635200562> for no.",
        color=0x2f3136)
    #set the author and icon
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
    print("Embed created")
    #send the embed
    message = await ctx.channel.send(embed=embed)
    #add the reactions
    await message.add_reaction("<a:JKtick:1045972372701847612>")
    await message.add_reaction("<:furo_Wrong:1208687798635200562>")


@client.command()
async def serverbanner(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0x2f3136)
    embed.set_image(url=ctx.guild.banner_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


@client.command()
async def joinvc(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"**{tick} | Successfully Joined The VC Where You Are!**")


@client.command()
async def leavevc(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send(f"**{tick} | Successfully Left The VC!**")


########### TEMP MUTE #####


@client.command(aliases=['tm'])
@commands.cooldown(3, 15, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def tempmute(ctx,
                   member: discord.Member = None,
                   tiempo=None,
                   *,
                   reason=None):

    if member == None:
        await ctx.send(f"{cross} | **Please mention a member to be tempmuted**"
                       )
    else:
        if member == ctx.author:
            await ctx.send(f"{cross} | **You cant tempmute yourself**")
        else:
            if tiempo == None:
                await ctx.send(f"{cross} | **Enter a time input `e.g 1h`**")

            guild = ctx.guild
            tempmuted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            time_convert = {
                "s": 1,
                "m": 60,
                "h": 3600,
                "d": 86400,
                "w": 604800,
                "mo": 2628000,
                "y": 31536000
            }
            tmpmute = (int(tiempo[:-1]) * (time_convert[tiempo[-1]]))
            await member.add_roles(tempmuted_role, reason=reason)
            await ctx.reply(
                f"{tick} | **Successfully TempMuted:** \n Member: {member.mention} \n Time: {tiempo} \n Reason: {reason}"
            )

            await asyncio.sleep(int(tmpmute))
            await member.remove_roles(tempmuted_role)
            await ctx.send(f"{tick} | {member.mention} has been unmuted")
            await member.send(f"You Have Been Unmuted in {guild.name}")


########## JOIN & LEAVE ############


@client.event
async def on_guild_remove(guild):
    log_channel = client.get_channel(844924055361945620)
    embed = discord.Embed(title='Floma',
                          color=0x2f3136,
                          description=f'Removed From A Server!')
    embed.add_field(name='Server Name', value=f'**`{guild.name}`**')
    embed.add_field(name='Server Owner', value=f'**`{guild.owner}`**')
    embed.add_field(name='Server Members', value=f'**`{len(guild.members)}`**')
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/attachments/990083771787247707/993747223017951302/Lynx_1.gif'
    )
    await log_channel.send(embed=embed)


@client.listen("on_guild_join")
async def foo(guild):
    channel = guild.text_channels[0]
    rope = await channel.create_invite(unique=True)
    me = client.get_channel(844924055361945620)
    await me.send(
        f"Hey Devs i have been added to a new server\nGuild Name - {guild.name}\nGuild Owner - {guild.owner}\nMembers Count - {len(guild.members)}"
    )
    await me.send(rope)


#################### REPORT ####################


@client.command(aliases=["rep"])
async def report(ctx, *, message=None):
    if message == None:
        await ctx.send(
            f"**{cross} | Please Do `-report (the bug you want to report)` For This Command To Work!**"
        )
    else:
        await ctx.send(
            f"**{tick} | Successfully Submitted Your Report Our Dev Team Will Fix The Error/Bug ASAP!**"
        )

        channel = client.get_channel(844924055361945620)
        embed = discord.Embed(
            title=
            f"<:furo_correct:1208687672047042671> | Error/Bug Reported By `{ctx.author.name}`#  {ctx.author.discriminator}",
            description=f"**__Bug__** - **{message}**",
            color=0x2f3136)
        await channel.send(embed=embed)


@client.command(aliases=["dev", "abt", "clientdev"])
async def about(ctx):
    embed = discord.Embed(title=':receipt:**About Floma**', color=0x2f3136)
    embed.add_field(
        name='**<:furo_correct:1208687672047042671> Floma Information!**',
        value=
        '**\n <:furo_correct:1208687672047042671> Floma is a Security Bot With 24/7 Anti-Nuke \n To Protect Your Server!!**',
        inline=False)
    embed.add_field(
        name=':receipt:**__Developers__**',
        value=
        f'<:furo_correct:1208687672047042671>[ash3r#1337](https://discord.gg/floma)  \n ',
        inline=False)
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/attachments/990083771787247707/993747223017951302/Lynx_1.gif'
    )
    embed.add_field(
        name=':receipt:**__Owner__**',
        value=
        f'<:furo_correct:1208687672047042671>[Incognito#6365](https://discord.gg/floma)\n<:furo_correct:1208687672047042671>\n ',
        inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=["ui"])
async def userinfo(ctx, x: discord.Member = None):
    if x is None:
        x = ctx.author
    xx = discord.Embed(colour=0x2f3136)
    xx.set_thumbnail(url=x.avatar_url)
    xx.set_footer(text=f"Requested by {ctx.author}",
                  icon_url=ctx.author.avatar_url)
    xx.add_field(name="User Name", value=x, inline=False)
    xx.add_field(name="User ID", value=x.id, inline=False)
    xx.add_field(name="User Top Role", value=x.top_role, inline=False)
    xx.add_field(name="User Status", value=x.status, inline=False)
    xx.add_field(name="User Registered",
                 value=x.created_at.strftime("%B %d, %Y %I:%M %p"),
                 inline=False)
    xx.add_field(name="User Joined",
                 value=x.joined_at.strftime("%B %d, %Y %I:%M %p"),
                 inline=False)
    if len(x.roles) > 1:
        role_string = ''.join([r.mention for r in x.roles][1:])
    xx.add_field(name="User Roles", value=role_string, inline=False)
    perm_string = ', '.join([
        str(p[0]).replace("_", " ").title() for p in x.guild_permissions
        if p[1]
    ])
    xx.add_field(name="User Permissions", value=perm_string, inline=False)
    await ctx.send(embed=xx)


@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(f'{tick} | SuccessFully Locked {channel.mention}')


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(f'{tick} | SuccessFully Unlocked {channel.mention}')


################ AFK #######################


@client.command()
async def afk(ctx, *, reason="Iam AFK"):
    with open('afks.json', 'r') as f:
        afks = json.load(f)
        if str(ctx.author.id) not in afks:
            afks[str(ctx.author.id)] = "True"
            await ctx.reply(embed=discord.Embed(
                description=f'{tick} | You Are Now AFK | Reason: {reason}',
                mention_author=False))
        else:
            await ctx.send(
                embed=discord.Embed(description=f'{cross} | Failed To Set AFK',
                                    mention_author=False))
    with open('afks.json', 'w') as f:
        json.dump(afks, f, indent=4)


async def afkevent(message):
    with open('afks.json', 'r') as f:
        afks = json.load(f)
    for user_mention in message.mentions:
        if str(user_mention.id) in afks and afks[str(
                user_mention.id)] == "True":
            await message.reply(embed=discord.Embed(
                description=f'{user_mention.name} is Currently AFK  ',
                mention_author=True))
        else:
            return
    try:
        if afks[str(message.author.id)] == "True":
            await message.reply(embed=discord.Embed(
                description=
                f"Welcome Back {message.author}, Your AFK Has Been Removed!",
                mention_author=False))
            afks.pop(str(message.author.id))
        else:
            return
    except KeyError:
        return
    with open('afks.json', 'w') as f:
        json.dump(afks, f, indent=4)


@client.command(aliases=["onc"])
@commands.guild_only()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def onlinecount(ctx):
    onmc = 0
    idlemc = 0
    dndmc = 0
    offmc = 0
    estmem = 0
    for mem in list(ctx.guild.members):
        estmem += 1
        if f"{mem.status}" == "online":
            onmc += 1
        elif f"{mem.status}" == "idle":
            idlemc += 1
        elif f"{mem.status}" == "dnd":
            dndmc += 1
        elif f"{mem.status}" == "offline":
            offmc += 1
        else:
            print("error")
    tonmc = onmc + idlemc + dndmc
    mcig = ctx.guild.member_count
    embed = discord.Embed(
        color=0x2f3136,
        title=f"{ctx.guild.name}",
        description=
        f"\n<:Online:1036517661464612884>{onmc}\n<:Idle:1036517585778393138>{idlemc}\n<:Dnd:1036517508959707216>{dndmc}\n<:Offline:1036517711234216037>{offmc}\n\n**Total Online - {tonmc}\nTotal Members - {mcig}**"
    )
    await ctx.send(embed=embed)


############### ERROR ############

############# IDK #################

Unknown_xD_id = "844924055361945620"
client_id = "1057948119674925196"
supportlink = "https://dsc.gg/floma"
invitelink = f"https://discordapp.com/oauth2/authorize?client_id={client_id}&scope=client+applications.commands&permissions=0"
tick = "<:furo_correct:1208687672047042671>"
cross = "<:furo_Wrong:1208687798635200562>"
warn = "<:furo_error:1208045081383272508>"
arrow = "<a:Arrow:1210595776250773595>"
reply = "<:furo_correct:1208687672047042671>"
dash = ":receipt:"
color = "0x2f3136"
client_name = "Floma"


#### Logging #####
@client.command(aliases=["loggingchannel"])
@commands.has_permissions(administrator=True)
async def logset(ctx, channel: discord.TextChannel):
    with open('logsch.json', 'r') as f:
        logs = json.load(f)
        if str(ctx.guild.id) not in logs:
            logs[str(ctx.guild.id)] = str(channel.id)
            await ctx.send(
                f"**{tick} | Successfully Updated The Logs Channel To {channel.mention}**"
            )
            await channel.send(embed=discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"**{tick}This Channel Has Been Added As Logs Channel And All Logs Will Be Shown Here**"
            ))
        elif str(ctx.guild.id) in logs:
            logs[str(ctx.guild.id)] = str(channel.id)
            await ctx.send(
                f'**{tick}| Successfully Updated the logs channel to {channel.mention}**',
                mention_author=False)
            await channel.send(embed=discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"**{tick} This Channel Has Been Added As Logs Channel And All Logs Will Be Shown Here!**"
            ))
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


@client.command(aliases=["loggingshow", "showlogs", "showlog"])
@commands.has_permissions(administrator=True)
async def logshow(ctx):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        try:
            await ctx.send(
                f'**{tick} | The Logs Channel For This Server is <#{logs[str(ctx.guild.id)]}>**',
                mention_author=False)
        except KeyError:
            await ctx.send(
                f"**{cross}| No Logs Channel Has Been Found In The Server!**",
                mention_author=False)


@client.command(
    aliases=["loggingremove", "logsremove", " removelog", "removelogs"], )
@commands.has_permissions(administrator=True)
async def logremove(ctx):
    with open('logsch.json', 'r') as f:
        logs = json.load(f)
        if str(ctx.guild.id) not in logs:
            await ctx.send(
                f"**{cross}| There is No Logs Channel in The Server!**",
                mention_author=False)
        else:
            logs.pop(str(ctx.guild.id))
            await ctx.send(
                f"**{cross} | Successfully Removed Logs Channel From The Server!**",
                mention_author=False)
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


#--- events ----#
async def joinlog_event(member):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(member.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} {member} | {member.id}\n{reply} created at: <t:{int(member.created_at.timestamp())}:D>\n{reply} links: [avatar]({member.avatar_url})"
            )
            em.set_thumbnail(url=member.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Member joined!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(member.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(member.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def leavelog_event(member):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(member.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} {member} | {member.id}\n{reply} created at: <t:{int(member.created_at.timestamp())}:D>\n{reply} links: [avatar]({member.avatar_url})"
            )
            em.set_thumbnail(url=member.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Member left!", icon_url=client.user.avatar_url)
            logchid = logs[str(member.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(member.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def chcreatelog_event(channel):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(channel.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} #{channel.name} | {channel.id}\n{reply} type: {channel.type}\n{reply} position: {channel.position}"
            )
            em.set_thumbnail(url=client.user.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Channel created!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(channel.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(channel.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def chdellog_event(channel):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(channel.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} #{channel.name} | {channel.id}\n{reply} type: {channel.type}\n{reply} position: {channel.position}"
            )
            em.set_thumbnail(url=client.user.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Channel deleted!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(channel.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(channel.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def rolecrlog_event(role):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(role.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} {role.name} | {role.id}\n{reply} color: {role.color}\n{reply} position: {role.position}"
            )
            em.set_thumbnail(url=client.user.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Role created!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(role.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(role.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def roledellog_event(role):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(role.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} {role.name} | {role.id}\n{reply} color: {role.color}\n{reply} position: {role.position}"
            )
            em.set_thumbnail(url=client.user.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Role deleted!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(role.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(role.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def msgdellog_event(message):
    with open('logsch.json', 'r') as i:
        logs = json.load(i)
        if str(message.guild.id
               ) in logs and message.author.id != client.user.id:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} sent by: {message.author} in {message.channel.mention}\n{reply} content: {message.content}"
            )
            em.set_thumbnail(url=message.author.avatar_url)
            em.set_footer(text=f"{client_name}",
                          icon_url=client.user.avatar_url)
            em.set_author(name="Message deleted!",
                          icon_url=client.user.avatar_url)
            logchid = logs[str(message.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(message.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


async def msgeditlog_event(after, before):
    with open('logsch.json', 'r') as i:
        message = after
        logs = json.load(i)
        if str(message.guild.id) in logs:
            em = discord.Embed(
                color=discord.Colour(0x2f3136),
                description=
                f"{reply} sent by: {message.author} in {message.channel.mention}\n{reply} before: {after.content}\n{reply} after: {before.content}"
            ).set_thumbnail(url=message.author.avatar_url).set_footer(
                text=f"{client_name}",
                icon_url=client.user.avatar_url).set_author(
                    name="Message edited!", icon_url=client.user.avatar_url)
            logchid = logs[str(message.guild.id)]
            logsch = client.get_channel(int(logchid))
            await logsch.send(embed=em)
        elif str(message.guild.id) not in logs:
            return
    with open('logsch.json', 'w') as f:
        json.dump(logs, f, indent=4)


client.add_listener(joinlog_event, 'on_member_join')
client.add_listener(leavelog_event, 'on_member_remove')
client.add_listener(chcreatelog_event, 'on_guild_channel_create')
client.add_listener(chdellog_event, 'on_guild_channel_delete')
client.add_listener(rolecrlog_event, 'on_guild_role_create')
client.add_listener(roledellog_event, 'on_guild_role_delete')
client.add_listener(msgdellog_event, 'on_message_delete')
client.add_listener(msgeditlog_event, 'on_message_edit')
client.add_listener(afkevent, "on_message")

## Badges ##
with open('badges.json') as f:
    whitelisted = json.load(f)


@client.command(aliases=[("abadge")])
@commands.is_owner()
async def addbadge(ctx, user: discord.Member, *, badge):
    if ctx.author.id == 844924055361945620 or ctx.author.id == 814931758902411264:
        if user is None:
            await ctx.reply("You must specify a user to remove badge.")
            return
    with open("badges.json", "r") as f:
        idk = json.load(f)
    if str(user.id) not in idk:
        idk[str(user.id)] = []
        idk[str(user.id)].append(f"{badge}")
        await ctx.reply(f" Added badge {badge} to {user}.",
                        mention_author=False)
    elif str(user.id) in idk:
        idk[str(user.id)].append(f"{badge}")
        await ctx.reply(f" Added badge {badge} to {user}.",
                        mention_author=False)
    with open("badges.json", "w") as f:
        json.dump(idk, f, indent=4)


@client.command(aliases=["rbadge"])
@commands.is_owner()
async def removebadge(ctx, user: discord.Member, *, badge):
    if ctx.author.id == 844924055361945620 or ctx.author.id == 814931758902411264:
        if user is None:
            await ctx.reply(embed=discord.Embed(
                description="You must specify a user to remove badge"))
            return
        with open('badges.json', 'r') as f:
            badges = json.load(f)
        try:
            if str(user.id) in badges:
                badges.pop(str(user.id))

                with open('badges.json', 'w') as f:
                    json.dump(badges, f, indent=4)

                await user.send(embed=discord.Embed(
                    description=
                    f"Your badge has been removed from {ctx.author.mention}"))
        except KeyError:
            await ctx.reply("This user has no badge.")


@client.command(aliases=[("pr")])
async def badges(ctx, member: discord.Member = None):
    user = member or ctx.author
    with open("badges.json", "r") as f:
        idk = json.load(f)
    if str(user.id) not in idk:
        await member.send(embed=discord.Embed(
            description="You Dont have Badges"))
        await ctx.reply(embed=discord.Embed(
            description=f"{user} dont have badges", mention_author=False))
    elif str(user.id) in idk:
        embed = discord.Embed(color=discord.Colour(0x2f3136),
                              title=" Badges",
                              description="")
        for bd in idk[str(user.id)]:
            embed.description += f"{bd}\n"
        await ctx.reply(embed=embed, mention_author=False)


###--------np------------###


@client.command(name="npadd")
@commands.is_owner()
async def npadd(ctx, member: discord.Member = None):
    with open('np.json', 'r') as idk:
        data = json.load(idk)
    np = data["np"]
    if member.id not in np:
        np.append(member.id)
    with open('np.json', 'w') as idk:
        json.dump(data, idk, indent=4)
        embed = discord.Embed(
            title=f"Floma",
            description=f"Done added `{member.name}` To no prefix..!!")
        await ctx.reply(embed=embed)


@client.command(name="npremove")
@commands.is_owner()
async def np_remove(ctx, member: discord.Member = None):
    with open('np.json', 'r') as idk:
        data = json.load(idk)
    np = data["np"]
    if member.id not in np:
        await ctx.reply("**{} is not in no prefix!**".format(member))
    else:
        data["np"].remove(member.id)
    with open('np.json', 'w') as idk:
        json.dump(data, idk, indent=4)
        await ctx.reply("Removed {} from no prefix!".format(member))


@client.command(aliases=['setfriend', 'setfrnd'])
async def setupfriendlodaaaajsnjsjsj(ctx, role: discord.Role = None):
    with open('lund.json', 'r', encoding='utf-8') as f:
        key = json.load(f)
    key[str(ctx.guild.id)] = [str(role.id)]
    with open('lund.json', 'w', encoding='utf-8') as f:
        json.dump(key, f, indent=4)
        await ctx.send(embed=discord.Embed(
            description=f"Set Friends Role As {role.name}"))


@client.command(aliases=[("frnd")])
async def friend(ctx, mem: discord.Member = None):
    with open("lund.json", 'r') as f:
        key = json.load(f)
    if f'{ctx.guild.id}' not in key:
        await ctx.send('not found')
    elif f'{ctx.guild.id}' in key:
        for idk in key[str(ctx.guild.id)]:
            r = discord.utils.get(ctx.guild.roles, id=int(idk))
            await mem.add_roles(r)
            await ctx.send(embed=discord.Embed(
                description=f"Role Given To {mem.mention}"))


@client.command(aliases=[("rfrnd")])
async def rfriend(ctx, mem: discord.Member = None):
    with open("lund.json", 'r') as f:
        key = json.load(f)
    if f'{ctx.guild.id}' not in key:
        await ctx.send('not found')
    elif f'{ctx.guild.id}' in key:
        for idk in key[str(ctx.guild.id)]:
            r = discord.utils.get(ctx.guild.roles, id=int(idk))
            await mem.remove_roles(r)
            await ctx.send(embed=discord.Embed(
                description=f"Role Taken From {mem.mention}"))


@client.command(aliases=['setstaff', 'serofficial'])
async def setstafflodaaaajsnjsjsj(ctx, role: discord.Role = None):
    with open('official.json', 'r', encoding='utf-8') as f:
        key = json.load(f)
    key[str(ctx.guild.id)] = [str(role.id)]
    with open('official.json', 'w', encoding='utf-8') as f:
        json.dump(key, f, indent=4)
        await ctx.send(embed=discord.Embed(
            description=f"Set staff Role As {role.name}"))


@client.command(aliases=[("official")])
async def staff(ctx, mem: discord.Member = None):
    with open("official.json", 'r') as f:
        key = json.load(f)
    if f'{ctx.guild.id}' not in key:
        await ctx.send('not found')
    elif f'{ctx.guild.id}' in key:
        for idk in key[str(ctx.guild.id)]:
            r = discord.utils.get(ctx.guild.roles, id=int(idk))
            await mem.add_roles(r)
            await ctx.send(embed=discord.Embed(
                description=f"Role Given To {mem.mention}"))


@client.command(aliases=[("rofficial")])
async def rstaff(ctx, mem: discord.Member = None):
    with open("official.json", 'r') as f:
        key = json.load(f)
    if f'{ctx.guild.id}' not in key:
        await ctx.send('not found')
    elif f'{ctx.guild.id}' in key:
        for idk in key[str(ctx.guild.id)]:
            r = discord.utils.get(ctx.guild.roles, id=int(idk))
            await mem.remove_roles(r)
            await ctx.send(embed=discord.Embed(
                description=f"Role Taken From {mem.mention}"))


client.run(token)
