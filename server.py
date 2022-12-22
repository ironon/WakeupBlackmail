from math import floor
from flask import Flask, json, send_file
import threading
import time
import datetime
import os
import random
r = lambda: random.randint(0,255)

subtitles = ["asdjhsdgfdfhg", "frick", "fudge", "there are so many david tickets out there holy crap"]
descriptions = ["david needs to wake up", "sleephyhead daivd", "jlsdhfsdiufdsf did i really just give away a ticket because i SLEPT"]

def getSubtitle():
    return subtitles[floor(random.random() * len(subtitles))]
def getDesc():
    return descriptions[floor(random.random() * len(descriptions))]

def heWokeUpLate():
    ## color subtitle desc
    color = '#%02X%02X%02X' % (r(),r(),r())
    # color = "orange"
    os.system("node ticket \"" + getSubtitle() + "\" \"" + getDesc() + "\" \"" + color + "\"")



wakeup = datetime.time(hour=20,minute=2,second=0,microsecond=0)
wokeup = False
lastKnownDate = datetime.datetime.now().date().day
##CLOCK
def isNewDay():
    global lastKnownDate
    currentDay = datetime.datetime.now().date().day
    if lastKnownDate != currentDay:
        lastKnownDate = currentDay
        return True
    return False

def deadlock():
    now = datetime.datetime.now().time()
    global wokeup
    isPastWakeup = now > wakeup
    if isPastWakeup and not wokeup:
        wokeup = True
        print("HE WOKE UP LATE!")
        heWokeUpLate()
    if isNewDay():
        wokeup = False
    time.sleep(3)
    deadlock()
thread = threading.Thread(target=deadlock)
thread.start()

##API
api = Flask(__name__)
@api.route("/", methods=["GET"])
def get_button_page():
    return send_file("index.html")

@api.route("/safe", methods=["GET"])
def safe():
    wokeup = True
    return send_file("safe.html")

if __name__ == "__main__":
    api.run()

