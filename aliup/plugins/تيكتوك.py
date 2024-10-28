
import asyncio 
import shutil
import requests
from requests.exceptions import JSONDecodeError
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from aliup import l313l 
@l313l.ar_cmd(pattern="تيك(?: |$)(.*)")
async def zelzal_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.تيك) + رابـط او بالـرد ع رابـط**", 10)
    if "tiktok.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من تيـك تـوك .. للتحميــل ؟!**", 10)
    cap_zzz = f"تم تحميـل مـن تيـك تـوك .. بنجـاح ☑️"
    chat = "@downloader_tiktok_bot"
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من تيـك تـوك .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await zedub(unblock("downloader_tiktok_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
