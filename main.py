import discord
from discord import *
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime, timedelta, timezone

from util import *
import asyncio
import pytz
from random import *
import luck
import re

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

startDateTime = datetime.utcnow()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="도움말", description="못말이의 명령어 사용법을 알려줘요!")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="명령어", description="!오늘의운세 : 오늘의 운세를 볼 수 있어요!\n!마법의소라고동님 : 무언가에 대해 정할 수 있어요!", color=discord.Color.from_rgb(119,79,219))
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="임베드생성", description="관리자용 명령어 임베드")
@commands.has_permissions(administrator=True)
async def embedGen(interaction:discord.Interaction,채널:str,타이틀:str,본문:str="",링크:str=""):
    embed=discord.Embed()
    color = discord.Color.from_rgb(119,79,219)
    채널 = re.sub(r'[^\w\s]', '', 채널)
    if 본문=="" and 링크=="": embed = discord.Embed(title=타이틀, color=color)
    elif 본문=="" and 링크!="": embed = discord.Embed(title=타이틀, description=getBox(링크), color=color)
    elif 링크=="" and 본문!="": embed = discord.Embed(title=타이틀, description=본문, color=color)
    else: embed = discord.Embed(title=타이틀, description=f"**{본문}**\n```"+링크+"```", color=color)

    channel = bot.get_channel(int(채널))
    await channel.send(embed=embed)
    await interaction.response.send_message(f"{channel.name} 채널에 임베드를 전송했습니다.", ephemeral=True)

@bot.tree.command(name="채팅", description="관리자용 명령어. 채팅")
@commands.has_permissions(administrator=True)
async def genNormalMsg(interaction:discord.interactions,채널:str,내용:str):
    채널 = re.sub(r'[^\w\s]', '', 채널)

    await bot.get_channel(채널).send(내용)
    await interaction.response.send_message(f"", ephemeral=True)

@bot.tree.command(name="초대링크", description="관리자용 명령어. 초대링크 전송")
@commands.has_permissions(administrator=True)
async def genInviteMsg(interaction:discord.interactions, div:int):
    msg = [
        "와글와글 못말리는 단톡방 올 길드원은 편하게 요 링크로 신청해!❤️ 일중이라 수락 좀 느리니 취소하지마랑!!!! \nhttps://invite.kakao.com/tc/HK07biB58S",
        "데박 당신은 못말리는 단톡방에 초대됬다 요 링크로 신쳥하지 안으면 당신은 쥭는다 \nhttps://invite.kakao.com/tc/HK07biB58S",
        "당신은 월급 루팡의 성지 못말리는 단톡방에 초대됐다! 길드원들 모두 여기서 신나게 놀고 있으니 어서 신청해라!! \nhttps://invite.kakao.com/tc/HK07biB58S",
        "초특✠급 ㅇㅣ벤트! 못말ت❢ㄹㅣ는  ε단톡방❅ ✮입➸장권 □ㅏ감 임박! 늦ㄱㅣ전에 오rㄹr!➨ \nhttps://invite.kakao.com/tc/HK07biB58S",
        "못말리는 카톡방에 초대됐다고? 완저이 럭키비키니시티잖아~ \nhttps://invite.kakao.com/tc/HK07biB58S",
        "♚♚데박 이벤☆트 ♚♚못말♡리는 단♧톡 $$ 신청시 무료 입장☜☜못말리는 굿즈※ ♨추첨 증정♨ 이벤트 당첨￥ 특정조건 §§월급루팡 클럽§§ ★활발한 잡담★링크 신청안할시 죾음@@즉시이동 \nhttps://invite.kakao.com/tc/HK07biB58S"
    ]
    await bot.get_channel(1235186405081354282).send(msg[div])
    await interaction.response.send_message(f"초대링크를 성공적으로 전송했어요.", ephemeral=True)

@bot.event
async def on_ready():
        synced = await bot.tree.sync()
        print(f'Logged in as {bot.user}')

# 일반 User 사용 가능 기능
    
@bot.command(name="오늘의운세")
async def genFortune(ctx):
    await ctx.send(luck.getFortune())


@bot.command(name="마법의소라고동님")
async def genRandomBool(ctx,*txt:str):
    msg = ""
    for i in txt:
        msg+=i
    if 1 > len(msg.replace(" ","")):
        await ctx.send(choice(["뭐.","왜."]))
        return
    result = randrange(0,2)
    if result == 1:
        await ctx.send(choice(["그래.","그럼."]))
    else:
        await ctx.send(choice(["아니.","안 돼."]))


# 특정 채널에서만 명령어를 받을 수 있도록 필터링하는 검사 함수
def is_admin(ctx):
    return ctx.author.guild_permissions.administrator


@bot.command(name="genSticky")
@commands.check(is_admin)
async def stickyMsg(msg):
    return

@bot.command(name="업타임")
async def uptime(ctx):
    now = datetime.utcnow()
    delta = now - startDateTime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours} 시간, {minutes} 분, {seconds} 초"
    await ctx.send(f"업타임: {uptime_str}")


# @tasks.loop(hours=1)
# async def send_invite():
#     chan = bot.get_channel(1235186405081354282)
#     dt = datetime.now()
#     timezone_kst = timezone(timedelta(hours=9))
#     dt_kst = dt.astimezone(timezone_kst)
#     print(f"h{dt_kst.hour} m{dt_kst.minute}")
#     message = "와글와글 못말리는 단톡방 올 길드원은 편하게 요 링크로 신청해!❤️ 일중이라 수락 좀 느리니 취소하지마랑!!!! ```https://invite.kakao.com/tc/HK07biB58S```"
#     if (dt_kst.hour == 12):
#         await chan.send(message)
    

@bot.command(name="출석리스트")
@commands.check(is_admin)
async def get_at_users(ctx, date: str):
    # 채널 객체 가져오기
    channel = bot.get_channel(1235182853386403882)
    if not channel:
        await ctx.send("Invalid channel ID.")
        return
    
    # 날짜 파싱
    target_date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=23, minute=59, second=59, microsecond=59)
    
    # 메시지 가져오기
    users = set()
    async for message in channel.history(limit=None, after=target_date, before=end_date):
        # "출석" 또는 "출첵"이 포함된 경우와 봇이 아닌 경우만 처리
        if any(keyword in message.content for keyword in ["!출석", "!출첵"]) and not message.author.bot:
            # 메시지 작성자가 Member 객체인지 확인
            if isinstance(message.author, discord.Member):
                # 별명 가져오기, 별명이 없으면 기본 사용자명 사용
                nickname = message.author.nick if message.author.nick else message.author.name
            else:
                # Member 객체가 아니면 기본 사용자명 사용
                nickname = message.author.name
            users.add(f"{nickname}")
    
    # 결과 출력
    if users:
        user_list = "\n".join(users)
        # embed = discord.Embed(title="출석 유저", description=f"{users}", color=discord.Color.from_rgb(119,79,219))
        embed = discord.Embed(title="출석 사용자", description=f"{date}에 출석한 사용자들:\n{user_list}", color=discord.Color.from_rgb(119,79,219))
        await ctx.send(embed=embed)
    else:
        await ctx.send("No messages found on that date.")


@bot.command(name="기간출석리스트")
@commands.check(is_admin)
async def get_users(ctx, start_date: str, end_date: str):
    # 채널 객체 가져오기
    channel = bot.get_channel(1235182853386403882)
    if not channel:
        await ctx.send("Invalid channel ID.")
        return
    
    KST = timezone(timedelta(hours=9))
    
    # 날짜 파싱
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=23, minute=59, second=59, microsecond=59)
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        return


    # 메시지 가져오기
    user_dates = {}
    user_nicknames = {}
    async for message in channel.history(limit=None, after=start_date, before=end_date):
        if any(keyword in message.content for keyword in ["!출석", "!출첵"]) and not message.author.bot:
            nickname = message.author.nick if isinstance(message.author, discord.Member) and message.author.nick else message.author.name
            display_name = message.author.display_name
            
            # 날짜를 키로 하여 사용자의 출석 기록 저장
            message_date = message.created_at.astimezone(pytz.timezone('Asia/Seoul')).date()
            if nickname not in user_dates:
                user_dates[nickname] = set()
                user_nicknames[nickname] = display_name  # 사용자 별명 저장
            user_dates[nickname].add(message_date)

    # 카운트
    user_counts = {user: len(dates) for user, dates in user_dates.items()}

    # 정렬: 횟수가 많은 순으로
    sorted_user_counts = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

    # 결과 출력
    if sorted_user_counts:
        user_list = "\n".join([f"{user}: {count}회" for user, count in sorted_user_counts])
        embed = discord.Embed(title="출석 사용자", description=f"{start_date.date()}부터 {end_date.date()}까지 출석한 사용자들:\n{user_list}", color=discord.Color.from_rgb(119, 79, 219))
        await ctx.send(embed=embed)
    else:
        await ctx.send("No messages found in that date range.")



@bot.command(name="기간출석리스트중복")
@commands.check(is_admin)
async def get_at_users(ctx, start_date: str, end_date: str):
    # 채널 객체 가져오기
    channel = bot.get_channel(1235182853386403882)
    if not channel:
        await ctx.send("Invalid channel ID.")
        return
    
    # 날짜 파싱
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Seoul')).replace(hour=23, minute=59, second=59, microsecond=59)
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        return

    # 메시지 가져오기
    user_counts = {}
    async for message in channel.history(limit=None, after=start_date, before=end_date):
        if any(keyword in message.content for keyword in ["!출석", "!출첵"]) and not message.author.bot:
            if isinstance(message.author, discord.Member):
                nickname = message.author.nick if message.author.nick else message.author.name
            else:
                nickname = message.author.name
            
            user_counts[nickname] = user_counts.get(nickname, 0) + 1

    # 정렬: 횟수가 많은 순으로
    sorted_user_counts = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

    # 결과 출력
    if sorted_user_counts:
        user_list = "\n".join([f"{user}: {count}회" for user, count in sorted_user_counts])
        embed = discord.Embed(title="출석 사용자(중복 포함)", description=f"{start_date.date()}부터 {end_date.date()}까지 출석한 사용자들:\n{user_list}", color=discord.Color.from_rgb(119, 79, 219))
        await ctx.send(embed=embed)
    else:
        await ctx.send("No messages found in that date range.")


bot.run(TOKEN)