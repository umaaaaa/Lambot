#!/usr/bin/env python
# encoding: utf-8

import boto3
import datetime
from sayings import *
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
      if (cmd == 'aws'):
        if (cmd_list[i+1] == 'billing'):
          billing = get_aws_billing()
          lambot_message = "%sまでのAWSの料金は、$%sだ！" % (billing['date'], billing['cost'])
          break

  return { 'text': lambot_message }


if __name__=='__main__':
  value = handle({
    'text': 'lambot hoge',
    'token': os.environ['OUTGOING_SLACK_TOKEN']
  }, '')
  print(value)
