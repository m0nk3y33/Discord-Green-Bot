import discord
import json
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.command(pass_context=True)
async def reactrole(ctx, emoji, role: discord.Role, emoji_two, role_two: discord.Role, *, message):
    await ctx.message.delete()
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Nie masz uprawnień do tej komendy")
        return

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)
    await msg.add_reaction(emoji_two)

    with open('reactrole.json') as plik:
        data = json.load(plik)

        new_react_role = {
            'role_name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'role_name_two': role_two.name,
            'role_id_two': role_two.id,
            'emoji_two': emoji_two,
            'message_id': msg.id
        }

        data.append(new_react_role)

    with open('reactrole.json', 'w') as j:
        json.dump(data, j, indent=4)


def setup(cmd):
    cmd.add_command(reactrole)
