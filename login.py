import asyncio
import json
from helper.login import login
from helper.pam_log import pamlog
#load config for accounts
config=json.load(open('config.json'))
group_source_id=str(config['group_source_username'])
group_target_id=str(config['group_target_username'])
auto_join=bool(config['auto_join'])
async def loginall():
    PAM = pamlog('PAM-START_LOGIN')
    PAM.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PAM.info(phone)
        await login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id)
asyncio.run(loginall())
