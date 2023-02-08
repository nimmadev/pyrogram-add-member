from pyroadd import pyroadd
#workdir = 'session/'
method = input('choose method username or id: ').lower()
app = pyroadd('config.json')
app.get_data('PAM-GetData', 'session', method)


