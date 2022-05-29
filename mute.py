import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.command()
async def unmute(ctx, member: discord.Member, ):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("Ta komenda wymaga uprawnień ``Manage Messages`` ")
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name="Muted")

    if not muteRole:
        await ctx.send("User nie jest już wyciszony")
        return

    await member.remove_roles(muteRole)
    await ctx.send(f"User {member} został odciszony, mamy nadzieję że poprawiłeś swoje zachowanie.")
    await member.send(f"Zostałeś odciszony przez: **{ctx.author}** | **Nie zapomnij podziękować!**")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("Ta komenda wymaga uprawnień ``Manage Messages`` ")
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name="Muted")

    if not muteRole:
        muteRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await ctx.send("Nie znaleziono takiej roli. Tworzenie w toku...")
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=True)
    await member.add_roles(muteRole, reason=reason)
    await ctx.send(f"User {member} został wyciszony, musi czekać na dobro administracji kiedy go odcziszą.")
    await member.send(f"Zostałeś wyciszony przez: **{ctx.author}** | Powód: **{reason}**")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


def setup(dupa):
    dupa.add_command(unmute)
    dupa.add_command(mute)
