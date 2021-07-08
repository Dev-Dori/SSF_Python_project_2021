import discord
from discord.ext import commands
import requests

game = discord.Game("히히")
client = discord.Client()
bot = commands.Bot(command_prefix='', status=discord.Status.online, activity=game)

@bot.command(aliases=['도움말'])
async def info(ctx):
    embed = discord.Embed(title="School Bot", description="유니폭스와 함께 만드는 학교봇", color=0x4432a8)
    embed.add_field(name="1. 학교정보", value=" = 명령어 = ", inline=False)
    embed.add_field(name="2. 오늘의 급식", value=" = 명령어 = ", inline=False)
    embed.add_field(name="3. 시간표", value="= 명령어 =", inline=False)
    embed.add_field(name="4. 학사일정", value="= 명령어 =", inline=False)
    embed.add_field(name="이것은 필드 3입니다.", value="필드의 값입니다.", inline=True)
    return await ctx.send(embed=embed)

@bot.command(aliases=['학교정보'])
async def school(ctx, name):
    print(name)
    url = "https://open.neis.go.kr/hub/schoolInfo?Type=json&pIndex=1&pSize=100&KEY=0e4b9ebffe9b4389b2b2a610de303fe7&SCHUL_NM="+name
    print(url)
    data = requests.get(url).json()
    print(data)
    return await ctx.send(data)

@bot.command(aliases=['급식정보'])
async def lunch(ctx, name):
    print(name)
    url = "https://open.neis.go.kr/hub/schoolInfo?Type=json&pIndex=1&pSize=100&KEY=0e4b9ebffe9b4389b2b2a610de303fe7&SCHUL_NM="+name
    print(url)
    data = requests.get(url).json()
    print(data)
    return await ctx.send(data)





bot.run('NzUyNTQ0NzQzMDc4MjMyMTE0.X1ZL6A.d8NStWRYjTnWQEuce5-oJkEZi2k')
