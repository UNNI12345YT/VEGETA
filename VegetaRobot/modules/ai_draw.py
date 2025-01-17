



from VegetaRobot import pgram, aiohttpsession as session, BOT_USERNAME
from pyrogram import filters, types, enums, errors



async def get_output(prompt: str):

    
    url = 'https://modelslab.com/api/v6/images/text2img'
    headers = {'Content-Type': 'application/json'}
  
    data = {
       "key": "bNNEFRpouWM914ZriDSChuHH5vf2jBIyB4BYccbPLkuq01IdUd2djg2qZHIS",
       "model_id": "anything-v3",
       "prompt": prompt,
       "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
       "width": "512",
       "height": "512",
       "samples": "4",
       "num_inference_steps": "30",
       "seed": None,
       "guidance_scale": 7.5,
       "webhook": None,
       "track_id": None
       }
  
    async with session.post(
      url, 
      headers=headers, 
      json=data
    ) as response:
        images = []
  
        if response.status == 200:
            images = (await response.json()).get('output')
        return images


@pgram.on_message(filters.command(['draw', 'imagine']))
async def DrawAI(bot, message):
     m = message
     if len(m.text.split()) == 1:
        return await m.reply_text(
           text='**🙋 Write some text to draw....**'
        )
     prompt = m.text.split(maxsplit=1)[1]

     msg = await m.reply_text('**✨ Drawing please wait some seconds..**')
  
     images = await get_output(prompt)
     if images:
         media = []
         for image_url in images:
             media.append(
                 types.InputMediaPhoto(image_url)
             )
         try:
           is_send = await bot.send_media_group(
             chat_id=m.chat.id,
             media=media, 
             reply_to_message_id=m.id
             )
           if is_send:
                return await msg.delete()
         except Exception as e:
             return await msg.edit(f'❌ Error: {str(e)}')
     else:
         return await msg.edit('**❌ No media fetched**')
       
__mod_name__ = "Draw"

__help__ = f"""
✨ **AI DRAW**:

Text to Image System by @{BOT_USERNAME}
Use `/draw anime cute girl`
"""

