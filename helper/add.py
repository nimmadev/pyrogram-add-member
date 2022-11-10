import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
# function used to update counter.txt
def updatecount(count):
    with open('current_count.txt', 'w') as g:
        g.write(str(count))
        g.close()

# function used to login all account in addmember


async def addlogin(config):
    # create logger
    logger = logging.getLogger('PAM')
    logger.setLevel(logging.INFO)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # create formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    
    # add formatter to ch
    ch.setFormatter(formatter)
    
    # add ch to logger
    logger.addHandler(ch)
    #login starthere
    applist = []
    for account in config:
        phone = account["phone"]
        app = Client(phone,api_id=account["api_id"], api_hash=account["api_hash"], workdir="session")
        await app.start()
        check = await app.get_me() 
        try:   
            spam = config["spam_check"]
        except:
            spam = False
        if check:
            logger.info(f'{phone} login sucess')
            # print('\n',account["phone"], 'login sucess')
            # applist.append({'phone': phone, 'app': app})
            if spam:
                try:
                    messegespam = await app.send_message('@spambot', '/start')
                    messget = await  app.get_messages('@spambot', message_ids=(int(messegespam.id) + 1)).text
                    listofnum =["1","2","3","4","5","6","7","8","9","0"]
                    checktext = [x for x in listofnum if(x in messget)] 
                    if checktext:
                        logger.info(f'{phone} is limited or disabled! will no be used for this RUN')
                    else:
                        applist.append({'phone': account["phone"], 'app': app})
                except (BaseException, YouBlockedUser):
                    logger.info(f'could not perform spam test on this {phone}')
                    applist.append({'phone': account["phone"], 'app': app})
            else:
                applist.append({'phone': account["phone"], 'app': app})
        else:
            logger.info(f'{phone} login failed')
            await asyncio.sleep(1)
    return applist

#main function whih add member
async def add_mem(user_id, config, active, method):
    #check if need continue
    try:
        with open('current_count.txt') as f:
            counter = int(f.read())             
    except:
            counter = 0

    chat_idt = int(str(-100) +str(config['group_target']))

    # all zero value avar initali
    added = skipped = privacy = uc = um = bot = noname = osr = 0
    try:
        waittime = config["wait_time"]
    except:
        waittime = 120

    # single function for sleep and time logger.info
    async def prints():
        updatecount(counter)
        print('sleep: ' + str(waittime / len(applist)))
        await asyncio.sleep(waittime / len(applist))

    #single line f string for printinf final output
    def printfinal():
        print(f"{added} : members were added\n {skipped} : members were skipped\n {privacy} : members had privacy enable or not in mutual contact\n {uc} : user banned in chat\n {um} : members not in mutual contat\n {bot}:  bot accont skipped")
        if method == 'username':
            print("%s : accont has no usernames" % noname)
        updatecount(counter)
        print(datetime.now().strftime("%H:%M:%S"))
    
    print('total account trying to login',len(config['accounts']))
    await asyncio.sleep(0.4)
    applist = await addlogin(config['accounts'])
    print("total logind account ", len(applist))
    await asyncio.sleep(1)
    if method[0] == 'u':
        usermethod = "username"
    else:
        usermethod = "userid"
    print(len(user_id), counter)
    while (len(user_id) - counter) > 1:
        for account in applist:
            if (len(user_id) - counter) == 0:
                printfinal()
                break
            if len(applist) == 0:
                printfinal()
                break
            phone = account['phone']
            app = account['app']
            user_active = user_id[counter]["status"]
            try:
                if user_id[counter]["bot"]:
                    counter += 1
                    bot += 1
                    updatecount(counter)
                elif user_id[counter][usermethod] == 'None':
                    counter += 1
                    noname += 1
                    updatecount(counter)
                elif user_active in active:
                    print("trying to add", user_id[counter]["userid"], 'by account', applist.index(account), '/', len(applist))
                    await app.add_chat_members(chat_id=chat_idt, user_ids=user_id[counter][usermethod])
                    print(user_id[counter]["userid"], "added success")
                    counter += 1
                    added += 1
                    await prints()
                else:
                    counter += 1
                    skipped += 1
                    updatecount(counter)
            except UserKicked:
                print('this user is banned')
                counter +=1
                await prints()
            except PhoneNumberBanned: 
                applist.remove(account)  
                await app.stop()
                print('phone number banned', phone)  
                await prints()
            except PeerFlood:
                applist.remove(account)
                await app.stop()
                counter +=1
                print(phone, 'removed for this run')
                try: 
                    await prints()
                except:
                    printfinal()
            except UserChannelsTooMuch:
                counter += 1
                uc += 1
                print('user already in too many channel')
                await prints()
            except FloodWait as e:
                applist.remove(account)
                await app.stop()
                print('%s seconds sleep is required for the account %s' %(e.value, phone))
            except (ChatAdminRequired, ChannelPrivate):
                print("Chat admin permission required or Channel is private")
                applist.remove(account)
                await app.stop()
                await prints()
            except UserRestricted:
                print("removing this restricted account")
                applist.remove(account)
                await app.stop()
            except UserIdInvalid:
                print("user invalid or u never met user", phone)
                counter +=1
                await prints()
            except UserNotMutualContact:
                print('user is not mutal contact')
                counter += 1
                um += 1
                await prints()
            except PeerIdInvalid as e:
                print("if You see this line many time rerun the get_data.py")
                #applist.remove(account)
                counter +=1
                await prints()
            except UserPrivacyRestricted:
                print("user have privacy enabled")
                counter +=1
                privacy += 1
                await prints()
            except TimeoutError:
                print('network problem was encounterd')
            except RPCError as e:
                print(phone, "Rpc error")
                print(e)
                print(user_id)
                counter +=1
                await prints()
            except OSError:
                osr +=1
            except BaseException as e:
                print(phone, "error info below")
                print(e)
                print(user_id)
                counter +=1
                await prints()
            if osr == 30:
                printfinal()
        
                await asyncio.sleep(700)
            try:
                if added == (30 * len(applist)):
                    printfinal()
                    print()
                    print("Sleeping for two hours")
                    print()
                    now = datetime.now()
                    end = datetime.now() + timedelta(hours=2)
                    print("Sleep started at : ", now.strftime("%H:%M:%S"))
                    print("Sleep End at : ", end.strftime("%H:%M:%S"))
                    added = 0
                    await asyncio.sleep(3500)
                    print("1 hour left to continue")
                    await asyncio.sleep(3500)
                    
            except ZeroDivisionError:
                printfinal()
                print()
                print("Sleeping for two hours")
                print()
                now = datetime.now()
                end = datetime.now() + timedelta(hours=2)
                print("Sleep started at : ", now.strftime("%H:%M:%S"))
                print("Sleep End at : ", end.strftime("%H:%M:%S"))
                added = 0
                await asyncio.sleep(3500)
                print("1 hour left to continue")
                await asyncio.sleep(3500)

    else:
        printfinal()

