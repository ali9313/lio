
import asyncio
from telethon import events
from aliup import l313l


hussein_enabled = False
ali_enabled = False
JOKER_ID = {}

@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mark_as_read(event):
    global ali_enabled, JOKER_ID
    sender_id = event.sender_id
    if ali_enabled and sender_id in JOKER_ID:
        ali_time = JOKER_ID[sender_id]
        if ali_time > 0:
            await asyncio.sleep(ali_time)
        await event.mark_read()

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر تعطيل$'))
async def Hussein(event):
    global ali_enabled
    ali_enabled = False
    await event.edit('** تم تعطيل امر التكبر بنجاح ✅**')

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر (\d+) (\d+)$'))
async def Hussein(event):
    global ali_enabled, JOKER_ID
    ali_time = int(event.pattern_match.group(1))
    user_id = int(event.pattern_match.group(2)) 
    JOKER_ID[user_id] = ali_time
    ali_enabled = True
    await event.edit(f'** تم تفعيل امر التكبر بنجاح مع  {ali_time} ثانية للمستخدم {user_id}**')

@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def Hussein(event):
    global hussein_enabled
    if hussein_enabled:
        if hussein_time > 0:
            await asyncio.sleep(hussein_time)
        await event.mark_read()

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.مود التكبر تعطيل$'))
async def Hussein(event):
    global hussein_enabled
    hussein_enabled = False
    await event.edit('** تم تعطيل امر التكبر على الجميع بنجاح ✅**')

@l313l.on(admin_cmd(pattern=f"مود التكبر (\d+)"))
async def Hussein(event):
    global hussein_enabled
    hussein_time = int(event.pattern_match.group(1))
    hussein_enabled = True
    await event.edit(f'** تم تفعيل امر التكبر بنجاح مع  {hussein_time} ثانية**')
