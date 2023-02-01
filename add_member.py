from pyroadd import pyroadd
#option for choose username or id
option = input('choose method username or id: ').lower() 
app = pyroadd('config.json')
app.Login('PAM-Login', 'session', True)
app.add_member('PAM-AddMember', 'session', option, applist)
