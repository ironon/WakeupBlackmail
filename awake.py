
import os
import datetime
import time
from math import floor
import random


subtitles = ["asdjhsdgfdfhg", "frick", "fudge", "there are so many david tickets out there holy crap"]
descriptions = ["david needs to wake up", "sleephyhead daivd", "jlsdhfsdiufdsf did i really just give away a ticket because i SLEPT"]

def getSubtitle():
    return subtitles[floor(random.random() * len(subtitles))]
def getDesc():
    return descriptions[floor(random.random() * len(descriptions))]


def heWokeUpLate():
    global wokeup
    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    wokeup = True
    print("Punishing..")
    os.system("node ticket \"" + getSubtitle() + "\" \"" + getDesc() + "\" \"" + color + "\"")




wakeup = datetime.time(hour=7,minute=0,second=0,microsecond=0)
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

def heIsNotAwakeButHeShouldBe():
    now = datetime.datetime.now().time()
    global wokeup
    isPastWakeup = now > wakeup
    if isPastWakeup and not wokeup:
        wokeup = True
        print("HE WOKE UP LATE!")
        return True
    if isNewDay():
        wokeup = False
    return False