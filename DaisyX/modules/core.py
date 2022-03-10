import os

from DaisyX.services.events import register
from DaisyX.services.telethon import tbot

# from LEGEND import LEGENDX, telethn as client

TEMP_DOWNLOAD_DIRECTORY = "./"
path = "./"
opn = []


@register(pattern="/open")
async def _(event):
    xx = await event.reply("Processing...")
    if not event.reply_to_msg_id:
        return await event.reply("Reply to a readable file")
    a = await event.get_reply_message()
    if not a.media:
        return await event.reply("Reply to a readable file")
    b = await a.download_media()
    with open(b, "r") as c:
        d = c.read()
    n = 4096
    for bkl in range(0, len(d), n):
        opn.append(d[bkl : bkl + n])
    for bc in opn:
        await event.client.send_message(
            event.chat_id,
            f"{bc}",
            reply_to=event.reply_to_msg_id,
        )
    await event.delete()
    opn.clear()
    os.remove(b)
    await xx.delete()


client = tbot


@register(pattern="^/dox ?(.*)")
async def get(event):
    name = event.text[5:]
    if name is None:
        await event.reply("reply to text message as `.ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await event.reply("reply to text message as `.ttf <file name>`")


__help__ = """
 *You can make a file 
  name. *
 ✪ /dox tag a message <i>file name</i> example /dox example.py
 ✪ /open tag a file 
"""

__mod_name__ = "Core "
