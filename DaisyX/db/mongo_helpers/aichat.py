from DaisyX.services.mongo import mongodb as db_x

lydia = db_x["CAHTBOT"]
talkmode = db_x["TALKMODE"]


def add_chat(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    if stark:
        return False
    lydia.insert_one({"chat_id": chat_id})
    return True


def remove_chat(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    lydia.delete_one({"chat_id": chat_id})
    return True


def get_all_chats():
    return r if (r := list(lydia.find())) else False


def get_session(chat_id):
    stark = lydia.find_one({"chat_id": chat_id})
    return stark or False


def add_chat_t(chat_id):
    star = talkmode.find_one({"chat_id": chat_id})
    if star:
        return False
    talkmode.insert_one({"chat_id": chat_id})
    return True


def remove_chat_t(chat_id):
    star = talkmode.find_one({"chat_id": chat_id})
    if not star:
        return False
    talkmode.delete_one({"chat_id": chat_id})
    return True


def get_session_t(chat_id):
    star = talkmode.find_one({"chat_id": chat_id})
    return star or False
