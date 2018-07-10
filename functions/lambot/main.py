#!/usr/bin/env python
# encoding: utf-8


def handle(event, context):
    text = event['text']
    cmd_list = text.split()
    for cmd in cmd_list:
        # 最初の1つ目はlambotのはずなのでスキップ
        if (cmd == text_list[0]):
            continue
        return {'text': cmd }
    return {'text': '町ではお前が法律かもしれないが、ここでは俺が法律だ'}


if __name__=='__main__':
  handle({'text': 'lambot hoge'}, '')
