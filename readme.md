
# Pyrogram-Add-Member

This Project Let You add members from Your group to another group or supergroup.

This project is most optimised Telegram member adder.



![Logo](https://raw.githubusercontent.com/nimma0001/pyrogram-add-member/master/logo/20220918_025117_0000.png)


## Acknowledgements

 - [Pyrogram](https://github.com/pyrogram/pyrogram)



## Authors

- [@nimma](https://www.github.com/nimma0001)
- [@R5pro](http://t.me/R5pro)


## Deployment

- To deploy this project run you must have python3 installed and git
- use other command if first one give error 


```
Get Api_Id and Api_Hash From my.telegram.org
```
```bash
  git clone https://github.com/nimma0001/pyrogram-add-member
```
```
 RUN pip3 install -r requirements.txt or pip -r install requirments.txt 
```
Now We Will Add Account Which Will be Used For Adding 
```
RUN python3 make_config.py or python make_config.py
```
- first is number of account You have
- 2nd  and 3rd is group id it look like this 8272873688
- 4th and 5th is Group username like @r5pro
- 6th is last time user was online [6 option available] default to Long ago Check FAQ FOR THIS ONE
- 7, 8, 9 is phone number, api_id and api_hash
```
RUN python3 login.py or python login.py 
```
- Follow on screen instructions
- Don't use Bot token
```
RUN python3 get_data.py or python get_data.py
```
- this will extract 10k members from source group
- there are two option username or id 
- id will add more member but scraping take long
- username is best if you want to save time
```
RUN python3 add_member.py or python add_member.py
```
- member adding has started
- there two option username/id
- choose what you picked above
- dont missmatch pick it will give erros

## Features

- Faster speed
- skip admins
- skip bot
- add by username or id
- auto save last count
- Better Error Handling 
- auto_make config
- Unlimited account
- Account are used with sync so less wait time
- Cross platform
- First open source add member written in pyrogram 


## Support

For support, [@R5pro](http://t.me/R5pro) on Telegram

Or join [@pyrogram-add-member](https://t.me/pyrogram_add_member)


## FAQ

#### How Many Member 20 Account can add?

600 - 1000 Member daily

#### How Many Account are recommended 

I will Suggest 15 but depends on ur biggest

Buy account from : [@R5pro](http://t.me/R5pro) on Telegram

Check @spambot on Telegram if ur account is limited

#### 6th point from deployment

option are
```
 UserStatus.LONG_AGO
 UserStatus.LAST_MONTH
 UserStatus.LAST_WEEK
 UserStatus.OFFLINE
 UserStatus.RECENTLY
 UserStatus.ONLINE
 ```
 6th option add user who are online and 1st add all the user

other should be clear from name

#### Is There a Paid version Available?

Yes

#### My Etc wallet address

0x9de7da7f7c578ab43446edef5405d88509694b34
