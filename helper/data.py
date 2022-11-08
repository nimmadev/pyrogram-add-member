async def get_data(gp_s_id, gp_t_id, config, stop):
    try:
        count = 0
        with open('current_count.txt', 'w') as g:
            g.write(str(count))
            g.close()
    except:
        pass
    for account in config['accounts']:
        phone = account["phone"]
        print(phone, 'getting source user data')
        async with Client(phone, workdir="session") as app: 
            if await app.get_me():
                print(phone, "is logined")
            else:
                print(phone, "login failed")
            try:
                await app.get_chat(gp_s_id)
            except ValueError:
                print("%s has not joined source chat or RUN get_data.py" % phone)
                await asyncio.sleep(1)
                continue
            try:
                await app.get_chat(gp_t_id)
            except ValueError:
                print("%s has not joined target chat or RUN get_data.py" % phone)
                await asyncio.sleep(1)
                continue
            mem=[]
            async for member in app.get_chat_members(chat_id=gp_s_id):
                await asyncio.sleep(.0025)
                try:
                    #scrap member
                    memb = {
               		  "userid": str(member.user.id),
              		  "status": str(member.user.status),
              		  "name": str(member.user.first_name),
                      "bot": member.user.is_bot,
                      "username": str(member.user.username)
                    }
                    mem.append(memb)
                except:
                    print('error')
        if "username" == stop:
            break
    phonedata = config["accounts"][0]
    phone = phonedata["phone"]
    async with Client(phone, workdir="session") as app: 
        if await app.get_me():
            print(phone, "is logined")
        else:
            print(phone, "login failed")
        try:
            await app.get_chat(gp_s_id)
        except ValueError:
            print("%s has not joined source chat or RUN get_data.py" % phone)
            await asyncio.sleep(1)
        try:
            await app.get_chat(gp_t_id)
        except ValueError:
            print("%s has not joined target chat or RUN get_data.py" % phone)
            await asyncio.sleep(1)
        mem2=[] 
        async for member in app.get_chat_members(chat_id=gp_t_id):
            await asyncio.sleep(.0025)
            try:
                    #scrap member
                memb = {
             	  "userid": str(member.user.id),
              	  "status": str(member.user.status),
              	  "name": str(member.user.first_name),
                  "bot": member.user.is_bot,
                  "username": str(member.user.username)
          	    }
          	    
                mem2.append(memb)
            except:
                print('error')
                
        print(phone, 'getting target user data')
        mem3=[]
        async for member in app.get_chat_members(chat_id=gp_s_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            try:
                    #scrap member
                memb = {
               		"userid": str(member.user.id),
               		"name": str(member.user.first_name),
                    "bot": member.user.is_bot,
                    "username": str(member.user.username)
                }
                
                mem3.append(memb)
            except:
                print('error')
                
        print(phone, 'getting admin user data')
        with open('data/source_user.json', 'w', encoding='utf-8') as f:
            json.dump(mem, f, indent=4, ensure_ascii=False)
            print("saving source user")
        with open('data/target_user.json', 'w', encoding='utf-8') as f:
            json.dump(mem2, f, indent=4, ensure_ascii=False)
            print("saving target user")
        with open('data/source_admin.json', 'w', encoding='utf-8') as f:
            json.dump(mem3, f, indent=4, ensure_ascii=False)
            print("saving admin user")
                
            # refresh hash acces for all accounts 
 