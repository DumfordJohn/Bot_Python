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
    with open("./cogs/jsonfiles/prefixes.json", "r") as f:
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

@bot.event
async def on_guild_join(guild):
    with open("./cogs/jsonfiles/prefixes.json", "r") as p:
        prefix = json.load(p)

    prefix[str(guild.id)] = "!"
    
    with open("./cogs/jsonfiles/prefixes.json", "w") as p:
        json.dump(prefix, p, indent=4)
    with open("./cogs/jsonfiles/mute.json", "r") as m:
        mute_role = json.load(m)

        mute_role[str(guild.id)] = None
    with open("./cogs/jsonfiles/mute.json", "w") as m:
        json.dump(mute_role, m, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open("./cogs/jsonfiles/prefixes.json", "r") as p:
        prefix = json.load(p)

    prefix.pop(str(guild.id))
    
    with open("./cogs/jsonfiles/prefixes.json", "w") as p:
        json.dump(prefix, p, indent=4)
    with open("./cogs/jsonfiles/mute.json", "r") as m:
        mute_role = json.load(m)

        mute_role.pop(str(guild.id))
    with open("./cogs/jsonfiles/mute.json", "w") as m:
        json.dump(mute_role, m, indent=4)

@bot.command()
async def setprefix(ctx, *, newprefix: str):
    with open("./cogs/jsonfiles/prefixes.json", "r") as f:
        prefix = json.load(p)

    prefix[str(ctx.guild.id)] = newprefix
    
    with open("./cogs/jsonfiles/prefixes.json", "w") as p:
        json.dump(prefix, p, indent=4)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())