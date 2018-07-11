import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import praw

bot = commands.Bot(command_prefix='#')

# Reddit API linking
reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET',
                     user_agent='USER_AGENT')

@bot.event
async def on_ready():
    print ("Running on " + bot.user.name + " with the ID " + bot.user.id)

@bot.command(pass_context=True)
async def ball(ctx): # Simulate a Magic 8-ball
    # Absolutely huge array with all 20 possible answers of a Magic 8-ball inside
    answers = ['It is certain.', 'It is decidedly so.', 'Without a doubt', 'Yes - definitely', 'You may rely on it.',
               'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
               'Reply hazy, try again', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again',
               'Don\'t count on it.', 'My reply is no.', 'My sources say no', 'Outlook not so good', 'Very doubtful.']

    await bot.say(":8ball: " + random.choice(answers))

@bot.command()
async def meme(): # Pull a random meme from r/dankmemes
    memes_submissions = reddit.subreddit('dankmemes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await bot.say(submission.url)

@bot.command(pass_context=True) # Retrieve info on a server member
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Discord Information".format(user.name), color=0x3F4F4F)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Top Rank", value=user.top_role, inline=True)
    embed.add_field(name="Join Date", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True) # Kick a server member (in progress)
async def kick(ctx, user: discord.Member):
    await bot.say("{} has been kicked.".format(user.name))
    await bot.kick(user)

@bot.command(pass_context=True) # Flip a coin
async def coin(ctx):
    face = random.randrange(1)

    if (face == 0):
        await bot.say("Heads")

    if (face == 1):
        await bot.say("Tails")

@bot.command(pass_context=True)
async def purge(ctx, amount = 100): # Purge a user-specified amount of messages
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit = int(amount) + 1):
        messages.append(message)

    await bot.delete_messages(messages)
    await bot.say("{} Messages purged.".format(amount))        
  
@bot.command(pass_context=True)
async def fhelp(ctx): # Basic help command
    await bot.say("**Thank you for adding Fuji!**\nCurrently, Fuji has four commands:\n`#ball (question)`, which simulates a Magic 8-Ball,\n`#meme`, which fetches a random meme from r/memes\n`#info (username)`, which gives you information about a server member\n`#kick (username)`, which kicks a server member\n`coin`, which flips a coin")

bot.run("TOKEN")
