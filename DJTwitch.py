import string
import sys
import os
import socket
from grooveshark import Client
from grooveshark.classes.song import Song
import subprocess
import vlc
import ConfigParser
import threading
import time
from PyQt4 import QtGui, QtCore


global whovoted
whovoted=[]
global currentsongname
currentsongname="None Playing. Please vote with !DJ"
global top10song
top10song = []
global playing
playing = 0
global player

class Example(QtGui.QMainWindow):
        
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setMaximum(100)
        sld.setValue(100)
        sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setGeometry(140, 110, 300, 30)
        sld.valueChanged[int].connect(volume)

        lcd = QtGui.QLCDNumber(self)
        lcd.setGeometry(140, 50, 100, 50)
        sld.valueChanged.connect(lcd.display)

        global lcdsn
        lcdsn = QtGui.QLabel(currentsongname, self)
        lcdsn.setGeometry(140, 0, 300, 50)
        
        global playb
        playb = QtGui.QPushButton('Play', self)
        playb.setCheckable(True)
        playb.move(10, 10)
        playb.clicked.connect(playbt)
        
        global pauseb
        pauseb = QtGui.QPushButton('Pause', self)
        pauseb.setCheckable(True)
        pauseb.move(10, 60)
        pauseb.clicked.connect(pausebt)

        global skipb
        skipb = QtGui.QPushButton('Skip', self)
        skipb.setCheckable(True)
        skipb.move(10, 110)
        skipb.clicked.connect(skipbt)
        
        self.setGeometry(300, 500, 500, 150)
        self.setWindowTitle('DJ Twitch')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:#kills everything when escape is hit
            global player
            try:
                player.release()
            except:
                pass
            self.close()
            exit()
    
def nameupdate():
    global lcdsn
    global currentsongname
    lcdsn.repaint()
    lcdsn.setText(QtCore.QString(currentsongname))
    
def volume(slide_var):
    global player
    player.audio_set_volume(slide)
    
def playbt(playbt_var):
    global playb
    global player
    playb.toggle()
    player.play()
    
def pausebt(pausebt_var):
    global pauseb
    global player
    pauseb.toggle()
    player.pause()
    
def skipbt(skipbt_var):
    global skipb
    global player
    skipb.toggle()
    player.stop()

def gui():    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

def find(songname):
    client = Client()
    client.init()
    songs = []
    print "start search"
    for song in client.search(songname, Client.SONGS):
        songs.append(song)
    if songs:
        return songs[0]

def play(SongUrl):
    global playing
    playing = 1
    instance=vlc.Instance()
    media=instance.media_new(SongUrl)
    global player
    player=instance.media_player_new()
    player.set_media(media)
    player.play()
    print "play"
    global player_events
    player_events=player.event_manager()
    player_events.event_attach(vlc.EventType.MediaPlayerEndReached, SongFinished, 1)
    player_events.event_attach(vlc.EventType.MediaPlayerStopped, SongFinished, 1)
    global foreverstart
    foreverstart = 1
        

@vlc.callbackmethod    
def SongFinished(self, data):
    print "SONG IS OVER"
    global playing
    playing = 0
    global currentsongname
    currentsongname = "Playing None"
    nameupdate()
    player_events.event_detach(vlc.EventType.MediaPlayerEndReached)
    player_events.event_detach(vlc.EventType.MediaPlayerStopped)


def vote(votedsong):
    voted = 0
    global top10song
    for songelement in top10song:
        if votedsong.name == songelement[0]:
            songelement[1] = votedsong.stream.url
            songelement[2] = songelement[2] + 1
            voted = 1
        if voted:
            break
    if voted == 0:
        top10song[9][0] = votedsong.name.encode('ascii','ignore')
        top10song[9][1] = votedsong.stream.url
        top10song[9][2] = 1
    sortvoting()

def sortvoting():
    global top10song
    for i in range(0,9):
        if (top10song[9-i][2] > top10song[9-i-1][2]):
            holder = top10song[9-i]
            top10song[9-i] = top10song[9-i-1]
            top10song[9-i-1] = holder
    for i in range(0,10):
        print str(i+1) + ". " + "(" + str(top10song[i][2]) + ") " + top10song[i][0] 

def djtwitchPlay():
    while True:
        time.sleep(2)
        global top10song
        if top10song[0][2] >=1:
            if playing ==0:
                print "Loading next song in queue..."
                global s
                s.send(bytes("PRIVMSG #%s : Now Playing... %s (%d)\r\n" % (CHAT_CHANNEL, str(top10song[0][0]), top10song[0][2])))
                threadurl = top10song[0][1]
                global currentsongname
                currentsongname = top10song[0][0]
                if thread2.is_alive():
                    nameupdate()
                play(threadurl)
                global whovoted
                del whovoted[:]
                top10song[0] = ["","",0]
                sortvoting()
                
for i in range(0,10):
    top10song.append(["","",0])

if os.path.isfile("settings.txt"):
    config = ConfigParser.ConfigParser()
    config.read("settings.txt")
    HOST = config.get('Settings', 'HOST')
    PORT = config.getint('Settings', 'PORT')
    AUTH = config.get('Settings', 'AUTH')
    NICK = config.get('Settings', 'USERNAME').lower()
    global CHAT_CHANNEL
    CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()

global s
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("connected")
s.send(bytes("PASS %s\r\n" % AUTH))
s.send(bytes("NICK %s\r\n" % NICK))
s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK)))
s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL));
s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL))
print("Sent connected message to channel %s" % CHAT_CHANNEL)

readbuffer = ""

thread = threading.Thread(target = djtwitchPlay)
thread.start()

thread2 = threading.Thread(target = gui)
thread2.start()
while 1:
            
    readbuffer = readbuffer+s.recv(1024)
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        x = 0
        out = ""
        line=string.rstrip(line)
        line=string.split(line)

        for index, i in enumerate(line):
            if x == 0:
                user = line[index]
                user = user.split('!')[0]
                user = user[0:12] + ": "
            if x == 3:
                out += line[index]
                out = out[1:]
            if x >= 4:
                out += " " + line[index]
            x = x + 1
            
        if user == "PING: ":
            #s.send(bytes("PONG tmi.twitch.tv\r\n"))
            print line
            s.send(bytes(str("PONG " + line[1][1:] + "\r\n")))
        elif user == ":tmi.twitch.tv: ":
            pass
        elif user == ":tmi.twitch.: ":
            pass
        elif user == ":%s.tmi.twitch.tv: " % NICK:
            pass
        else:
            try:
                print(user + out)
            except UnicodeEncodeError:
                print(user)
        
        if out and not out.isspace() and out[0] == "!":
            command = out.lower().split()[0]
            if command == '!ping':
                print "PONG!\n"
                s.send(bytes("PRIVMSG #%s :PONG\r\n" % CHAT_CHANNEL))
            if command == '!dj':
                alreadyvoted = 0
                for names in whovoted:
                    if user == names:
                        alreadyvoted = 1
                        print user, "already voted"
                if alreadyvoted == 0:
                    print "hasn't voted yet"
                    out = out[4:]
                    if out:
                        votedsong = find(out)
                        if votedsong:
                            print "song found"
                            whovoted.extend([user])
                            vote(votedsong)
                            output = votedsong.name.encode('ascii', 'ignore')
                            print "Voted", output
                        else:
                            print "song not found :("


    
                
