#!/usr/bin/env python
# encoding: utf-8

import boto3
from slackclient import SlackClient
import datetime
from config import *
import random
import os
import re


def check_authorization(token):
  if token == os.environ['OUTGOING_SLACK_TOKEN']:
    return

  raise ValueError("token is not authorization")


def get_aws_billing():
  response = boto3.client('cloudwatch', region_name='us-east-1')

  get_metric_statistics = response.get_metric_statistics(
    Namespace='AWS/Billing',
    MetricName='EstimatedCharges',
    Dimensions=[
      {
        'Name': 'Currency',
        'Value': 'USD'
        }
      ],
    StartTime=datetime.datetime.today() - datetime.timedelta(days=1),
    EndTime=datetime.datetime.today(),
    Period=86400,
    Statistics=['Maximum'])

  cost = get_metric_statistics['Datapoints'][0]['Maximum']
  date = get_metric_statistics['Datapoints'][0]['Timestamp'].strftime('%Y年%m月%d日')

  return {'cost': cost, 'date': date}


# 寸→センチ
def convert_sun_to_cm(sun):
  cm = float(sun) * 3.030
  return round(cm, 2)


# センチ→尺寸
def convert_cm_to_sun(cm):
  sun   = float(cm) / 3.030
  return {
    'shaku': int(sun / 10),
    'sun': round(float(sun % 10), 2)
  }


def acme(cmd, word):
  if (cmd in ['マグロ', 'まぐろ', '鮪']):
    return 'あいよ っ🍣'
  if (cmd == 'say'):
    return random.choice(SAYING_LIST)
  if (cmd == '回文'):
    return word[::-1]


def post_slack(channel_name, message, user):
  token = os.environ['SLACK_TOKEN']
  sc = SlackClient(token)
  if user == 'lambot':
    sc.api_call(
      "chat.postMessage",
      channel=channel_name,
      text=message,
      as_user='true',
    )


def handle(event, context, *, dry_run=0):
  check_authorization(event['token'])

  channel_name   = event['channel_name']
  text           = event['text']
  cmd_list       = text.split()
  lambot_message = '';
  user           = 'lambot';

  for i, cmd in enumerate(cmd_list):
    # 最初の1つ目はlambotのはずなのでスキップ
    if (i == 0):
      continue
    if (i == 1):
      if (cmd == 'choice'):
        lambot_message = random.choice(cmd_list[2:])
        break

      if (cmd == 'shuffle'):
        shuffled = random.sample(cmd_list[2:], len(cmd_list[2:]))
        lambot_message = ' '.join(shuffled)
        break

      if re.compile('寸|sun').search(cmd):
        pattern=r'([+-]?[0-9]+\.?[0-9]*)'  # 数字判別の正規表現パターン
        numbers = re.findall(pattern,cmd)  # 数字を抽出したリスト
        # HACK リストには一つしか入らないはずなので[0]指定
        sun = numbers[0]
        cm  = convert_sun_to_cm(sun)
        lambot_message = "%s寸 は 約%scmだ！" % (sun, cm)
        break;

      if re.compile('cm|センチ').search(cmd):
        pattern=r'([+-]?[0-9]+\.?[0-9]*)'  # 数字判別の正規表現パターン
        numbers = re.findall(pattern,cmd)  # 数字を抽出したリスト
        # HACK リストには一つしか入らないはずなので[0]指定
        cm    = numbers[0]
        shaku_sun = convert_cm_to_sun(cm)
        lambot_message = "%scm は 約%s尺%s寸だ！" % (cm, shaku_sun['shaku'], shaku_sun['sun'])
        break;

      if (cmd == 'aws'):
        if (cmd_list[i+1] == 'billing'):
          billing = get_aws_billing()
          lambot_message = "%sまでのAWSの料金は、$%sだ！" % (billing['date'], billing['cost'])
          break

      if (cmd in ACME_WORDS):
        word = ''
        if (i != len(cmd_list)-1):
          word = cmd_list[i+1]
        lambot_message = acme(cmd, word)

  if dry_run:
    print(lambot_message)
    return

  post_slack(channel_name, lambot_message, user)

  return


if __name__=='__main__':
  handle({
    'channel_name': 'sandbox',
    'text': '@lambot 回文 abcdefg',
    'token': os.environ['OUTGOING_SLACK_TOKEN']
  }, '', dry_run=1)
