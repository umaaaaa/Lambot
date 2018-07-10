#!/usr/bin/env python
# encoding: utf-8

from slackclient import SlackClient
import os


def post_slack(message):
    token = os.environ['SLACK_TOKEN']
    sc = SlackClient(token)
    sc.api_call(
        "chat.postMessage",
        channel='#general',
        text=message,
        username='lambot',
    )


def handle(event, context):
    return {'text': '町ではお前が法律かもしれないが、ここでは俺が法律だ'}


if __name__=='__main__':
    handle('', '')
