#!/usr/bin/python

import sys
import os
import time
import struct
import json
import traceback

#https://github.com/SavinaRoja/PyUserInput
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/PyUserInput")
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

# v0.6: working version
# v0.7: add timestamp key, delay expiration, and traceback catching

def Main():
  message_number = 0

  SendMessage({"version": "0.7"})

  while 1:
    # Read the message type (first 4 bytes).
    text_length_bytes = sys.stdin.read(4)

    if len(text_length_bytes) == 0:
      time.sleep(.1)
      continue

    # Read the message length (4 bytes).
    text_length = struct.unpack('i', text_length_bytes)[0]

    # Read the text (JSON object) of the message.
    text = sys.stdin.read(text_length).decode('utf-8')
    request = json.loads(text)

    message_number += 1

    try:
      ProcessRequest(request, text, message_number)
    except:
      SendMessage({"id": message_number, "ack": text, "resp": {}, "timestamp": round(time.time() * 1000), "crash": True, "traceback": traceback.format_exc()})

def ProcessRequest(request, text, message_number):
  resp = {}

  delay = 0
  if "timestamp" in request:
    delay = round(time.time() * 1000) - request["timestamp"]

  if "click" in request:
    if delay > 2 * 1000:
      resp["clicked"] = False
    else:
      try:
        m.click(request["click"]["x"], request["click"]["y"], request["click"]["b"])
        resp["clicked"] = True
      except:
        resp["clicked"] = False

  if "key" in request:
    if delay > 2 * 1000:
      resp["keypressed"] = False
    else:
      try:
        #press modifiers
        if "mod" in request["key"]:
          for key in request["key"]["mod"]:
            k.press_key(key)
            time.sleep(.05)
        #type seq
        for key in request["key"]["keys"]:
          k.tap_key(key)
        #release modifiers
        if "mod" in request["key"]:
          request["key"]["mod"].reverse()
          for key in request["key"]["mod"]:
            k.release_key(key)
        resp["keypressed"] = True
      except:
        resp["keypressed"] = False
  
  SendMessage({"id": message_number, "ack": text, "resp": resp, "timestamp": round(time.time() * 1000), "delay": delay})

def SendMessage(message):
  messtext = json.dumps(message)

  try:
    sys.stdout.write(struct.pack("I", len(messtext)))
    sys.stdout.write(messtext)
    sys.stdout.flush()
  except IOError:
    quit()

if __name__ == '__main__':
  Main()


