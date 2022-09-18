import os
import asyncio
import time
import json
from pyrogram import Client, enums
from pyrogram.errors import RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate
from itertools import dropwhile

async def main():
        #loads member
        user_id = (json.load(open("data/user.json")))
        
        #loads users and channel info
        config = (json.load(open("config.json")))
        chat_idq = int(str(-100) +str(config['group_target']))
        
        #list to chcek active member
        activelist = ['UserStatus.LONG_AGO', 'UserStatus.LAST_MONTH', 'UserStatus.LAST_WEEK', 'UserStatus.OFFLINE', 'UserStatus.RECENTLY', 'UserStatus.ONLINE' ]
        #count retrive old state
        try:
            with open('current_count.txt') as f:
                count = int(f.read())               
        except:
                count = int(len(user_id) -1)
        #update function           
        def updatecount():
            with open('current_count.txt', 'w') as g:
                g.write(str(count))
                g.close()
        last_active = config["from_date_active"]
        added = 0
        active = []
        
        for x in dropwhile(lambda y: y != last_active, activelist):
           active.append(x)
        while count >= 1:
            for account in config["accounts"]:
                phone = account["phone"]
                user_active = user_id[count]["status"]
               # if last_active = "UserStatus.LAST_MONTH" 
                async with Client(phone, workdir="session") as app:
                    try:
                        if user_active in active:
                                print("trying to add", user_id[count]["userid"])
                                await app.add_chat_members(chat_id=chat_idq, user_ids=user_id[count]["userid"])
                                print(user_id[count]["userid"], "added success")
                                count -= 1
                                added += 1
                                print('sleep: ' + str(120 / len(config["accounts"])))
                                time.sleep(120 / len(config["accounts"]))
                                updatecount()
                            
                        
                    except (ChatAdminRequired, ChannelPrivate):
                        print("Chat admin permission required or Channel is private")
                        config["accounts"].remove(account)
                    except UserRestricted:
                        print("removing this restricted account")
                        config["accounts"].remove(account)
                    except UserIdInvalid:
                        print("user invalid or u never met user")
                        print('sleep: ' + str(120 / len(config["accounts"])))
                        time.sleep(120 / len(config["accounts"]))
                        count -= 1
                    except PeerIdInvalid as e:
                        print("you need to intrect with this user first")
                        config["accounts"].remove(account)
                    except UserPrivacyRestricted:
                        print("user have privacy enabled")
                        print('sleep: ' + str(120 / len(config["accounts"])))
                        time.sleep(120 / len(config["accounts"]))
                        count -= 1
                    except BaseException as e:
                        print(phone, "Rpc error")
                        print(e)
                        print,(user_id)
                        print('sleep: ' + str(120 / len(config["accounts"])))
                        time.sleep(120 / len(config["accounts"]))
                        updatecount()
                        count -= 1
            if config["accounts"] is False:
                print(added, ": members were added")
                break
            if added == (30 * len(config["accounts"])):
                time.sleep(7500)


asyncio.run(main())
