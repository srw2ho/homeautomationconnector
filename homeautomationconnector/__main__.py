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
from homeautomationconnector.daikindevice.daikin import DaikinDevice
from homeautomationconnector.gpiodevice.gpiodevice import GPIODevice
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice
from homeautomationconnector.kebawallboxdevice.keykontactP30 import KeykontactP30

from homeautomationconnector.processbase import ProcessBase
from homeautomationconnector.sdmdevice.sdmdevice import SDM630Device
# from homeautomationconnector.gpiodevice import G

# from gpiozero import Button, LED

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
    if not os.path.exists(LOGFOLDER):
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
        "DeviceServiceNames": [
            "SDM630_WR",
            "SDM630_WP",
            # "SDM630_WB",
            "DaikinWP",
            "SPH_TL3_BH_UP",
        ],
        "LoggingLevel": 1,
    }

    mqttServiceDeviceClient = MQTTServiceDeviceClient(
        deviceKey="ServiceDeviceClient", deviceConfig=deviceConfig
    )

    # Wechselrichter SDM
    SDM630_WR = SDM630Device("SDM630_WR", mqttServiceDeviceClient)
    # Wärmepumpe SDM
    SDM630_WP = SDM630Device("SDM630_WP", mqttServiceDeviceClient)

    # Wallbox SDM
    SDM630_WB = SDM630Device("SDM630_WB", mqttServiceDeviceClient)

    # Growatt Inverter SPH_TL3_BH_UP
    SPH_TL3_BH_UP = GrowattDevice("SPH_TL3_BH_UP", mqttServiceDeviceClient)
    # Wallbox SDM
    kebaWallbox = KeykontactP30("kebaWallbox", mqttServiceDeviceClient)

    DaikinWP = DaikinDevice("DaikinWP", mqttServiceDeviceClient)
    # gpioDevice = GPIODevice("GPIODevice")
        

    RefreshTime: int = 2
    useddevices: dict = {}
    useddevices["SDM630_WR"] = SDM630_WR
    useddevices["SDM630_WP"] = SDM630_WP
    useddevices["DaikinWP"] = DaikinWP
    useddevices["SPH_TL3_BH_UP"] = SPH_TL3_BH_UP
    # useddevices["SDM630_WB"] = SDM630_WB
    # useddevices["GrowattWr"] = GrowattWr
    # useddevices["kebaWallbox"] = kebaWallbox

    processBase = ProcessBase(useddevices, mqttServiceDeviceClient,toml)

    processBase.doWaitForInitialized()
    processBase.subScribeTopics()
    processBase.setUsedDevices()
    

    while True:
        # importedenergie = SDM630_WR.get_import_energy_active()
        # totalenergie = SDM630_WR.get_total_power_active()

        # l12_voltage = SDM630_WR.get_l12_voltage()
        # l23_voltage = SDM630_WR.get_l23_voltage()
        # l31_voltage = SDM630_WR.get_l31_voltage()

        # serialnumber = SDM630_WR.get_serial_number()
        processBase.doProcess()

        time.sleep(RefreshTime)

    # globMQTTClient.subscribe(MQTT_TOPIC_PPMP, mqtt_producer)
    # start OPC-UA client(s)


if __name__ == "__main__":
    main()
