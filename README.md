DJTwitch
==================
http://djtwitch.org/main.html

Files
* DJTwitch.py - the main app python file
* settings.txt - the config for the app

![preview](https://cloud.githubusercontent.com/assets/4276174/2560345/7faf0208-b7c0-11e3-8bcd-fff2304468b8.png)


Settings.txt
=============
[Settings]

HOST = irc.twitch.tv (you can put other irc servers as well)

PORT = 6667

AUTH = oauth:###################### (get it from http://twitchapps.com/tmi/)

USERNAME = username

CHAT_CHANNEL = channelname (This most likely will be your username. Unless you are using other irc servers)

Modules Required (Only required when running .py)
================
* vlc - https://wiki.videolan.org/Python_bindings/
* grooveshark - http://koehlma.github.io/projects/pygrooveshark.html
* PyQt4 - http://www.riverbankcomputing.com/software/pyqt/download (PyQt4-4.10.4)
