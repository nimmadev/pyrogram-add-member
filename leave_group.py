import asyncio
import json
from helper.leave_group import leave, leave2
from helper.pam_log import pamlog
#load config for accounts
config=json.load(open('config.json'))
group_source_id= '-100 ' + str(config['group_source'])
group_target_id= '-100' + str(config['group_target'])
option = input('type 1 to leave source group and 2 for both: ')
async def loginall():
    PAM = pamlog('PAM-Leave_Group')
    PAM.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PAM.info(phone)
        if option == '1':
            await leave(phone, api_id, api_hash, group_source_id)
        elif option == '2':
            await leave2(phone, api_id, api_hash, group_source_id,  group_target_id) 
        else:
            PAM.info('Wrong option')
asyncio.run(loginall())
