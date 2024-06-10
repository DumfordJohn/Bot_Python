import discord
from discord.ext import commands
import json

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        await print("Mute.py is ready")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmute(self, ctx, role=discord.Role):
        with open("./cogs/jsonfiles/mute.json", "r") as m:
            mute_role = json.load(m)

        mute_role[str(ctx.guild.id)] = role.name
        
        with open("./cogs/jsonfiles/mute.json", "w") as m:
            json.dump(mute_role, m, indent=4)

        conf_embed = discord.Embed(title="Mute Role Success", color=discord.Color.red())
        conf_embed.add_field(name="Mute Role is set!", value=f"The mute role for the server is '{role.mention}' for this server.  Anyone who is muted will have this role.")

        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        with open("./cogs/jsonfiles/mute.json", "r") as m:
            role = json.load(m)

            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.add_roles(mute_role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        with open("./cogs/jsonfiles/mute.json", "r") as m:
            role = json.load(m)

            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.remove_roles(mute_role)


async def setup(bot):
    await bot.add_cog(Mute(bot))