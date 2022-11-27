import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
from helper.pam_log import pamlog
async def login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id):
    # create logger
    PAM = pamlog('PAM-Login-Signup')
    async with Client(phone, api_id, api_hash, workdir='session')as app:
        if await app.get_me():
            PAM.info(f'{phone} is logined')
            if auto_join is True:
                try:
                    await app.join_chat(group_source_id)
                except BaseException as e:
                     PAM.info("could not join maybe already in source group")

                try:
                    await app.join_chat(group_target_id)
                except BaseException as e:
                    PAM.info("could not join maybe already in target group")
            else:
                PAM.info('auto join is off check config')
            await asyncio.sleep(.1)
        else:
            PAM.info(phone, 'login failed')
