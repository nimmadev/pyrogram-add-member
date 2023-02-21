from pyroadd import pyroadd
import asyncio
#option for choose username or id
option = input('choose method username or id: ').lower() 
app = pyroadd('config.json')
# async def add():
#     applist =await app._login('PAM-Login', 'session', True)
#     await app._add_member('PAM-AddMember', 'session', option, applist)

# asyncio.run(add())
app.add_member('PAM-AddMember', 'session', option)
