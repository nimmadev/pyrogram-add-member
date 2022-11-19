import asyncio
import json, os
import ast
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked, UserDeactivatedBan, UsernameNotOccupied
from pathlib import Path
from helper.applist import addlogin
from datetime import datetime, timedelta
import logging
# function used to update counter.txt
def updatecount(count):
    with open('current_count.py', 'w') as g:
        g.write(str(count))
        g.close()


#main function whih add member
async def add_mem(user_id, config, active, method):
    #check if need continue
    try:
        with open('current_count.py') as f:
            data = f.read()       
            counterall = ast.literal_eval(data)    
            counter = counterall["counter"]
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
        updatecount(counterall)
        print('sleep: ' + str(waittime / len(applist)))
        await asyncio.sleep(waittime / len(applist))

    #single line f string for printinf final output
    def printfinal():
        print(f"{added} : members were added\n {skipped} : members were skipped\n {privacy} : members had privacy enable or not in mutual contact\n {uc} : user banned in chat\n {um} : members not in mutual contat\n {bot}:  bot accont skipped")
        if method == 'username':
            print("%s : accont has no usernames" % noname)
        updatecount(counterall)
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
    
    while len(user_id) - counter > 1:
        leftmem = len(user_id) - counter
        counterall = {'counter': int(counter), 'left_to_add': int(leftmem)}
        for account in applist:
            if (len(user_id) - counter) == 0:
                printfinal()
                exit()
            if len(applist) == 0:
                printfinal()
                exit()
            phone = account['phone']
            app = account['app']
            user_active = user_id[counter]["status"]
            try:
                if user_id[counter]["bot"]:
                    counter += 1
                    bot += 1
                    updatecount(counterall)
                elif user_id[counter][usermethod] == 'None':
                    counter += 1
                    noname += 1
                    updatecount(counterall)
                elif user_active in active:
                    print("trying to add", user_id[counter]["userid"], 'by phone number', phone)
                    await app.add_chat_members(chat_id=chat_idt, user_ids=user_id[counter][usermethod])
                    print(user_id[counter]["userid"], "added success")
                    counter += 1
                    added += 1
                    await prints()
                else:
                    counter += 1
                    skipped += 1
                    updatecount(counterall)
            except UsernameNotOccupied:
                print("user not using username anymore")
                counter +=1
                await prints()
            except UserDeactivatedBan:
                print("user removed from telegram")
                counter +=1
                await prints()
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
        exit()

