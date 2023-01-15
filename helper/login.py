import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, UserDeactivatedBan, UserAlreadyParticipant, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
from helper.pam_log import pamlog
def get_device():
    with open(Path('helper/device.json'), 'r', encoding='utf-8') as f:
        device_data = json.load(f)
        device_data = random.choice(device_data)
        device_model = device_data['device_model']
        system_version = device_data['system_version']
        return [device_model, system_version]

async def create(phone, api_id, api_hash):
    PAM = pamlog('PAM-Signup')
    PAM.propagate = False
    DATA = get_device()
    device_model = DATA[0]
    system_version = DATA[1]

    try:
        async with Client(phone, api_id, api_hash, workdir='session', app_version='7.9.2',
                                device_model=device_model, system_version=system_version, lang_code='en') as app:
            if await app.get_me():
                PAM.info(f'{phone} is logined')
    except Exceptionas as e:
        PAM.info(f'{e}')

async def login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id):
    # create logger
    PAM = pamlog('PAM-Login')
    PAM.propagate = False
    try:
        async with Client(phone, api_id, api_hash, workdir='session')as app:
            if await app.get_me():
                PAM.info(f'{phone} is logined')
                if auto_join is True:
                    try:
                        await app.join_chat(group_source_id)
                    except UserAlreadyParticipant:
                        await app.get_chat(group_source_id)
                    except BaseException as e:
                        PAM.info("could not join maybe already in source group")

                    try:
                        await app.join_chat(group_target_id)
                    except UserAlreadyParticipant:
                        pass
                    except BaseException as e:
                        PAM.info("could not join maybe already in target group")
                else:
                    PAM.info('auto join is off check config')
                await asyncio.sleep(.1)
            else:
                PAM.info(phone, 'login failed')
    except UserDeactivatedBan:
        PAM.info(f'account deleted {phone}')
    except BaseException as e:
        PAM.info(f'error : {e}')
