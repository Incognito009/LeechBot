import os
import time
import json
import asyncio

from pyrogram import Client, Message, Filters
from bot import COMMAND, LOCAL, CONFIG
from bot.database import *


@Client.on_message(Filters.private & Filters.photo)
async def save_photo(bot, update):
    if update.from_user.id in CONFIG.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    if update.media_group_id is not None:
        download_location = CONFIG.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"
        if not os.path.isdir(download_location):
            os.makedirs(download_location)
        await df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        download_location = CONFIG.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
        await df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text=LOCAL.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message_id
        )


@Client.on_message(Filters.private & Filters.command(["deletethumbnail"]))
async def delete_thumbnail(bot, update):
    if update.from_user.id in CONFIG.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    thumb_image_path = CONFIG.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    
    try:
        await del_thumb(update.from_user.id)
    except:
        pass

    try:
        os.remove(thumb_image_path)
    except:
        pass

    await bot.send_message(
        chat_id=update.chat.id,
        text=LOCAL.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
