import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(client.user.name)

@client.event
async def on_message(message):
    prefix = "/"
    command = message.content[1:]
    if message.content.startswith(prefix):
        if command[0:4] == "회원가입":
            if command[5:7] == "/?":
                await message.channel.send("""
사용법:
        /회원가입 (기본적인 유저권한을 발급받습니다.)""")
            else:
                await message.channel.send("권한을 발급합니다.")
                author = message.guild.get_member(int(message.author.id))
                role = discord.utils.get(message.guild.roles, name="회원")
                await author.add_roles(role)
                role = discord.utils.get(message.guild.roles, name="비회원")
                await author.remove_roles(role)
        if command[0:4] == "회원탈퇴":
            if command[5:7] == "/?":
                await message.channel.send("""
사용법:
        /회원탈퇴 (기본 회원 권한을 뺏깁니다.)""")
            else:
                await message.channel.send("권한을 삭제합니다.")
                author = message.guild.get_member(int(message.author.id))
                role = discord.utils.get(message.guild.roles, name="회원")
                await author.remove_roles(role)
                role = discord.utils.get(message.guild.roles, name="비회원")
                await author.add_roles(role)
        elif command[0:4] == "도움":
            await message.channel.send("""
도움은 명령어 뒤에 /? 를 붙여주세요.
/도움
/회원가입
/회원탈퇴""") 

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
