import asyncio
import json, os, sys
import gc
from pyrogram import Client, enums
from pyrogram.errors import *
from pyrogram.raw import functions, types
from pathlib import Path
from datetime import datetime, timedelta
import logging
import random
from itertools import dropwhile
import platform
import signal
import readchar

def pamlog(name):
    # create logger Name PAM
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
    # create console handler and set level to INFO
        pam = logging.StreamHandler()
        pam.setLevel(logging.INFO)
        
        # create formatter For PAM
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        
        # add formatter to pam
        pam.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(pam)
    else:
        pass
    return logger


class pyroadd(object):

    def __init__(self, config):
        self.root = Path().cwd()
        self.config = json.load(open(self.root / config, 'r',
                                     encoding='utf-8'))
        self.source_groupid = int(str("-100")+str(self.config['group_source']))
        self.target_groupid =int(str("-100")+str(self.config['group_target']))
        self.source_group = self.config.get('group_source_username', None)
        self.target_group = self.config.get('group_target_username', None)
        self.accounts = self.config['accounts']
        self.activelist = ['UserStatus.LONG_AGO', 'UserStatus.LAST_MONTH', 'UserStatus.LAST_WEEK', 'UserStatus.OFFLINE', 'UserStatus.RECENTLY', 'UserStatus.ONLINE' ]
        self.active = []
        self.counterall = {}
        self.loop = asyncio.run
        for x in dropwhile(lambda y: y != self.config["from_date_active"], self.activelist):
           self.active.append(x)

    def Signup(self, pam_log, work_dir):
        self.loop(self._signup(pam_log, work_dir))
    async def _signup(self, pam_log, work_dir):
        PAM = pamlog(pam_log)
        for account in self.accounts:
            phone = account['phone']
            api_id = int(account['api_id'])
            api_hash = account['api_hash']
            device_model= account['device_model']
            system_version= account['system_version']
            app_version= account['app_version']
            PAM.info(phone)
            if not (self.root / work_dir).exists():
                os.makedirs(self.root / work_dir)

            try:
                async with Client(phone,
                                  api_id,
                                  api_hash,
                                  workdir=self.root / work_dir,
                                  app_version=app_version,
                                  device_model=device_model,
                                  system_version=system_version,
                                  lang_code='en') as app:

                    await app.invoke(functions.account.UpdateStatus(offline=False))
                    if await app.get_me():
                        PAM.info(f'{phone} is logined')
                        await app.invoke(functions.account.UpdateStatus(offline=True))
            except Exceptionas as e:
                PAM.info(f'{e}')

    def Login(self, pam_log, work_dir, applist):
        return self.loop(self._login(pam_log, work_dir, applist))
    async def _login(self, pam_log, work_dir, applist):
        PAM = pamlog(pam_log)
        self.app_list = []
        for account in self.accounts:
            phone = account['phone']
            api_id = int(account['api_id'])
            api_hash = account['api_hash']
            device_model= account['device_model']
            system_version= account['system_version']
            app_version= account['app_version']
            try:
                app = Client(phone, api_id, api_hash,
                                    app_version=app_version,
                                  device_model=device_model,
                                  system_version=system_version,
                                  lang_code='en',
                                  workdir=self.root / work_dir)
                await app.start()
                await app.invoke(functions.account.UpdateStatus(offline=False))
                if await app.get_me():
                    PAM.info(f'{phone} is logined')
                    if self.config['auto_join'] is True:
                        try:
                            await app.join_chat(self.source_group)
                            PAM.info(f"{phone} joined source group")
                        except UserAlreadyParticipant:
                            await app.get_chat(self.source_group)
                            PAM.info(f"{phone} already in source group")
                        except BaseException as e:
                            PAM.info(
                                "could not join maybe already in source group"
                            )
                        try:
                            await app.join_chat(self.target_group)
                            PAM.info(f"{phone} joined target group")
                        except UserAlreadyParticipant:
                            await app.get_chat(self.target_group)
                            PAM.info(f"{phone} already in target group")
                        except BaseException as e:
                            PAM.info(
                                "could not join maybe already in target group"
                            )
                    else:
                        PAM.info('auto join is off check config')
                    self.app_list.append({
                            'phone': account["phone"],
                            'app': app
                        })

                    await asyncio.sleep(.1)
                else:
                    PAM.info(phone, 'login failed')
            except UserDeactivatedBan:
                PAM.info(f'account deleted {phone}')
            except BaseException as e:
                PAM.info(f'error : {e}')
        if applist:
            return self.app_list
        else:
            for appp in self.app_list:
                try:
                    await appp.stop()
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                except:
                    pass

    def get_data(self, pam_log, work_dir, stop):
        self.loop(self._get_data(pam_log, work_dir, stop))
    async def _get_data(self, pam_log, work_dir, stop):
        PAM = pamlog('PAM-GET-DATA')
        try:
            count = {}
            with open(self.root / 'current_count.py', 'w') as g:
                g.write(str(count))
                g.close()
        except BaseException:
            pass
        firstrun = True
        mem = []
        for phonedata in self.accounts:
            phone = phonedata["phone"]
            api_id = int(phonedata['api_id'])
            api_hash = phonedata['api_hash']
            device_model= phonedata['device_model']
            system_version= phonedata['system_version']
            app_version= phonedata['app_version']
            try:
                async with Client(phone, api_id, api_hash,
                                        app_version=app_version,
                                    device_model=device_model,
                                    system_version=system_version,
                                    lang_code='en', workdir=self.root / work_dir) as app:
                    await app.invoke(functions.account.UpdateStatus(offline=False))
                    if await app.get_me():
                        pass
                    else:
                        PAM.info(f"{phone} login failed")
                    try:
                        await app.get_chat(self.source_groupid)
                    except:
                        PAM.info(
                            f"{phone} has not joined source chat or RUN login.py")
                        co = input('will you like to continue Y/N')
                        if co.lower() == 'n':
                            PAM.info('Exiting The program')
                            exit()
                    try:
                        await app.get_chat(self.target_groupid)
                    except:
                        PAM.info(
                            f"{phone} has not joined target chat or RUN login.py")
                        await asyncio.sleep(1)
                    mem = []
                    async for member in app.get_chat_members(
                            chat_id=self.source_groupid):
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
                    if firstrun:
                        mem2 = []
                        PAM.info(f'{phone} getting target user data')
                        async for member in app.get_chat_members(
                                chat_id=self.target_groupid):
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
                        mem3 = []
                        PAM.info(f'{phone} getting admin user data')
                        async for member in app.get_chat_members(
                                chat_id=self.source_groupid,
                                filter=enums.ChatMembersFilter.ADMINISTRATORS):
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
                        firstrun = False
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    await app.stop()
                    if stop:
                        break
            except UserDeactivatedBan as e:
                PAM.info(e)
            if not mem:
                PAM.info(f"NO DATA")
            else:
                self.filterus(mem, mem2, mem3)
            
                    

    def filterus(self, p1, p2, p4):
        # create logger
        p3 = self.root / "data" / "user.json"
        if not (self.root / "data").exists():
            os.makedirs(self.root / "data")
        try:
            garbage_id = {d['userid'] for d in p2}
            json1 = [
                item for item in p1 if item['userid'] not in garbage_id
            ]
            with open(p3, 'w', encoding='utf-8') as file:
                json.dump(json1, file, ensure_ascii=False, indent=4)
            print("Filter process done")
        except:
            print("failed to make filter json")
        #path_group3 = 'data/user.json'
        if p3.exists():
            try:
                garbage_i = {d['userid'] for d in p4}
                json2 = [
                    item for item in json1 if item['userid'] not in garbage_i
                ]
                with open(p3, "w", encoding='utf-8') as f:
                    json.dump(json2, f, ensure_ascii=False, indent=4)
            except:
                print("no admin in group")
    
    def handler(signum, frame):
        msg = " Ctrl-c OR Ctrl-z was pressed. Do you really want to exit? y/n "
        print(msg)
        res = readchar.readchar()
        if res == 'y':
            self.updatecount(self.counterall)
            print('Bye!')
            sys.exit()
        else:
            print(f'Okay then I will continue')

    def updatecount(count):
        with open('current_count.py', 'w') as g:
            g.write(str(count))
            g.close()
    
    def add_member(self, pam_log, work_dir, method, applist):
        self.loop(self._add_member(pam_log, work_dir, method, applist))
    async def _add_member(self,pam_log, work_dir, method, applist):
        PAM = pamlog(pam_log)
        user_id = json.load(open( self.root / "data" / "user.json", "r", encoding="utf-8"))
        try:
            with open('current_count.py') as f:
                data = f.read()       
                self.counterall = ast.literal_eval(data)    
                counter = self.counterall["counter"]
                added2 = self.counterall["added"]
                skipped2  = self.counterall['skipped']
                privacy2  = self.counterall['privacy']
                uc2  = self.counterall['already in too many channel/group']
        except:
                counter = added2 = privacy2 = uc2 = skipped2 =  0
        added = skipped = privacy = uc = um = bot = noname = osr = 0
        waittime = self.config.get('wait_time', 300)

        async def prints():
            self.updatecount(self.counterall)
            wait_time = str(waittime / len(applist))
            PAM.info(f'sleep: {wait_time}')
            await asyncio.sleep(waittime / len(applist))

        def printfinal():
            print(f"{added} : members were added\n {skipped} : members were skipped\n {privacy} : members had privacy enable or not in mutual contact\n {uc} : user banned in chat\n {um} : members not in mutual contat\n {bot}:  bot accont skipped")
            if method == 'username':
                PAM.info(f"{noname} : accont has no usernames")
            self.updatecount(self.counterall)
            print(datetime.now().strftime("%H:%M:%S"))
        logined_account = len(applist)
        PAM.info(f"total logind account {logined_account}")
        await asyncio.sleep(1)
        usermethod = "username" if method[0] == 'u' else "userid"
        print(len(user_id), counter)

        if platform.system() == 'Windows':
            signal.signal(signal.SIGTERM, self.handler)
            signal.signal(signal.SIGINT, self.handler)
        else:
            signal.signal(signal.SIGINT, self.handler)
            signal.signal(signal.SIGTSTP, self.handler)
        
        while len(user_id) - counter > 1:
            leftmem = len(user_id) - counter
            self.counterall = {'counter': int(counter), 
                        'left_to_add': int(leftmem),
                        'added': int(added2) + int(added),
                        'skipped': int(skipped2) + int(skipped),
                        'privacy': int(privacy2) + int(privacy),
                        'already in too many channel/group':int(uc2) + int(uc)}
            for account in applist:
                try:
                    if applist == False:
                        printfinal()
                        exit()
                    elif added == (30 * len(applist)):
                        printfinal()
                        PAM.info("Sleeping for two hours")

                        now = datetime.now()
                        end = datetime.now() + timedelta(hours=2)
                        print("Sleep started at : ", now.strftime("%H:%M:%S"))
                        print("Sleep End at : ", end.strftime("%H:%M:%S"))
                        added = 0
                        await asyncio.sleep(3500)
                        PAM.info("1 hour left to continue")
                        await asyncio.sleep(3500)
                except Exception as e:
                                PAM.info(str(e))
                phone = account['phone']
                app = account['app']
                try:  
                    while user_id[counter]["bot"] == True or user_id[counter][usermethod] == 'None' or user_id[counter]["status"] not in active:
                        try:
                            if user_id[counter]["status"] not in active:   
                                counter += 1
                                skipped += 1
                                self.updatecount(self.counterall)
                                PAM.info('Inactive user skipped')
                            if user_id[counter]["bot"] == True:
                                counter += 1
                                bot += 1
                                self.updatecount(self.counterall)
                                PAM.info("bot skipped")
                            if user_id[counter][usermethod] == 'None':
                                counter += 1
                                noname += 1
                                self.updatecount(self.counterall)
                                PAM.info('NO USERNAME found for this user skipped')
                        except:
                            printfinal()
                            PAM.info("Finished")
                except:
                    printfinal()
                    PAM.info("Finished")
                try:
                    postiton = applist.index(account)
                    current_user = user_id[counter]["userid"]
                    postion2 = len(applist)
                    PAM.info(f"trying to add {current_user} by : {phone} account-postiton : {postiton + 1} / {postion2}")
                    await app.invoke(functions.account.UpdateStatus(offline=False))
                    await app.add_chat_members(chat_id=self.target_groupid, user_ids=user_id[counter][usermethod])
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info(f"{current_user} added success")
                    counter += 1
                    added += 1
                    await prints()
                except (UserBannedInChannel, PhoneNumberBanned, PeerFlood, FloodWait, ChatAdminRequired, ChannelPrivate) as e: 
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    await app.stop()
                    applist.remove(account)  
                    PAM.error(f'{e}')  
                    await prints()
                except (UsernameNotOccupied, UserDeactivatedBan, UserKicked, UserIdInvalid) as e:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.error(f"{e}")
                    counter +=1
                    await prints()
                except UserChannelsTooMuch:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    counter += 1
                    uc += 1
                    PAM.info('user already in too many channel')
                    await prints()
                except UserNotMutualContact:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info('user is not mutal contact')
                    counter += 1
                    um += 1
                    await prints()
                except PeerIdInvalid:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info("if You see this line many time rerun the get_data.py")
                    #applist.remove(account)
                    counter +=1
                    await prints()
                except UserPrivacyRestricted:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info("user have privacy enabled")
                    counter +=1
                    privacy += 1
                    await prints()
                except TimeoutError:
                    PAM.info('network problem was encounterd')
                except RPCError as e:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info(f"{phone} Rpc error")
                    PAM.info(f"{e}")
                    m = user_id[counter][usermethod]
                    PAM.info(f"{m}")
                    counter +=1
                    await prints()
                except OSError:
                    osr +=1
                except BaseException as e:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info(phone, "error info below")
                    PAM.info(f"{e}")
                    m = user_id[counter][usermethod]
                    PAM.info(f"{m}")
                    counter +=1
                    await prints()
                if osr == 30:
                    await app.invoke(functions.account.UpdateStatus(offline=True))
                    PAM.info("osr is 30")
                    PAM.info('This increase beacuse of internet problem try again later')
                    await prints()
                    exit()