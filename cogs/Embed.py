import discord
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Embed.py is ready.")

    @commands.command()
    async def embed(self, ctx):
        embed_message = discord.Embed(title="Embed Title", description="Embed descritption", color=discord.Color.green())
        
        embed_message.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(name="Field name", value="field value", inline=False)
        embed_message.set_footer(text="This is the footer", icon_url=ctx.author.avatar)

        await ctx.send(embed = embed_message)


async def setup(bot):
    await bot.add_cog(Embed(bot))