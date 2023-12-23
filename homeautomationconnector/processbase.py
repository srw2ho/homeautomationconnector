from enum import Enum
import json
import logging
import math
import time

from datetime import datetime, timezone
from tomlconfig.tomlutils import TomlParser
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient
from ppmpmessage.v3.device_state import DeviceState
from homeautomationconnector.daikindevice.daikin import DaikinDevice
from homeautomationconnector.gpiodevicehome.gpiodevicehome import (
    GPIODeviceHomeAutomation,
)
from ppmpmessage.v3.device import Device
from ppmpmessage.v3.util import local_now
from ppmpmessage.convertor.simple_variables import SimpleVariables
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice
from homeautomationconnector.helpers.timespan import TimeSpan
from homeautomationconnector.kebawallboxdevice.keykontactP30 import KeykontactP30
from homeautomationconnector.sdmdevice.sdmdevice import SDM630Device
from suntime import Sun, SunTimeException


SERVICE_DEVICE_NAME = "homemqttservice"
SERVICE_DEVICE_NETID = "homeconnector"
DEVICE_TYPE_CTRL = "homeconnector"

logger = logging.getLogger("root")


class SwitchONOff(Enum):
    ON = "ON"
    OFF = "OFF"
    Waiting_On = "Waiting_On"
    Waiting_Off = "Waiting_Off"

    def __getstate__(self):
        return self.value


class InverterStateONOff(Enum):
    UNDEF = -1
    ON = 1
    OFF = 0

    def __getstate__(self):
        return self.value


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

        self.m_today_sr = None
        self.m_today_ss = None
        self._SPH_TL3_BH_UP_OnOff = None

        self._SPH_TL3_BH_UP_OnOff = None
        self._DaikinWP_WATER_turn_onState = None
        self._SPH_TL3_BH_UP_Inverter_Status = None
        self._DaikinWP_WATER_turn_on = None
        self._DaikinWP_CLIMATE_turn_on = None
        self._DaikinWP_CLIMATE_temperature = None
        self._DaikinWP_WATER_target_temperature = None
        self._DaikinWP_CLIMATE_target_temperature = None
        self._DaikinWP_Sensor_OutsideTemperature = None
        self._DaikinWP_Sensor_LeavingWaterTemperatur = None
        self._DaikinWP_WATER_tank_state = None
        self._DaikinWP_WATER_temperature = None

        self.m_lastday = 0
        self.m_GPIODevice: GPIODeviceHomeAutomation = GPIODeviceHomeAutomation(
            "GPIODevice", tomlParser
        )

        self._DaikinWP_WATER_target_temperature_Saved = 0
        self._SPH_TL3_BH_UP_PLocalLoad_total = 0

        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF
        self._DaikinWP_CLIMATE_turn_onState = SwitchONOff.OFF

        self._SPH_TL3_BH_UP_Inverter_Status = 0

        self._PLocalLoad_Household = 0

        self.m_TimeSpan = TimeSpan()
        # self.m_TimeSpan_Sunrise = TimeSpan()
        self.m_TimeSpan_Daikin_Control_Water = TimeSpan()

        self.m_ctrldevice = Device(
            additionalData={
                "type": DEVICE_TYPE_CTRL,
                "hostname": SERVICE_DEVICE_NAME,
            },
        )

        ctrldevicenetid = f"{SERVICE_DEVICE_NAME}_{SERVICE_DEVICE_NETID}"

        self.m_ctrldevice.setNetId(ctrldevicenetid)
        self.m_ctrldevice.sethostNameByNetId(SERVICE_DEVICE_NETID)
        # PV_SURPLUS=1000
        # PV_SURPLUS_PERFORMANCE_MODE=3000
        self.m_PV_Surplus = self.m_tomlParser.get("daikin.PV_SURPLUS", 0)
        self.m_PV_Surplus_PerformanceMode = self.m_tomlParser.get(
            "daikin.PV_SURPLUS_PERFORMANCE_MODE", 0
        )

        self.m_PV_Surplus_Time_secs = self.m_tomlParser.get(
            "daikin.PV_SURPLUS_TIME_SECS", 0
        )
        self.m_PV_Surplus_Time_On_secs = self.m_tomlParser.get(
            "daikin.PV_SURPLUS_TIME_ON_SECS", 0
        )

        self.m_doProcessInverterStatus = self.m_tomlParser.get(
            "homeautomation.DO_PROCESS_INVERTER_STATUS", 0
        )

        self.m_MPPT_StartVoltage = self.m_tomlParser.get(
            "homeautomation.MPPT_StartVoltage", 120.0
        )

        self.m_doProcessDaikinControlWater = self.m_tomlParser.get(
            "homeautomation.DO_PROCESS_DAIKIN_CONTROL_WATER", 0
        )
        self.m_doProcessDaikinControlClimate = self.m_tomlParser.get(
            "homeautomation.DO_PROCESS_DAIKIN_CONTROL_CLIMATE", 0
        )

        self.m_INVERTER_TEMPERATURE_FAN_ON = self.m_tomlParser.get(
            "homeautomation.INVERTER_TEMPERATURE_FAN_ON", 38
        )
        self.m_INVERTER_TEMPERATURE_FAN_OFF = self.m_tomlParser.get(
            "homeautomation.INVERTER_TEMPERATURE_FAN_OFF", 35
        )
        self.m_REFRESHTIME = self.m_tomlParser.get("mqttdevices.refresh_time", 5.0)

        self.m_DAIKIN_USE_SMARTGRID_CONTACTS = self.m_tomlParser.get(
            "daikin.USE_SMARTGRID_CONTACTS", 0
        )
        self.m_LOCAL_LATIDUDE = self.m_tomlParser.get(
            "homeautomation.LOCAL_LATIDUDE", 49.30547
        )
        self.LOCAL_LONGITUDE = self.m_tomlParser.get(
            "homeautomation.LOCAL_LONGITUDE", 7.31442
        )

        for key in self.m_useddevices.keys():
            self.m_DevicedoProcessing[key] = False

        self.getsunrise_sunsetTime()

    def getsunrise_sunsetTime(self):
        try:
            sun = Sun(self.m_LOCAL_LATIDUDE, self.LOCAL_LONGITUDE)

            # Get today's sunrise and sunset in UTC
            self.m_today_sr = sun.get_sunrise_time().astimezone()
            self.m_today_ss = sun.get_sunset_time().astimezone()
            # self.m_today_sr = sun.get_sunrise_time()
            # self.m_today_ss = sun.get_sunset_time()
            logger.info(
                f"getsunrise_sunsetTime: sunrise: {self.m_today_sr.strftime('%m/%d/%Y, %H:%M:%S')} sunset:{self.m_today_ss.strftime('%m/%d/%Y, %H:%M:%S')}"
            )
        except SunTimeException as e:
            self.m_today_sr = None
            self.m_today_ss = None
            logger.error(f"getsunrise_sunsetTime error: {e}")
            # print("Error: {0}.".format(e))

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
            self._SPH_TL3_BH_UP_Vpv1 = self.m_SPH_TL3_BH_UP.get_Vpv1()
            self._SPH_TL3_BH_UP_Vpv2 = self.m_SPH_TL3_BH_UP.get_Vpv2()

            self._SPH_TL3_BH_UP_Pac = self.m_SPH_TL3_BH_UP.get_Pac()
            self._SPH_TL3_BH_UP_Pactogrid_total = (
                self.m_SPH_TL3_BH_UP.get_Pactogrid_total()
            )

            self._SPH_TL3_BH_UP_Pactouser_total = (
                self.m_SPH_TL3_BH_UP.get_Pactouser_total()
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

        if (self.m_SDM630_WP != None) and (self.m_SDM630_WR != None):
            self._SDM630_WR_total_power_active = (
                self.m_SDM630_WR.get_total_power_active()
            )

            self._SDM630_WP_total_power_active = (
                self.m_SDM630_WP.get_total_power_active()
            )

            if self._SPH_TL3_BH_UP_Pcharge1 > 0:
                pass

            self._PLocalLoad_Household = (
                self._SPH_TL3_BH_UP_PLocalLoad_total
                - self._SDM630_WP_total_power_active
            )

        if self.m_DaikinWP != None:
            self._DaikinWP_CLIMATE_hvac_mode = self.m_DaikinWP.get_CLIMATE_hvac_mode()
            self._DaikinWP_WATER_temperature = self.m_DaikinWP.get_WATER_temperature()
            self._DaikinWP_WATER_turn_on = self.m_DaikinWP.get_WATER_turn_on()
            self._DaikinWP_CLIMATE_turn_on = self.m_DaikinWP.get_CLIMATE_turn_on()
            self._DaikinWP_WATER_tank_state = self.m_DaikinWP.get_WATER_tank_state()

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
            if not self.m_DevicedoProcessing["kebaWallbox"]:
                return

            pass

    def doProcess_KebaWallbox(self):
        if self.m_kebaWallbox != None:
            if not self.m_DevicedoProcessing["kebaWallbox"]:
                return
        pass

    def doUnProcess_SPH_TL3_BH_UP(self):
        self.m_GPIODevice.switch_InverterFan(False)
        self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)

    def doProcess_DaikinWP(self):
        if self.m_DaikinWP != None and self.m_SPH_TL3_BH_UP != None:
            if not self.m_DevicedoProcessing["DaikinWP"]:
                return
            if not self.m_DevicedoProcessing["SPH_TL3_BH_UP"]:
                return
            self.doProcess_ControlDaikinWP()
        pass

    def doProcess_SPH_TL3_BH_UP(self):
        if self.m_SPH_TL3_BH_UP != None:
            if not self.m_DevicedoProcessing["SPH_TL3_BH_UP"]:
                self.doUnProcess_SPH_TL3_BH_UP()

            else:
                if self._SPH_TL3_BH_UP_Inverter_Status >= 0:
                    self.doProcess_InverterTemperature()

                    self.doProcess_InverterState()

    def doProcess_InverterTemperature(self):
        if self.m_SPH_TL3_BH_UP != None:
            # 0 == not in Subscibe List
            if self._SPH_TL3_BH_UP_Temp1 != 0:
                if self._SPH_TL3_BH_UP_Temp1 >= self.m_INVERTER_TEMPERATURE_FAN_ON:
                    state = self.m_GPIODevice.get_InverterFan()

                    if not state:
                        state = self.m_GPIODevice.switch_InverterFan(True)
                        logger.info(
                            f"doProcess_InverterState: switch_InverterFan(True)"
                        )

                if self._SPH_TL3_BH_UP_Temp1 <= self.m_INVERTER_TEMPERATURE_FAN_OFF:
                    state = self.m_GPIODevice.get_InverterFan()
                    if state:
                        state = self.m_GPIODevice.switch_InverterFan(False)

                        logger.info(
                            f"doProcess_InverterState: switch_InverterFan(False)"
                        )

    def doProcess_InverterState(self):
        if self.m_SPH_TL3_BH_UP != None:
            if self.m_doProcessInverterStatus > 0:
                if self.m_today_ss and self.m_today_sr:
                    # 0 == not in Subscibe List
                    timestamp = datetime.now(timezone.utc).astimezone()
                    timestamp_ss = self.m_today_ss
                    timestamp_sr = self.m_today_sr
                    # check for inverter zwischen sonnen-aufgang und sonnen-untergang
                    # inverter immer einschalten

                    InverterTimeOn = timestamp_sr <= timestamp <= timestamp_ss
                    if not InverterTimeOn:
                        InverterTimeOn = (
                            (self._SPH_TL3_BH_UP_Vpv1 > self.m_MPPT_StartVoltage * 3.0)
                            and (
                                self._SPH_TL3_BH_UP_Vpv2
                                > self.m_MPPT_StartVoltage * 3.0
                            )
                            and self._SDM630_WR_total_power_active > 0
                        )

                    # zwischen Sonnenauf und Sonneununtergang oder bei hoher MPPT-Spannung
                    if InverterTimeOn:
                        if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                            self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                            logger.info(f"doProcess_InverterState: set_OnOff(1)")

                    else:
                        if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.ON.value:
                            # keine Leistung vom WR
                            if (
                                self._SPH_TL3_BH_UP_Vpv1 < self.m_MPPT_StartVoltage
                            ) and (self._SPH_TL3_BH_UP_Vpv2 < self.m_MPPT_StartVoltage):
                                if (
                                    self._SPH_TL3_BH_UP_SOC_Min * 0.8
                                    <= self._SPH_TL3_BH_UP_SOC
                                    <= self._SPH_TL3_BH_UP_SOC_Min
                                ):
                                    if self._SDM630_WR_total_power_active < 0:
                                        self.m_SPH_TL3_BH_UP.set_OnOff(
                                            InverterStateONOff.OFF.value
                                        )
                                        logger.info(
                                            f"doProcess_InverterState: set_OnOff(0)"
                                        )
                else:
                    if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                        self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                        logger.info(f"doProcess_InverterState: set_OnOff(0)")

            else:
                if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                    self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                    logger.info(f"doProcess_InverterState: set_OnOff(0)")

    def doProcess_ControlDaikinWater(self, timestamp):
        # self.m_TimeSpan_Daikin_Control_Water
        if self.m_doProcessDaikinControlWater > 0:
            if self._DaikinWP_WATER_turn_on:
                if self._DaikinWP_WATER_turn_onState == SwitchONOff.OFF:
                    # PV Überschuss, Tank-Temperatur kleiner Max Temperatur
                    #
                    # wir speisen zur Zeit ein
                    if self._SPH_TL3_BH_UP_Pactogrid_total > self.m_PV_Surplus:
                        self.m_TimeSpan_Daikin_Control_Water.setActTime(timestamp)
                        # stop_time = timestamp + datetime.timedelta(minutes=10)
                        # self.m_TimeSpan_Daikin_Control_Water.setStopTime(stop_time)
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.Waiting_On
                        logger.info(
                            f"doProcess_ControlDaikinWater: {self._SPH_TL3_BH_UP_Pactogrid_total} > {self.m_PV_Surplus} "
                        )

                elif self._DaikinWP_WATER_turn_onState == SwitchONOff.Waiting_On:
                    # PV Überschuss, Tank-Temperatur kleiner Max Temperatur
                    #
                    difference = (
                        self.m_TimeSpan_Daikin_Control_Water.getTimeSpantoActTime()
                    )
                    difference_secs = (
                        self.m_TimeSpan_Daikin_Control_Water.getTimediffernceintoSecs(
                            difference
                        )
                    )

                    if self._SPH_TL3_BH_UP_Pactogrid_total > self.m_PV_Surplus:
                        # wir speisen zur Zeit ein
                        if difference_secs >= self.m_PV_Surplus_Time_secs:
                            if (
                                self._DaikinWP_WATER_temperature
                                < self.m_DaikinWP.get_WATER_max_temp()
                            ):
                                self._DaikinWP_WATER_target_temperature_Saved = (
                                    self._DaikinWP_WATER_target_temperature
                                )

                                if self.m_DAIKIN_USE_SMARTGRID_CONTACTS:
                                    logger.info(
                                        f"doProcess_ControlDaikinWater: activate Smart Grid"
                                    )
                                    self.m_GPIODevice.switch_SmartGridWP(
                                        state_grid_1=1, state_grid_2=1
                                    )
                                else:
                                    # if (
                                    #     self._DaikinWP_WATER_temperature
                                    #     > self._DaikinWP_WATER_target_temperature
                                    # ):
                                    #     WATER_max_temp = (
                                    #         self._DaikinWP_WATER_temperature + 5
                                    #     )
                                    # else:
                                    #     WATER_max_temp = (
                                    #         self._DaikinWP_WATER_target_temperature + 5
                                    #     )
                                    WATER_max_temp = (
                                            self._DaikinWP_WATER_temperature + 5
                                        )
                                    if (
                                        self._SPH_TL3_BH_UP_Pactogrid_total
                                        > self.m_PV_Surplus_PerformanceMode
                                    ):
                                        execute = self.m_DaikinWP.set_WATER_tank_state(
                                            "performance"
                                        )
                                        logger.info(
                                            f"doProcess_ControlDaikinWater: activate performance Mode"
                                        )

                                    execute = (
                                        self.m_DaikinWP.set_WATER_target_temperature(
                                            WATER_max_temp
                                        )
                                    )
                                    logger.info(
                                        f"doProcess_ControlDaikinWater: set_WATER_target_temperature({WATER_max_temp})"
                                    )
                            self.m_TimeSpan_Daikin_Control_Water.setActTime(timestamp)
                            self._DaikinWP_WATER_turn_onState = SwitchONOff.ON

                    else:
                        logger.info(
                            f"doProcess_ControlDaikinWater: {self._SPH_TL3_BH_UP_Pactogrid_total} < {self.m_PV_Surplus}"
                        )
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

                elif self._DaikinWP_WATER_turn_onState == SwitchONOff.ON:
                    difference = (
                        self.m_TimeSpan_Daikin_Control_Water.getTimeSpantoActTime()
                    )
                    difference_secs = (
                        self.m_TimeSpan_Daikin_Control_Water.getTimediffernceintoSecs(
                            difference
                        )
                    )
                    doCancel = False
                    if (
                        self._DaikinWP_WATER_temperature
                        >= self._DaikinWP_WATER_target_temperature
                    ):
                        doCancel = True

                    actpowerWR = (
                        self._SDM630_WR_total_power_active
                        - self._SPH_TL3_BH_UP_Pdischarge1
                        - self._SDM630_WP_total_power_active
                    )

                    if actpowerWR < 100 or self._SPH_TL3_BH_UP_Pactouser_total > 0:
                        if difference_secs >= self.m_PV_Surplus_Time_On_secs:
                            doCancel = True
                    else:
                        if actpowerWR > 100:
                            self.m_TimeSpan_Daikin_Control_Water.setActTime(timestamp)

                    logger.info(
                        f"doProcess_ControlDaikinWater: actual Power WR:{actpowerWR} = ( {self._SDM630_WR_total_power_active}- actual Discharge: {self._SPH_TL3_BH_UP_Pdischarge1} - actual Power WP:{ self._SDM630_WP_total_power_active})"
                    )

                    if actpowerWR < (self.m_PV_Surplus_PerformanceMode / 10.0):
                        # von performance to normal setzen
                        if self._DaikinWP_WATER_tank_state == "performance":
                            execute = self.m_DaikinWP.set_WATER_tank_state("heat_pump")
                            logger.info(
                                f"doProcess_ControlDaikinWater: deactivate performance Mode"
                            )

                    if doCancel:
                        if self.m_DAIKIN_USE_SMARTGRID_CONTACTS:
                            self.m_GPIODevice.switch_SmartGridWP(
                                state_grid_1=0, state_grid_2=0
                            )
                            logger.info(
                                f"doProcess_ControlDaikinWater: deactivate Smart Grid"
                            )
                        else:
                            execute = self.m_DaikinWP.set_WATER_target_temperature(
                                self._DaikinWP_WATER_target_temperature_Saved
                            )
                            if self._DaikinWP_WATER_tank_state == "performance":
                                execute = self.m_DaikinWP.set_WATER_tank_state(
                                    "heat_pump"
                                )
                                logger.info(
                                    f"doProcess_ControlDaikinWater: deactivate performance Mode"
                                )

                            logger.info(
                                f"doProcess_ControlDaikinWater: set_WATER_target_temperature({self._DaikinWP_WATER_target_temperature_Saved})"
                            )
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

    def doProcess_ControlDaikinClimate(self, timestamp):
        if self.m_doProcessDaikinControlClimate > 0:
            if self._DaikinWP_CLIMATE_turn_on:
                if self._DaikinWP_CLIMATE_turn_onState == SwitchONOff.OFF:
                    pass
                    # PV Überschuss, Tank-Temperatur kleiner Max Temperatur
                    #

                    # self._DaikinWP_CLIMATE_turn_onState == SwitchONOff.ON

                elif self._DaikinWP_CLIMATE_turn_onState == SwitchONOff.ON:
                    # self._DaikinWP_CLIMATE_turn_onState == SwitchONOff.OFF
                    pass

    def doProcess_ControlDaikinWP(self, timestamp):
        if self.m_SPH_TL3_BH_UP != None:
            # Water-Turn-Betrieb

            # self._SPH_TL3_BH_UP_Pactogrid_total
            # self._SPH_TL3_BH_UP_PLocalLoad_total
            self.doProcess_ControlDaikinWater(timestamp)
            self.doProcess_ControlDaikinClimate(timestamp)

    def getTopicByKey(self, key: str) -> str:
        topic = f"mh/{SERVICE_DEVICE_NAME}/{SERVICE_DEVICE_NETID}/data/{key}"

        return topic

    def getMetaKeyByKey(self, key: str) -> str:
        return f"@{SERVICE_DEVICE_NETID}.{key}"

    def getActTime(self):
        timestamp = datetime.now(timezone.utc).astimezone()
        posix_timestamp = datetime.timestamp(timestamp) * 1000
        return posix_timestamp

    def getPayloadfromValue(self, identifier: str, value: any) -> dict:
        try:
            payload = {}
            payload = {
                "metakey": self.getMetaKeyByKey(identifier),
                "identifier": identifier,
                "posix_timestamp": self.getActTime(),
                "value": value,
            }

        finally:
            return payload

    def doPublishPayload(self, jsonpayload: dict, retained: bool = False):
        try:
            if self.m_mqttDeviceClient.getMQTTClient().isConnected():
                changedPayload = {
                    k: self.getPayloadfromValue(k, v)
                    for k, v in jsonpayload.items()
                    # if isValueChanged(k, v)
                }

                # write changed Values over MQTT
                for k, v in changedPayload.items():
                    try:
                        self.m_mqttDeviceClient.getMQTTClient().publish(
                            self.getTopicByKey(k),
                            json.dumps(v),
                            retain=retained,
                        )
                    except Exception as e:
                        logger.error(f"doPublishPayload: publish : Error->{e}")

                acttime = local_now()
                simplevars = SimpleVariables(self.m_ctrldevice, jsonpayload, acttime)
                ppmppayload = simplevars.to_ppmp()
                self.m_mqttDeviceClient.getMQTTClient().publish(
                    self.m_ctrldevice.ppmp_topic(), ppmppayload, retain=False
                )

                # if len(changedPayload.keys()) > 0:
                #     self.m_lastMQTTPayload.update(jsonpayload)
            else:
                logger.error(f"doPublishPayload: error-> MQTT is not connected")
        except Exception as e:
            logger.error(f"doPublishPayload: error:{e}")

    def doProcess(self):
        timestamp = datetime.now(timezone.utc).astimezone()
        difference_act = self.m_TimeSpan.getTimeSpantoActTime()
        hours_actsecs = self.m_TimeSpan.getTimediffernceintoSecs(difference_act)

        # difference_act_Sunrise = self.m_TimeSpan_Sunrise.getTimeSpantoActTime()
        # hours_actsecs_Sunrise = self.m_TimeSpan_Sunrise.getTimediffernceintoHours(
        #     difference_act_Sunrise
        # )

        actualday = timestamp.day

        # all 5 hourse get sunrise/sunset time
        if self.m_lastday != actualday:
            self.getsunrise_sunsetTime()
            self.m_lastday = actualday
            # self.m_TimeSpan_Sunrise.setActTime(timestamp)

        #  val = 0 if ret == None else ret  # Requires Python version >= 2.5
        if hours_actsecs >= self.m_REFRESHTIME:
            payload = {
                "CPU_Temperature": self.m_GPIODevice.getCpuTemperature(),
                "is_PVSurplus": self.m_GPIODevice.is_PVSurplus(),
                "is_WPClimateOn": self.m_GPIODevice.is_WPClimateOn(),
                "SPH_TL3_BH_UP_OnOff": 0
                if self._SPH_TL3_BH_UP_OnOff == None
                else self._SPH_TL3_BH_UP_OnOff,
                "DaikinWP_WATER_turn_on": False
                if self._DaikinWP_WATER_turn_on == None
                else self._DaikinWP_WATER_turn_on,
                "DaikinWP_CLIMATE_turn_on": False
                if self._DaikinWP_CLIMATE_turn_on == None
                else self._DaikinWP_CLIMATE_turn_on,
                "SPH_TL3_BH_UP_Inverter_Status": 0
                if self._SPH_TL3_BH_UP_Inverter_Status == None
                else self._SPH_TL3_BH_UP_Inverter_Status,
                "DaikinWP_WATER_tank_state": ""
                if self._DaikinWP_WATER_tank_state == None
                else self._DaikinWP_WATER_tank_state,
                "DaikinWP_WATER_temperature": 0.0
                if self._DaikinWP_WATER_temperature == None
                else self._DaikinWP_WATER_temperature,
                "DaikinWP_CLIMATE_temperature": 0
                if self._DaikinWP_CLIMATE_temperature == None
                else self._DaikinWP_CLIMATE_temperature,
                "DaikinWP_WATER_target_temperature": 0.0
                if self._DaikinWP_WATER_target_temperature == None
                else self._DaikinWP_WATER_target_temperature,
                "DaikinWP_CLIMATE_target_temperature": 0.0
                if self._DaikinWP_CLIMATE_target_temperature == None
                else self._DaikinWP_CLIMATE_target_temperature,
                "DaikinWP_Sensor_OutsideTemperature": 0
                if self._DaikinWP_Sensor_OutsideTemperature == None
                else self._DaikinWP_Sensor_OutsideTemperature,
                "DaikinWP_Sensor_LeavingWaterTemperatur": 0
                if self._DaikinWP_Sensor_LeavingWaterTemperatur == None
                else self._DaikinWP_Sensor_LeavingWaterTemperatur,
                "sunrise": ""
                if self.m_today_sr == None
                else self.m_today_sr.strftime("%Y-%m-%d, %H:%M:%S"),
                "sunset": ""
                if self.m_today_ss == None
                else self.m_today_ss.strftime("%Y-%m-%d, %H:%M:%S"),
            }

            self.doPublishPayload(payload)

            self.m_TimeSpan.setActTime(timestamp)

            self.getProcessValues()

            self.doProcess_SPH_TL3_BH_UP()

            self.doProcess_ControlDaikinWP(timestamp)

            # else:
            #     if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF:
            #         self.m_SPH_TL3_BH_UP.set_OnOff(self, InverterStateONOff.ON)

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
