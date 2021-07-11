import discord
from discord.ext import commands
import requests

game = discord.Game("히히")
bot = commands.Bot(command_prefix='>', status=discord.Status.online, activity=game)
SCHUL_INFO = {}



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
    data = info_request(name)
    return await ctx.send(data)

@bot.command(aliases=['급식정보'])
async def lunch(ctx, name):
    info = info_request(name)
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?Type=Json&SD_SCHUL_CODE="+info[1]
    url += "&ATPT_OFCDC_SC_CODE="+info[2]+"&MLSV_YMD=20210709&KEY=<API KEY>"
    #print(url)
    data = requests.get(url).json()
    data = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].replace("<br/>","\n")
    return await ctx.send(data)

@bot.command(aliases=['시간표'])
async def timetable(ctx, name, date):
    #https://open.neis.go.kr/hub/misTimetable?ATPT_OFCDC_SC_CODE=T10&SD_SCHUL_CODE=7003714 
    table = ""
    info = info_request(name)
    url = "https://open.neis.go.kr/hub/hisTimetable?SD_SCHUL_CODE="+info[1]+"&ATPT_OFCDC_SC_CODE="+info[2]+"&GRADE=2&CLASS_NM=3&ALL_TI_YMD="+date+"&Type=json&KEY=<API KEY>&SCHUL_NM="
    data = requests.get(url).json()
    data = data['hisTimetable']
    for i in range(len(data[1]['row'])):
        table += f"{i+1}교시 : {data[1]['row'][i]['ITRT_CNTNT']}\n" #data[1]['row'][i]['ITRT_CNTNT']+"\n"
    return await ctx.send(table)

@bot.command(aliases=['학사일정'])
async def school(ctx, name):
    data = info_request(name)
    return await ctx.send(data)

def info_request(name):
    if SCHUL_INFO.get(name) == None:
        url = url = "https://open.neis.go.kr/hub/schoolInfo?Type=json&pIndex=1&pSize=100&KEY=<API KEY>&SCHUL_NM=" + name
        data = requests.get(url).json()
        print(data)
        info = data['schoolInfo'][1]['row'][0]
        SCHUL_INFO.update({info['SCHUL_NM']:[info['SCHUL_NM'],info['SD_SCHUL_CODE'],info['ATPT_OFCDC_SC_CODE']]})
        return [info['SCHUL_NM'],info['SD_SCHUL_CODE'],info['ATPT_OFCDC_SC_CODE']]
    else : 
        return SCHUL_INFO[name]


bot.run('<discord token>')