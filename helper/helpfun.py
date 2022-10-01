import asyncio
import json, os, sys
from time import sleep
import ujson
from pyrogram import Client, errors, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch
from pathlib import Path
import readchar, platform, signal

''' 
login funtion on line 8-21
filterus function on line 25-59
get-member function on line 61-114
update count 118-224
add-member function on line 226-
'''


async def login(phone, api_id, api_hash, auto_join, group_target_id, group_source_id):
    async with Client(phone, api_id, api_hash, workdir='session')as app:
        if await app.get_me():
            print(phone, 'is logined')
            if auto_join is True:
                try:
                    await app.join_chat(group_source_id)
                except BaseException as e:
                     print(phone,' number is already in group or join manually for group source' )
                try:
                    await app.join_chat(group_target_id)
                except BaseException as e:
                    print(phone,' number is already in group or join manually for group target')
            else:
                print('auto join is off check config')
        else:
            print(phone, 'login failed')


def filterus(p1,p2,p4):
        p3 = Path("data/user.json")
        if os.path.isfile(p1):
            print('starting filter user')
            try: 
                with open(p1) as f:
                    json11 = ujson.loads(f.read())
                with open(p2) as b:
                    json22 = ujson.loads(b.read())

                newjson = [user for user in json11 if not any(
                    user["userid"] == other["userid"] for other in json22)]
                with open(p3, 'w', encoding='utf-8') as file:
                    ujson.dump(newjson, file, ensure_ascii=False, indent=4)
                print("Filter process done")
            except:
                print("failed to make filter json")
        #path_group3 = 'data/user.json'
        if os.path.isfile(p3):
            try:
                with open(p3) as c:
                    json33 = ujson.loads(c.read())
                with open(p4) as h:
                    json44 = ujson.loads(h.read())
                finaljson = [user for user in json33 if not any(
                    user["userid"] == other["userid"] for other in json44)]
                 
                with open(p3, "w", encoding='utf-8') as f:
                    ujson.dump(finaljson, f, ensure_ascii=False, indent=4)
                
            except:
                print("no admin in group")
            #disconect

async def get_data(gp_s_id, gp_t_id, config, stop):
    for account in config['accounts']:
        phone = account["phone"]
        async with Client(phone, workdir="session") as app: 
            print(phone, "is logined") if await app.get_me() else print(phone, "login failed")
            mem=[] 
            async for member in app.get_chat_members(chat_id=gp_s_id):
                await asyncio.sleep(.0025)
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
              		  "status": str(member.user.status),
              		  "name": str(member.user.first_name),
                      "bot": member.user.is_bot,
                      "username": str(member.user.username)
               			        }
                except:
                    print('error')
                mem.append(memb)
            print(phone, 'getting source user data')
            mem2=[] 
            async for member in app.get_chat_members(chat_id=gp_t_id):
                await asyncio.sleep(.0025)
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
              		  "status": str(member.user.status),
              		  "name": str(member.user.first_name),
                      "bot": member.user.is_bot,
                      "username": str(member.user.username)
                      
               			        }
                except:
                    print('error')
                mem2.append(memb)
            print(phone, 'getting target user data')
            mem3=[]
            async for member in app.get_chat_members(chat_id=gp_s_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                try:
                    #scrap member
                    memb = {
               		"userid": str(member.user.id),
               		"name": str(member.user.first_name),
                    "bot": member.user.is_bot,
                    "username": str(member.user.username)
               			        }
                except:
                    print('error')
                mem3.append(memb)
            print(phone, 'getting admin user data')
            with open('data/source_user.json', 'w', encoding='utf-8') as f:
                json.dump(mem, f, indent=4, ensure_ascii=False)
                print("saving source user")
            with open('data/target_user.json', 'w', encoding='utf-8') as f:
                json.dump(mem2, f, indent=4, ensure_ascii=False)
                print("saving target user")
            with open('data/source_admin.json', 'w', encoding='utf-8') as f:
                json.dump(mem3, f, indent=4, ensure_ascii=False)
                print("saving admin user")
                
        if "username" == stop:
            break
            # refresh hash acces for all accounts 
 
def updatecount(count):
    with open('current_count.txt', 'w') as g:
        g.write(str(count))
        g.close()

               
async def add_mem(user_id, config, active, method):
    try:
        with open('current_count.txt') as f:
            counter = int(f.read())             
    except:
            counter = 0

    chat_idt = int(str(-100) +str(config['group_target']))
    added = 0
    print('total account trying to login',len(config['accounts']))
    await asyncio.sleep(0.4)
    applist = []
    for account in config['accounts']:
        phone = account["phone"]
        apiid = account['api_id']
        apihash = account['api_hash']
        app = Client(phone,api_id=apiid, api_hash=apihash, workdir="session")
        await app.start()
        check = await app.get_me()
        if check:
            print('\n',phone, 'login sucess', end='\r')
            # applist.append({'phone': phone, 'app': app})
            try:
                messegespam = await app.send_message('@spambot', '/start')
                messget = await  app.get_messages('@spambot', message_ids=(int(messegespam.id) + 1))
                if str(messget.text) == "Good news, no limits are currently applied to your account. You’re free as a bird!":
                    applist.append({'phone': phone, 'app': app})
                else:
                    print(phone, 'is limited or disabled! will no be used for this RUN', end='\r')
            except (BaseException, YouBlockedUser):
                print('could not perform spam test on this', phone)
                applist.append({'phone': phone, 'app': app})
                
                
        
        else:
            print('\n', phone, "login failed")
            await asyncio.sleep(1)
       
    print('\n', 'total logind account ', len(applist))
    await asyncio.sleep(1)
    if method == 'username':
        usermethod = "username"
    else:
        usermethod = "userid"
    print(len(user_id), counter)
    while (len(user_id) - counter) > 1:
        for account in applist:
            if (len(user_id) - counter) == 0:
                break
            phone = account['phone']
            app = account['app']
            user_active = user_id[counter]["status"]
            try:
                if user_id[counter][usermethod] == 'None':
                    counter += 1
                    updatecount(counter)
                    continue
                if user_id[counter]["bot"]:
                    counter += 1
                    updatecount(counter)
                    continue
                if user_active in active:
                    print("trying to add", user_id[counter]["userid"], 'by', phone)
                    await app.add_chat_members(chat_id=chat_idt, user_ids=user_id[counter][usermethod])
                    print(user_id[counter]["userid"], "added success")
                    counter += 1
                    added += 1
                    print('sleep: ' + str(120 / len(applist)))
                    await asyncio.sleep(120 / len(applist))
                    updatecount(counter)
                else:
                    counter += 1
                    updatecount(counter)
            except PhoneNumberBanned: 
                applist.remove(account)  
                await app.stop()
                print('phone number banned', phone)    
            except PeerFlood:
                applist.remove(account)
                await app.stop()
                counter +=1
                print(phone, 'has been limited by telegram wait or check spambot')
            except UserChannelsTooMuch:
                counter += 1
                print('user already in too many channel')
                updatecount(counter)
            except FloodWait as e:
                applist.remove(account)
                await app.stop()
                print(e.value, 'is required for mobile no', phone)
            except (ChatAdminRequired, ChannelPrivate):
                print("Chat admin permission required or Channel is private")
                applist.remove(account)
                await app.stop()
            except UserRestricted:
                print("removing this restricted account")
                applist.remove(account)
                await app.stop()
            except UserIdInvalid:
                print("user invalid or u never met user", phone)
                print('sleep: ' + str(120 / len(applist)))
                await asyncio.sleep(120 / len(applist))
                counter +=1
                updatecount(counter)
            except UserNotMutualContact:
                print('user is not mutal contact')
                counter += 1
                updatecount(counter)
            except PeerIdInvalid as e:
                print("if You see this line many time rerun the get_data.py")
                #applist.remove(account)
                counter +=1
                updatecount(counter)
            except UserPrivacyRestricted:
                print("user have privacy enabled")
                print('sleep: ' + str(120 / len(applist)))
                await asyncio.sleep(120 / len(applist))
                counter +=1
                updatecount(counter)
            except TimeoutError:
                print('network problem was encounterd')
            except RPCError as e:
                print(phone, "Rpc error")
                print(e)
                print,(user_id)
                print('sleep: ' + str(120 / len(applist)))
                await asyncio.sleep(120 / len(applist))
                counter +=1
                updatecount(counter)
            except BaseException as e:
                print(phone, "error info below")
                print(e)
                print,(user_id)
                print('sleep: ' + str(120 / len(applist)))
                await asyncio.sleep(120 / len(applist))
                counter +=1
                updatecount(counter)
            if len(applist) == 0:
                print(added, ": members were added")
                updatecount(counter)
                exit()
            if added == (30 * len(applist)):
                print(added, ": members were added")
                await asyncio.sleep(7000)
                
