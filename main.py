import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from itertools import cycle
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
bot_status = cycle(["$help for Help", "DON'T WORK"])

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord")
    change_status.start()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())