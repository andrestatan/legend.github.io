from flask import Flask, render_template
import json
from pyamf import remoting
import requests
import numpy as np

app = Flask(__name__)
url = "https://playninjalegends.com/amf_nl/"
idChar = "40257"
loginVerificationToken = "A9110a384f1caf477af9f2ce094b4f040"
service = "ClanService.executeService"
jsonInformationCopy = []
acumulatedRep = []
slowPlayers = []
valueComparation = True
identifier = "/1"
method = "getMembersInfo"
headers = {
    "value": "POST/amf_nl/HTTP/1.1",
    "Referer": "app:/NinjaLegends.swf",
    "Content-type": "application/x-amf",
    "Accept": "text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, "
              "image/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, "
              "flv-application/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5, "
              "application/x-mpegURL",
    "User-Agent": "Mozilla/5.0 (Windows; U; en) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/33.1",
    "Connection": "Keep-Alive",
    "Host": "playninjalegends.com",
    "Accept-Encoding": "gzip,deflate",
    "Content-Length": "111",
    "x-flash-version": "33,1,1,926"
}

def sendNetStreamUnpauseNotify():
    resp = requests.post(url, headers=headers,
                         data="\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u001a" + service + "\u0000\u0002/1\u0000"
                              "\u0000\u0000E\n\u0000\u0000\u0000\u0001\u0011\t\u0005\u0001\u0006\u001d" + method + "\t"
                              "\u0005\u0001\u0006\u000b" + idChar + "\u0006" + loginVerificationToken,
                         verify=False)

    resp_msg = remoting.decode(resp.content)
    return resp_msg.bodies


def sortAcumulatedReputation(e):
    formatedValue = int(e['Acumulated_Rep'])
    return formatedValue

def sortSpeedPerMinutes(e):
    formatedValue = int(e['Acumulated_Rep'])
    return formatedValue

def data_procesing():
    dataProcesing = sendNetStreamUnpauseNotify()
    procesingString = str(dataProcesing[0])
    procesingString = procesingString.replace("('/1', <Response status=/onResult>{'status': 1, 'error': 0, 'members': ",
                                              "")
    procesingString = procesingString.replace("}</Response>)", "")
    procesingString = procesingString.replace("'", "\"")
    jsonInformation = json.loads(procesingString)
    return jsonInformation


def fasterPlayersComponent():
    jsonInformation = data_procesing()
    valueDummyComparation = []
    global jsonInformationCopy
    global acumulatedRep
    global valueComparation
    global slowPlayers
    if valueComparation:
        jsonInformationCopy = jsonInformation.copy()
        valueComparation = False
    for elemento in jsonInformation:
        if jsonInformationCopy:
            for elementComparition in jsonInformationCopy:
                if elemento['member_name'] == elementComparition['member_name']:
                    jsonInformation[jsonInformation.index(elemento)]["Acumulated_Rep"] = (
                                int(elemento['member_reputation'])
                                - int(elementComparition["member_reputation"]))
                    break

    jsonInformation.sort(key=sortAcumulatedReputation, reverse=True)
    acumulatedRep = valueDummyComparation
    return jsonInformation

def slowPlayersComponent():
    jsonInformation = data_procesing()
    valueDummyComparation = []
    global jsonInformationCopy
    global acumulatedRep
    global valueComparation
    global slowPlayers
    if valueComparation:
        jsonInformationCopy = jsonInformation.copy()
        valueComparation = False
    for elemento in jsonInformation:
        if jsonInformationCopy:
            for elementComparition in jsonInformationCopy:
                if elemento['member_name'] == elementComparition['member_name']:
                    jsonInformation[jsonInformation.index(elemento)]["Acumulated_Rep"] = (
                            int(elemento['member_reputation'])
                            - int(elementComparition["member_reputation"]))
                    break

    jsonInformation.sort(key=sortSpeedPerMinutes, reverse=False)
    acumulatedRep = valueDummyComparation
    return jsonInformation



@app.route("/")
def hello_world():
    data_procesing()
    return render_template("main.html", fastPlayers=fasterPlayersComponent(), slowPlayers=slowPlayersComponent())


if __name__ == '__main__':
    app.run()