# Lambot
AWS Lambda + bot

# Overview

## Description
Slack bot on AWS Lambda

## Install
Install [Apex](http://apex.run/)

```
$ mkdir Lambot
$ cd Lambot
$ apex init
```

Write the common setting. `./project.json`

```
  "role": "***************",
  "environment": {
    "SLACK_TOKEN": "*******************"
  }
```

### Function
#### AWS-billing-information
Write the function setting.  `./functions/AWS-billing-information/function.json`

```
  "hooks": {
    "build": "pip install -r requirements.txt -t ./site-packages"
  },
  "environment": {
    "PYTHONPATH": "/var/runtime:/var/task/site-packages"
  }
```

## deploy
```
$ apex deploy { $function_name }
```

## License
[MIT](https://github.com/umaaaaa/Lambot/blob/master/LICENSE)

## Author
[umaaaaa](https://github.com/umaaaaa)
