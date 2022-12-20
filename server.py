from flask import Flask, json, send_file
import threading
import time
import datetime


def DavidHasWokenUpLate():
    



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
        DavidHasWokenUpLate()
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

