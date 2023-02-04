from pyromod import pyroadd

option = input('Login or Signup type one : ')
app = pyroadd('config.json')

if option.lower()[0] == 's':
    app.Signup('PAM-Signup', 'session')
elif option.lower()[0] == 'l':
    app.Login('PAM-Login', 'session', False)
