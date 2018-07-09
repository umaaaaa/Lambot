#!/usr/bin/env python
# encoding: utf-8

import boto3
from slackclient import SlackClient
import datetime
import os

def get_billing_information():
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

def post_slack(message):
    token = os.environ['SLACK_TOKEN']
    sc = SlackClient(token)
    sc.api_call(
        "chat.postMessage",
        channel='#general',
        text=message,
        username='金の亡者',
        icon_emoji=':money_with_wings:'
    )


def handle(event, context):
    billing_information = get_billing_information()
    billing_information_text = "%sまでのAWSの料金は、$%sです。" % (billing_information['date'], billing_information['cost'])
    
    post_slack(billing_information_text)
