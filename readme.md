> [!IMPORTANT]
> We have just moved to pycord so follow the new instructions listed in [How To Install](#how-to-install)
# Welcome to Microwave bot's official repo
Here you will find many things you can use for your bot, have an issue? shoot us an [email](mailto:help@microwavebot.tech) or open an issue

# Table Of Contents

- [TODO](#todo)
- [Dev's](#devs)
- [How to install](#how-to-install)
- [Badge Stuff](#badge-stuff)

# TODO 

- N/A

# Dev's

Founder/Head of Bot Development [Galaxine](https://github.com/galaxine-senpai)

Assistant Head of Bot Development [Fonta22](https://github.com/Fonta22)

Bot Developer [yapudjus](https://github.com/yapudjus)

Bot Developer [Sopy](https://github.com/sopyb)

# How to install
To install microwave bot just follow these simple steps!
```sh
git clone https://github.com/galaxine-senpai/microwave.git
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
#pip3 should work on all OS's
pip3 install discord
#this gets it ready for pycord
pip3 uninstall discord.py
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
    "m!"
  ],
  "activity": "m!help | https://microwavebot.tech/team",
  "activity_type": "listening",
  "status_type": "online",
  "version": "2.0.0",
  "lastupdate": "<t:1649652060:f> (<t:1649652060:R>)",
  "playing": "m!help | https://microwavebot.tech"
}
```
Let me explain what the first 3 do (the rest are not hard to figure out on your own)

- "devperms" that is for the owner only commands
- "devs" that is for the info command
- "trueowners" that again is for the info command

Now for the real fun... Starting the bot for the first time!

simply do python3 index.py (if you get a weird error you can ignore it, thats just flask being rude because something is using its port, why flask is used is for the main bot so it's uptime can be monitored)

Once it's running enjoy!

# Badge Stuff

![Discord Bots](https://top.gg/api/widget/867964961417203743.svg) 

[click here for top.gg page](https://top.gg/bot/867964961417203743)
