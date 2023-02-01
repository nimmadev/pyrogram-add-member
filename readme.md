
# Pyrogram-Add-Member

This Project Let You add members from Your group to another group or supergroup.

This project is most optimised Telegram member adder.



![Logo](https://raw.githubusercontent.com/nimma0001/pyrogram-add-member/master/logo/20220918_025117_0000.png)


## Acknowledgements

 - [Pyrogram](https://github.com/pyrogram/pyrogram)

 - [addmember-telegram](https://github.com/south1907/addmember-telegram)

## Authors

- [@nimmadev](https://www.github.com/nimmadev)
- [@P5pro](http://t.me/P5pro)


## Deployment

- To deploy this project run you must have python3 installed and git
use another command if first one gives an error 


```
Get Api_Id and Api_Hash From my.telegram.org [optional]
```
#
### clone repo
```bash
  git clone https://github.com/nimmadev/pyrogram-add-member
```
#
### Install required dependencies
```
 pip3 install -r requirements.txt or pip -r install requirments.txt 
```
#
### make Config
```python
python make_config.py
```
check config.example.json for configurations
#
### login
```
python3 login.py or python login.py 
```
#
### Scrapping members
```
python3 get_data.py or python get_data.py
```
- this will extract 10k members from source group
- there are two options username or id 
- id will add more member but scraping take long
- username is best if you want to save time

#
### Add members
```
python3 add_member.py or python add_member.py
```
- member adding has started
- there two option username/id
- choose what you picked above
- don`t miss match pick it will give errors
  
<br>

## Features
### GitHub Version
- 10k members scraping 
- Faster speed
- skip admins
- skip bot
- auto check spambot
- add by username or id
- auto save last count
- Better Error Handling 
- auto_make config
- Unlimited account
- Account are used with sync so less wait time
- Cross platform
- First open source add member written in pyrogram 

### Premium Version
- all from GitHub
- scrap full group not just 10k
- 40-80 times faster
- use parallel get_data
- scraps contacts and save in .CSV file
- Setup help contact @P5pro on telegram 


## Support or donation 

For Premium version it's 40USD [US] Contact, [@P5pro](http://t.me/P5pro) on Telegram

Or help and support [@pyrogram-add-member](https://t.me/nimmadev)


## FAQ

#### How Many Member 20 Account can add?

600 - 1000 Member daily

### Error on login.py

use correct username for channel

### Error on get_data.py
raise an issue or use telegram support

### How Many Accounts are recommended 

I will Suggest 15 but depends on ur biggest

Buy account from : [@P5pro](http://t.me/P5pro) on Telegram

Check @spambot on Telegram if ur account is limited

#### 6th point from deployment

option is
```
 UserStatus.LONG_AGO - User was seen long ago
 UserStatus.LAST_MONTH - User was seen last month
 UserStatus.LAST_WEEK - User was seen last week
 UserStatus.OFFLINE - User is offline
 UserStatus.RECENTLY - User was online recently
 UserStatus.ONLINE - User is online
 ```
 6th option add user who are online and 1st add all the user

other should be clear from name

#### Is There a Paid version Available?

Yes it's called donation version 

#### My ETH wallet address

0x9de7da7f7c578ab43446edef5405d88509694b34

## Contributing:

* Fork the repo on Github

* Clone the repo using `git clone addmember-telegram`

* Make changes and stage the files: `git add .`

* Commit the changes: `git commit -m "Changed a few things"`

* Push the changes to your Github repo: `git push -u origin main`

* Submit a pull request.

* Don't add feature writen in donation

* Don't sell the code 😅😡
