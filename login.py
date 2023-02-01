from pyroadd import pyroadd

option = input('Login or Signup type one : ')
app = pyroadd('config.json')

if option.lower()[0] == 'l':
    app.Signup('PAM-Signup', 'session')
elif option.lower()[0] == 's':
    app.Login('PAM-Login', 'session', False)
