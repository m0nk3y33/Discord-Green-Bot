import discord
import json
from discord.ext import commands

with open('reports.json', encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {'users': []}

bot = commands.Bot(command_prefix="!")


@bot.command(pass_context=True)
async def warn(ctx, user: discord.User, *reason: str):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(f"**{ctx.author}** Nie masz uprawnień do tej komendy")
    if not reason and ctx.author.guild_permissions.administrator:
        await ctx.send(f"**{ctx.author}** Proszę podać powód ")
        return
    if ctx.author.guild_permissions.administrator:

        reason = ' '.join(reason)
        for current_user in report['users']:
            if current_user['name'] == user.name:
                current_user['reasons'].append(reason)
                break
        else:
            report['users'].append({
                'name': user.name,
                'reasons': [reason, ],
            })
        with open('reports.json', 'w+') as dupa:
            json.dump(report, dupa)

    if len(current_user['reasons']) >= 3:
        await user.ban(reason="Dostałeś 3 warny, co skutkuje banem")
        await ctx.send(f"User : **{discord.user} został zbanowany za nieprzestrzeganie zasad.**")


@bot.command(pass_context=True)
async def warnings(ctx, user: discord.User):
    for current_user in report['users']:
        if user.name == current_user['name']:
            warningsEmbed = discord.Embed(title="Ostrzeżenia", colour=0xff0000)
            warningsEmbed.set_author(name=str(user))
            warningsEmbed.set_thumbnail(url=user.avatar_url)
            warningsEmbed.add_field(name=f"Ilość", value=f"**{len(current_user['reasons'])}**")
            warningsEmbed.add_field(name=f"Treść", value=f"{' | '.join(current_user['reasons'])}")
            await ctx.send(embed=warningsEmbed)
            break
    else:
        warningsNeverEmbed = discord.Embed(title="Ostrzeżenia", colour=0x00ff00)
        warningsNeverEmbed.set_author(name=str(user))
        warningsNeverEmbed.set_thumbnail(url=user.avatar_url)
        warningsNeverEmbed.add_field(name="Użytkownik", value=f"**{user.name}** nigdy nie został zgłoszony. Przykład do naśladowania")
        await ctx.send(embed=warningsNeverEmbed)


def setup(cmd):
    cmd.add_command(warn)
    cmd.add_command(warnings)
