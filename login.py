import asyncio
from helper.class_pam import PAM

option = input('Login or Signup type one : ')
app = PAM('config.json')
async def createall():
    await app.Signup('PAM-Signup', 'session')
async def loginall():
    await app.Login('PAM-Login', 'session', False)
if option.lower()[0] == 'l':
    asyncio.run(loginall())
elif option.lower()[0] == 's':
    asyncio.run(createall())
