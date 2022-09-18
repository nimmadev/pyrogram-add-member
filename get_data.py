import asyncio
import json, os
from pyrogram import Client, enums
#loads config

#workdir = 'session/'

async def main():
     config = (json.load(open("config.json")))
     group_source_id = int(str("-100")+str(config['group_source']))
     group_target_id = int(str("-100")+str(config['group_target']))
     for account in config["accounts"]:
     	phone = account["phone"]
     	mem = []
     	mem2 = []
     	mem3 = []
     	async with Client(phone, workdir="session") as app:
            print( "is logined") if await app.get_me() else print("login failed")
            async for member in app.get_chat_members(chat_id=group_source_id):
               
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
              		  "status": str(member.user.status),
              		  "name": str(member.user.first_name)
               			        }
                except:
              	   print('error')
                mem.append(memb)
            async for member in app.get_chat_members(chat_id=group_target_id):
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
              		  "status": str(member.user.status),
              		  "name": str(member.user.first_name)
               			        }
                except:
              	   print('error')
                mem2.append(memb)
            async for member in app.get_chat_members(chat_id=group_source_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
               		  "name": str(member.user.first_name)
               			        }
                except:
              	   print('error')
                mem3.append(memb)
            with open('data/source_user.json', 'w', encoding='utf-8') as f:
                json.dump(mem, f, indent=4, ensure_ascii=False)
                print("done")
            with open('data/target_user.json', 'w', encoding='utf-8') as f:
                json.dump(mem2, f, indent=4, ensure_ascii=False)
                print("done")
            with open('data/source_admin.json', 'w', encoding='utf-8') as f:
                json.dump(mem3, f, indent=4, ensure_ascii=False)
                print("done")
            # refresh hash acces for all accounts 
            
            

def filterus():
        path_group = 'data/source_user.json'
        path_group2 = 'data/target_user.json'
        path_group4 = 'data/source_admin.json'
        if os.path.isfile(path_group):
            try: 
                with open(path_group) as f:
                    json11 = json.loads(f.read())
                with open(path_group2) as b:
                    json22 = json.loads(b.read())

                newjson = [user for user in json11 if not any(
                    user["userid"] == other["userid"] for other in json22)]
                with open('data/user.json', "w") as f:
                    json.dump(newjson, f, ensure_ascii=False, indent=4)
                print("Filter process done")
            except:
                print("failed to make filter json")
        path_group3 = 'data/user.json'
        if os.path.isfile(path_group3):
            try:
                with open(path_group3) as c:
                    json33 = json.loads(b.read())
                with open(path_group4) as c:
                    json44 = json.loads(b.read())
                finaljson = [user for user in json33 if not any(
                    user["userid"] == other["userid"] for other in json44)]
                 
                with open('data/user.json', "w") as f:
                    json.dump(finaljson, f, ensure_ascii=False, indent=4)
                
            except:
                print("no admin in group")
            #disconect
            
asyncio.run(main())
filterus()