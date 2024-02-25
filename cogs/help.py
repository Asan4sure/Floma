import discord
import datetime
import os
import random
import asyncio
import contextlib
import json
from discord_components import *
from discord.ext import commands

client = discord.Client

update = "`All bug fixed`"

funembed = discord.Embed(title="<a:1210597854142275635> __**Utility**__",
                         description="""
`afk`, `setprefix`, `invite` ,`about`, `botinfo/stats` ,`ping`, `report` ,`membercount`, `Embed`, `poll`, `Urban`,
""",
                         color=0x2f3136)
funembed.set_footer()

serverembed = discord.Embed(
    title=
    "<:role:1209892317226606612>__**Server Role**__<:role:1209892317226606612>",
    description="""
`setfriend [role]`, `setfrnd` ,`friend[mention]`, `rfriend`, `setstaff [role]`, `staff[mention]`, `rstaff` \n\n
""",
    color=0x2f3136)
funembed.set_footer()

utilityembed = discord.Embed(
    title=
    "**<a:close:1210114467036135424>  __**Moderation**__** <a:close:1210114467036135424> ",
    description="""
`Lock [channel]`, `lockall` , `unlockall`, `Unlock [channel]`, `Kick [user]`, `Hide [channel]`, `Unhide [channel]`, `Warn [user]`, `Unbanall`, `FuckBan [user]`, `Steal [emoji]`, `Purge [amount]`, `AddRole [user] [role]`, `RemoveRole or rr [user] [role]`, `Mute [user]`, `UnMute [user]`, `Steal [emoji]`, `Ban [user]`, `SlowMode [seconds]`, `TempMute [time in s, m, h, d, w,]`,`Roleall`,`addchannel [name]`,`deletechannel[name]`,
""",
    color=0x2f3136)
utilityembed.set_footer()

infoembed = discord.Embed(
    title=
    "<:logging:1076497369371254875> __**Logging**__ <:logging:1076497369371254875>",
    description="""
`loggingchannel`, `loggingshow`, `loggingremove`
""",
    color=0x2f3136)
infoembed.set_footer()

greetembed = discord.Embed(
    title=
    "<:voice_channel:1162068032152162404> **__Voice__**",
    description="""
`vckick`, `vchide`, `moveall`
""",
    color=0x2f3136)
infoembed.set_footer()

giveawayembed = discord.Embed(
    title=
    "<a:Giveaways:1066715947458637884> **__Giveaway Commands__** <a:Giveaways:1066715947458637884>",
    description="""
`gstart`, `gend`, `greroll`
""",
    color=0x2f3136)
infoembed.set_footer()

moderationembed = discord.Embed(
    title=
    "<a:antinuke:1210601781977948221> __**Anti-Nuke**___",
    description="""**\nThe AntiNuke is Automatically Enabled**""",
    color=0x2f3136)
moderationembed.add_field(
    name="<a:close:1210114467036135424> __**Punishment Type__**",
    value=f"**<a:Arrow:1210595776250773595> Ban**",
    inline=False)
moderationembed.add_field(
    name="<a:Arrow:1210595776250773595>  __**Security Status**__",
    value=
    f"<a:Arrow:1210595776250773595> **Enabled** <:furo_correct:1208687672047042671>",
    inline=False)
moderationembed.add_field(
    name="<a:Loading:1210602862753874000> Features",
    value=
    "`Anti Ban`,`Anti Unban`,`Anti Kick`,`Anti Bot Add`,`Anti Channel Create`,`Anti Channel Delete`,`Anti Channel Update`,`Anti Role Create`,`Anti Role Delete`,`Anti Webhook Update`"
)
moderationembed.add_field(name="<a:Loading:1210602862753874000> **Vanity**",
                          value="`setvanity [vanity]`,`vanity[]`")
moderationembed.add_field(name="<a:Loading:1210602862753874000> **Admins only**",
                          value="`whitelist`,`unwhitelist` , `whitelisted`")
moderationembed.set_footer()

marryembed = discord.Embed(title="<:hack_extra:1210613237985320981> __**Extra**__",
                           description="""
`truth`, `dare`, `meme`, `afk`, `userinfo`,  `serverinfo`, `roleinfo`, `av`, `banner`,  `invites`, `servericon`, `serverbanner`
""",
                           color=0x2f3136)
marryembed.set_footer()


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["h"])
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx):
        await self.selectboxtesting(ctx)

    async def selectboxtesting(self, ctx):
        funemoji = self.bot.get_emoji(1178727096823070751)
        utilityemoji = self.bot.get_emoji(1178727096823070751)
        infoemoji = self.bot.get_emoji(1178727096823070751)
        modemoji = self.bot.get_emoji(1178727096823070751)
        memoji = self.bot.get_emoji(1178727096823070751)
        embed = discord.Embed(title="Floma Help Menu",
                              description=f"""
**• Prefix for this server is `-`
• Type `<command | module>` for more info\n• [Get Floma](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) ・[Support](https://dsc.gg/floma)**"""
                              )
        embed.add_field(
            name="",
            value="""**__Main Modules__
            __Extra Modules__
            <:antinuke:1210612629102399629> `:` [Antinuke](https://dsc.gg/floma)        <:servers:1209892052637196370> `:` [Server Roles](https://dsc.gg/floma)
            <:moderation:1210612622962196520> `:` [Moderation](https://dsc.gg/floma)        <:Utility:1210615546588954644> `:` [Utility](https://dsc.gg/floma)
            <:giveaway:1210612598886891540> `:` [Giveaway](https://dsc.gg/floma)        <:voice:1210613247116316673> `:` [Voice](https://dsc.gg/floma)
            <:k9logging:1210612593379647589> `:` [Logging](https://dsc.gg/floma)      <:hack_extra:1210613237985320981> `:` [Extra](https://dsc.gg/floma) **""",
            inline=True)
        embed.add_field(
            name="",
            value=
            """
           """,
            inline=False)
        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/1037641994119422013/1038971573375356988/IMG_0715.gif"
        )
        embed.set_footer()
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        interaction1 = await ctx.send(
            embed=embed,
            components=[[
                Select(placeholder="Choose a Categ..",
                       options=[
                           SelectOption(label="Utility..",
                                        value="1",
                                        emoji=funemoji),
                           SelectOption(label="Giveaway..",
                                        value="2",
                                        emoji=funemoji),
                           SelectOption(label="Moderation..",
                                        value="3",
                                        emoji=utilityemoji),
                           SelectOption(label="Logging..",
                                        value="4",
                                        emoji=infoemoji),
                           SelectOption(label="AntiNuke..",
                                        value="5",
                                        emoji=modemoji),
                           SelectOption(label="Voice..",
                                        value="8",
                                        emoji=funemoji),
                           SelectOption(label="Server Roles..",
                                        value="6",
                                        emoji=memoji),
                           SelectOption(label="Extra..", value="7",
                                        emoji=memoji),
                       ],
                       custom_id="selectboxtesting")
            ]]),
        while True:
            try:
                interaction2 = await self.bot.wait_for(
                    "select_option",
                    check=lambda inter: inter.custom_id == "selectboxtesting",
                    timeout=900)
                res = interaction2.values[0]
                if res == "1":
                    await interaction2.send(embed=funembed)
                elif res == "2":
                    await interaction2.send(embed=giveawayembed)
                elif res == "3":
                    await interaction2.send(embed=utilityembed)
                elif res == "4":
                    await interaction2.send(embed=infoembed)
                elif res == "6":
                    await interaction2.send(embed=serverembed)
                elif res == "5":
                    await interaction2.send(embed=moderationembed)
                elif res == "8":
                    await interaction2.send(embed=greetembed)
                elif res == "7":
                    await interaction2.send(embed=marryembed)
                else:
                    pass
            except discord.errors.HTTPException:
                error = "Error!"
                print(error)


def setup(bot):
    bot.add_cog(help(bot))
