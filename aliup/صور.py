from telethon import TelegramClient, events
import requests
import uuid
from aliup import *

async def generate_image(prompt):
    G1 = str(uuid.uuid4())
    G2 = str(uuid.uuid4())

    headers = {
        'Host': 'api.aiacdemy.com:18000',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'keep-alive'
    }

    params = {
        'app_version_code': '363',
        'app_version_name': '3.8.0',
        'device_id': G1,
        'ad_id': G2,
        'platform': 'android'
    }

    data = {
        'diamond_remain': 12,
        'height': 1024,
        'model_id': 'general',
        'prompt': prompt,
        'prompt_translated': prompt,
        'width': 1024,
        'work_type': 'text2img'
    }

    try:
        response = requests.post('https://api.aiacdemy.com:18000/comfyapi/v4/prompt', params=params, headers=headers, json=data).json()
        
        if 'images' in response and response['images']:
            img_url = response['images'][0]
            return img_url
        else:
            return None
    except Exception as e:
        return None

@l313l.ar_cmd(pattern="صور(?:\s|$)([\s\S]*)")
async def handler(event):
    # استخرج الوصف من الرسالة بعد أمر .صوره
    prompt = event.pattern_match.group(1)
    image_url = await generate_image(prompt)

    if image_url:
        # تنزيل الصورة
        image_response = requests.get(image_url)
        
        # تحقق من أن الطلب كان ناجحًا
        if image_response.status_code == 200:
            # احفظ الصورة في ذاكرة مؤقتة
            image_bytes = image_response.content
            
            # إرسال الصورة إلى المستخدم
            await event.reply(file=image_bytes)
        else:
            await event.reply("حدث خطأ أثناء تنزيل الصورة.")
    else:
        await event.reply("لم يتم إنشاء الصورة.")