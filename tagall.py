# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
from threading import Thread  # try multithreading approach to checking for summon / banish commands
import time
import random
import sys
import json
import codecs
import threading
import glob
import re
import string
import os
import requests
import six
import ast
import pytz
import urllib
import urllib3
import urllib.parse
import traceback
import atexit

# This is for login via Link and via Email
#gye = LINE()
#gye = LINE("Email","Password")
#gye.log("Auth Token : " + str(gye.authToken))
#channelToken = gye.getChannelResult()
#gye.log("Channel Token : " + str(channelToken))

# Please Edit As You Wish
# Provided Neat And Response
# if you want to log in Via qr Change Only
# Or Login Via Emal
# Don't Forget to Add Admin
#==============================================================================#
botStart = time.time()

gye = LINE("email", "password")
gye.log("Auth Token : " + str(gye.authToken))
channelToken = gye.getChannelResult()
gye.log("Channel Token : " + str(channelToken))
print ()

print ("\n Account Logged In Successfully!\n")

mainMID = "u7b7eb93b3bc0b9245b873f732f44b54d"  # Replace with your MID
gyeMID = gye.profile.mid

creator = [mainMID]
Owner = [mainMID]
admin = [mainMID]

gyeProfile = gye.getProfile()
lineSettings = gye.getSettings()
oepoll = OEPoll(gye)
responsename = gye.getProfile().displayName
#==============================================================================#

with open('Owner.json', 'r') as fp:
    Owner = json.load(fp)

with open('admin.json', 'r') as fp:
    admin = json.load(fp)

myProfile = {
    "displayName": "",
   	"statusMessage": "",
   	"pictureStatus": ""
}

myProfile["displayName"] = gyeProfile.displayName
myProfile["statusMessage"] = gyeProfile.statusMessage
myProfile["pictureStatus"] = gyeProfile.pictureStatus

readOpen = codecs.open("read.json", "r", "utf-8")
settingsOpen = codecs.open("settings.json", "r", "utf-8")

#==============================================================================#

read = json.load(readOpen)
settings = json.load(settingsOpen)


def restartBot():
    print ("[ INFO ] BOT RESET")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)


def logError(text):
    gye.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt", "a") as error:
        error.write("\n[%s] %s" % (str(time), text))


def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":' + json.dumps(mid) + '}'
        text_ = '@x '
        gye.sendMessage(to, text_, contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'}, contentType=0)
    except Exception as error:
        logError(error)


def welcomeMembers(to, mid):
    try:
        arrData = ""
        textx = "「Welcome!」\n".format(str(len(mid)))
        arr = []
        no = 1
        num = 2
        for i in mid:
            ginfo = gye.getGroup(to)
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S': slen, 'E': elen, 'M': i}
            arr.append(arrData)
            # textx += mention + wait["welcome"]
            textx += mention + settings["welcome"]
            if no < len(mid):
                no += 1
                textx += "%i " % (num)
                num = (num + 1)
            else:
                try:
                    no = "\n╚══[ {} ]".format(str(gye.getGroup(to).name))
                except:
                    no = "\n╚══[ Success ]"
        gye.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        gye.sendMessage(to, "[ INFO ] Error :\n" + str(error))


def helpmessage():
    helpMessage = "╭════════╬♦╬════════╮" + "\n" + \
                  "║͜͡☆➣ TAGALL BOT" + "\n" + \
                  "╰════════╬♦╬════════╯" + "\n" + \
                  "╭════════╬♦╬════════╮" + "\n" + \
                  "║͜͡☆➣ HELP MENU" + "\n" + \
                  "╰════════╬♦╬════════╯" + "\n" + \
                  "╭════════╬♦╬════════╮" + "\n" + \
                  "║͜͡☆➣  Tagall" + "\n" + \
                  "║͜͡☆➣ .Tagall" + "\n" + \
                  "║͜͡☆➣ " + "\n" + \
                  "║͜͡☆➣  spamtag: [number]" + "\n" + \
                  "║͜͡☆➣  spamtag @[Mention]" + "\n" + \
                  "║͜͡☆➣ " + "\n" + \
                  "║͜͡☆➣  Check Welcome" + "\n" + \
                  "║͜͡☆➣  Welcome On/Off" + "\n" + \
                  "║͜͡☆➣  Set welcome: [Message]" + "\n" + \
                  "║͜͡☆➣ " + "\n" + \
                  "║͜͡☆➣  AdminAdd @[Mention]" + "\n" + \
                  "║͜͡☆➣  AdminDel @[Mention]" + "\n" + \
                  "║͜͡☆➣  AdminList" + "\n" + \
                  "║͜͡☆➣ " + "\n" + \
                  "║͜͡☆➣  OwnerAdd @[Mention]" + "\n" + \
                  "║͜͡☆➣  OwnerDel @[Mention]" + "\n" + \
                  "║͜͡☆➣  OwnerList" + "\n" + \
                  "║͜͡☆➣ " + "\n" + \
                  "║͜͡☆➣  Sp (speedtest)" + "\n" + \
                  "║͜͡☆➣  Restart" + "\n" + \
                  "║͜͡☆➣  Runtime" + "\n" + \
                  "╰════════╬♦╬════════╯" + "\n" + \
                  "╭════════╬♦╬════════╮" + "\n" + \
                  "║͜͡☆➣ TAGALL BOT" + "\n" + \
                  "╰════════╬♦╬════════╯"
    return helpMessage

#==============================================================================#


def backupData():
    try:
        backup = settings
        f = codecs.open('settings.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False


def command(text):
    pesan = text.lower()
    if pesan.startswith(settings["keyCommand"]):
        cmd = pesan.replace(settings["keyCommand"], "")
    else:
        cmd = "Undefined command"
    return cmd
#==============================================================================#


def sendMessage1(self, messageObject):
        return self.talk.sendMessage(0, messageObject)
#==============================================================================#


def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END_OF_OPERATION")
            return


# -------------------------------------------------------------------------------
        if op.type == 17:
            ginfo = gye.getGroup(op.param1)
            contact = gye.getContact(op.param2).picturePath
            image = 'http://dl.profile.line.naver.jp' + contact
            welcomeMembers(op.param1, [op.param2])
            gye.sendImageWithURL(op.param1, image)
# -------------------------------------------------------------------------------
        if op.type == 26:
            print ("[ 26 ] RECEIVE_MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != gye.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                if text.lower() == 'help':
                    if sender in admin:
                        helpMessage = helpmessage()
                        gye.sendMessage(to, str(helpMessage))
#==============================================================================#
                elif text.lower() == 'sp':
                    if sender in admin:
                        start = time.time()
                        gye.sendMessage(to, "Checking Speed...")
                        elapsed_time = time.time() - start
                        gye.sendMessage(to, format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    if sender in Owner:
                        gye.sendMessage(to, "Please Wait...")
                        time.sleep(5)
                        gye.sendMessage(to, "Restart Successful")
                        restartBot()
                elif text.lower() == 'runtime':
                    if sender in admin:
                        timeNow = time.time()
                        runtime = timeNow - botStart
                        runtime = format_timespan(runtime)
                        gye.sendMessage(to, "Bot has been running for {}".format(str(runtime)))
#==============================================================================#
                elif msg.text.lower().startswith("owneradd "):
                    if sender in creator:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                Owner[target] = True
                                f = codecs.open('Owner.json', 'w', 'utf-8')
                                json.dump(Owner, f, sort_keys=True, indent=4, ensure_ascii=False)
                                gye.sendMessage(msg.to, "Owner ☢-Bot-☢\nAdd\nExecuted")
                                backupData()
                            except:
                                pass
                    else:
                        gye.sendMessage(msg.to, "Creator Permission Required")

                elif msg.text.lower().startswith("ownerdel "):
                    if sender in creator:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                del Owner[target]
                                f = codecs.open('Owner.json', 'w', 'utf-8')
                                json.dump(Owner, f, sort_keys=True, indent=4, ensure_ascii=False)
                                gye.sendMessage(msg.to, "Owner ☢-Bot-☢\nRemove\nExecuted")
                                backupData()
                            except:
                                pass
                    else:
                        gye.sendMessage(msg.to, "Creator Permission Required")
# -------------------------------------------------------------------------------
                elif text.lower() == 'ownerlist':
                    if sender in admin:
                        if Owner == []:
                            gye.sendMessage(msg.to, "The Owner List is empty")
                        else:
                            gye.sendMessage(msg.to, "Please Wait...")
                            mc = "╔═══════════════\n╠Bot\n╠══✪〘 Owner List 〙✪═══\n"
                            for mi_d in Owner:
                                mc += "╠✪ " + gye.getContact(mi_d).displayName + "\n"
                            gye.sendMessage(msg.to, mc + "╠═══════════════\n╠✪〘 Bot 〙\n╚═══════════════")
# -------------------------------------------------------------------------------
                elif msg.text.lower().startswith("adminadd "):
                    if sender in Owner:
                        targets = []
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                admin[target] = True
                                f = codecs.open('admin.json', 'w', 'utf-8')
                                json.dump(admin, f, sort_keys=True, indent=4, ensure_ascii=False)
                                gye.sendMessage(msg.to, "Admin ☢-Bot-☢\nAdd\nExecuted")
                                backupData()
                                break
                            except:
                                gye.sendMessage(msg.to, "Added Target Fail !")
                                break
                    else:
                        gye.sendMessage(msg.to, "Owner Permission Required")

                elif msg.text.lower().startswith("admindel "):
                    if sender in Owner:
                        targets = []
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                del admin[target]
                                f = codecs.open('admin.json', 'w', 'utf-8')
                                json.dump(admin, f, sort_keys=True, indent=4, ensure_ascii=False)
                                gye.sendMessage(msg.to, "Admin ☢-Bot-☢\nRemove\nExecuted")
                                backupData()
                                break
                            except:
                                gye.sendMessage(msg.to, "Deleted Target Fail !")
                            break
                    else:
                        gye.sendMessage(msg.to, "Owner Permission Required")
# -------------------------------------------------------------------------------
                elif text.lower() == 'adminlist':
                    if sender in admin:
                        if admin == []:
                            gye.sendMessage(msg.to, "The Admin List is empty")
                        else:
                            gye.sendMessage(msg.to, "Please Wait...")
                            mc = "╔═══════════════\n╠Bot\n╠══✪〘 Admin List 〙✪═══\n"
                            for mi_d in admin:
                                mc += "╠✪ " + gye.getContact(mi_d).displayName + "\n"
                            gye.sendMessage(msg.to, mc + "╠═══════════════\n╠✪〘 Bot 〙\n╚═══════════════")
#==============================================================================#
                elif text.lower() == 'tagall' or text.lower() == '.tagall':
                    if sender in admin:
                        group = gye.getGroup(msg.to)
                        nama = [contact.mid for contact in group.members]
                        k = len(nama) // 20
                        for a in range(k + 1):
                            txt = u''
                            s = 0
                            b = []
                            for i in group.members[a * 20: (a + 1) * 20]:
                                b.append({"S": str(s), "E": str(s + 6), "M": i.mid})
                                s += 7
                                txt += u'@Zero \n'
                            gye.sendMessage(msg.to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES': b})}, contentType=0)
#==============================================================================#
                elif text.lower().startswith("spamtag: "):
                    if sender in admin:
                         proses = text.split(":")
                         strnum = text.replace(proses[0] + ":", "")
                         num = int(strnum)
                         settings["RAlimit"] = num
                         gye.sendMessage(msg.to, "「 Status Spamtag 」\nSuccessfully changed to {} times".format(str(strnum)))
                         backupData()
#==============================================================================#
                elif text.lower().startswith("spamtag "):
                    if sender in admin:
                         if 'MENTION' in msg.contentMetadata.keys() != None:
                             key = eval(msg.contentMetadata["MENTION"])
                             key1 = key["MENTIONEES"][0]["M"]
                             zx = ""
                             zxc = " "
                             zx2 = []
                             pesan2 = "@a"" "
                             xlen = str(len(zxc))
                             xlen2 = str(len(zxc) + len(pesan2) - 1)
                             zx = {'S': xlen, 'E': xlen2, 'M': key1}
                             zx2.append(zx)
                             zxc += pesan2
                             msg.contentType = 0
                             msg.text = zxc
                             lol = {'MENTION': str('{"MENTIONEES":' + json.dumps(zx2).replace(' ', '') + '}')}
                             msg.contentMetadata = lol
                             jmlh = int(settings["RAlimit"])
                             if jmlh <= 1000:
                                 for x in range(jmlh):
                                     try:
                                         gye.sendMessage1(msg)
                                     except Exception as e:
                                         gye.sendMessage(msg.to, str(e))
                             else:
                                 gye.sendMessage(msg.to, "The number exceeds 1000")
#==============================================================================#
                # elif 'set welcome: ' in msg.text:
                elif text.lower().startswith("set welcome: "):
                   if sender in admin:
                      spl = msg.text.replace('set welcome: ', '')
                      if spl in ["", " ", "\n", None]:
                          gye.sendMessage(msg.to, "Failed to replace Welcome Msg")
                      else:
                          settings["welcome"] = spl
                          backupData()
                          gye.sendMessage(msg.to, "「Successfully Replaced」\nWelcome Msg is :\n\n{}".format(str(spl)))

                elif text.lower() == "check welcome":
                    if sender in admin:
                       gye.sendMessage(msg.to, "「Status Welcome」\nWelcome Msg is :\n\n" + str(settings["welcome"]))

                # elif 'Welcome ' in msg.text:
                elif text.lower().startswith("welcome "):
                   if sender in admin:
                      spl = msg.text.replace('welcome ', '')
                      if spl == 'on':
                          # if msg.to in settings[welcome]:
                          #     msgs = "Welcome Msg is active"
                          if settings["welcomeOn"]:
                              msgs = "Welcome Msg is active"
                          else:
                              settings["welcomeOn"] = True
                              backupData()
                              msgs = "Welcome Msg is active"
                          gye.sendMessage(msg.to, "「Status Welcome」\n" + msgs)
                      elif spl == 'off':
                            if not settings["welcomeOn"]:
                                msgs = "Welcome Msg is inactive"
                            else:
                                settings["welcomeOn"] = False
                                backupData()
                                msgs = "Welcome Msg inactive"
                            gye.sendMessage(msg.to, "「 Status Welcome 」\n" + msgs)
#==============================================================================#
    except Exception as error:
        logError(error)


#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
