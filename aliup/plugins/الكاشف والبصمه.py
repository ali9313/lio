import random
import asyncio
import re
import requests
import time
import psutil
from datetime import datetime
from platform import python_version

import sys
import typing
from heroku3 import from_key
from cachetools import cached, LRUCache

from telethon import version, events, types
from telethon.tl import types, functions
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.utils import get_display_name
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from . import StartTime, l313l
from ..Config import Config
from ..helpers.utils import reply_id
from ..core.logger import logging
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from . import BOTLOG, BOTLOG_CHATID, mention
vocself = False

@l313l.ar_cmd(pattern="تفعيل الكاشف الذكي(?: |$)(.*)")
async def start_zelzali(event):
    input_str = event.pattern_match.group(1)
    #if not input_str:
        #return await edit_or_reply(event, "**- ارسل الامر + اليوزر او الايدي**")
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    uid = None
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    private_chat_ids = await get_private_chat_ids(uid)
    if uid not in private_chat_ids:
        return await edit_or_reply(event, "**⎉╎عـذرا عـزيـزي ..✖️**\n**⎉╎لايوجـد لديك خاص مسبقاَ**\n**⎉╎مع صاحب هذا الحساب**\n**⎉╎لـ مراقبـة حالة متصل لـ هـذا الشخص ☑️**")
    ZAZ = gvarstatus("ZAZ") and gvarstatus("ZAZ") != "false"
    if ZAZ and gvarstatus("UIU") == f"{uid}":
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await l313l(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. مفعـله مسبقـاً لمراقبـة حالة هذا الشخص ☑️**")
    else:
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await l313l(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        addgvar("ZAZ", True)
        addgvar("UIU", f"{uid}")
        zzz = await event.client.get_entity(uid)
        Zname = f"{zzz.first_name} {zzz.last_name}" if zzz.last_name else zzz.first_name
        Zid = uid
        Zuser = f"@{zzz.username}" if zzz.username else "None"
        target = f"[{Zname}](tg://user?id={Zid})"
        await edit_or_reply(event, f"**⎉╎تم تفعيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**\n**⎉╎لـ مراقبـة الحسـاب** {target}")

@l313l.ar_cmd(pattern="(تعطيل الكاشف الذكي|تعطيل اشعارات الحالة)")
async def stop_zelzali(event):
    ZAZ = gvarstatus("ZAZ") and gvarstatus("ZAZ") != "false"
    if ZAZ:
        addgvar("ZAZ", False)
        delgvar("UIU")
        await edit_or_reply(event, "**⎉╎تم تعطيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**")
    else:
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. معطلـه مسبقـاً ☑️**")



@l313l.on(events.UserUpdate)
async def zelzal_online_ai(event):
    if gvarstatus("ZAZ") == "false":
        return
    if gvarstatus("ZAZ") is None:
        return
    if gvarstatus("UIU") is None:
        return
    TARGET_USER_ID = int(gvarstatus("UIU"))
    if event.user_id == TARGET_USER_ID and event.online:  # تحقق من أن المستخدم هو المستهدف وأنه متصل
        user = await event.get_user()
        first_name = user.first_name
        last_name = user.last_name
        full_name = f"{user.first_name}{user.last_name}"
        full_name = full_name if last_name else first_name
        if BOTLOG:
            zaz = f"<b>⌔┊الحسـاب : </b>" 
            zaz += f'<a href="tg://user?id={user.id}">{full_name}</a>'
            zaz += f"\n<b>⌔┊اصبـح متصـل الان ⦿</b>"
            await l313l.send_message(Config.PM_LOGGER_GROUP_ID, zaz, parse_mode="html")


@l313l.ar_cmd(pattern="المتصليين?(.*)")
async def _(e):
    if e.is_private:
        return await edit_or_reply(e, "**- عـذراً ... هـذه ليـست مجمـوعـة ؟!**")
    chat = await e.get_chat()
    if not chat.admin_rights and not chat.creator:
        await edit_or_reply(e, "**- عـذراً ... يجب ان تكـون مشرفـاً هنـا ؟!**")
        return False
    zel = await edit_or_reply(e, "**- جـارِ الكشـف اونـلايـن ...**")
    zzz = e.pattern_match.group(1)
    o = 0
    zilzali = "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - 🝢 - الڪـٓاشـف الذڪـٓي](t.me/ZThon) 𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**- تـم انتهـاء الكشـف .. بنجـاح ✅**\n**- قائمـة بعـدد الاعضـاء المتصليـن واسمائـهـم :**\n"
    xx = f"{zzz}" if zzz else zilzali
    zed = await e.client.get_participants(e.chat_id, limit=99)
    for users, bb in enumerate(zed):
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            xx += f"\n- [{get_display_name(bb)}](tg://user?id={bb.id})"
    await e.client.send_message(e.chat_id, xx)
    await zel.delete()
    
    
@l313l.ar_cmd(pattern="(تفعيل البصمه الذاتيه|تفعيل البصمه الذاتية|تفعيل البصمة الذاتيه|تفعيل البصمة الذاتية)")
async def start_datea(event):
    global vocself
    if vocself:
        return await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎مفعلـه .. مسبقـاً ✅**")
    vocself = True
    await edit_or_reply(event, "**⎉╎تم تفعيل حفظ البصمه الذاتية 🎙**\n**⎉╎تلقائياً .. بنجاح ✅**")

@l313l.ar_cmd(pattern="(تعطيل البصمه الذاتيه|تعطيل البصمه الذاتية|تعطيل البصمة الذاتيه|تعطيل البصمة الذاتية)")
async def stop_datea(event):
    global vocself
    if vocself:
        vocself = False
        return await edit_or_reply(event, "**⎉╎تم تعطيل حفظ البصمه الذاتية 🎙**\n**⎉╎الان صارت مو شغالة .. ✅**")
    await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎معطلـه .. مسبقـاً ✅**")

@l313l.on(events.NewMessage(func=lambda e: e.is_private and (e.audio or e.voice) and e.media_unread))
async def sddm(event):
    global vocself
    if vocself:
        # التحقق من وجود صلاحية انتهاء (رسالة ذاتية التدمير)
        if getattr(event.message, 'ttl_period', None):
            sender = await event.get_sender()
            username = f"@{sender.username}" if sender.username else "لا يوجد"
            voc = await event.download_media()
            await l313l.send_file(
                "me", voc,
                caption=f"حفـظ البصمه الذاتيه \n**⌔ مࢪحبـاً .. عـزيـزي 🫂\n⌔ تـم حفظ البصمه الذاتية .. تلقائياً ☑️** ❝\n**⌔ معلومـات المـرسـل :-**\n"
                        f"**• الاسم :** {_format.mentionuser(sender.first_name, sender.id)}\n"
                        f"**• اليوزر :** {username}\n"
                        f"**• الايدي :** `{sender.id}`"
            )