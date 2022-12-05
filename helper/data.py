import asyncio
import json
import gc
from pyrogram.client import Client, enums
from helper.pam_log import pamlog

async def get_data(gp_s_id, gp_t_id, config, stop):
    # create logger
    PAM = pamlog('PAM-GET-DATA')
    PAM.propagate = False
    try:
        count = {}
        with open('current_count.py', 'w') as g:
            g.write(str(count))
            g.close()
    except BaseException:
        pass
    phonedata = config["accounts"][0]
    phone = phonedata["phone"]
    async with Client(phone, workdir="session") as app:
        if await app.get_me():
            pass
        else:
            PAM.info(f"{phone} login failed")
        try:
            await app.get_chat(gp_s_id)
        except ValueError:
            PAM.info(f"{phone} has not joined source chat or RUN get_data.py")
            await asyncio.sleep(1)
        try:
            await app.get_chat(gp_t_id)
        except ValueError:
            PAM.info(f"{phone} has not joined target chat or RUN get_data.py")
            await asyncio.sleep(1)
        mem2 = []
        async for member in app.get_chat_members(chat_id=gp_t_id):
            await asyncio.sleep(.0025)

            try:
                # scrap member
                memb = {
                    "userid": str(member.user.id),
                    "status": str(member.user.status),
                    "name": str(member.user.first_name),
                    "bot": member.user.is_bot,
                    "username": str(member.user.username)
                }

                gc.disable()
                mem2.append(memb)
                gc.enable()
            except BaseException:
                PAM.info('error')

        PAM.info(f'{phone} getting target user data')
        mem3 = []
        async for member in app.get_chat_members(chat_id=gp_s_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            try:
                # scrap member
                memb = {
                    "userid": str(member.user.id),
                    "name": str(member.user.first_name),
                    "bot": member.user.is_bot,
                    "username": str(member.user.username)
                }
                gc.disable()
                mem3.append(memb)
                gc.enable()
            except BaseException:
                PAM.info('error')
        app.stop()
        PAM.info(f'{phone} getting admin user data')
        with open('data/source_user.json', 'w', encoding='utf-8') as f:
            json.dump(mem, f, indent=4, ensure_ascii=False)
            PAM.info("saving source user")
        with open('data/target_user.json', 'w', encoding='utf-8') as f:
            json.dump(mem2, f, indent=4, ensure_ascii=False)
            PAM.info("saving target user")
        with open('data/source_admin.json', 'w', encoding='utf-8') as f:
            json.dump(mem3, f, indent=4, ensure_ascii=False)
            PAM.info("saving admin user")
        
        if "u" == stop[0]:
            exit()
    total_account = len(config['accounts'])
    account = config['accounts']
    for numb in range(1, total_account+1):
        phone = account[numb]["phone"]
        PAM.info(f'{phone} getting source user data')
        async with Client(phone, workdir="session") as app:
            if await app.get_me():
                PAM.info(f"{phone} is logined")
            else:
                PAM.info(f"{phone} login failed")
            try:
                await app.get_chat(gp_s_id)
            except ValueError:
                PAM.info(f"{phone} has not joined source chat or RUN get_data.py")
                await asyncio.sleep(1)
                continue
            try:
                await app.get_chat(gp_t_id)
            except ValueError:
                PAM.info(f"{phone}' has not joined target chat or RUN get_data.py")
                await asyncio.sleep(1)
                continue
            mem = []
            async for member in app.get_chat_members(chat_id=gp_s_id):
                await asyncio.sleep(.0025)
                gc.disable()
                try:
                    # scrap member
                    memb = {
                        "userid": str(member.user.id),
                        "status": str(member.user.status),
                        "name": str(member.user.first_name),
                        "bot": member.user.is_bot,
                        "username": str(member.user.username)
                    }
                    gc.disable()
                    mem.append(memb)
                    gc.enable()
                except BaseException:
                    PAM.info('error')

            # refresh hash acces for all accounts
