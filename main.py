from keep_alive import keep_alive

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import re
from replit import db
import asyncio
from nextcord.ui import Button, View

client = commands.Bot(command_prefix="!")
token = os.environ.get("DISCORD_BOT_SECRET")

# (1653737844)
def smart_truncate1(text, max_length=100, suffix='...'):

    if len(text) > max_length:
        pattern = r'^(.{0,%d}\b.{0,10})' % (max_length-len(suffix)-1)
        x = re.findall(pattern,text)
        return x[0]+suffix if len(x) > 0 else suffix
    else:
        return text

@client.event
async def on_ready():
  await client.change_presence(activity=nextcord.Game(name=f"on {len(client.guilds)} servers | "+str(db['n'])+" portals created!"))
  '''channel00 = client.get_channel(663606787265658891)
  await channel00.send(content=':egg:')'''
        
testserverid=918729030344273940

@client.slash_command(name="portal",description="Create a portal")
async def portal(interaction: Interaction,channel: nextcord.abc.GuildChannel =  nextcord.SlashOption(name="channel",description="Select a channel",required=True,channel_types=[nextcord.ChannelType.text])):
  db['n']=db['n']+1
  await on_ready()
  channel = client.get_channel(channel.id)
  tobeedited = await channel.send(embed=nextcord.Embed(title='Making Portal'))
  theurl=tobeedited.jump_url
  button=Button(label='Enter the Wormhole',url=theurl,emoji='🕳️')
  view=View()
  view.add_item(button)
  embed = nextcord.Embed(title='Portal Enter',url=theurl,type='link', description="Portal to: <#"+str(channel.id)+">",color=0x4ab581)
  embed.set_footer(text="Portal created by: "+str(interaction.user), icon_url=interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed,view=view)
  channel2 = client.get_channel(interaction.channel_id)
  gethistory = await channel2.history(limit=4).flatten()
  theurl2='https://discord.com/channels/'+str(interaction.guild.id)+'/'+str(channel2.id)+'/'+str(gethistory[0].id)
  embed2 = nextcord.Embed(title='Portal Exit',url=theurl2,type='link', description= "Portal from: <#"+str(channel2.id)+">\n\n"+'\n\n'.join(["> <@"+str(damsg.author.id)+">: ["+' '.join(damsg.content.split()[:6])+"...]("+damsg.jump_url+")" for damsg in gethistory[:0:-1]]), color=0x4ab581)
  embed2.set_footer(text="Portal created by: "+str(interaction.user), icon_url=interaction.user.display_avatar.url)
  button2=Button(label='Exit the Wormhole',url=theurl2,emoji='🕳️')
  view2=View()
  view2.add_item(button2)
  await tobeedited.edit(embed=embed2,view=view2)


@client.event
async def on_message(message):  
#    
  if message.author == client.user:
    return
  elif '!!https://discord.com/channels/' in message.content:
   pattern='!!https://discord.com/channels/[0-9]*/[0-9]*/[0-9]*';
   x=(re.findall(pattern, message.content))
   if len(list(re.compile(pattern).finditer(message.content)))==1:
     link = x[0].split('/')
     server_id, channel_id, msg_id = int(link[4]), int(link[5]), int(link[6])
     server = client.get_guild(server_id)
     channel = server.get_channel(channel_id)
     message2 = await channel.fetch_message(msg_id)
     await message.channel.send(content='Sharing an embed',embed=message2.embeds[0])
  elif '!https://discord.com/channels/' in message.content:
   pattern='!https://discord.com/channels/[0-9]*/[0-9]*/[0-9]*';
   x=(re.findall(pattern, message.content))
   embedd = nextcord.Embed(title='Discord Message Links', color=0xf76b07)
   for index0 in range(len(x)):
     link = x[index0].split('/')
   
     server_id, channel_id, msg_id = int(link[4]), int(link[5]), int(link[6])
     server = client.get_guild(server_id)
     channel = server.get_channel(channel_id)
     message2 = await channel.fetch_message(msg_id)
     embedd.add_field(name="Message "+str(index0+1), value="> <@"+str(message2.author.id)+">: ["+smart_truncate1(message2.content)+"]("+(x[index0])[1:]+")", inline=False)
   embedd.set_footer(text="Message links shared by "+str(message.author), icon_url=message.author.display_avatar.url)
   await message.channel.send(embed=embedd)

keep_alive()
client.run(token)