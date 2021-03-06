import discord
import random
import asyncio
import requests
from bs4 import BeautifulSoup
import time
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("sample_in.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("jalnan.ttf", 40)

client = discord.Client()

@client.event
async def on_ready():
    global timer
    print(client.user.name)
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="{} 개의 도시, {} 명의 약한 시민들".format(len(client.guilds), len(client.users))))
        await asyncio.sleep(3)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="+도움 을 입력하세요"))
        await asyncio.sleep(3)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="어디든지 날아가 드립니다"))
        await asyncio.sleep(3)

@client.event
async def on_message(message):
    embed = discord.Embed(title="채팅로그", description=str(message.author) + " 님의 채팅")
    embed.add_field(name="서버", value=str(message.author.guild))
    embed.add_field(name="채팅", value=message.content)
    await client.get_channel(632152755561037834).send(embed=embed)
    prefix  = "+"
    command = message.content[1:]
    if message.content.startswith(prefix):
       if command[0:3] == "텍스트":
            await message.channel.send("텍스트를 입력하세요.")
            def check(m):
                return m.channel == channel
            try:
                m = await client.wait_for('message', timeout=7.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send("시간초과!")
            else:
                await message.channel.send("알겠습니다.")
                draw.text((0, 0),"Sample Text",(1,1,1),font=font)
                img.save('sample-out.jpg')
                await message.channel.send(file=discord.File("sample-out.jpg"))
        elif command[0:3] == "메시지":
            if command[4:6] == "/?":
                await message.channel.send("""
사용법:
        +메시지 <메시지>""")
            else:
                say = message.content[4:]
                await message.channel.send(say)
        elif command[0:2] == "정보":
            if command[3:5] == "/?":
                await message.channel.send("""
사용법:
        +정보""")
            else:
                global sangte
                global s
                global sa
                sangte = message.author.status
                s = str(sangte)
                if s == "online":
                    sa = "온라인"
                if s == "idle":
                    sa = "자리비움"
                if s == "dnd":
                    sa = "다른 용무 중"
                if s == "offline":
                    sa = "오프라인"
                embed = discord.Embed(title="당신의 정보", description="당신의 정보",color=0x00ff00)
                embed.add_field(name="이름", value=message.author.mention)
                embed.add_field(name="상태", value=sa)
                embed.add_field(name="클라이언트 아이디", value=str(message.author.id))
                embed.add_field(name="역할", value=message.author.roles[1].name)
                embed.set_thumbnail(url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command[0:2] == "투표":
            if command[3:5] == "/?":
                await message.channel.send("""
이것으로 투표를 진행할수 있습니다.
사용법:
        +투표 <1번> <2번> <......""")
            else:
                global tu
                tu = command[3:].split(" ")
                if len(tu) > 5:
                    await message.channel.send(message.author.mention + ", 투표는 5이하로만 해주세요. (도배 위험)")
                else:
                    tu = command[3:].split(" ")
                    await message.channel.send("```투표를 진행합니다.```")
                    embed = discord.Embed(title="투표", description="투표를 진행하겠습니다")
                    for x in range(len(tu)):
                        haha = tu[x]
                        embed.add_field(name=haha, value=haha + "이(가) 마음에드시면 " + str(x + 1) + " (이)라고 해주세요.")
                    embed.set_footer(text=message.author.name + " 님의 요청")
                    await message.channel.send(embed=embed)
                
        elif command[0:2] == "수학":
            if command[3:5] == "/?":
                await message.channel.send("""
설명:
        당신은 6초안에 출제되는 수학문제를 맞추셔야 합니다. 그냥 답을 숫자로 메시지를 보내주시면 되요.
사용법:
        +수학
        봇: X + X 은?
        사람: (답인 숫자)""")
            else:
                global answer
                what = random.randint(1, 3)
                await message.channel.send("수학 문제 들어갑니다~!")
                channel = message.channel
                a1 = int(random.randint(1, 9))
                a2 = int(random.randint(1, 9))
                human = int(message.author.id)

                if what == 1:
                    answer = a1 + a2
                    await message.channel.send(str(a1) + " + " + str(a2) + " 은?")
                elif what == 2:
                    answer = a1 - a2
                    await message.channel.send(str(a1) + " - " + str(a2) + " 은?")
                elif what == 3:
                    answer = a1 * a2
                    await message.channel.send(str(a1) + " x " + str(a2) + " 은?")

                def check(m):
                    return m.content == str(answer) and m.channel == channel and int(message.author.id) == human
                try:
                    m = await client.wait_for('message', timeout=5.0, check=check)
                except asyncio.TimeoutError:
                    await channel.send("땡!")
                else:
                    await channel.send("우와 정말 대.단.한.걸.??")
        elif command[0:4] == "서버":
            if command[3:5] == "/?":
                await message.channel.send("""
사용법:
        +서버""")
            else:
                embed = discord.Embed(title="슈퍼준영맨", description="도움이 필요한 도시들 목록",color=0x00ff00)
                server = client.guilds
                for x in range(0, len(server)):
                    aa = server[x]
                    embed.add_field(name=aa, value="소중한 도시")
                embed.set_footer(text=message.author.name + " 당신도 이중에 하나입니다")
                await message.channel.send(embed=embed)
        elif command[0:4] == "서버정보":
            await message.channel.send(message.author.guild)
        elif command[0:2] == "규칙":
            if command[3:5] == "/?":
                await message.channel.send("""
설명:
        이 봇의 규칙입니다.
사용법:
        +규칙 <규칙 번호>""")
            else:
                global rule
                rule = ['에티켓을 지켜주세요!', '맘대로 서버 막 초대하고 그러면 테러해드립니다 ^^', '이 봇 해킹하면 죽여버릴꺼에요 ^^']
                n = command[3:]
                try:
                    print(n)
                except discord.errors.HTTPException:
                    await message.channel.send("흠.... 잘못된것 같은데요..")
                try:
                    nn = int(n)
                except ValueError:
                    await message.channel.send("숫자만 입력하세요.")
                if nn > 3:
                    await message.channel.send("3보다 클순 없어요.")
                else:
                    await message.channel.send(rule[nn - 1])
                
        elif command[0:2] == "도움":
            if command[3:5] == "/?":
                await message.channel.send("와... 설마 이런것 까지 볼려했다니.. 대단해! " + message.author.mention + "!")
            else:
                embed = discord.Embed(title="도움말", description="""
도움은 명령어 뒤에 /? 를 붙여주세요.
+메시지 /?
+정보 /?
+수학 /?
+도움 /?
+서버 /?
+규칙 /?
+투표 /?
+프로필 (얘는 /?가 필요없습니다.)
+초대
+날씨 /?
+디스코드 /?
+타이머
+웹체크 /?
----개발 & 테스트중----
+검색
----개발예정----
위키 검색""")
                await message.channel.send(embed=embed)
        elif command == "프로필":
            embed = discord.Embed(title="프로필", description=str(message.author))
            embed.set_image(url=message.author.avatar_url)
            embed.set_footer(text=str(message.author) + " 님의 요청")
            embed.add_field(name="만약 보이지 않는다면?", value="[[ 사진 보기 ]](" + str(message.author.avatar_url) + ")")
            await message.channel.send(embed=embed)
        elif command[0:2] == "날씨":
            if command[3:5] == "/?":
                await message.channel.send("""
설명:
        이건 우리나라 지역만 날씨를 볼수있으며 실제 기상청에서 발표한 자료입니다. (네이버 날씨)
사용법:
        +날씨 <지역>""")
            else:
                try:
                    wldur = command[3:]
                    response = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + wldur + '날씨')

                    html = response.text

                    bs_obj = BeautifulSoup(html, "html.parser")
                    div = bs_obj.find("span", {"class": 'todaytemp'})
                    div2 = bs_obj.find("p", {"class": "cast_txt"})
                    div3 = bs_obj.find("span", {"class": "num"})
                    div4 = bs_obj.find("span", {"class": "indicator"})
                    div5 = div4.find("span", {"class": "num"})

                    w = int(div5.text)

                    embed = discord.Embed(title=wldur + " 의 날씨", description="날씨, 미세먼지등 기상정보 입니다.", color=0x28b3fd)
                    embed.add_field(name=div.text + "℃", value=div2.text, inline=False)
                    embed.add_field(name="초미세먼지", value=div3.text + "㎍/㎥", inline=False)
                    if w < 3:
                        ww = "자외선지수 " + str(w) + ", 이런날에 썬크림을 바르진 않겠죠?"
                    if w > 2 and w < 6:
                        ww = "자외선지수 " + str(w) + ", 뭐.. 썬크림 바를꺼면 바르세요.."
                    if w > 5 and w < 8:
                        ww = "자외선지수 " + str(w) + ", 오늘 썬크림 바르는게 어떨까요?"
                    if w > 7 and w < 11:
                        ww = "자외선지수 " + str(w) + ", 오늘 썬크림 꼭! 바르세요!"
                    if w > 10:
                        ww = "오늘 그냥 나가지마세요...."
                    embed.add_field(name="자외선 지수", value=ww)
                    await message.channel.send(embed=embed)
                except AttributeError or IndexError:
                    await message.channel.send("죄송하지만 알수 없는 오류가 발생하였습니다.")
        elif command[0:2] == "검색":
            if command[3:5] == "/?":
                await message.channel.send("""
사용법:
        +검색 <검색할 것>""")
            else:

                learn = command[3:]
                response = requests.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + learn)

                html = response.text

                bs_obj = BeautifulSoup(html, "html.parser")
                div = bs_obj.find("ul", {"class": 'type01'})
                div2 = div.find("a", {"class": '_sp_each_url _sp_each_title'})

                embed = discord.Embed(title=learn, description=learn + " 의 검색결과")
                embed.add_field(name="결과", value=div2, inline=False)
                await message.channel.send(embed=embed)
        elif command[0:2] == "초대":
            await message.channel.send(message.author.mention + ", https://discord.gg/ActTD3v 슈퍼준영맨 서버에 들어오세요.")
        elif command[0:4] == "디스코드":
            if command[5:7] == "/?":
                await message.channel.send("""
설명:
        API ping, API 업타임, 게이트웨이, 미디어 프록시 업타임을 보여줍니다.""")
            else:
                response = requests.get('https://status.discordapp.com')
                html = response.text
                bs = BeautifulSoup(html, "html.parser")
                api_uptime = bs.find("span", {"id": 'uptime-percent-rhznvxg4v7yh'}).text
                gateway_uptime = bs.find("span", {"id": 'uptime-percent-9lgt8qqpcqck'}).text
                media_proxy = bs.find("span", {"id": 'uptime-percent-r3wq1zsx72bz'}).text

                embed = discord.Embed(title="디스코드", description="디스코드 상태입니다.")
                embed.add_field(name="API 업타임: " + str(api_uptime), value="60일 이내로 잘 작동된 날의 비율입니다.", inline=False)
                embed.add_field(name="게이트웨이 업타임: " + str(gateway_uptime), value="기준은 API 업타임과 같습니다.", inline=False)
                embed.add_field(name="미디어 프록시 업타임: " + str(media_proxy), value="이하 동문입니다.", inline=False)
                embed.set_footer(text=str(message.author) + "의 요청, 더 자세한 정보가 궁금하다면 https://status.discordapp.com")
                await message.channel.send(embed=embed)
        elif command[0:3] == "타이머":
            all_break = "break"
            await asyncio.sleep(1)
            all_break = "start"
            timer = "시간: "
            set_time = "0"
            ui = timer + set_time
            uii = int(ui[3:])
            go = await message.channel.send(ui)
            go
            while uii < 100:
                await asyncio.sleep(1)
                uii = uii + 1
                await go.edit(content=timer + "`" + str(uii) + "`")
                if all_break == "break":
                    break
        elif command[0:3] == "웹체크":
            if command[4:6] == "/?":
                await message.channel.send("""설명:
    수동으로 원하는 웹사이트의 Html 소스 (요소) 를 가져올수 있습니다.
    단, 로그인이 필요한 사이트는 접근할수 없습니다.
    또 출력이 제대로 안될수 있습니다. 한번에 여러개의 소스는 가져올수 없습니다.
    예) url: https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=서울날씨, 태그: span class todaytemp""")
            else:
                channel = message.channel
                user = message.author
                await message.channel.send("URL 을 입력해주세요.")
                def check(m):
                    return m.channel == channel
                try:
                    m = await client.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await channel.send("시간초과로 다시 불러주세요.")
                else:
                    url = m.content
                    await message.channel.send("태그를 입력해주세요. (잘 모르시겠다면 +웹체크 /? 를 입력해주세요.)")
                    def check(m):
                        return m.channel == channel and m.author == user
                    try:
                        m = await client.wait_for('message', timeout=10.0, check=check)
                    except asyncio.TimeoutError:
                        await channel.send("시간초과로 다시 불러주세요.")
                    else:
                        tag = m.content
                        try:
                            tag1 = tag.split(" ")
                            tag2 = tag1[0]
                            tag3 = tag1[1]
                            tag4 = tag1[2]
                            response = requests.get(url)
                            html = response.text
                            bs = BeautifulSoup(html, "html.parser")
                            source = bs.find(tag2, {tag3: tag4}).text
                            embed = discord.Embed(title=url + " 에서 찾은 결과", description=source)
                            await message.channel.send(embed=embed)
                        except:
                            await message.channel.send("입력이 잘못되었습니다.")
        else:
            await message.channel.send("'" + command + "' (은)는 명령어가 아닙니다.")
            
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
