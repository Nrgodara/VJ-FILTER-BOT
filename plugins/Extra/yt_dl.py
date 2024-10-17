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
import yt_dlp
from yt_dlp import YoutubeDL


import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

@Client.on_message(filters.command(['song', 'mp3'])) 
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    query = ' '.join(message.command[1:])

    logging.info(f"Query: {query}")
    
    m = await message.reply(f"**Searching for your song...!**")

    if not os.path.exists("cookies.txt"):
        return await m.edit("Cookies file not found. Please ensure cookies.txt is in the correct location.")
    
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookies": "cookies.txt",  # Path to your cookies file
        "default_search": "ytsearch1",  # To search YouTube by name
        "noplaylist": True,  # Disable playlists
        "geo_bypass": True,
    }

    try:
        logging.info("Performing YouTube search")
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        logging.info(f"Found video: {title} | {link}")

    except Exception as e:
        logging.error(f"Error during search: {e}")
        return await m.edit(f"**Could not find the song. Please try again with a different query.**\n\nError: {str(e)}")

    await m.edit("🎶🌹🎶\n**Downloading your song...!**")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logging.info("Attempting to download the audio")
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        cap = f"<b>{title}</b>\n\nRequested By: [{user_name}](tg://user?id={user_id})"
        await message.reply_audio(
            audio_file,
            caption=cap,
            quote=False,
            title=title,
            duration=int(duration.split(':')[0]) * 60 + int(duration.split(':')[1]),
            performer="MAHI®",
            thumb=thumb_name
        )
        await m.delete()

    except Exception as e:
        logging.error(f"Error during download: {e}")
        if "cookies" in str(e).lower():
            return await m.edit("Cookies may have expired or are invalid. Please update your cookies file.")
        await m.edit(f"Error during download: {str(e)}")

    finally:
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            logging.error(f"Error during file cleanup: {e}")
            

        

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

        ydl_opts = {
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])],
            'cookiefile': 'cookies.txt'
        }


        

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)

            if title:
                ydl.download([url])
                uploading_msg = await message.reply_text("Uploading video...")
                video_filename = f"downloaded_video_{info_dict['id']}.mp4"
                sent_message = await client.send_video(message.chat.id, video=open(video_filename, 'rb'), caption=title)

                
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
