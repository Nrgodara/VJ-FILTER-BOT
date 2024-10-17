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
    query = ' '.join(message.command[1:])

    print(f"Query: {query}")
    m = await message.reply(f"**ѕєαrchíng чσur ѕσng...!\n {query}**")

    # Construct the cookies file path in the home directory
    cookies_path = os.path.expanduser("~/cookies.txt")
    
    # Check if the cookies file exists
    if not os.path.exists(cookies_path):
        return await m.edit("Cookies file not found in the home directory. Please place `cookies.txt` in your home folder.")

    # yt-dlp options for both searching and downloading
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookies": cookies_path,  # Use cookies from the home directory
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",  # Act as a browser
        "geo_bypass": True,
        "nocheckcertificate": True,  # Bypass SSL certificate issues
        "quiet": True,  # Suppress unnecessary output
        "default_search": "ytsearch1",  # Perform a YouTube search for the query and get the first result
    }

    await m.edit("🎶🌹🎶\n**dσwnlσαdíng чσur ѕσng...!**")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Use yt-dlp to search and download the best matching result
            info_dict = ydl.extract_info(query, download=False)
            link = info_dict.get("webpage_url")
            title = info_dict.get("title")[:40]
            thumbnail = info_dict.get("thumbnail")
            performer = f"MAHI®🇮🇳"
            duration = info_dict.get("duration")

            # Download the thumbnail
            thumb_name = f'thumb_{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            with open(thumb_name, 'wb') as thumb_file:
                thumb_file.write(thumb.content)

            # Download the audio file
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

    except Exception as e:
        print(f"Error during song processing: {e}")
        return await m.edit(f"An error occurred: {str(e)}")

    try:
        # Prepare caption and audio duration
        cap = f"<b>{title}</b>\n\n𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒆𝒅 𝑩𝒚 ➤ [{temp.B_NAME}](https://t.me/{temp.U_NAME})\n𝑹𝒆𝒒𝒖𝒆𝒔𝒕𝒆𝒅 𝑩𝒚 ➤ {rpk} 🥀"
        await message.reply_audio(
            audio_file,
            caption=cap,
            quote=False,
            title=title,
            duration=duration,
            performer=performer,
            thumb=thumb_name
        )

        # Log the downloaded audio in the channel
        await client.send_audio(
            chat_id=LOG_CHANNEL,
            audio=audio_file,
            caption=f"Downloaded song by [{user_name}](tg://user?id={user_id})\n\n{cap}",
            title=title,
            duration=duration,
            performer=performer,
            thumb=thumb_name
        )
        await m.delete()

    except Exception as e:
        await m.edit(f"An error occurred while sending the song: {str(e)}")
        print(f"Error while sending audio: {e}")

    # Cleanup
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(f"Cleanup error: {e}")
        

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
