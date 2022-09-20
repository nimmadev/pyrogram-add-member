import asyncio
import json, os
from pyrogram import Client, enums
from helper.helpfun import filterus, get_data
#loads config

#workdir = 'session/'

async def main():
     config = (json.load(open("config.json")))
     gp_s_id = int(str("-100")+str(config['group_source']))
     gp_t_id = int(str("-100")+str(config['group_target']))
     path_group = 'data/source_user.json'
     path_group2 = 'data/target_user.json'
     path_group4 = 'data/source_admin.json'
     path_group3 = 'data/user.json'
     await get_data(gp_s_id, gp_t_id, config)
     filterus(path_group,path_group2,path_group3, path_group4)
     

            
asyncio.run(main())

