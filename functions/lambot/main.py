#!/usr/bin/env python
# encoding: utf-8

from sayings import *
import random

def handle(event, context):
    text = event['text']
    cmd_list = text.split()
    lambot_message = '???';
    for i, cmd in enumerate(cmd_list):
        # 最初の1つ目はlambotのはずなのでスキップ
        if (i == 0):
            continue
        if (i == 1):
            if (cmd == 'say'):
                lambot_message = random.choice(SAYING_LIST)

    return { 'text': lambot_message }


if __name__=='__main__':
  handle({'text': 'lambot hoge'}, '')
