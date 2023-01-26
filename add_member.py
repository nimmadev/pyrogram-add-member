
import asyncio
from helper.class_pam import PAM
#option for choose username or id
option = input('choose method username or id: ').lower() 
app = PAM('config.json')
async def main():
    applist =await app.Login('PAM-Login', 'session', True)
    await app.add_member('PAM-AddMember', 'session', option, applist)

asyncio.run(main())
