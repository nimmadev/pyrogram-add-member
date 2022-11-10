
# Pyrogram-Add-Member

This Project Let You add members from Your group to another group or supergroup.

This project is most optimised Telegram member adder.



![Logo](https://raw.githubusercontent.com/nimma0001/pyrogram-add-member/master/logo/20220918_025117_0000.png)


## Acknowledgements

 - [Pyrogram](https://github.com/pyrogram/pyrogram)

 - [addmember-telegram](https://github.com/south1907/addmember-telegram)

## Authors

- [@nimmadev](https://www.github.com/nimmadev)
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
- first  id of group you want to scrap
- second id of ur group
- source username is the link or username of group you want to scrap
- target username is the link or username of your group
- if you have api_id and hash for ur numbers type YES otherwise 

# For NO
if you did not add number in phone.csv you will be asked for 
how many numbers you want to add
- first add ur phone numbers in phone.csv (optional)
- type the number one by one with country code example 918571000000 [91 is my country code] (only required if you did not fill phone.csv)
# For YES
-  enter number of account you want to add example: 10 or 5
-  enter ur number with country code example 918571000000 [91 is my country code]
-  enter ur api id. get from https://my.telegram.org/auth
-  enetr ur api hash. get from https://my.telegram.org/auth


### AutoJoin and SpamCheck accepts [True/false] editable in  config.py after you run make_confg.py

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

- faster get_data.py in donation version
- unlimited scraping of members in donation version
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


## Support or donation 

For donation version files, [@R5pro](http://t.me/R5pro) on Telegram

Or help and support [@pyrogram-add-member](https://t.me/nimmadev)


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
