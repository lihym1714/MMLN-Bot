import discord
from discord import *
from discord.ext import commands

TOKEN="MTI0NzAzOTU2MjIzNzA4MzcwOQ.GbMNYO.Syu-nhPHHY1hZUYgAcFpn-wPTI1Npz5tdwPcD8"

ADMIN_CHANNEL_ID="1235481317085544468"

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Successfully running")

# 특정 채널에서만 명령어를 받을 수 있도록 필터링하는 검사 함수
def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.command(name="genEmbed")
@commands.check(is_admin)
async def genEmbed(ctx, message:str):
    main = message.split("|")[0]
    link = message.split("|")[1]
    embed = discord.Embed(title=main, description="```"+link+"```", color=10181046)
    await ctx.send(embed=embed)

# 명령어가 특정 조건을 만족하지 않을 때 발생하는 예외를 처리하는 핸들러
@genEmbed.error
async def gen_embed_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Permission denied, Only admin can use this command.')
    else:
        await ctx.send('Unknown Error Required.')



bot.run(TOKEN)