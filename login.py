import asyncio
import json
from helper.login import login, create
from helper.pam_log import pamlog
#load config for accounts
config=json.load(open('config.json', 'r', encoding='utf-8'))
group_source_id=str(config['group_source_username'])
group_target_id=str(config['group_target_username'])
auto_join=bool(config['auto_join'])
option = input('Login or Signup type one : ')
async def createall():
    PAM = pamlog('PAM-START_LOGIN')
    PAM.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PAM.info(phone)
        await create(phone, api_id, api_hash)
async def loginall():
    PAM = pamlog('PAM-START_LOGIN')
    PAM.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PAM.info(phone)
        await login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id)
if option.lower()[0] == 'l':
    asyncio.run(loginall())
elif option.lower()[0] == 's':
    asyncio.run(createall())
