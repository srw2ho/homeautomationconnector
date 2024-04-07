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
from homeautomationconnector.gpiodevicehome.gpiodevicehome import GPIODeviceHomeAutomation
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice
from homeautomationconnector.kebawallboxdevice.keykontactP30 import KeykontactP30
from homeautomationconnector.modbusdevicebase import ModBusDeviceBase
from homeautomationconnector.espaltherma.espalthermadevice import ESPAltherma
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


MQTTDEVICELIST = toml.get("mqttdevices.DEVICELIST", [""])

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

# def http_error(status):
#     match status:
# case 400:
# return "Bad request"
# case 404:
# return "Not found"
# case 418:
# return "I'm a teapot"

# # If an exact match is not confirmed, this last case will be used if provided
# case _:
# return "Something's wrong with the internet"


def createDeviceByKey(
    key: str, mqttServiceDeviceClient: MQTTServiceDeviceClient
) -> ModBusDeviceBase:
    # Wechselrichter SDM
    if key == "SDM630_WR":
        SDM630_WR = SDM630Device("SDM630_WR", mqttServiceDeviceClient)
        return SDM630_WR
    # Wärmepumpe SDM
    if key == "SDM630_WP":
        SDM630_WP = SDM630Device("SDM630_WP", mqttServiceDeviceClient)
        return SDM630_WP

    # Wallbox SDM
    if key == "SDM630_WB":
        SDM630_WB = SDM630Device("SDM630_WB", mqttServiceDeviceClient)
        return SDM630_WB

    # Growatt Inverter SPH_TL3_BH_UP
    if key == "SPH_TL3_BH_UP":
        SPH_TL3_BH_UP = GrowattDevice("SPH_TL3_BH_UP", mqttServiceDeviceClient)
        return SPH_TL3_BH_UP
    # Wallbox SDM
    if key == "kebaWallbox":
        kebaWallbox = KeykontactP30("kebaWallbox", mqttServiceDeviceClient)
        return kebaWallbox
    if key == "DaikinWP":
        DaikinWP = DaikinDevice("DaikinWP", mqttServiceDeviceClient)
        return DaikinWP
    
    if key == "ESPAltherma":
        espAltherma = ESPAltherma("ESPAltherma", mqttServiceDeviceClient)
        return espAltherma
    
    return None

def main():
    activate_logging = toml.get("mqttdevices.activate_logging", 0)
    deviceConfig: dict = {
        "mqtt.host": MQTT_HOST,
        "mqtt.port": MQTT_PORT,
        "mqtt.username": MQTT_NETWORK_NAME,
        "mqtt.password": MQTT_PASSWORD,
        "mqtt.tls_cert": MQTT_TLS_CERT,
        "mqtt.mqtt_devicename": "mqtt_devicename",
        "DeviceServiceNames": MQTTDEVICELIST,
        "LoggingLevel": activate_logging,
    }

    mqttServiceDeviceClient = MQTTServiceDeviceClient(
        deviceKey="ServiceDeviceClient", deviceConfig=deviceConfig
    )

    # # Wechselrichter SDM
    # SDM630_WR = SDM630Device("SDM630_WR", mqttServiceDeviceClient)
    # # Wärmepumpe SDM
    # SDM630_WP = SDM630Device("SDM630_WP", mqttServiceDeviceClient)

    # # Wallbox SDM
    # SDM630_WB = SDM630Device("SDM630_WB", mqttServiceDeviceClient)

    # # Growatt Inverter SPH_TL3_BH_UP
    # SPH_TL3_BH_UP = GrowattDevice("SPH_TL3_BH_UP", mqttServiceDeviceClient)
    # # Wallbox SDM
    # kebaWallbox = KeykontactP30("kebaWallbox", mqttServiceDeviceClient)

    # DaikinWP = DaikinDevice("DaikinWP", mqttServiceDeviceClient)
    # # gpioDevice = GPIODevice("GPIODevice")

    RefreshTime: int = 2

    useddevices: dict = {
        device: createDeviceByKey(device, mqttServiceDeviceClient)
        for device in MQTTDEVICELIST
    }

    # useddevices["SDM630_WR"] = SDM630_WR
    # useddevices["SDM630_WP"] = SDM630_WP
    # useddevices["DaikinWP"] = DaikinWP
    # useddevices["SPH_TL3_BH_UP"] = SPH_TL3_BH_UP
    # useddevices["SDM630_WB"] = SDM630_WB
    # useddevices["GrowattWr"] = GrowattWr
    # useddevices["kebaWallbox"] = kebaWallbox

    processBase = ProcessBase(useddevices, mqttServiceDeviceClient, toml)

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

        time.sleep(0.2)

    # globMQTTClient.subscribe(MQTT_TOPIC_PPMP, mqtt_producer)
    # start OPC-UA client(s)


if __name__ == "__main__":
    main()
