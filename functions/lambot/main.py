#!/usr/bin/env python
# encoding: utf-8

import boto3
from slackclient import SlackClient
import datetime
from config import *
import random
import os


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


def post_slack(channel_id, message, user):
  token = os.environ['SLACK_TOKEN']
  sc = SlackClient(token)
  if user == 'lambot':
    sc.api_call(
      "chat.postMessage",
      channel=channel_id,
      text=message,
      as_user='true',
    )


def handle(event, context):
  check_authorization(event['token'])

  channel_id     = event['channel_id']
  text           = event['text']
  cmd_list       = text.split()
  lambot_message = '';
  user           = 'lambot';

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
        shuffled = random.sample(cmd_list[2:], len(cmd_list[2:]))
        lambot_message = ' '.join(shuffled)
        break
      if (cmd == 'aws'):
        if (cmd_list[i+1] == 'billing'):
          billing = get_aws_billing()
          lambot_message = "%sまでのAWSの料金は、$%sだ！" % (billing['date'], billing['cost'])
          break

  post_slack(channel_id, lambot_message, user)
  return


if __name__=='__main__':
  handle({
    'channel_id': 'C9Q6L6SE6',
    'text': 'lambot shuffle hoge fuga piyo',
    'token': os.environ['OUTGOING_SLACK_TOKEN']
  }, '')
