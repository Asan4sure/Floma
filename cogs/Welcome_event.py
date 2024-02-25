import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb


class welcome_event(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://wkmt9r:bi8uh@cluster0.y0yvfyr.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.connection["Zeon"]["servers"]

    @commands.Cog.listener()
    async def on_member_join(self, user):
        try:
            guild = user.guild
            data = await self.db.find_one({"guild": guild.id})

            if data["welcome"]["enabled"] != True:
                return            
            if data["welcome"]["channel"] == None:
                return
            if data["embed"] == False: 

              if data["welcome"]["message"] == None:
                return
              else: 

                channel = self.client.get_channel(data["welcome"]["channel"])
                message = data["welcome"]["message"]
                if "{user.id}" in message:
                    message = message.replace("{user.id}", "%s" % (user.id))

                if "{user.mention}" in message:
                  message = message.replace("{user.mention}", "%s" % (user.mention))

                if "{user.tag}" in message:
                  message = message.replace("{user.tag}", "%s" % (user.discriminator))

                if "{user.name}" in message:
                  message = message.replace("{user.name}", "%s" % (user.name))
                
                if "{user.avatar}" in message:
                  message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

                if "{server.name}" in message:
                  message = message.replace("{server.name}", "%s" % (user.guild.name))
                
                if "{server.membercount}" in message:
                  message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
                
                if "{server.icon}" in message:
                  message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

                await channel.send(message)

            else:
              channel = self.client.get_channel(data["welcome"]["channel"])
              message = data["welcome"]["description"]
              message1 = data["welcome"]["title"]
              thumbnail = data["welcome"]["thumbnail"]
              image = data["welcome"]["image"] 
              
              if "{user.id}" in message:
                    message = message.replace("{user.id}", "%s" % (user.id))

              if "{user.mention}" in message:
                message = message.replace("{user.mention}", "%s" % (user.mention))

              if "{user.tag}" in message:
                message = message.replace("{user.tag}", "%s" % (user.discriminator))

              if "{user.name}" in message:
                message = message.replace("{user.name}", "%s" % (user.name))
                
              if "{user.avatar}" in message:
                message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

              if "{server.name}" in message:
                message = message.replace("{server.name}", "%s" % (user.guild.name))
                
              if "{server.membercount}" in message:
                message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
                
              if "{server.icon}" in message:
                message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

              if "{user.id}" in message1:
                    message1 = message1.replace("{user.id}", "%s" % (user.id))

              if "{user.mention}" in message1:
                message1 = message1.replace("{user.mention}", "%s" % (user.mention))

              if "{user.tag}" in message1:
                message1 = message1.replace("{user.tag}", "%s" % (user.discriminator))

              if "{user.name}" in message1:
                message1 = message1.replace("{user.name}", "%s" % (user.name))
                
              if "{user.avatar}" in message1:
                message1 = message1.replace("{user.avatar}", "%s" % (user.avatar_url))

              if "{server.name}" in message1:
                message1 = message1.replace("{server.name}", "%s" % (user.guild.name))
                
              if "{server.membercount}" in message1:
                message1 = message1.replace("{server.membercount}", "%s" % (user.guild.member_count))
                
              if "{server.icon}" in message1:
                message1 = message1.replace("{server.icon}", "%s" % (user.guild.icon_url))

              if "{user.avatar}" in thumbnail:
                thumbnail = thumbnail.replace("{user.avatar}", "%s" % (user.avatar_url))  

              if "{server.icon}" in thumbnail:
                thumbnail = thumbnail.replace("{server.icon}", "%s" % (user.guild.icon_url)) 

              if "{user.avatar}" in image:
                image = image.replace("{user.avatar}", "%s" % (user.avatar_url))  

              if "{server.icon}" in image:
                image = image.replace("{server.icon}", "%s" % (user.guild.icon_url))  

              embed = discord.Embed(title=f"{message1}",description=f"{message}", color=0x01f5b6)  
              embed.set_thumbnail(url=f"{thumbnail}")
              embed.set_image(url=f"{image}")

              await channel.send(embed=embed)
              
          
        except Exception:
            pass

def setup(client):
    client.add_cog(welcome_event(client))