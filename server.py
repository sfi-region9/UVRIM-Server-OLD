import glob
import sys
import os
import threading
import time
import codecs
import json
from datetime import datetime

from flask import Flask, request, send_file, make_response
from pymessenger.bot import Bot


class Verif(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print("Launch Automatic Verification")
            print("Rev")
            if os.path.exists("/home/servs/saves/lastsentmessage.save"):
                verification()
            time.sleep(6 * 3600)


app = Flask(__name__)
ACCES_TOKEN = "TOKEN"
ID = "CO_ID"
VERIFY_TOKEN = "This_Is_A_Token_@"
bot = Bot(ACCES_TOKEN)


def getAll():
    return ""


# SAVE IN /home/servs/saves/<SCC>.<NAME>.uvrim


def test():
    bot.send_text_message(ID, "Test#01")


@app.route("/", methods=['GET', 'POST'])
def receive():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verif(token_sent)
    if request.method == 'POST':
        output = request.get_json();
        print(str(output))
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    fichier = open("saves/log.l", "w")
                    fichier.write(recipient_id + "\n")
                    fichier.flush()
                    fichier.close()
                    return 'Done'


@app.route("/submit", methods=['POST'])
def d():
    if request.method == 'POST':
        ob = request.get_json()
        return save_uvrim(ob['scc'], ob['name'], ob['uvrim'])


@app.route("/latest.jar")
def lsercs():
    return send_file("/home/servs/versions/latest/UAS_V." + erLa() + ".jar")


@app.route("/start_auto")
def start_auto():
    t = Verif()
    t.start()
    return "true"


@app.route("/user_register", methods=['POST'])
def ref():
    if request.method == 'POST':
        objec = request.get_json()
        register_user(objec['scc'], objec['name'])
        return "Test"


@app.route("/is_sent", methods=['GET'])
def e():
    if request.method == 'GET':
        return str(isSent())


@app.route("/hello")
def sle():
    return "Hello World"


@app.route("/get_latest")
def sler():
    return erLa()


def verif(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"


def register_user(scc, name):
    if os.path.exists("/home/servs/saves/" + scc + "." + name + ".uvrim"):
        print("exist")
    else:
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "x", encoding="utf-8")
        fichier.close()


def save_uvrim(scc, name, uvrim):
    if not os.path.exists("/home/servs/saves/" + scc + "." + name + ".uvrim"):
        return "Error"
    else:
        os.remove("/home/servs/saves/" + scc + "." + name + ".uvrim")
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "x", encoding="utf-8")
        fichier.close()
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "w", encoding="utf-8")
        fichier.write(uvrim)
        fichier.flush()
        fichier.close()
        verification()
    return "save success"


# LATEST V /home/servs/versions/UAS_V.<VERSION>.<NAME>.jar
def erLa():
    print("get_latest")
    la = ""
    for files in glob.iglob("/home/servs/versions/latest/*.jar"):
        la = os.path.basename(open(files).name)
    la = la.replace("UAS_V.", "")
    la = la.replace(".jar", "")
    return la;


def verification():
    print("Verif")
    # TODO: VERIFY DATE AND SEND ALL UNSEND UVRIMS
    if isSent():
        return False
    # SENT ALL UVRIMS
    day = datetime.now().day;
    if day == 30:
        print("envoi")
        list = []
        for files in glob.iglob("/home/servs/saves/*.uvrim"):
            list.append(open(files).read())
        for st in list:
            bot.send_text_message(ID, st)
            time.sleep(10)
        remake()
        remake_files()
        return True
    else:
        return False


@app.route('/manual_launch')
def manual_launch():
    print("envoi")
    list = []
    for files in glob.iglob("/home/servs/saves/*.uvrim"):
        list.append(open(files).read())
    for st in list:
        bot.send_text_message(ID, st)
        time.sleep(10)
    remake()
    return True


def isSent():
    if not os.path.exists("/home/servs/saves/lastsentmessage.save"):
        open("/home/servs/saves/lastsentmessage.save", "x")
        return False
    else:
        now = datetime.now()
        month = now.month  # CURRENT NOW
        m = open("/home/servs/saves/lastsentmessage.save", "r").read()  # SAVE MOUNTH
        i = int(m)
        if month == i:
            return True
        if month > i:
            return False
        if month < i:
            return False


@app.route('/syncronize', methods=['POST'])
def syncronize():
    arr = request.get_json();
    scc = arr['scc'];
    name = arr['name']

    if not os.path.exists("/home/servs/saves/" + scc + "." + name + ".uvrim"):
        return "Error";

    array = [];
    with open("/home/servs/saves/" + scc + "." + name + ".uvrim") as file:
        isf = 0;
        for line in file:
            if isf == 0 or isf == 1:
                continue;
            array.append(line);
            isf += 1;
    print(array.count())
    s = "\\n";

    return str(array);


def remake():
    if not os.path.exists("/home/servs/saves/lastsentmessage.save"):
        return False
    else:
        toWrite = str(datetime.now().month)
        os.remove("/home/servs/saves/lastsentmessage.save")
        fichier = open("/home/servs/saves/lastsentmessage.save", "x")
        fichier.close()
        fichier = open("/home/servs/saves/lastsentmessage.save", "w")
        fichier.write(toWrite)
        fichier.flush()
        fichier.close()
        return True


def remake_file(file):
    path = os.path.abspath(file)
    name = os.path.basename(path)
    name = name.replace(".uvrim", "")
    s = name.split(".")
    os.remove(path)
    fichier = open(path, "x")
    fichier.close()
    fichier = open(path, "w")
    nam = str(str(s[0]) + str("\n") + str("Nom : " + str(s[1]) + str("\n") + str("Tout vas bien")))
    fichier.write(nam)
    fichier.flush()
    fichier.close()
    return True


def test():
    bot.send_text_message(ID, "Test")


@app.route("/remake_files")
def rmkfi():
    remake_files()


def remake_files():
    for files in glob.iglob("/home/servs/saves/*.uvrim"):
        remake_file(files)


if __name__ == '__main__':
    t = Verif()
    t.start()
    app.run()
else:
    print("error")
