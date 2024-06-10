import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await print("Moderation.py is ready.")

#   -----------Clear Command---------------
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)

#   -----------Kick Command---------------
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modReason):
        await ctx.guild.kick(member)
        conf_embed = discord.Embed(title="Kick Success", color=discord.Color.pink())
        conf_embed.add_field(name="Kicked", value=f"{member.mention}, has been kicked by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason: ", value=modReason, inline=False)

        await ctx.send(embed=conf_embed)

#   -----------Ban Command---------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modReason):
        await ctx.guild.ban(member)
        conf_embed = discord.Embed(title="Ban Success", color=discord.Color.pink())
        conf_embed.add_field(name="Banned", value=f"{member.mention}, has been banned by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason: ", value=modReason, inline=False)

        await ctx.send(embed=conf_embed)

#   -----------UnBan Command---------------

async def setup(bot):
    await bot.add_cog(Moderation(bot))