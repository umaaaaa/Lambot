#!/usr/bin/env python
# encoding: utf-8

from slackclient import SlackClient
from pprint import pprint
import datetime
import os
import argparse


def post_slack(*, username, channel, message, icon_emoji):
    token = os.environ['SLACK_TOKEN']
    sc = SlackClient(token)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        username=username,
        icon_emoji=icon_emoji
    )

def change_signboard():
  mention = os.environ['OWNER']
  return {
    'username': 'カンバルマン',
    'icon_emoji': ':muscle:',
    'channel': 'general',
    'message': 'お店の看板の休業日表示を変更してください ' + mention
  }


def greeting():
  return {
    'username': 'ベビーサン(from テレタビーズ)',
    'icon_emoji': ':sun_with_face:',
    'channel': 'general',
    'message': '今日も一日頑張るぞい'
  }


def handle(event, context, *, dry_run=0):
  post_info = {}
  # 月末に動作
  if (event['resources'][0] == os.environ['LAST_MONTH_LAST_HOURS']):
    post_info = change_signboard()
  # 一日の最初に動作
  if (event['resources'][0] == os.environ['FIRST_HOURS']):
    post_info = greeting()

  if (dry_run):
    pprint(post_info)
    return

  if (post_info):
    post_slack(
      username=post_info['username'],
      channel=post_info['channel'],
      message=post_info['message'],
      icon_emoji=post_info['icon_emoji']
    )

  return


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--dry_run', type=int, default=1)
  args = parser.parse_args()
  handle({'resources': [os.environ['FIRST_HOURS']]},'', dry_run=args.dry_run)
