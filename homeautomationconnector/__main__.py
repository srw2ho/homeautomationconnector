import logging
from logging.handlers import RotatingFileHandler
from queue import Queue

# import sys
import os

# import json
import time

# import msgpack
# import io

# import asyncio
# from mqttconnector.client import MQTTClient
from ppmpmessage.v3.device_state import DeviceState

# from ppmpmessage.v3.device import Device
# from ppmpmessage.v3.util import machine_message_generator
# from ppmpmessage.v3.util import local_now
# from ppmpmessage.convertor.simple_variables import SimpleVariables
# from ppmpmessage.v3.device import Device
# from ppmpmessage.v3.device import iotHubDevice
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient

# from tcpconnector.tcpclient import TCPClient
# from tcpconnector.tcptarget import TCPTarget
# from tcpconnector.tcpclient import msgPayload
# from tcpconnector.tcpclient import msgPayloadType
# from tcpconnector.tcpclient import msgConnectionInfo
# from tcpconnector.tcpclient import connectionInfoType

from pathlib import Path
from threading import Thread
from tomlconfig.tomlutils import TomlParser

from statistics import mean, median

import statistics
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice

from homeautomationconnector.processbase import ProcessBase
from homeautomationconnector.sdmdevice.sdmdevice import SDM630Device

MQTT_TOPIC_PPMP = "mh" + "/+/" + "ppmp"

PROJECT_NAME = "homeautomationconnector"

# load configuration from config file
toml = TomlParser(f"{PROJECT_NAME}.toml")

MQTT_ENABLED = toml.get("mqtt.enabled", True)
MQTT_NETWORK_NAME = toml.get("mqtt.network_name", "mh")
MQTT_HOST = toml.get("mqtt.host", "localhost")
MQTT_PORT = toml.get("mqtt.port", 1883)
MQTT_USERNAME = toml.get("mqtt.username", "")
MQTT_PASSWORD = toml.get("mqtt.password", "")
MQTT_TLS_CERT = toml.get("mqtt.tls_cert", "")


LOGFOLDER = "./logs/"


# configure logging
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

try:
    os.mkdir(LOGFOLDER)
    logger.info(f"create logfolder: {LOGFOLDER}")
except OSError as error:
    logger.info(f"create logfolder: {LOGFOLDER}:{error}")
# fl = logging.FileHandler('OPC-UA.log')
# Rotation file handler miit 200 000 bytes pro file und 10 files in rotation
fl = RotatingFileHandler(
    f"{LOGFOLDER}{PROJECT_NAME}.log", mode="a", maxBytes=2 * (10**5), backupCount=10
)
fl.setLevel(logging.ERROR)
fl.setFormatter(formatter)
logger.addHandler(fl)


# list of all OPC-UA client processes


def main():
    deviceConfig: dict = {
        "mqtt.host": MQTT_HOST,
        "mqtt.port": MQTT_PORT,
        "mqtt.username": MQTT_NETWORK_NAME,
        "mqtt.password": MQTT_PASSWORD,
        "mqtt.tls_cert": MQTT_TLS_CERT,
        "mqtt.mqtt_devicename": "mqtt_devicename",
        "DeviceServiceNames": ["SDM630_1"],
        "LoggingLevel": 1,
    }

    mqttServiceDeviceClient = MQTTServiceDeviceClient(
        deviceKey="ServiceDeviceClient", deviceConfig=deviceConfig
    )

    processBase = ProcessBase(["SDM630_1"], mqttServiceDeviceClient)

    processBase.doWaitForInitialized()
    processBase.subScribeTopics()

    sdm630Device = SDM630Device("SDM630_1", mqttServiceDeviceClient)
    growattDevice = GrowattDevice("SDM630_1", mqttServiceDeviceClient)
 
    
    RefreshTime: int = 2
    while True:
        importedenergie = sdm630Device.get_import_energy_active()
        totalenergie = sdm630Device.get_total_power_active()

        l12_voltage = sdm630Device.get_l12_voltage()
        l23_voltage = sdm630Device.get_l23_voltage()
        l31_voltage = sdm630Device.get_l31_voltage()

        serialnumber = sdm630Device.get_serial_number()
        processBase.doProcess()

        time.sleep(RefreshTime)

    # globMQTTClient.subscribe(MQTT_TOPIC_PPMP, mqtt_producer)
    # start OPC-UA client(s)


if __name__ == "__main__":
    main()
