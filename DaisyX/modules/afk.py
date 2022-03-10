import time

from telethon import events, types

from DaisyX.services.events import register
from DaisyX.services.sql import afk_sql as sql

# Importing from the serices
from DaisyX.services.telethon import tbot


@register(pattern=r"(.*?)")
async def _(event):
    if event.is_private:
        return
    sender = await event.get_sender()
    prefix = event.text.split()
    if prefix[0] == "/afk":
        cmd = event.text[len("/afk ") :]
        reason = cmd if cmd is not None else ""
        firsname = sender.first_name
        # print(reason)
        start_time = time.time()
        sql.set_afk(sender.id, reason, start_time)
        await event.reply("**{} is now AFK !**".format(firsname), parse_mode="markdown")
        return

    if sql.is_afk(sender.id):
        res = sql.rm_afk(sender.id)
        if res:
            firstname = sender.first_name
            text = "**{} is no longer AFK !**".format(firstname)
            await event.reply(text, parse_mode="markdown")


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    if event.is_private:
        return
    sender = event.sender_id
    str(event.text)
    global let
    global userid
    userid = None
    let = None
    if event.reply_to_msg_id:
        await event.get_reply_message()
        userid = event.sender_id
    else:
        try:
            for (ent, txt) in event.get_entities_text():
                if ent.offset != 0:
                    break
                if not isinstance(
                    ent, types.MessageEntityMention
                ) and not isinstance(ent, types.MessageEntityMentionName):
                    return
                c = txt
                a = c.split()[0]
                let = await tbot.get_input_entity(a)
                userid = let.user_id
        except Exception:
            return

    if not userid:
        return
    if sender == userid:
        return

    if not event.is_group:
        return
    if sql.is_afk(userid):
        user = sql.check_afk_status(userid)
        etime = user.start_time
        if not user.reason:
            elapsed_time = time.time() - float(etime)
            final = time.strftime("%Hh: %Mm: %Ss", time.gmtime(elapsed_time))
            fst_name = "User"
            res = "**{} is AFK !**\n\n**Last seen**: {}".format(fst_name, final)

        else:
            elapsed_time = time.time() - float(etime)
            final = time.strftime("%Hh: %Mm: %Ss", time.gmtime(elapsed_time))
            fst_name = "This user"
            res = "**{} is AFK !**\n\n**He said to me that**: {}\n\n**Last seen**: {}".format(
                fst_name, user.reason, final
            )
        await event.reply(res, parse_mode="markdown")
    userid = ""  # after execution
    let = ""  # after execution


__mod_name__ = "AFK"
__help__ = """
 - /afk [reason]: mark yourself as AFK(Away From Keyboard)
"""
