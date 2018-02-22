import os
import time
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

enableChannels = ["C61K9HKDM"]
enableResponses = {"Hello":"Hi"}

def postMsg(msg, channel):
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )
def responseMsg(rtm, msg):
    postMsg(msg, channel=rtm["channel"])

def response(rtm):
    for er in enableResponses.keys():
        if rtm["text"] == er:
            postMsg(enableResponses[er], rtm["channel"])

def addRespond(rtm):
    if rtm["text"][0:17] == "nosetting Respond":
        list = rtm["text"].split()
        del list[0:2]
        inRes = "false"
        res = ""
        mes = ""
        for s in list:
            if s == "to":
                inMes = "true"
                continue
            if inMes == "true":
                mes += s
            else:
                res += s
        if inMes == "false":
            responseMsg(rtm,"Error")
            return
        enableResponses[mes] = res
        responseMsg(rtm,"Success")

def showDetails(rtm):
    if rtm["text"] == "nosetting show enable Channels":
        responseMsg(rtm,enableChannels)
    if rtm["text"] == "nosetting show responses":
        responseMsg(rtm,enableResponses)

def addChannel(rtm):
    if rtm["text"] == "nosetting addThisChannel":
        enableChannels.append(rtm["channel"])
        responseMsg(rtm,"Success")

def disChannel(rtm):
    if rtm["text"] == "nosetting disThisChannel":
        enableChannels.remove(rtm["channel"])
        responseMsg(rtm,"Success")


if sc.rtm_connect():
    while True:
        for rtm in sc.rtm_read():
            print(rtm)
            if rtm["type"] == "message":
                if "subtype" not in rtm and "text" in rtm:
                    inCh = "false"
                    for ec in enableChannels:
                        if rtm["channel"] == ec:
                            inCh = "true"
                            break
                    if inCh == "true":
                        response(rtm)
                        addRespond(rtm)
                        disChannel(rtm)
                    else:
                        addChannel(rtm)
                """
                elif rtm["subtype"] = "bot_message" and "text" in rtm:
                    if rtm["bot_id"] != "B9864DFTL":
                    response(rtm)
                    addRespond(rtm)
                    addChannel(rtm)
                """
        time.sleep(1)
else:
    print("Connection Failed")