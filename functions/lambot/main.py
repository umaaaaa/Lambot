#!/usr/bin/env python
# encoding: utf-8

from sayings import *
import random
import os


def check_authorization(token):
    if token == os.environ['OUTGOING_SLACK_TOKEN']:
        return

    raise ValueError("token is not authorization")


def handle(event, context):
    check_authorization(event['token'])

    text           = event['text']
    cmd_list       = text.split()
    lambot_message = '';

    for i, cmd in enumerate(cmd_list):
        # 最初の1つ目はlambotのはずなのでスキップ
        if (i == 0):
            continue
        if (i == 1):
            if (cmd == 'say'):
                lambot_message = random.choice(SAYING_LIST)
                break
            if (cmd == 'choice'):
                lambot_message = random.choice(cmd_list[2:])
                break
            if (cmd == 'shuffle'):
                lambot_message = random.shuffle(cmd_list[2:])
                break

    return { 'text': lambot_message }


if __name__=='__main__':
    value = handle({
        'text': 'lambot hoge',
        'token': os.environ['OUTGOING_SLACK_TOKEN']
    }, '')
    print value
