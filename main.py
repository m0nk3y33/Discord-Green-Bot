import discord
import json
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print("I'm ready to use")
    print(f"Prędkość łącza - {round(bot.latency * 1000)}ms")
    await bot.change_presence(activity=discord.Streaming(name="Minecraft", url='https://www.twitch.tv/greeinek'))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    else:
        with open('reactrole.json') as file:
            data = json.load(file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)

                if x['emoji_two'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    second_role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x['role_id_two'])
                    await payload.member.add_roles(second_role)


@bot.event
async def on_raw_reaction_remove(payload):
    with open('reactrole.json') as file:
        data = json.load(file)
    for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
            role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x['role_id'])
            await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@bot.event
async def on_member_join(member):
    logEmbed = discord.Embed(title=member, colour=0xCD5C5C)
    logEmbed.set_author(name="Dołączył do nas")
    logEmbed.add_field(name="ID", value=member.id, inline=False)
    logEmbed.add_field(name="Cyfra po Haszu", value=member.discriminator, inline=False)
    logEmbed.add_field(name="Konto stworzono", value=member.created_at.strftime("%A, %d %B %Y | %H:%M:%S"), inline=False)
    logEmbed.add_field(name="Dołączono", value=member.joined_at.strftime("%A, %d %B %Y | %H:%M:%S"), inline=False)
    logEmbed.add_field(name="Czy jest botem", value=member.bot, inline=False)
    logEmbed.set_thumbnail(url=member.avatar_url)
    channel = bot.get_channel(841381710502953000)
    await channel.send(embed=logEmbed)


@bot.event
async def on_member_remove(member):
    logEmbed = discord.Embed(title=member, colour=0xFFFF00)
    logEmbed.set_author(name="Opuścił nas")
    logEmbed.add_field(name="ID", value=member.id, inline=False)
    logEmbed.add_field(name="Cyfra po Haszu", value=member.discriminator, inline=False)
    logEmbed.add_field(name="Dołączył", value=member.joined_at.strftime("%A, %d %B %Y | %H:%M:%S"), inline=False)
    logEmbed.add_field(name="Czy jest botem", value=member.bot, inline=False)
    logEmbed.set_thumbnail(url=member.avatar_url)
    channel = bot.get_channel(841381710502953000)
    await channel.send(embed=logEmbed)


bot.load_extension("mute")
bot.load_extension("BanKick")
bot.load_extension("advertisement")
bot.load_extension("clear")
bot.load_extension("warns")
bot.load_extension("roles")
bot.load_extension("donate")

bot.run("ODM2ODk5Nzg4NDQzMDkxMDA1.YIktqg.u27KPgYWPcMkqunuGZ4PgTHJQj8")
