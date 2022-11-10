import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging

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
                