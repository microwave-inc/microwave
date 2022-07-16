> This repo will no longer be maintained due to changes within pycord and discord.py 2.0 updates that have broken the bot
# Welcome to Microwave bot's official repo
Here you will find many things you can use for your bot, have an issue? shoot us an [email](mailto:microwave@microwavebot.tech) or open an issue

# "Important badges"

[![Contact us - microwave@microwavebot.tech](https://img.shields.io/badge/Contact_us-microwave%40microwavebot.tech-FFFFFF?logo=Mail.Ru&logoColor=000000)](mailto:microwave@microwavebot.tech "Contact us")
[![Organization - Microwave Inc.](https://img.shields.io/badge/Organization-Microwave_Inc.-white?logo=Github&logoColor=%233776AB)](https://github.com/microwave-inc "Our GitHub page")
#
[![py - >=3.7.0](https://img.shields.io/badge/py->=3.7-Green?logo=Python&logoColor=%233776AB)](https://python.org "Go to the Python homepage")
![Version](https://img.shields.io/badge/dynamic/json?label=Version&query=version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fmicrowave-inc%2Fmicrowave%2Fmaster%2Fconfig.json)
![License  - GPL 3.0](https://img.shields.io/badge/License_-GPL_3.0-blue)
#
[![Dependency's  - requirements.txt](https://img.shields.io/badge/Dependency's_-requirements.txt-blue?logo=Python&logoColor=%233776AB)](https://github.com/microwave-inc/microwave/blob/master/requirements.txt "Reqirements file")
#
[![issues](https://img.shields.io/github/issues/microwave-inc/microwave)](https://github.com/microwave-inc/microwave/issues)
![Maintained - yes](https://img.shields.io/badge/Maintained-yes-green)
![License - GPL 3.0](https://img.shields.io/badge/License-GPL_3.0-blue)

# Table Of Contents

- [TODO](#todo)
- [Dev's](#devs)
- [How to install](#how-to-install)
- [Badge Stuff](#badge-stuff)

# How to install
To install microwave bot just follow these simple steps!
```sh
git clone https://github.com/microwave/microwave.git
```
Now that we have cloned the repo we need to go into it

For windows:
```sh
cd C:\Users\your-user\path\to\folder
```
For linux:
```sh
cd ~/path/to/folder
```
Once inside you must do the following:
```python
pip3 install -r requirements.txt
```
Once you have finished all of that you can move onto the next step the ENV!

first create a file simply called .env in the root directory and then put this stuff (minus the comments) in the file
```py
TOKEN = #you will place your token here
APIKEY = #you can get the nasa api key from https://api.nasa.gov
```
And once you have finished setting up your .env file we can move on!

now we set up the config, to do this all we need to do is put the stuff you want inside so for example:
```json
{
  "join_message": "Microwave bot has arrived! use ``m!help`` for help \nand check out our website @ https://microwavebot.tech",
  "devperms": [
    "your_id_here"
  ],
  "devs": [
    "your_id_here"
  ],
  "trueowners": [
    "your_id_here"
  ],
  "prefix": [
    "m!",
    "customprefix!"
  ],
  "version": "vX.X.X",
  "lastupdate": "6/28/2022 10:42 PST",
  "changelog": "Updated readme.md"
}
```
Let me explain what the first 3 do (the rest are not hard to figure out on your own)

- "devperms" that is for the owner only commands
- "devs" that is for the info command
- "trueowners" that again is for the info command

Now for the real fun... Starting the bot for the first time!

simply do python (python3 for Linux) index.py (if you get a weird error you can ignore it, thats just flask being rude because something is using its port, why flask is used is for the main bot so it's uptime can be monitored)

Once it's running enjoy!

# Badge Stuff

[![stars - microwave](https://img.shields.io/github/stars/microwave-inc/microwave?style=social)](https://github.com/microwave-inc/microwave "Stars")
[![forks - microwave](https://img.shields.io/github/forks/microwave-inc/microwave?style=social)](https://github.com/microwave-inc/microwave "Forks")
#

