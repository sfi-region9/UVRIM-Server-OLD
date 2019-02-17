import glob
import os
import threading
import time
from datetime import datetime

from flask import Flask, request
from pymessenger.bot import Bot


class Verif(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print("Launch Automatic Verification")
            if os.path.exists("/home/servs/saves/lastsentmessage.save"):
                verification()
            time.sleep(60 * 60 * 6)


app = Flask(__name__)
ACCES_TOKEN = "EAAFqeesT4ZB0BAKBegdekleyYEuw4bwVBdHtVyOMSaEnnzZCNUFDassNeXp7wflwdMeNwG3GPQx2k3WfvcuJTgTaq2rJQVIJhnL05avRK2J9OM7ERQ7VNCdRQgEZC8PrUi7JMOk3OGogRwYRTYAcZCs92wlvzeSvjgNsKKuesgZDZD"
ID = "2564006353628871"
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

def verif(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"


def register_user(scc, name):
    if os.path.exists("/home/servs/saves/" + scc + "." + name + ".uvrim"):
        print("exist")
    else:
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "x")
        fichier.close()


def save_uvrim(scc, name, uvrim):
    if not os.path.exists("/home/servs/saves/" + scc + "." + name + ".uvrim"):
        return "Error"
    else:
        os.remove("/home/servs/saves/" + scc + "." + name + ".uvrim")
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "x")
        fichier.close()
        fichier = open("/home/servs/saves/" + scc + "." + name + ".uvrim", "w")
        fichier.write(uvrim)
        fichier.flush()
        fichier.close()
        verification()
    return "save success"


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
        return True
    else:
        return False


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


def test():
    bot.send_text_message(ID, "Test")


if __name__ == '__main__':
    t = Verif()
    t.start()
    app.run()
else:
    print("error")
