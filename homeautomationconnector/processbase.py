import time

from datetime import datetime, timezone
from tomlconfig.tomlutils import TomlParser
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient
from ppmpmessage.v3.device_state import DeviceState
from homeautomationconnector.daikindevice.daikin import DaikinDevice
from homeautomationconnector.gpiodevicehome.gpiodevicehome import GPIODeviceHomeAutomation
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice
from homeautomationconnector.helpers.timespan import TimeSpan
from homeautomationconnector.kebawallboxdevice.keykontactP30 import KeykontactP30
from homeautomationconnector.sdmdevice.sdmdevice import SDM630Device


class ProcessBase(object):
    def __init__(
        self,
        useddevices: dict = [],
        mqttDeviceClient: MQTTServiceDeviceClient = None,
        tomlParser: TomlParser = None,
    ):
        self.m_useddevices: dict = useddevices
        self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        self.m_mqttDeviceClient.AddnotityInfoStateFunction(self.notifyInfoStateFunction)
        self.m_subScribedMetaData: dict = {}
        self.m_DevicedoProcessing: dict = {}
        self.m_SDM630_WR: SDM630Device = None
        self.m_SDM630_WP: SDM630Device = None
        self.m_SDM630_WB: SDM630Device = None
        self.m_SPH_TL3_BH_UP: GrowattDevice = None
        self.m_kebaWallbox: KeykontactP30 = None
        self.m_DaikinWP: DaikinDevice = None
        self.m_tomlParser = tomlParser
        self.m_GPIODevice: GPIODeviceHomeAutomation = GPIODeviceHomeAutomation("GPIODevice", tomlParser)

        self.m_TimeSpan = TimeSpan()

        self.m_INVERTER_TEMPERATURE_FAN_ON = self.m_tomlParser.get(
            "homeautomation.INVERTER_TEMPERATURE_FAN_ON", 38
        )
        self.m_INVERTER_TEMPERATURE_FAN_OFF = self.m_tomlParser.get(
            "homeautomation.INVERTER_TEMPERATURE_FAN_OFF", 35
        )
        self.m_REFRESHTIME = self.m_tomlParser.get("mqttdevices.refresh_time", 2)

        for key in self.m_useddevices.keys():
            self.m_DevicedoProcessing[key] = False

    def notifyInfoStateFunction(self, hostname: str = "", infostate: str = ""):
        if infostate == DeviceState.OK.value:
            self.m_DevicedoProcessing[hostname] = True
            # self.subScribeTopics()
        if infostate == DeviceState.ERROR.value:
            self.m_DevicedoProcessing[hostname] = False
            # self.m_mqttDeviceClient.unsubscribeallTopics()

    #   sdm630Device = SDM630Device("SDM630_1", mqttServiceDeviceClient)
    #     growattDevice = GrowattDevice("SDM630_1", mqttServiceDeviceClient)

    def getProcessValues(self):


        if self.m_SPH_TL3_BH_UP != None:
           
            self._SPH_TL3_BH_UP_OnOff = self.m_SPH_TL3_BH_UP.get_OnOff()
            self._SPH_TL3_BH_UP_Ppv = self.m_SPH_TL3_BH_UP.get_Ppv()
            self._SPH_TL3_BH_UP_Ppv1 = self.m_SPH_TL3_BH_UP.get_Ppv1()
            self._SPH_TL3_BH_UP_Ppv2 = self.m_SPH_TL3_BH_UP.get_Ppv2()
            self._SPH_TL3_BH_UP_Pac = self.m_SPH_TL3_BH_UP.get_Pac()
            self._SPH_TL3_BH_UP_Pactogrid_total = (
                self.m_SPH_TL3_BH_UP.get_Pactogrid_total()
            )
            self._SPH_TL3_BH_UP_PLocalLoad_total = (
                self.m_SPH_TL3_BH_UP.get_PLocalLoad_total()
            )
            self._SPH_TL3_BH_UP_Pdischarge1 = self.m_SPH_TL3_BH_UP.get_Pdischarge1()
            self._SPH_TL3_BH_UP_Pcharge1 = self.m_SPH_TL3_BH_UP.get_Pcharge1()
            self._SPH_TL3_BH_UP_SOC = self.m_SPH_TL3_BH_UP.get_BMS_SOC()
            self._SPH_TL3_BH_UP_SOC_Min = self.m_SPH_TL3_BH_UP.get_SOC_Min()
            self._SPH_TL3_BH_UP_Inverter_Status = (
                self.m_SPH_TL3_BH_UP.get_Inverter_Status()
            )
            self._SPH_TL3_BH_UP_Temp1 = self.m_SPH_TL3_BH_UP.get_Temp1()
            self._SPH_TL3_BH_UP_Temp2 = self.m_SPH_TL3_BH_UP.get_Temp2()

            self._SPH_TL3_BH_UP_Temp3 = self.m_SPH_TL3_BH_UP.get_Temp3()

        if self.m_SDM630_WR != None:

            self._SDM630_WR_total_power_active = (
                self.m_SDM630_WR.get_total_power_active()
            )

        if self.m_SDM630_WP != None:

            self._SDM630_WP_total_power_active = (
                self.m_SDM630_WP.get_total_power_active()
            )

        if self.m_DaikinWP != None:

            
            self._DaikinWP_CLIMATE_hvac_mode = self.m_DaikinWP.get_CLIMATE_hvac_mode()
            self._DaikinWP_WATER_temperature = self.m_DaikinWP.get_WATER_temperature()
            self._DaikinWP_WATER_turn_on = self.m_DaikinWP.get_WATER_turn_on()
            self._DaikinWP_CLIMATE_turn_on = self.m_DaikinWP.get_CLIMATE_turn_on()
            self._DaikinWP_WATER_target_temperature = (
                self.m_DaikinWP.get_WATER_target_temperature()
            )
            self._DaikinWP_CLIMATE_target_temperature = (
                self.m_DaikinWP.get_CLIMATE_target_temperature()
            )
            self._DaikinWP_CLIMATE_temperature = (
                self.m_DaikinWP.get_CLIMATE_temperature()
            )

            self._DaikinWP_Sensor_OutsideTemperature = (
                self.m_DaikinWP.get_Sensor_OutsideTemperature()
            )
            self._DaikinWP_Sensor_LeavingWaterTemperatur = (
                self.m_DaikinWP.get_Sensor_LeavingWaterTemperature()
            )
            
        if self.m_kebaWallbox != None:
            if not self.m_DevicedoProcessing["kebaWallbox"]: return
            

            pass

    def doProcess_KebaWallbox(self):
        if self.m_kebaWallbox != None:
            if not self.m_DevicedoProcessing["kebaWallbox"]: return
        pass

    def doProcess_DaikinWP(self):
        if self.m_DaikinWP != None and self.m_SPH_TL3_BH_UP != None:
            if not self.m_DevicedoProcessing["DaikinWP"]: return
            if not self.m_DevicedoProcessing["SPH_TL3_BH_UP"]: return
            self.doProcess_ControlDaikinWP()
        pass
    
    def doProcess_SPH_TL3_BH_UP(self):
        if self.m_SPH_TL3_BH_UP != None:
            if not self.m_DevicedoProcessing["SPH_TL3_BH_UP"]: return
            self.doProcess_InverterTemperature()
        pass

    def doProcess_InverterTemperature(self):
        if self.m_SPH_TL3_BH_UP != None:
            # 0 == not in Subscibe List
            if self._SPH_TL3_BH_UP_Temp1 != 0:
                if self._SPH_TL3_BH_UP_Temp1 >= self.m_INVERTER_TEMPERATURE_FAN_ON:
                    self.m_GPIODevice.switch_InverterFan(True)

                if self._SPH_TL3_BH_UP_Temp1 <= self.m_INVERTER_TEMPERATURE_FAN_OFF:
                    self.m_GPIODevice.switch_InverterFan(False)

        pass

    def doProcess_ControlDaikinWP(self):
        if self.m_SPH_TL3_BH_UP != None:
            
            self._SPH_TL3_BH_UP_Pac = self.m_SPH_TL3_BH_UP.get_Pac()
            self._SPH_TL3_BH_UP_Pactogrid_total = (
                self.m_SPH_TL3_BH_UP.get_Pactogrid_total()
            )
            self._SPH_TL3_BH_UP_PLocalLoad_total = (
                self.m_SPH_TL3_BH_UP.get_PLocalLoad_total()
            )
            self._SPH_TL3_BH_UP_Pdischarge1 = self.m_SPH_TL3_BH_UP.get_Pdischarge1()
            self._SPH_TL3_BH_UP_Pcharge1 = self.m_SPH_TL3_BH_UP.get_Pcharge1()

        pass

    def doProcess(self):
        timestamp = datetime.now(timezone.utc).astimezone()
        difference_act = self.m_TimeSpan.getTimeSpantoActTime()
        hours_actsecs = self.m_TimeSpan.getTimediffernceintoSecs(difference_act)

        if hours_actsecs >= self.m_REFRESHTIME:
            self.m_TimeSpan.setActTime(timestamp)

            self.getProcessValues()

            self.doProcess_SPH_TL3_BH_UP()

    def setUsedDevices(self) -> None:
        if "SDM630_WR" in self.m_useddevices:
            self.m_SDM630_WR = self.m_useddevices["SDM630_WR"]
            self.m_DevicedoProcessing

        if "SDM630_WP" in self.m_useddevices:
            self.m_SDM630_WP = self.m_useddevices["SDM630_WP"]

        if "SDM630_WB" in self.m_useddevices:
            self.m_SDM630_WB = self.m_useddevices["SDM630_WB"]

        if "SDM630_WB" in self.m_useddevices:
            self.m_SDM630_WB = self.m_useddevices["SDM630_WB"]

        if "SPH_TL3_BH_UP" in self.m_useddevices:
            self.m_SPH_TL3_BH_UP = self.m_useddevices["SPH_TL3_BH_UP"]

        if "kebaWallbox" in self.m_useddevices:
            self.m_kebaWallbox = self.m_useddevices["kebaWallbox"]

        if "DaikinWP" in self.m_useddevices:
            self.m_DaikinWP = self.m_useddevices["DaikinWP"]

    def doWaitForInitialized(self) -> bool:
        self.m_mqttDeviceClient.doInit()

        state: bool = False
        while True:
            state = True
            for key in self.m_useddevices.keys():
                devstate = self.m_mqttDeviceClient.getdeviceStateByDevKey(devkey=key)
                if devstate != DeviceState.OK.value:
                    state = False
            if state:
                break
            else:
                time.sleep(0.5)

        return state

    def subScribeTopics(self) -> bool:
        def isDeviceinDeviceKeys(key="") -> bool:
            device = self.m_mqttDeviceClient.getdeviceByKey(key)
            if device in self.m_useddevices:
                return True
            return False

        self.m_subScribedMetaData = {}
        MetaData = self.m_mqttDeviceClient.getCompleteMetaData()
        self.m_subScribedMetaData = {
            key: value
            for key, value in MetaData.items()
            if isDeviceinDeviceKeys(key=key)
        }
        for key in self.m_subScribedMetaData.keys():
            self.m_mqttDeviceClient.subscribeTopicByKey(key)
