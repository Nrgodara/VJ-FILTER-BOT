# Don't Remove Credit @Mahi_Botz
# Subscribe movie Channel For Amazing Bot
# Ask Doubt on telegram @fake_one


from __future__ import unicode_literals

import os, requests, asyncio, math, time, wget
from pyrogram import filters, Client
from pyrogram.types import Message
from info import *
from utils import temp

from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL


@Client.on_message(filters.command(['song', 'mp3'])) 
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = await message.reply(f"**ѕєαrchíng чσur ѕσng...!\n {query}**")
    #ydl_opts = {"format": "bestaudio[ext=m4a]"}
    if not os.path.exists("cookies.txt"):
        return await m.edit("Cookies file not found. Please make sure cookies.txt is in the correct location.")
    
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookies": "cookies.txt"  # Path to your cookies file
    }
        
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        performer = f"MAHI®🇮🇳" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    except Exception as e:
        print(str(e))
        return await m.edit("**Give Command with **song name**\n\nExample:** `/song Jannat Ve`")
                
    await m.edit("🎶🌹🎶\n**dσwnlσαdíng чσur ѕσng...!**")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        if "cookies" in str(e).lower():
            return await m.edit("Cookies may have expired or are invalid. Please update your cookies file.")
        
            
  

        cap = f"<b>{title}</b>\n\n𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒆𝒅 𝑩𝒚 ➤ [{temp.B_NAME}](https://t.me/{temp.U_NAME})\n𝑹𝒆𝒒𝒖𝒆𝒔𝒕𝒆𝒅 𝑩𝒚 ➤ {rpk} 🥀"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await message.reply_audio(
            audio_file,
            caption=cap,            
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )

        #Send audio to the log channel
        await client.send_audio(
            chat_id=LOG_CHANNEL,
            audio=audio_file,
            caption=f"Downloaded song by [{user_name}](tg://user?id={user_id})\n\n{cap}",
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**\n**➥`{str(e)}`")
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    query = get_text(message)
    if not query:
        return await message.reply("**Please provide a video name or a YouTube link.**")

    pablo = await client.send_message(message.chat.id, "⌛")

    try:
        # Check if the query is a YouTube link
        if "youtube.com" in query or "youtu.be" in query:
            url = query
        else:
            # Search for the video based on the query
            search = SearchVideos(query, offset=1, mode="dict", max_results=1)
            result = search.result()["search_result"][0]
            url = result["link"]
            thum = result["title"]
            fridayz = result["id"]
            kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
            sedlyf = wget.download(kekme)

        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "cookies": "cookies.txt",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": False,  # Set quiet to False to print error messages
        }

        

        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)

        file_stark = f"{ytdl_data['id']}.mp4"
        capy = f"""**TITLE :**{ytdl_data['title']}\n**𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒆𝒅 𝑩𝒚 ➤ [{temp.B_NAME}](https://t.me/{temp.U_NAME})\n𝑹𝒆𝒒𝒖𝒆𝒔𝒕𝒆𝒅 𝑩𝒚 ➤** {message.from_user.mention}"""

        # Send video to the user
        await client.send_video(
            message.chat.id,
            video=open(file_stark, "rb"),
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            thumb=sedlyf if 'sedlyf' in locals() else None,
            caption=capy,
            supports_streaming=True,
        )
        await pablo.delete()

        # Send video to the log channel
        if 'sedlyf' in locals():
            await client.send_video(
                chat_id=LOG_CHANNEL,
                video=open(file_stark, "rb"),
                duration=int(ytdl_data["duration"]),
                file_name=str(ytdl_data["title"]),
                thumb=sedlyf,
                caption=f"<b>#Downloaded_video</b> by [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n{capy}",
                supports_streaming=True
            )

            # Remove downloaded files
            for files in (sedlyf, file_stark):
                if files and os.path.exists(files):
                    os.remove(files)

    except Exception as e:
        await pablo.edit(f"**Download Failed. Please Try Again.**\n**Error:** `{str(e)}`")
        print(f"Error in vsong command: {e}")

        # Print traceback if needed
        import traceback
        traceback.print_exc()
