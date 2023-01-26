import asyncio
from helper.class_pam import PAM
#workdir = 'session/'
method = input('choose method username or id: ').lower()
app = PAM('config.json')
async def main():
     await app.get_data('PAM-GetData', 'session', method)

asyncio.run(main())

