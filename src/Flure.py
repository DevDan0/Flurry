#!/usr/bin/env python3
import json
import discord
import praw
import random
from gtts import gTTS
from moviepy.editor import *
import time 
import textwrap
import asyncio
from asyncio import sleep
from datetime import datetime,timezone,date
from random import randrange
from discord.ext import commands
from discord.ext.commands import has_permissions

# wacky shenanigans to import token and ids from file
intents = discord.Intents.default()
intents.members = True
print("Importing data from secrets file...")
secrets_file = 'secrets'
with open(secrets_file) as f:
    secrets = f.read()
print("Reconstructing data as dict...")
secrets = json.loads(secrets)
del(secrets)

#make a reddit app and fill the following:
reddit = praw.Reddit(
client_id="",
client_secret="",
user_agent="",
)
# end 

client = commands.Bot(command_prefix='?')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        invalid_args = discord.Embed(title='Error', color=0xff0000)
        invalid_args.add_field(name='Invalid amount of arguments', value='Missing arguments..', inline=False)
        await ctx.send(embed=invalid_args)
    if isinstance(error, commands.MissingPermissions):
        invalid_perms = discord.Embed(title='Error', color=0xff0000)
        invalid_perms.add_field(name='Permission denied', value='You dont have the permission to use this command.', inline=False)
        await ctx.send(embed=invalid_perms)

@client.command(brief="Shows Bot Delay in ms")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong: {round(client.latency * 1000)}ms")
    return
  
@client.command(brief="convert pounds to kg")
async def lbstokg(ctx, argument:float):
    lool = argument*0.45359237
    await ctx.send(lool)
    return
 
@client.command(brief="convert inches to centimeter")
async def inchestocm(ctx, argume:float):
    lpl = argume/0.39370
    await ctx.send(f'{lpl} cm')
    return

@client.command(brief="conveft celsius to fahrenheit ")
async def ctof(ctx, c:float):
    pol = (c*1.8)+32
    await ctx.send(f'{pol} ??f')
    return

@client.command(brief="current time in utc")
async def time(ctx):
	current_time = datetime.now(timezone.utc)
	await ctx.send(f'{current_time}')  

@client.command(brief="Game of Death!", description="Russian Roulette")
async def rusroulet(ctx):
  user = ctx.message.author
  await ctx.send("""
  ??????????????????????????????????????????
???????????????????????????????????????????????????
???????????????????????????????????????????????????
???????????????????????????????????????????????????
  """)
  await ctx.send("I will be generating two numbers, if they match you die, if they don't you live to see another day!")
  num1 = random.randint(0,6)
  num2 = random.randint(0,6)
  if num1 == num2:
    await ctx.send(f"Your Numbers are {num1} and {num2}, You Loose!")
    role = discord.utils.get(user.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send("Muted For 10 Minutes as Result of losing!")
    await asyncio.sleep(600)
    await user.remove_roles(role, atomic=True)
  else:
    await ctx.send(f"Your Numbers are {num1} and {num2}, You live to see another day!")
  return

@client.command(brief="get user avatar")
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
    return		

@client.command(brief="juicy memes from r/memes")
async def meme(ctx):
    memes = reddit.subreddit("memes").random()
    await ctx.send(f"{memes.title}                        {memes.url}")
    await ctx.message.delete()
    return

@client.command(brief="calculator")
async def math(ctx,opreation:str):
    await ctx.send(eval(opreation))
    return
	
@client.command(brief="for when you're bored!")
async def bored(ctx):
	ino = reddit.subreddit("mildlyinteresting").random()
	await ctx.send(f"{ino.title}                          {ino.url}")
	await ctx.message.delete()
	return

@client.command(brief="make the bot say something!")
#@has_permissions(administrator=True)
async def echo(ctx, *, lol):
	await ctx.send(lol)
	await ctx.message.delete()
	return 

@client.command(brief="surf the internet")
async def search(ctx, *, earch):
   lo = earch.replace(" ","+")
   ct = (f'https://duckduckgo.com/?q={lo}')
   embed = discord.Embed()
   embed.description = f"Search Result: [{earch}]({ct})"
   await ctx.send(embed=embed)
   return

@client.command(brief="ban members")
@commands.has_permissions(ban_members=True)
async def ban(ctx, shart:discord.Member=None, reason=None):
    await shart.ban(reason=reason)
    await ctx.send(f"user {shart} has been banned for {reason}")
    return

@client.command(brief="clear messages")
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.manage_messages:
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
        amount = amount - 1
        clembed = discord.Embed(title='Clear', color=0x123456)
        clembed.add_field(name='Teletubbies vacuum.', value=f'Number of messages deleted: {amount}')
        await ctx.send(embed=clembed)
        print(f'[ADMIN] Cleared {amount} messages in {ctx.channel}. Invoked by {ctx.message.author}')
    return

@client.command(brief="roll a dice")
async def roll(ctx, limit=5):
    limit = limit + 1
    print("[DEBUG] got here")
    number = randrange(1,limit)
    await ctx.send(f":game_die: {number}")
    return
    
@client.command(brief="make the bot say something")
async def eightball(ctx):
	ers = ["yes", "no", "im not sure", "fuck off"]
	joke = random.choice(ers)
	await ctx.send(joke)

@client.command(brief="get the square of a number")
async def square(ctx, numbo:float):
  suw = numbo*numbo
  await ctx.send(suw)
  return

@client.command(brief="Text to speech")
async def tts(ctx, *, txt):
  language = "en"
  obj = gTTS(text=txt,lang=language,slow=False,tld="ie")
  obj.save("tts.mp3")
  await ctx.send(file=discord.File("tts.mp3"))
  os.system("rm tts.mp3")
  return


@client.command(brief="Get the server information")
async def serverinfo(ctx):
	user = ctx.message.author
	svrn = ctx.guild.name
	svrc = len(ctx.guild.members)
	svro = len(ctx.guild.roles)
	embed = discord.Embed(title = "Flurry", description = "Server information", color = discord.Color.red())
	embed.set_thumbnail(url = str(ctx.guild.icon_url))
	embed.add_field(name = f"Server Name: ", value= svrn, inline=True)
	embed.add_field(name = f"Number Of Members In Server: ", value = svrc, inline=True)
	embed.add_field(name = f"Number of roles: " ,value = svro, inline = True)
	await ctx.send(embed=embed)
	return 
	
@client.command(brief="quotes")
async def makeaquote(ctx,*,quote):
  myim = Image.open("black.png")
  title_text = f"""{textwrap.fill(quote, width=45)}
               -{ctx.message.author}"""
  I1 = ImageDraw.Draw(myim)
  font = ImageFont.truetype('dank.ttf',60)
  I1.text((10,10), title_text, fill=(255,255,255))
  myim.save("quote.png")
  await ctx.send(file=discord.File('quote.png'))
  os.system("rm quote.png")
  return

@client.command(brief="play music")
async def play(ctx,link):
  vcc = ctx.author.voice
  if vcc:
    if "&" in link:
      await ctx.send("You can't do that!")
      return
    if "|" in link:
      await ctx.send("You can't do that!")
      return
    await ctx.send("joinning channel....")
    c=await vcc.channel.connect()
    if link.startswith("https://") or link.startswith("http://"):
      os.system(f"./yt-dlp -x -o song.opus {link}")
    else:
      await ctx.send(f"finding {link}....")
      os.system(f"./yt-dlp -x -o song.opus 'ytsearch:\"{link}\"'")
    await asyncio.sleep(8)
    c.play(discord.FFmpegPCMAudio("song.opus"))
    while c.is_playing() == True:
      await asyncio.sleep(1)
    os.system("rm song.opus")
    await c.disconnect()
  else:
    await ctx.send("join a vc first")
  return

@client.command()
async def despicableme(ctx):
  if ctx.message.attachments:
    for attachment in ctx.message.attachments:
      await attachment.save("lol.mp3")
      videoclip = VideoFileClip("lol.mp3")
      audioclip = AudioFileClip("despicable.mp3")
      new_audioclip = CompositeAudioClip([audioclip])
      videoclip.audio = new_audioclip
      videoclip.write_videofile("new.mp4")
      await ctx.send(file=discord.File('new.mp4'))
      os.system("rm lol.mp3")
      os.system("rm new.mp4")
    return
  else:
    await ctx.send("no")
    return
  
  return
  
################



@client.event
async def on_ready():
    print('[BOT] Bot ready.')
    print('[BOT] Started logging')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='?help'))

#The below code runs the bot.
print("i have no idea how this started but, yes.")
print("using token: " +secrets["token"])
print("----------------------")
client.run(secrets["token"], bot=True)
