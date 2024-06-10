import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from itertools import cycle
import asyncio
import json

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

def get_server_prefix(bot, message):
    with open("./cogs/files/prefixes.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())
bot_status = cycle(["$help for Help", "DON'T WORK"])

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord")
    change_status.start()

#   Custom Server Prefixes
@bot.event
async def on_guild_join(guild):
    with open("./cogs/files/prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "!"
    
    with open("./cogs/files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open("./cogs/files/prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))
    
    with open("./cogs/files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

@bot.command()
async def setprefix(ctx, *, newprefix: str):
    with open("./cogs/files/prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix
    
    with open("./cogs/files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
#   ----------------------------------------------------------
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())