import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import datetime as dt
import traceback as tb
from config import RED, GREEN, YELLOW, PREFIX, LOG_ID

# load .env vars
load_dotenv()


# Initialise
class Bot(commands.Bot):
    start_time = dt.datetime.utcnow()

    async def on_error(self, event, *args, **kwargs):
        em = discord.Embed(colour=RED, title=f"{event} Error")
        em.description = f"```py\n{tb.format_exc()}\n```"
        args = [repr(a) for a in args]
        if args:
            em.add_field(name="Args", value="\n".join(args))
        em.timestamp = dt.datetime.utcnow()

        channel = self.get_channel(LOG_ID)
        await channel.send(embed=em)


intents = discord.Intents(guild_messages=True, guilds=True, members=True, guild_reactions=True)
bot = Bot(command_prefix=PREFIX, case_insensitive=True, owner_ids=[114352655857483782, 307624079647834112],
          allowed_mentions=discord.AllowedMentions(roles=False, everyone=False), intents=intents,
          chunk_guilds_at_startup=False)

# Remove basic help command
bot.remove_command("help")

# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print("Loading: " + filename[:-3].title())
        bot.load_extension("cogs." + filename[:-3])


@bot.event
async def on_ready():
    # Print startup message
    startup = bot.user.name + " is running"
    print(startup)
    print("-" * len(startup))  # Print a line of dashes as long as the last print line for neatness
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"for updates"))


# Start bot
bot.run(getenv("BOT_TOKEN"))
