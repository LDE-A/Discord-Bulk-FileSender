"""
使い方
1.pythonをインストール
2.cmd開いてpy -m pip install pipでpipをインストール
3.requirementsに書いてあるライブラリをpipでインストール
4.下のTOKENにdiscordのTOKENを入れる
5.このpyファイル実行
6.youtubeの動画URLかプレイリストURLもしくはローカルのフォルダ名をdiscordのチャンネルに送信
------------------------------------------------
8mb以上のものnitroがないとアップロードできないです
ユーザー名は下記のように?と置き換えてokです
C:/Users/?/Downloads/folderName
"""
TOKEN = "" #自分のDISCORD TOKEN(str)
nitro = "None" #None,Classic,Normalのどれか

import os
import time
import discord
from pytube import YouTube
from pytube import Playlist
from discord.ext import commands

client = commands.Bot(command_prefix="",self_bot=True)
username = os.environ["USERNAME"]
path = f"C:/Users/{username}/Downloads"
maxFilesize = 8388605 if nitro == "None" else 52428795 if nitro == "Classic" else 104857600


@client.event
async def on_ready():
    print("準備完了")
    

@client.event
async def on_message(message):
    mc = message.content
    ch = client.get_channel(message.channel.id)
    if message.author.id != client.user.id:
        return
    if "list=" in mc:
        await message.delete()
        try:
            pl = Playlist(mc)
            print(f"「{pl.title}」内の動画を送信中")
        except Exception:
            print("プレイリストが非公開になっている可能性があります\nプレイリストの公開設定を公開もしくは限定公開にしてください")
            time.sleep(5)
            exit(0)
        for vid in pl.videos:
            try:
                vid.streams.filter(only_audio=True)[0].download(path)
                title = vid.title.translate(str.maketrans("","",r'\\/:*?"<>|.~#;\','))
                os.rename(f"{path}/{title}.mp4",f"{path}/{title}.mp3")
                filesize = os.path.getsize(f"{path}/{title}.mp3")
                if filesize < maxFilesize:
                    file = f"{path}/{title}.mp3"
                    await ch.send(f"`{title}`",file=discord.File(file))
                    os.remove(f"{path}/{title}.mp3")
                    print(f"[+] {title}のアップロード完了")
                    time.sleep(1)
                else:
                    os.remove(f"{path}/{title}.mp3")
                    print(f"[x] {title}のアップロード失敗(容量上限)")
            except Exception:
                try:
                    os.remove(path + "/" + vid.title.translate(str.maketrans("","",r'\\/:*?"<>|.#~;\',')) + ".mp4")
                except Exception as e:
                    error = "エラー発生:" + str(e)
                    print("-"*len(error) + "\n" + error + "\n" + "-"*len(error))
    elif "youtu" in mc and "list=" not in mc:
        await message.delete()
        vid = YouTube(mc)
        vid.streams.filter(only_audio=True)[0].download(path)
        title = vid.title.translate(str.maketrans("","",r'\\/:*?"<>|.~#;\','))
        os.rename(f"{path}/{title}.mp4",f"{path}/{title}.mp3")
        filesize = os.path.getsize(f"{path}/{title}.mp3")
        if filesize < maxFilesize:
            file = f"{path}/{title}.mp3"
            await ch.send(f"`{title}`",file=discord.File(file))
            os.remove(f"{path}/{title}.mp3")
            print(f"[+] {title}のアップロード完了")
        else:
            os.remove(f"{path}/{title}.mp3")
            print(f"[x] {title}のアップロード失敗(容量上限)")
    elif "\\" in mc:
        await message.delete()
        mc = mc.replace("\"","").replace("?",username)
        if os.path.isdir(mc) == False:
            return
        files = os.listdir(mc)
        for file in files:
            if os.path.getsize(f"{mc}\{file}") < maxFilesize:
                await ch.send(file=discord.File(f"{mc}\{file}"))
                print(f"[o] {file}の送信完了")
            else:
                print(f"[x] {file}のアップロード失敗(容量上限)")
    else:
        pass


client.run(TOKEN,bot=False)
