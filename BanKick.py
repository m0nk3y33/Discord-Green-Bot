import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!")


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Ta komenda wymaga uprawnień, skontaktuj się z administratorem w celu sprawdzenia błędu.")
        return
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} został wyrzucony z serwera | Powód: **{reason}**')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Ta komenda wymaga uprawnień, skontaktuj się z administratorem w celu sprawdzenia błędu.")
        return
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} został zbanowany na tym serwerze | Powód **{reason}**')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


@bot.command()
async def unban(ctx, *, member):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Ta komenda wymaga uprawnień, skontaktuj się z administratorem w celu sprawdzenia błędu.")
        return
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'User {user.mention} został odbanowany, witamy.')
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Źle podano argumenty do komendy")


def setup(cmd):
    cmd.add_command(kick)
    cmd.add_command(ban)
    cmd.add_command(unban)
