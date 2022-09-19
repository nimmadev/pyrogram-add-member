import asyncio
import json
from pyrogram import Client, errors


# load config
config = (json.load(open("config.json")))
# group target link
group_source_id = str(config['group_target_username'])
group_source_id = str(config['group_source_username'])
#workdir = 'session/'


def main():
    for account in config["accounts"]:
        phone = account["phone"]
        api_id = account["api_id"]
        api_hash = account["api_hash"]
        print(phone)
        with Client(phone, api_id, api_hash, workdir="session") as app:
            if app.get_me():
                print(phone, "is logined")
                try:
                    app.join_chat(group_target_id)
                    app.join_chat(group_source_id)
                except BaseException:
                    print("couldn't add u to the groups or maybe this number already in group")
            else:
               print(phone, "login failed")
main()
