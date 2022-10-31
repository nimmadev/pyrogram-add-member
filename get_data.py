import asyncio
import json, os
from pyrogram import Client, enums
from helper.helpfun import filterus, get_data
from pathlib import Path
#loads config

#workdir = 'session/'
stop = input('choose method username or id: ').lower()
async def main():
     root = Path.cwd()
     config = (json.load(open("config.json")))
     gp_s_id = int(str("-100")+str(config['group_source']))
     gp_t_id = int(str("-100")+str(config['group_target']))
     path_group =  root / 'data' / 'source_user.json'
     path_group2 = root / 'data' / 'target_user.json'
     path_group4 = root / 'data' / 'source_admin.json'
     await get_data(gp_s_id, gp_t_id, config, stop)
     filterus(path_group,path_group2, path_group4, root)
     

            
asyncio.run(main())

