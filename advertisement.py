import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.command()
async def ogloszenie(ctx, title, *,  content):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("Ta komenda wymaga uprawnień, skontaktuj się z administratorem w celu sprawdzenia błędu.")
        return
    OgloszenieEmbed = discord.Embed(title=ctx.author, colour=0xCD5C5C)
    OgloszenieEmbed.add_field(name=f'{title}', value=f'{content}')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=OgloszenieEmbed)
    return


@ogloszenie.error
async def ogloszenie_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


def setup(cmd):
    cmd.add_command(ogloszenie)
