<img src="https://royalproductions.xyz/images/serverquery/ServerQueryV4.5.png"></img>
# ServerQuery
ServerQuery is a Discord.py bot designed to query game servers that use A2S (Valve Query API), FiveM, Minecraft, and SAMP. This bot provides server and player information, making it an excellent tool for discord server owners who hosts dedicated servers who wants to display server and player information in a fully customizable but beautifully designed way!

Quick Links:<br>
[Requirement](https://github.com/ihasTaco/ServerQuery#requirements)<br>
[Setup](https://github.com/ihasTaco/ServerQuery#setup)<br>
[Known Bugs](https://github.com/ihasTaco/ServerQuery#known-bugs)<br>
[Coming Soon](https://github.com/ihasTaco/ServerQuery#coming-soon)<br>
[Supported Games](https://github.com/ihasTaco/ServerQuery#supported-games)<br>
[License](https://github.com/ihasTaco/ServerQuery#license)<br>

# What's New
* Stability - this was an issue from my [last bot], and from the start, I aimed to make it as stable as possible
* JSON Support - I wanted to use something that was easy to setup straight from the beginning, so all server info & customization is stored in a JSON file for easy access
* Easy Module Installation - The script will take care of most of the installation!
* You can now add/edit/delete servers right inside the script!
* Server Specific Customization - again an issue that I saw with my [last bot] was that it lacked specific server customization, so this was an issue that I was looking to fix in this bot!
* More Customization - now you can finally customize everything in the embed!
    - Change Color of the Embed
    - Set Thumbnail URL
    - Set Footer Text and URL
    - Title
      1. Use Config Name
      2. Use Server Name
      3. Use Custom Name
    - Description
      1. Disable
      2. Show Steam Quick Connect Link
      3. Use Custom Description
    - Fields
      - Enable/Disable every field and reorder them
    - Players
      - Enable/Disable Player Names
    - Graph
      - Enable/Disable Player Graph
      - Title
        - Use a Custom Title for the graph
        - Change Color of the title
      - Labels & Tick Marks
        - Use custom Labels for X & Y axis
        - Change the colors of the Labels
        - Change the color of the Tick Marks
      - Graph Lines
        - Player Count
          - Change Color of Online Player Line
          - Enable/Disable Online Player Fill
          - Change the color of the Online Player Fill
        - Trend Line
          - Enable/Disable Player Trend Line
          - Change the color of the Player Trend Line
      - Grid
        - Enable/Disable Grid Lines
        - Change Color of the Grid Lines
        - Set Opacity of the Grid Lines
      - Legend
        - Enable/Disable the Legend
        - Change Color of the Legend Background and the Legend border
        - Set Opacity of the Legend
    And this can be customized for every server
* Logging System
* Notifications for Server Status Change

# Requirements
ServerQuery requires the following Python libraries to function correctly:

* python-a2s<br>
* mcstatus<br>
* requests<br>
* fivempy<br>
* samp_client<br>
* discord<br>
* fuzzywuzzy - For the check_api search function<br>
* matplotlib<br>

The script will install any missing and necessary libraries automatically.

# Setup
Before you can use ServerQuery, make sure you have Python and pip installed on your machine. You can download Python from the official website and install it on your computer. <br>

Once installed, you can check if pip is installed with the following command:<br>
`python -m ensurepip --upgrade`


Next, clone the repository:<br>
```git clone https://github.com/ihasTaco/ServerQuery/```

Don't Forget to set the Graph Image Dump Guild/Channel ID's and Status Change Notification Guild/Channel ID's as well as add your bot token!
After that, you can run the bot by executing the following command:<br>
Note: there is no need to install the requirements as they will be installed on first run of the script below!
```python module_checker.py```

**Don't Forget** the bot requires these permissions in the server channels to work correctly:
* View Channel
* Send Messages
* Embed Links
* Read Message History

# Known Bugs
* Currently there aren't any known bugs in ServerQuery, if you find one please submit an issue!

# Coming Soon
* Organizing and cleaning up code ***(Currently In Progress)***
* Ability to import/export server customization configs - for faster server customization ***(Currently In Progress)***
* MariaDB/MySQL Database support - at this time the script is running off of a JSON file for all server information and customization, but I will be adding db support soon
* Dashboard - I want to make a django dashboard that will allow you to go to your localhost address (127.0.0.1:8000) and be able to customize and manage servers from there
* Add settings for notifications for each server, including ability to Enable/Disable, set guild/channel id, and set title 

And here is some query api's and games support that I will want to add eventually
* ASE
* GameSpy 1, 2, & 3
* Doom 3
* Nadeo
* Quake 2, & 3
* Unreal 2
* RageMP
* Terrarria
* Roblox
* Teamspeak

# Supported Games
Here is the list of games that *SHOULD* be supported. <br>
I added a Tested section, if that has an :x:, there is a slim chance that it may not be able to be queried or server/player info may not work! (but it should work fine) <br>

But, if you test out a server that hasnt been tested yet, please submit a pull request and I will update the list! <br>
Same thing for games that aren't on the list
If you do decide to test a server, and it doesn't work as expected please submit an issue, and I will look into the issue!

If you find a game that isn't on the list, please let me know!


|                  Game                 |                    App ID                     |     API     |       Tested       |    Server Info     |    Player Info    |
|---------------------------------------|:---------------------------------------------:|:-----------:|:------------------:|:------------------:|:-----------------:|
| 7 Days to Die                         | [251570](https://steamdb.info/app/251570/)    | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Age of Chivalry                       | [17510](https://steamdb.info/app/17510/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Alien Swarm                           | [630](https://steamdb.info/app/630/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| America's Army 3                      | [13140](https://steamdb.info/app/13140/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| America's Army: Proving Grounds       | [203290](https://steamdb.info/app/203290/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| ARK: Survival Evolved                 | [346110](https://steamdb.info/app/346110/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Armed Assualt 2: Operation Arrowhead  | [33930](https://steamdb.info/app/33930/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Armed Assault 2: DayZ Mod             | [224580](https://steamdb.info/app/224580/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Armed Assualt 3                       | [107410](https://steamdb.info/app/107410/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Battalion Legacy                      | [489940](https://steamdb.info/app/489940/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Brink                                 | [22350](https://steamdb.info/app/22350/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Call of Duty: Modern Warfare 3        | [115300](https://steamdb.info/app/115300/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Conan Exiles                          | [440900](https://steamdb.info/app/440900/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Counter-Strike 1.5                    | [--](## "I don't know what game this uses, so if someone knows more about cs 1.5, please edit this and submit a pull request")                                            | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Counter Strike 1.6                    | [--](## "I don't know what game this uses, so if someone knows more about cs 1.6, please edit this and submit a pull request")                                            | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Counter-Strike 2D                     | [666220](https://steamdb.info/app/666220/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Counter-Strike: Condition Zero        | [80](https://steamdb.info/app/80/)            | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Counter-Strike: Global Offensive      | [730](https://steamdb.info/app/730/)          | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Counter-Strike: Source                | [240](https://steamdb.info/app/240/)          | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Dark and Light                        | [529180](https://steamdb.info/app/529180/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| DayZ Standalone                       | [221100](https://steamdb.info/app/221100/)    | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Day of Defeat                         | [30](https://steamdb.info/app/30/)            | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Day of Defeat: Source                 | [300](https://steamdb.info/app/300/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Days of War                           | [454350](https://steamdb.info/app/454350/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Empyrion - Galactic Survival          | [383120](https://steamdb.info/app/383120/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Fortress Forever                      | [253530](https://steamdb.info/app/253530/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Garry's Mod                           | [4000](https://steamdb.info/app/4000/)        | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| GRAV Online                           | [332500](https://steamdb.info/app/332500/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Grand Theft Auto San Andreas (SAMP)   | [12120](https://steamdb.info/app/12120/)      | SAMP_Client | :white_check_mark: | :white_check_mark: | :x:
| Grand Theft Auto V (FiveM)            | [271590](https://steamdb.info/app/271590/)    | FiveMPy     | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Half-Life: Deathmatch                 | [360](https://steamdb.info/app/360/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Half-Life 2: Deathmatch               | [320](https://steamdb.info/app/320/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Half Life 2: Synergy Mod              | [17520](https://steamdb.info/app/17520/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Homefront                             | [55100](https://steamdb.info/app/55100/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Insurgency                            | [222880](https://steamdb.info/app/222880/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Just Cause 2 Multiplayer              | [259080](https://steamdb.info/app/259080/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Killing Floor 2                       | [232090](https://steamdb.info/app/232090/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Left 4 Dead                           | [500](https://steamdb.info/app/500/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Left 4 Dead 2                         | [550](https://steamdb.info/app/550/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Minecraft (Java)                      | --                                            | MCStatus    | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Minecraft (Bedrock)                   | --                                            | MCStatus    | :white_check_mark: | :white_check_mark: | :x:
| Natural Selection                     | [120](https://steamdb.info/app/120/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Natural Selection 2                   | [4920](https://steamdb.info/app/4920/)        | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| PixARK                                | [593600](https://steamdb.info/app/593600/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Quake Live                            | [282440](https://steamdb.info/app/282440/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Red Dead Redemption 2 (RedM)          | [1174180](https://steamdb.info/app/1174180/)  | FiveMPy     | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Red Orchestra 2: Heroes of Stalingrad | [43350](https://steamdb.info/app/35450/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Rising Storm                          | [234510](https://steamdb.info/app/234510/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Rust                                  | [252490](https://steamdb.info/app/252490/)    | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Shattered Horizon                     | [18110](https://steamdb.info/app/18110/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Starbound                             | [211820](https://steamdb.info/app/211820/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Space Engineers                       | [244850](https://steamdb.info/app/244850/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Squad                                 | [393380](https://steamdb.info/app/393380/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Team Fortress Classic                 | [20](https://steamdb.info/app/20/)            | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Team Fortress 2                       | [440](https://steamdb.info/app/440/)          | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| The Forest                            | [242760](https://steamdb.info/app/242760/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| The Ship                              | [383790](https://steamdb.info/app/383790/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Unturned                              | [304930](https://steamdb.info/app/304930/)    | A2S         | :white_check_mark: | :white_check_mark: | :white_check_mark:
| Wurm Unlimited                        | [366220](https://steamdb.info/app/366220/)    | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Zombie Master                         | [90047](https://steamdb.info/app/90047/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:
| Zombie Panic: Source                  | [17500](https://steamdb.info/app/17500/)      | A2S         | :x:                | :white_check_mark: | :white_check_mark:

# License
ServerQuery is released under the MPL 2.0 license
