# Runner Tracker System

[![Build Status](https://travis-ci.org/anfederico/Clairvoyant.svg?branch=master)](https://travis-ci.org/anfederico/Clairvoyant) ![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

## Basic Overview

 - #### Designed to automate and simplify process of tracking runners in marathons
 - #### Helps organizers to track all runners on checkpoints
 - #### Built using RFID antenna and multiple tags

## How It Works (locally)

#### Make sure you have <a href="https://www.docker.com/products/docker-desktop" target="blank">`docker`</a> installed.
1. Clone repository to your local machine by using this command:
```bash
git clone https://github.com/DimonLavron/RTS.git
```

2. Open folder by command:
```bash
cd {YOUR_FOLDER}/RTS
```
3. Start app by using this command:
```bash
docker-compose up --build
```
4. Wait for all process to be done, you have to see output like this:

```text
Starting rts_db_1   ... done
Starting rts_mqtt_1   ... done
Recreating rts_site_1 ... done
Starting rts_script_1 ... done
Attaching to rts_db_1, rts_mqtt_1, rts_script_1, rts_site_1
mqtt_1    | 1558705556: mosquitto version 1.5.8 starting
mqtt_1    | 1558705556: Config loaded from /mosquitto/config/mosquitto.conf.
mqtt_1    | 1558705556: Opening ipv4 listen socket on port 1883.
mqtt_1    | 1558705556: Opening ipv6 listen socket on port 1883.
mqtt_1    | 1558705557: New connection from 172.28.0.4 on port 1883.
mqtt_1    | 1558705557: New client connected from 172.28.0.4 as client-01 (c1, k60).
site_1    | [2019-05-24 13:45:57 +0000] [1] [INFO] Starting gunicorn 19.9.0
site_1    | [2019-05-24 13:45:57 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
site_1    | [2019-05-24 13:45:57 +0000] [1] [INFO] Using worker: sync
site_1    | [2019-05-24 13:45:57 +0000] [7] [INFO] Booting worker with pid: 7
mqtt_1    | 1558705558: New connection from 172.28.0.5 on port 1883.
site_1    | [2019-05-24 13:45:58,133] DEBUG in __init__: Connected client '' to broker mqtt:1883
mqtt_1    | 1558705559: Socket error on client <unknown>, disconnecting.
mqtt_1    | 1558705559: New connection from 172.28.0.5 on port 1883.
mqtt_1    | 1558705559: New client connected from 172.28.0.5 as 63781538-a5c5-44ee-b710-e9088a83af6c (c1, k5).
site_1    | [2019-05-24 13:45:59,138] DEBUG in __init__: Subscribed to topic: myTopic, qos: 0
```
5. If everything is good, open browser and type:
```text
localhost:8000
```
You will see our main page:

<img src="/site/app/media/main_page_test.png">

#### Now you can browse our webapp!
