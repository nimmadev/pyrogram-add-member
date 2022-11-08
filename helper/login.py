
async def login(phone, api_id, api_hash, auto_join, group_target_id, group_source_id):
    async with Client(phone, api_id, api_hash, workdir='session')as app:
        if await app.get_me():
            print(phone, 'is logined')
            if auto_join is True:
                try:
                    await app.join_chat(group_source_id)
                except BaseException as e:
                     print(phone,' number is already in group or join manually for group source' )
                try:
                    await app.join_chat(group_target_id)
                except BaseException as e:
                    print(phone,' number is already in group or join manually for group target')
            else:
                print('auto join is off check config')
        else:
            print(phone, 'login failed')
