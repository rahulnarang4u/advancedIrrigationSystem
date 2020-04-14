import json, requests, time
from boltiot import Bolt

import requests                 # for making HTTP requests
import json                     # library for handling JSON data
import time                     # module for sleep operation
from boltiot import Bolt        # importing Bolt from boltiot module
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier



"""Configurations for home_automation.py"""
# Bolt IoT Credentials
api_key = "5aaAPI Key of Bolt Cloud"     #API Key of Bolt Cloud
device_id  = "BOLTXXXXXX"                            #Device ID
# Telegram Credentials
telegram_chat_id = "@channel name"
telegram_bot_id = "botXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

URL = "https://api.telegram.org/" + telegram_bot_id

mybolt = Bolt(api_key, device_id)

light_pin1 = "12"
light_pin2 = "6"

last_message_id = None
last_text = None

def get_levelsensor_value_from_pin(pin):
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        mybolt.serialWrite("Level")
        response = mybolt.serialRead('10')
        print(response)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data["value"])
            return -999
        levelsensor_value = int(data["value"])
        return levelsensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def get_LDRsensor_value_from_pin(pin1):
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        mybolt.serialWrite("LDR")
        response = mybolt.serialRead('10')
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        LDRsensor_value = int(data["value"])
        return LDRsensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def get_rainsensor_value_from_pin(pin2):
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        mybolt.serialWrite("Rain")
        response = mybolt.serialRead('10')
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        rainsensor_value = int(data["value"])
        return rainsensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def get_Humidity():
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        mybolt.serialWrite("getHum")
        response = mybolt.serialRead('10')
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        humidity = int(data["value"])
        return humidity
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def get_Temperature():
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        mybolt.serialWrite("getTemp")
        response = mybolt.serialRead('10')
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        temperature = int(data["value"])
        return temperature
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999


def check_device_status():
    try:
        response = mybolt.isOnline()
        response = json.loads(response)
        if response["value"] == "online":
            print("Device is Online")
            return True
        else:
            print("Device is offline")
            send_telegram_message("Device is offline")
            return False
    except Exception as e:
        print("An error occurred in Checking device status.")
        print(e)
        return False

def send_telegram_message(message):
    """Sends message via Telegram"""
    print("Sending telegram message .....")
    url = URL + "/sendMessage?text=" + message + "&chat_id=" + telegram_chat_id
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        if js["ok"] == True:
            print("Messgae sent successfully.")
            return True
        else:
            print("Message on sent. Response: " + str(js["ok"]))
            print(js)
            return False
    except Exception as e:
        print("An error occurred in sending message via Telegram")
        print(e)
        return False

def get_last_message():
    """Gets last message from Telegram"""
    print("Getting last message .....")
    url = URL + "/getUpdates"
    try:
        text = None
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        num_updates = len(js["result"])
        last_update = num_updates - 1
        message_id = js["result"][last_update]["channel_post"]["message_id"]
        text = js["result"][last_update]["channel_post"]["text"]
        print("This is the last message : " + text)
        return (text, message_id)
    except Exception as e:
        print("An error occurred in getting message from Telegram")
        print(e)

while True:
    # Step 1 : Check Device Status
    print("Checking device Status .....")
    response = check_device_status()
    if response != True:
        time.sleep(10)
        continue
    # Step 2 : Sending Welcome message with options.
    message = "Welcome to Advanced Irrigation System\nMade with ❤\n" + "-" * 55 + "\nSelect Mode -\n1. Manual ON\n2. Manual OFF\n3. AUTO\n4. Venting Mode"
    response = send_telegram_message(message)
    if response != True:
        continue
    time.sleep(10)
    # Step 3 : Getting last message from telegram
    text, message_id = get_last_message()
    # Step 4 : Checking with previous message & message_id
    if (text !=last_text) or (message_id != last_message_id):
        if (text == "1") or (text == "Manual on") or (text == "manual on"):
            mybolt.digitalWrite('1','HIGH')
            mybolt.digitalWrite('2','HIGH')

            message = "Manual ON active, Irrigation valve fully open!"
            print(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=180,0&deviceName=BOLT3848684')
            send_telegram_message(message)
        elif (text == "2") or (text == "Manual OFF") or (text == "manual off"):
            mybolt.digitalWrite('1','LOW')
            mybolt.digitalWrite('2','LOW')
            
            message = "Manual OFF active, Irrigation valve fully closed!"
            print(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=0,0&deviceName=BOLT3848684')
            send_telegram_message(message)
        elif (text == "3") or (text == "AUTO") or (text == "auto"):
            mybolt.digitalWrite('1','HIGH')
            mybolt.digitalWrite('2','LOW')
            message = "AUTO MODE active!"
            print(message)
            send_telegram_message(message)
            time.sleep(5)
            levelsensor_value = get_levelsensor_value_from_pin('A1')
            print("The level sensor value is:", levelsensor_value)
            time.sleep(5)

            if levelsensor_value == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue
            rainsensor_value = get_rainsensor_value_from_pin('A3')
            print("The rain sensor value is:", rainsensor_value)
            time.sleep(5)

            if rainsensor_value == -999:
                print("Request was unsuccessfull. rainsensor Skipping.")
                time.sleep(10)

            LDRsensor_value = get_LDRsensor_value_from_pin('A5')
            print("The light sensor value is:", LDRsensor_value)
            time.sleep(5)

            if LDRsensor_value == -999:
                print("Request was unsuccessfull. LDRsensor Skipping.")
                time.sleep(10)
                continue

            humidity = get_Humidity()
            print("The humidity sensor value is:", humidity)
            time.sleep(5)

            if humidity == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue

            temperature = get_Temperature()
            print("The temp sensor value is:", temperature)
            time.sleep(5)

            if temperature == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue
            if levelsensor_value <=40:
                message = "Acquiring Sensor Data"
                print(message)
                send_telegram_message(message)
                data= pd.read_csv('3848684 (33).csv')
                message = "Predicting Valve Opening."
                print(message)
                send_telegram_message(message)
                time.sleep(5)
                data.columns
                data.head()
                data.info()
                data.drop(["d_id",],axis=1,inplace=True)
                data.drop(["time_stamp",],axis=1,inplace=True)
                data.info()
                y=data.Valve.values
                #normalization
                x_data=data.drop(["Valve"], axis=1)
                x=(x_data-np.min(x_data))/(np.max(x_data) -np.min(x_data))
                x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.6,random_state=22)
                dt= DecisionTreeClassifier()
                dt.fit(x_train,y_train)
                print("score :",dt.score(x_test,y_test))
                prediction = dt.predict([[levelsensor_value,LDRsensor_value,rainsensor_value]])
                print(prediction)
                value = str(prediction[0])
                message = "Irrigation Valve at: "+value+"."
                print(message)
                send_telegram_message(message)
                r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoWrite?pin=3&value='+value+'&deviceName=BOLT3848684')
                time.sleep(10)

                last_text = text
                last_message_id = message_id

            else:

                r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=0,180&deviceName=BOLT3848684')
                message = 'Level Crossed Threshold, AUTO Venting with Irrigation Valve Closed!'
                print(message)
                send_telegram_message(message)
                message = 'Level Value: '+str(levelsensor_value)+"."
                print(message)
                send_telegram_message(message)


        elif (text == "4") or (text == "Venting") or (text == "venting"):
            mybolt.digitalWrite('1','LOW')
            mybolt.digitalWrite('2','HIGH')
            message = "Venting operation Active, Irrigation Valve Closed!"
            print(message)
            send_telegram_message(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=0,180&deviceName=BOLT3848684')
        time.sleep(10)

    else:
        text = last_text

        if (text == "1") or (text == "Manual on") or (text == "manual on"):
            mybolt.digitalWrite('1','HIGH')
            mybolt.digitalWrite('2','HIGH')
            
            message = "Manual ON, Irrigation valve fully open!"
            print(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoWrite?pin=3&value=180&deviceName=BOLT3848684')
            send_telegram_message(message)
        elif (text == "2") or (text == "Manual OFF") or (text == "manual off"):
            mybolt.digitalWrite('1','LOW')
            mybolt.digitalWrite('2','LOW')
            
            message = "Manual OFF, Irrigation valve fully closed!"
            print(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoWrite?pin=3&value=0&deviceName=BOLT3848684')
            send_telegram_message(message)
        elif (text == "3") or (text == "AUTO") or (text == "auto"):

            mybolt.digitalWrite('1','HIGH')
            mybolt.digitalWrite('2','LOW')
            message = "AUTO MODE active!"
            print(message)
            send_telegram_message(message)
            time.sleep(5)
            levelsensor_value = get_levelsensor_value_from_pin('A1')
            print("Level sensor value is:", levelsensor_value)
            time.sleep(5)

            if levelsensor_value == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue
            rainsensor_value = get_rainsensor_value_from_pin('A3')
            print("The rain sensor value is:", rainsensor_value)
            time.sleep(5)

            if rainsensor_value == -999:
                print("Request was unsuccessfull. rainsensor Skipping.")
                time.sleep(10)

            LDRsensor_value = get_LDRsensor_value_from_pin('A5')
            print("The light sensor value is:", LDRsensor_value)
            time.sleep(5)

            if LDRsensor_value == -999:
                print("Request was unsuccessfull. LDRsensor Skipping.")
                time.sleep(10)
                continue

            humidity = get_Humidity()
            print("The humidity sensor value is:", humidity)
            time.sleep(5)

            if humidity == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue

            temperature = get_Temperature()
            print("The temp sensor value is:", temperature)
            time.sleep(5)

            if temperature == -999:
                print("Request was unsuccessfull. levelsensor Skipping.")
                time.sleep(10)
                continue
            if levelsensor_value <=40:
                message = "Acquiring Sensor Data"
                print(message)
                send_telegram_message(message)
                data= pd.read_csv('3848684 (33).csv')
                message = "Predicting Valve Opening."
                print(message)
                send_telegram_message(message)
                time.sleep(5)
                data.columns
                data.head()
                data.info()
                data.drop(["d_id",],axis=1,inplace=True)
                data.drop(["time_stamp",],axis=1,inplace=True)
                data.info()
                y=data.Valve.values
                #normalization
                x_data=data.drop(["Valve"], axis=1)
                x=(x_data-np.min(x_data))/(np.max(x_data) -np.min(x_data))
                x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.6,random_state=22)
                dt= DecisionTreeClassifier()
                dt.fit(x_train,y_train)
                print("score :",dt.score(x_test,y_test))
                prediction = dt.predict([[levelsensor_value,LDRsensor_value,rainsensor_value]])
                print(prediction)
                value = str(prediction[0])
                message = "Irrigation Valve at: "+value+"."
                print(message)
                send_telegram_message(message)
                r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoWrite?pin=3&value='+value+'&deviceName=BOLT3848684')
                time.sleep(10)

                last_text = text
                last_message_id = message_id

            else:

                r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=0,180&deviceName=BOLT3848684')
                message = 'Level Crossed Threshold, AUTO Venting with Irrigation Valve Closed!'
                print(message)
                send_telegram_message(message)
                message = 'Level Value: '+str(levelsensor_value)+"."
                print(message)
                send_telegram_message(message)

        elif (text == "4") or (text == "Venting") or (text == "Venting"):
            mybolt.digitalWrite('1','LOW')
            mybolt.digitalWrite('2','HIGH')
            
            message = "Venting operation Active, Irrigation Valve Closed!"
            print(message)
            send_telegram_message(message)
            r = requests.get('https://cloud.boltiot.com/remote/5aa5c2bf-f593-42a7-9a08-c0406022333e/servoMultiWrite?pins=3,4&values=0,180&deviceName=BOLT3848684')
    time.sleep(10)
