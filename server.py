from math import floor
from flask import Flask, json, send_file
import threading
import time
from flask import request
import datetime
import os
from urllib.parse import urljoin
import bot
import awake
import random

# globalURL = "http://127.0.0.1:5000"
globalURL = "http://ec2-54-221-53-67.compute-1.amazonaws.com:5000/"
discordThread = threading.Thread(target=bot.main)
def onWakeup():
    global ticketsEnabled
    global currentTicketId
    currentTicketId = getRandomTicketID()
    ticketsEnabled = True
    ticketURL = globalURL + "/tickets/" + str(currentTicketId)
    return ticketURL

bot.setWakeupCallback(onWakeup)
discordThread.start()
getRandomTicketID = lambda: random.randint(100,100000)
currentTicketId = getRandomTicketID()
ticketsEnabled = True
##API
api = Flask(__name__)
@api.route("/awake", methods=["GET"])
def get_button_page():
    return send_file("index.html")

@api.route("/safe", methods=["GET"])
def safe():
    awake.wokeup = True
    return send_file("safe.html")

def parseHTML():
    f = open("ticket.html", "r")
    string = f.read()
    f.close()
    imageurl = request.url_root  + "/images/"+str(currentTicketId)
    print(imageurl)
   
    string = string.replace("REPLACEME", imageurl)
    nf = open("./output/parsed.html", "w+")
    nf.write(string)
    nf.close()
@api.route("/tickets/<int:idd>")
def tickets(idd):
    if idd == currentTicketId and ticketsEnabled:
        parseHTML()
        return send_file("output/parsed.html")
    else:
        return send_file("404.html")
@api.route("/images/<int:idd>")
def images(idd):
    if idd == currentTicketId and ticketsEnabled:
        parseHTML()
        return send_file("output/latest.png")
    else:
        return send_file("404.html")

@api.route("/reset/<int:idd>", methods=["GET"])
def reset(idd):
    global ticketsEnabled
    if idd == currentTicketId:
        print("RESET ALL TICKETS")
        ticketsEnabled = False
        return "0"
    else:
        return send_file("404.html")


if __name__ == "__main__":
    api.run()


