# -*- coding: utf-8 -*-
from slackclient import SlackClient
import threading
import time
from config import *


sc = SlackClient(SLACKTOKEN)

def timer(_targetChannel,_finishTime):
  post = sc.api_call(
    "chat.postMessage",
    channel = _targetChannel,
    text = str(_finishTime)+" 秒",
    as_user = 'true'
  )
  startTime = time.time()
  timeStamp = post['ts']

  while _finishTime - int(time.time() - startTime) >= 0:
    sc.api_call(
      "chat.update",
      channel = _targetChannel,
      text = str(_finishTime - int(time.time() - startTime))+" 秒",
      ts = timeStamp,
      as_user = 'true'
    )
    time.sleep(2.0)

  sc.api_call(
    "chat.postMessage",
    channel = _targetChannel,
    text = "Time up!!",
    ts = timeStamp,
    as_user = 'true'
  )


if sc.rtm_connect():
    while True:
      time.sleep(1)
      stream = sc.rtm_read()
      print(stream)
      if len(stream) > 0 and 'type' in stream[0] and 'text' in stream[0]:
        inputSplit = stream[0]['text'].split()
        print(inputSplit)
        if stream[0]['type'] == 'message' and inputSplit[0] == '<@'+BOTID+'>':
          targetChannel = stream[0]['channel']
          if inputSplit[1].isdigit():
            finishTime = int(inputSplit[1])
            print('timer start')
            timer(targetChannel,finishTime)
          else:
            post = sc.api_call(
              'chat.postMessage',
              channel = targetChannel,
              text = '書き方 \n`@timer 秒数`',
              as_user = 'true'
            )
            