import asyncio
import json
from helper.helpfun import login
#load config for accounts
config=json.load(open('config.json'))
group_source_id=str(config['group_source_username'])
group_target_id=str(config['group_target_username'])
auto_join=bool(config['auto_join'])
async def loginall():
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        print(phone)
        await login(phone, api_id, api_hash, auto_join,group_target_id, group_source_id)
asyncio.run(loginall())
