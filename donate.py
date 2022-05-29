import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def donate(ctx):
    donateEmbed = discord.Embed(title="Pomoc w rozwoju", colour=0xFF7B25)
    donateEmbed.add_field(name="Dotacja", value="Wpłać chociaż drobną sume, abyt bot mógł się rozwijać bardziej")
    donateEmbed.add_field(name="Link", value="https://tipply.pl/u/m0nk3y3")
    await ctx.send(embed=donateEmbed)


def setup(cmd):
    cmd.add_command(donate)