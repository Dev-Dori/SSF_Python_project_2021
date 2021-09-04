import discord
from discord.ext import commands
import requests
import datetime

############# 제작환경 기초 설정 #############

    ########################
    #  1. 봇 설정하기       #
    ########################

game = discord.Game(">도움말") # <== 1. 자신이 원하는 봇의 상태 메세지를 지정하기
bot = commands.Bot(command_prefix='>',
                   status=discord.Status.online,
                   activity=game)

TOKEN = "<봇 토큰>"  # <== 2. 자신이 발급받은 디스코드 봇의 토큰을 입력 
API_KEY = "<API 키 >"    # <== 3. 자신이 발급받은 교육청 API 키를 입력


########### 디스코드 봇 활성화 알림 ###########
@bot.event
async def on_ready():
  print('==== 디스코드 봇 활성화됨 ====')

############### 이미지 설정하기 ################

# 자신이 응답으로 사용할 이미지를 지정
# * 자신이 원하는 사진의 URL을 넣어 이미지를 지정해주세요 *

# 학교정보에 사용될 이미지
img_school = "https://cdn.discordapp.com/attachments/867330041430802482/867571458023489597/images.png"

# 시간표에 사용될 이미지 (footer는 응답 메세지의 최하단에 있는 작은 이미지를 의미합니다)
timetable_img = "https://devdori.com/img/unifox/uni.png" 
timetable_footer_img = "https://cdn.discordapp.com/attachments/867330041430802482/867349566353309716/gqHl3eQJD4LgAAAABJRU5ErkJggg.png"

# 시간표에 사용될 이미지
calendar_img = 'https://cdn.discordapp.com/attachments/867330041430802482/875048808290082816/Z.png'

###############################################

SCHUL_INFO = {} 
now = datetime.datetime.now()


def info_request(name):
  print(name+"", SCHUL_INFO.get(name))
  if SCHUL_INFO.get(name) == None:

    #################################################################
    #==== 2. URL이라는 문자열과 name이라는 문자열을 더해서 연결하기 ====#
    #==== 3. 완성한 URL을 request 모듈을 활용하여 데이터를 요청하기 ====#
    #################################################################

       # url 완성 시키기
      url = "https://open.neis.go.kr/hub/schoolInfo?SCHUL_NM="+name 
      url += f"&Type=json&KEY={API_KEY}"  
      
      # API에서 받아온 데이터를 json형식으로 data에 저장

      data = requests.get(url).json()       # 완성시킨 URL로 데이터를 요청하기
      info = data['schoolInfo'][1]['row'][0]

      SCHUL_INFO[name]={
          "학교이름"      :info['SCHUL_NM'],
          "교육청"        :info['JU_ORG_NM'],
          "학교종류"      :info['SCHUL_KND_SC_NM'],
          "학교주소"      :info['ORG_RDNMA'],
          "학교번호"      :info['ORG_TELNO'],
          "홈페이지"      :info['HMPG_ADRES'],
          "남녀공학구분"  :info['COEDU_SC_NM'],
          "공립사립구분"  :info['FOND_SC_NM'],
          "학교코드"      :info['SD_SCHUL_CODE'],
          "교육청코드"    :info['ATPT_OFCDC_SC_CODE'],
          "설립일자"      :info['FOND_YMD'],
          "학교구분명"    :info['HS_SC_NM'],
      }



@bot.command(aliases=['도움말']) # <==   >도움말 명령어를 입력했을때 아래 함수가 작동하도록 만들어주세요
async def info(ctx):
  embed = discord.Embed(
          title="School Bot",
          description="유니폭스와 함께 만드는 학교봇\n ",
          color=0xb9e2ee
          )

  embed.add_field(
          name="1. 학교정보",
          value='''
                  ```
                  >학교정보 <학교명>
                  
                  예시)
                  >학교정보 선린인터넷고
                  ```
                '''.replace("  ",""),
          inline=False
          )

  embed.add_field(
          name="2. 오늘의 급식", 
          value='''
                  ```
                  >급식정보 <학교명> <월+일>
                  
                  예시)
                  >급식정보 선린인터넷고 601
                  ```
                '''.replace("  ",""),
          inline=False
          )

  embed.add_field(
          name="3. 시간표",
          value='''
                  ```
                  >시간표 <학교명> <학년> <반> <월+일>
                  
                  예시)
                  >시간표 선린인터넷고 2 3 601
                  ```
                '''.replace("  ",""), 
          inline=False
          )

  embed.add_field(
          name="4. 학사일정",
          value='''
                  ```
                  >학사일정 <학교명> <년+월+일>
                  
                  예시)
                  >학사일정 선린인터넷고 20210814
                  ```
                '''.replace("  ",""), 
          inline=False
          )
  return await ctx.send(embed=embed)



@bot.command(aliases=['학교정보']) # <==   >학교정보 라고 명령어를 입력했을때 아래 함수가 작동하도록 만들어주세요
async def school(ctx, name):
  try:
    info_request(name)  

    ##################################
    # ===== 4. 딕셔너리 사용하기 ====  #
    ##################################

    embed=discord.Embed(title=name+"의 정보",color=0xb9e2ee)
    embed.set_thumbnail(url=img_school)
    embed.add_field(name="교육청",value=SCHUL_INFO[name]["교육청"])
    embed.add_field(name="학교종류",value=SCHUL_INFO[name]["학교종류"])
    embed.add_field(name="학교 주소",value=SCHUL_INFO[name]["학교주소"])   # <= info_request 함수에 SCHUL_INFO를
    embed.add_field(name="학교 번호",value=SCHUL_INFO[name]["학교번호"])   # 참고해서 학교주소와 학교정보를 가져와주세요
    embed.add_field(name="학교 홈페이지",value=f"[홈페이지]({SCHUL_INFO[name]['홈페이지']})")
    embed.add_field(name="남/여/공학 구분",value=SCHUL_INFO[name]["남녀공학구분"])
    embed.add_field(name="공립/사립",value=SCHUL_INFO[name]["공립사립구분"])
    embed.add_field(name="학교 종류",value=SCHUL_INFO[name]["학교구분명"])
    embed.add_field(name="학교 설립일", 
                    value=f'''{SCHUL_INFO[name]["설립일자"][ :4]}/
                              {SCHUL_INFO[name]["설립일자"][4:6]}/
                              {SCHUL_INFO[name]["설립일자"][6:]}'''.replace("\n","")
                    )
    return await ctx.send(embed=embed)
  except:
    return await ctx.send(f"검색하신 학교정보를 찾을 수 없습니다.")



@bot.command(aliases=['급식정보']) #>급식정보
async def lunch(ctx, name, date):
  info_request(name)
  #학교/교육청 코드를 url에 추가함 -> 해당 정보가 없다면 url을 호출할 때 오류가 생김
  url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?"
  url += f"SD_SCHUL_CODE={SCHUL_INFO[name]['학교코드']}&"
  url += f"ATPT_OFCDC_SC_CODE={SCHUL_INFO[name]['교육청코드']}&"
  url += f"MLSV_YMD={date}"
  url += f"&Type=json&KEY={API_KEY}"

  try:
      data = requests.get(url).json()
      meal = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].replace("<br/>", "\n")
      embed = discord.Embed(title=name+"의 급식입니다",colour=discord.Colour.green())
      return_date = f"{now.strftime('%Y')}년 "
      return_date += f"{int(int(date)/100)}월 "
      return_date += f"{int(int(date)%100)}일"
      embed.add_field(name=return_date,value="```css\n"+meal+"```")
      return await ctx.send(embed=embed)

  except:
      data = f"{now.strftime('%Y')}년 "
      data += f"{int(int(date)/100)}월 "
      data += f"{int(int(date)%100)}일의 "
      data += f"{SCHUL_INFO[name]['학교이름']} "
      data += "급식 정보를 찾을 수 없습니다."
      return await ctx.send(data)


@bot.command(aliases=['시간표'])  # <==   >시간표 명령어를 입력했을때 아래 함수가 작동하도록 만들어주세요
async def timetable(ctx, name, grade, sclass, date):
  try:
    info_request(name)

    year = str(now.strftime('%Y'))[2:]
    month = int(int(date)/100)
    day = int(int(date)%100) # 시간 정보를 년도, 달, 일로 분할
    
    if SCHUL_INFO[name]['학교종류'] == "고등학교":
      url =  f"https://open.neis.go.kr/hub/hisTimetable?"

    elif SCHUL_INFO[name]['학교종류'] == "중학교":
      url =  f"https://open.neis.go.kr/hub/misTimetable?"      
    
    url += f"SD_SCHUL_CODE={SCHUL_INFO[name]['학교코드']}"
    url += f"&ATPT_OFCDC_SC_CODE={SCHUL_INFO[name]['교육청코드']}" #학교 코드를 url에 추가함 -> 해당 정보가 없다면 url을 호출할 때 오류가 생김
    url += f"&GRADE={grade}&CLASS_NM={sclass}"
    url += f"&ALL_TI_YMD={year}{str(month).zfill(2)}{str(day).zfill(2)}" #입력받은 날짜를 url에 추가함 -> 해당 정보가 없다면 url을 호출할 때 오류가 생김
    url += f"&Type=json&KEY={API_KEY}"

    data = requests.get(url).json()
    if SCHUL_INFO[name]['학교종류'] == "고등학교":
      data = data['hisTimetable']
    elif SCHUL_INFO[name]['학교종류'] == "중학교":
      data = data['misTimetable']


    #################################################
    #==== 5. 문자열 포맷팅을 사용해서 변수 사용하기 ====#
    #################################################

    # 년,월,일,학년,반 에 해당하는 변수를 넣어주세요 
    # (변수명 : 년 = year, 월 = month , 일 = day, 학년=grade, 반=sclass))
    embed = discord.Embed(title=f"{month}년 {day}월 {day}일",  
                          description=((name)+f"\n{grade}학년{sclass}반 시간표"),
                          color=0xb9e2ee)
                          
    embed.set_thumbnail(url=timetable_img)

    #############################
    #===== 6. for문 완성하기 ====#
    #############################
      
    for i in range(len(data[1]['row'])):  
        embed.add_field(name=f"{i+1} 교시 :  ",
                        value=data[1]['row'][i]['ITRT_CNTNT'],
                        inline=False)
    


    embed.set_footer(text="2021 소프트웨어 나눔 축제",icon_url=timetable_footer_img)
    return await ctx.send(embed=embed)

  except:
    return await ctx.send("요청하신 시간표를 찾을 수 없습니다.")


@bot.command(aliases=['학사일정']) #>학사일정
async def calendar(ctx, name, date):
  try:
    info_request(name)

    url = f"https://open.neis.go.kr/hub/SchoolSchedule?"
    url += f"ATPT_OFCDC_SC_CODE={SCHUL_INFO[name]['교육청코드']}&"
    url += f"SD_SCHUL_CODE={SCHUL_INFO[name]['학교코드']}&"
    url += f"Type=json&KEY={API_KEY}&AA_YMD={date}"
    data = requests.get(url).json()

    year = int(int(date)/10000)
    month = int(int(date)%10000/100)
    day = int(int(date)%100)
    
    embed = discord.Embed(title=((name)+f"의 학사일정"),
                          description=f"{year}년 {month}월 {day}일" ,
                          color=0xb9e2ee)
                          
    embed.set_thumbnail(url=calendar_img)
    event = data["SchoolSchedule"][1]["row"][0]

    if event["EVENT_CNTNT"] == None:
      EVENT_CNTNT="내용없음"


    ###########################################################
    #              ==== 7. <조건문 활용하기> ====              #   
    # 문자열 형변환과 문자열 길이를 비교하는 if 비교문을 작성하기 #
    ##########################################################

    # *조건* : date의 길이가 8일때와 8이 아닐경우 
    if len(date) == 8 : # date의 문자열 길이가 8이랑 같을때
      embed.add_field(name=(event["EVENT_NM"]), value=(EVENT_CNTNT),inline=False)
      return await ctx.send(embed=embed)

    else: # 조건과 다를 때
      embed.add_field(name="날짜 오류",value="날짜를 다시 입력해주세요.")
      return await ctx.send(embed=embed)
  except:
    return await ctx.send("요청하신 날짜에 대한 정보가 없습니다!")

bot.run(TOKEN)