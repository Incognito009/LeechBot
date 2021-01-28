# GOAL:
# getting track for logging

import os
import time
import json
import asyncio
import logging

LOGGER = logging.getLogger(__name__)

# GOAL:
# universal function for uploading file to telegram

from sample_config import Config
from translation import Translation
from os import path as os_path, listdir as os_lisdir, remove as os_remove, rmdir as os_rmdir
from time import time
from math import floor
from pyrogram import Client, Message
from bot import LOCAL, CONFIG, STATUS
from bot.plugins import formater, split, thumbnail_video, ffprobe
from data.database import *

async def func(filepath: str, client: Client,  message: Message, delete=False):
    if not os_path.exists(filepath):
        LOGGER.error(f'File not found : {filepath}')
        await message.edit_text(
            LOCAL.UPLOAD_FAILED_FILE_MISSING.format(
                name = os_path.basename(filepath)
            )
        )
        return

    if os_path.isdir(filepath):
        ls = os_lisdir(filepath)
        async for filepath in ls:
            await message.edit(
                LOCAL.UPLOADING_FILE.format(
                    name = os_path.basename(filepath)
                )
            )
            await func(filepath, message, delete)
        if delete:
            os_rmdir(filepath)
        return

    video = ['.mp4','.mkv','.avi','.webm','.wmv','.mov']
    photo = ['.jpg','.jpeg','.png']

    file_ext = os_path.splitext(filepath)[1].lower()
    LOGGER.debug(f'Uploading : {filepath}')

    if STATUS.UPLOAD_AS_DOC:
        upload_fn = client.send_document
    elif file_ext in photo:
        upload_fn = client.send_photo
    elif file_ext in video:
        async def upload_fn(chat_id, file, **kwargs):
            probe = await ffprobe.func(file.path)

            duration = int(float(probe["format"]["duration"]))

            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            width = int(video_stream['width'] if 'width' in video_stream else 0)
            height = int(video_stream['height'] if 'height' in video_stream else 0)


            await message.edit(
                LOCAL.GENERATE_THUMBNAIL.format(
                    name = file.name
                )
            )
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"

        if not os.path.exists(thumb_image_path):
            mes = await thumb(update.from_user.id)
            if mes != None:
                m = await bot.get_messages(update.chat.id, mes.msg_id)
                await m.download(file_name=thumb_image_path)
                thumb_image_path = thumb_image_path
            else:
                if "thumbnail" in response_json:
                    if response_json["thumbnail"] is not None:
                        thumbnail = response_json["thumbnail"]
                        thumbnail_image = response_json["thumbnail"]
                thumb_image_path = DownLoadFile(
                    thumbnail_image,
                    Config.DOWNLOAD_LOCATION + "/" +
                    str(update.from_user.id) + ".jpg",
                    Config.CHUNK_SIZE,
                    None,  # bot,
                    Translation.DOWNLOAD_START,
                    update.message_id,
                    update.chat.id
                )
            await client.send_video(
                chat_id,
                file, 
                supports_streaming=True,
                thumb=thumb_image_path,
                height=height,
                width=width,
                duration=duration,
                **kwargs
            )
            if not use_default_thumbnail:
                os_remove(str(thumbnail))
    else:
        upload_fn = client.send_document
    
    if os_path.getsize(filepath) > int(CONFIG.UPLOAD_MAX_SIZE):
        LOGGER.debug(f'File too large : {filepath}')
        await message.edit_text(
            LOCAL.SPLIT_FILE.format(
                name = os_path.basename(filepath)
            )
        )

    async for file in split.func(filepath, int(CONFIG.UPLOAD_MAX_SIZE)):
        await message.edit(
            LOCAL.UPLOADING_FILE.format(
                name = file.name
            )
        )
    
        info = {
            "time" : time(),
            "name" : file.name,
            "last_update" : 0,
            "prev_text" : ""
        }
        await upload_fn(
            message.chat.id,
            file,
            disable_notification=True,
            progress=progress_upload_tg,
            progress_args=(
                message,
                info
            ),
            caption=f'<code>{file.name}</code>'
        )            
        LOGGER.debug(f'Uploaded : {file.name}')
    if delete:
        os_remove(filepath)

async def progress_upload_tg(current, total, message, info):
    percentage = round(current * 10000 / total) / 100
    block = ""
    for i in range(1, int(CONFIG.BAR_SIZE) + 1):
        if i <= floor(percentage * int(CONFIG.BAR_SIZE)/100):
            block += LOCAL.BLOCK_FILLED
        else:
            block += LOCAL.BLOCK_EMPTY
    time_passed = time() - info["time"]
    up_speed = current / time_passed
    text = LOCAL.UPLOADING_PROGRESS.format(
            name = info["name"],
            block = block,
            percentage = percentage,
            size = formater.format_bytes(total),
            upload_speed = formater.format_bytes(up_speed),
            eta = formater.format_time((total - current)/up_speed)
        )
    if text != info["prev_text"] and (time() - info["last_update"]) >= int(CONFIG.EDIT_SLEEP):
        await message.edit(text)
        info.update({
            "prev_text" : text,
            "last_update" : time()
        })
