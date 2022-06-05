"""
使い方
1.pythonをインストール
2.cmd開いてpy -m pip install pipでpipをインストール
3.requirementsに書いてあるライブラリをpipでインストール
4.下のTOKENとchannelにdiscordのTOKENとチャンネルIDを入れる
5.このpyファイル実行
6.プレイリストのURLをdiscordで送信(公開か限定公開でないとエラー発生します)
(もちろんだけど8mb以上のものnitroないとはアップロードできないです)
"""
TOKEN = "" #自分のDISCORD TOKEN(str)
channel = 123456789876543210 #送信したいチャンネルID(int)
nitro = "None" #None,Classic,Normalのどれか

import os
import time
import json
import discord
from pytube import YouTube
from pytube import Channel
from pytube import Playlist
from discord.ext import commands

client = commands.Bot(command_prefix="",self_bot=True)
username = os.environ["USERNAME"]
path = f"C:/Users/{username}/Downloads"


@client.event
async def on_ready():
    print("BOT起動完了")
    

@client.event
async def on_message(message):
    if message.attachments or message.content.startswith("https://") == False or message.author.id != client.user.id:
        return
    url = message.content
    try:
        await message.delete()
    except Exception:
        pass
    if "list=" in url:
        maxFilesize = 8388605 if nitro == "None" else 52428795 if nitro == "Classic" else 104857600
        pl = Playlist(url)
        print(f"「{pl.title}」内の動画を送信中")
        ch = client.get_channel(channel)
        for vid in pl.videos:
            try:
                vid.streams.filter(only_audio=True)[0].download(path)
                title = vid.title.translate(str.maketrans("","",r'\\/:*?"<>|.~#;'))
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
                    os.remove(path + "/" + vid.title.translate(str.maketrans("","",r'\\/:*?"<>|.#~;')) + ".mp4")
                except Exception as e:
                    print("エラー発生:" + str(e))
        print("作業が完了しました。ウィンドウを閉じます")
        time.sleep(5)
        quit()
    else:
        pass


client.run(TOKEN,bot=False)
