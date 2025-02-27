from enum import Enum
import json
import logging
import math
import time

from datetime import datetime, timezone, timedelta
from tomlconfig.tomlutils import TomlParser
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient
from ppmpmessage.v3.device_state import DeviceState
from homeautomationconnector.daikindevice.daikin import DaikinDevice
from homeautomationconnector.espaltherma.espalthermadevice import ESPAltherma
from homeautomationconnector.gpiodevicehome.gpiodevicehome import (
    GPIODeviceHomeAutomation,
)
from ppmpmessage.v3.device import Device
from ppmpmessage.v3.util import local_now
from ppmpmessage.convertor.simple_variables import SimpleVariables
from homeautomationconnector.growattdevice.growattdevice import GrowattDevice
from homeautomationconnector.helpers.flyingaverage import FlyingAverage
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


class InverterState(Enum):
    WORKING_STATE = 0
    Normal = 5
    Normal_NoPV = 6
    Standby = 0
    Selftest = 1

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
        # self.m_DaikinWP: DaikinDevice = None
        self.m_ESPAltherma: ESPAltherma = None
        self.m_tomlParser = tomlParser

        self.m_today_sr = None
        self.m_today_ss = None

        self._SDM630_WP_total_power_active = 0.0

        self._SDM630_WP_import_energy_active = 0.0

        self.m_lastday = 0
        self.m_GPIODevice: GPIODeviceHomeAutomation = GPIODeviceHomeAutomation(
            "GPIODevice", tomlParser
        )

        self._DaikinWP_WATER_target_temperature_Saved = 0
        self._SDM630_WP_start_import_energy_active = 0.0
        self._availablepowerWR = 0.0
        self.WP_WATER_consume_energy = 0.0
        self._DaikinWP_WATER_Cancel_from_WP = False
        # Daikin Default-Values
        # self._DaikinWP_CLIMATE_hvac_mode = ""
        # self._DaikinWP_WATER_temperature = 0
        # self._DaikinWP_WATER_turn_on = False
        # self._DaikinWP_CLIMATE_turn_on = False
        # self._DaikinWP_WATER_tank_state = ""

        self._SPH_TL3_BH_UP_OnOff = 1
        self._SPH_TL3_BH_UP_Inverter_Status = 0
        # self._DaikinWP_WATER_tank_state = ""
        # self._DaikinWP_WATER_temperature = 0.0
        # self._DaikinWP_CLIMATE_temperature = 0
        # self._DaikinWP_Sensor_OutsideTemperature = 0
        # self._DaikinWP_Sensor_LeavingWaterTemperatur = 0

        # self._DaikinWP_WATER_target_temperature = 45
        # self._DaikinWP_CLIMATE_target_temperature = 0
        # self._DaikinWP_CLIMATE_temperature = 0

        # self._DaikinWP_Sensor_OutsideTemperature = 0
        # self._DaikinWP_Sensor_LeavingWaterTemperatur = 0

        # Daikin Default-Values

        self._SPH_TL3_BH_UP_Pactogrid_total_average = FlyingAverage(stack_size=5)

        self._SPH_TL3_BH_UP_Pdischarge1_average = FlyingAverage(stack_size=5)

        self._SDM630_WR_total_power_active_average = FlyingAverage(stack_size=5)

        self._SDM630_WP_total_power_active_average = FlyingAverage(stack_size=5)

        self.m_ESPAltherma_Flow_sensor_l_min_average = FlyingAverage(stack_size=5)
        self.m_ESPAltherma_INV_primary_current_average = FlyingAverage(stack_size=5)

        self.m_ESPAltherma_operation_mode = ""
        self.m_ESPAltherma_INV_Heat_Energy = float(0.0)
        self.m_ESPAltherma_INV_Heat_COP = float(0.0)
        self.m_ESPAltherma_INV_electric_HeatEnergy = float(0.0)

        self.m_ESPAltherma_INV_DHW_Energy = float(0.0)
        self.m_ESPAltherma_INV_DHW_COP = float(0.0)
        self.m_ESPAltherma_INV_electric_DHWEnergy = float(0.0)

        self.m_ESPAltherma_I_U_operation_mode = ""
        self.m_ESPAltherma_Thermostat_ON_OFF = ""

        self.m_ESPAltherma_Defrost_Operation = ""

        self.m_ESPAltherma_HPSU_Bypass_valve_position = 0
        self.m_ESPAltherma_HPSU_Tank_valve_position = 0
        self.m_ESPAltherma_HPSU_Mixed_leaving_water_R7T_DLWA2 = float(0.0)
        self.m_ESPAltherma_Water_pump_signal = 0
        self.m_ESPAltherma_Water_pressure = float(0.0)
        self.m_ESPAltherma_Flow_sensor_l_min = float(0.0)

        self.m_ESPAltherma_INV_primary_current = float(0.0)

        self.m_ESPAltherma_DHW_tank_temp_R5T = float(0.0)
        self.m_ESPAltherma_Inlet_water_temp_R4T = float(0.0)
        self.m_ESPAltherma_Refrig_Temp_liquid_side_R3T = float(0.0)
        self.m_ESPAltherma_Leaving_water_temp_BUH_R2T = float(0.0)
        self.m_ESPAltherma_Leaving_water_temp_BUH_R1T = float(0.0)
        self.m_ESPAltherma_DHW_setpoint = float(0.0)
        self.m_ESPAltherma_LW_setpoint_main = float(0.0)
        self.m_ESPAltherma_INV_frequency_rps = float(0.0)

        # self._DaikinWP_WATER_Start_temperature = 0
        self._SPH_TL3_BH_UP_PLocalLoad_total = 0

        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF
        self._DaikinWP_CLIMATE_turn_onState = SwitchONOff.OFF

        self._SPH_TL3_BH_UP_Inverter_Status = 0

        self._PLocalLoad_Household = 0

        self.m_TimeSpan_InverterState = TimeSpan()
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

        self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)
        self.m_GPIODevice.set_enableHeating(False)

        self.m_PV_Surplus = self.m_tomlParser.get("daikin.PV_SURPLUS", 0)
        # self.m_PV_Surplus_PerformanceMode = self.m_tomlParser.get(
        #     "daikin.PV_SURPLUS_PERFORMANCE_MODE", 0
        # )

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
        self.m_LOCAL_LONGITUDE = self.m_tomlParser.get(
            "homeautomation.LOCAL_LONGITUDE", 7.31442
        )

        self.m_PV_MAX_WATER_CONSUME_ENERGY = self.m_tomlParser.get(
            "daikin.PV_MAX_WATER_CONSUME_ENERGY", 1.0
        )

        self.m_PV_MIN_WATER_CONSUME_ENERGY = self.m_tomlParser.get(
            "daikin.PV_MIN_WATER_CONSUME_ENERGY", 0.5
        )

        # Sollwert unter welchem die Wasseraufbereitung  gestartet wird
        self.m_MIN_WATER_TEMPERATURE = self.m_tomlParser.get(
            "daikin.MIN_WATER_TEMPERATURE", 60.0
        )

        # Sollwert ab welcher noch die Wasseraufbereitung abgebruchen wird
        self.m_MAX_WATER_TEMPERATURE = self.m_tomlParser.get(
            "daikin.MAX_WATER_TEMPERATURE", 65.0
        )

        # self.m_USE_DAIKIN_API = self.m_tomlParser.get("daikin.USE_DAIKIN_API", 0)
        self.m_USE_ALTHERMA_API = self.m_tomlParser.get("daikin.USE_ALTHERMA_API", 1)

        for key in self.m_useddevices.keys():
            self.m_DevicedoProcessing[key] = False

        self.getsunrise_sunsetTime()
        


    def getsunrise_sunsetTime(self):
        try:
            
            # get_timestamp = datetime.now(timezone.utc).astimezone()

            
            get_timestamp = datetime.now(timezone.utc).astimezone()

            sun = Sun(self.m_LOCAL_LATIDUDE, self.m_LOCAL_LONGITUDE)

            # Get today's sunrise and sunset in UTC
            # BugFixing Sunset Time  one day behind Sunrise Time is wrong
            
            self.m_today_sr = sun.get_sunrise_time(at_date=get_timestamp).astimezone()
            self.m_today_ss = sun.get_sunset_time(at_date=get_timestamp).astimezone()


            # workaround bugfix: m_today_ss is one day before
            if self.m_today_sr > self.m_today_ss:
                logger.info(
                    f"getsunrise_sunsetTime: sunrise time: {self.m_today_sr.strftime('%m/%d/%Y, %H:%M:%S')} greater than sunset time:{self.m_today_ss.strftime('%m/%d/%Y, %H:%M:%S')}"
                )
                self.m_today_ss = self.m_today_ss + timedelta(days=1)
             

            if get_timestamp.day > self.m_today_sr.day:
                logger.info(
                    f"getsunrise_sunsetTime: sunrise time: {self.m_today_sr.strftime('%m/%d/%Y, %H:%M:%S')} not in getting time interval:{get_timestamp.strftime('%m/%d/%Y, %H:%M:%S')}"
                )
                self.m_today_sr = self.m_today_sr + timedelta(days=1)
               

            if get_timestamp.day > self.m_today_ss.day:
                logger.info(
                    f"getsunrise_sunsetTime: sunrise time: {self.m_today_ss.strftime('%m/%d/%Y, %H:%M:%S')} not in getting time interval:{get_timestamp.strftime('%m/%d/%Y, %H:%M:%S')}"
                )
                self.m_today_ss = self.m_today_ss + timedelta(days=1)

            # only for tesiting
            # self.m_today_ss = self.m_today_ss - timedelta(days=1)
            # self.m_today_sr = self.m_today_sr - timedelta(days=1)

            # self.m_today_sr = sun.get_sunrise_time()
            # self.m_today_ss = sun.get_sunset_time()
            logger.info(
                f"getsunrise_sunsetTime: actual time: {get_timestamp.strftime('%m/%d/%Y, %H:%M:%S')} sunrise time: {self.m_today_sr.strftime('%m/%d/%Y, %H:%M:%S')} sunset time:{self.m_today_ss.strftime('%m/%d/%Y, %H:%M:%S')}"
            )
        except SunTimeException as e:
            self.m_today_sr = None
            self.m_today_ss = None
            logger.error(f"getsunrise_sunsetTime error: {e}")
            # print("Error: {0}.".format(e))

    def notifyInfoStateFunction(self, hostname: str = "", infostate: str = ""):
        if infostate == DeviceState.OK.value:
            self.m_DevicedoProcessing[hostname] = True
            if hostname == "SPH_TL3_BH_UP":
                self._SPH_TL3_BH_UP_Pactogrid_total_average.reset()
                self._SPH_TL3_BH_UP_Pdischarge1_average.reset()
               

            if hostname == "SDM630_WR":
                self._SDM630_WR_total_power_active_average.reset()
            if hostname == "SDM630_WP":
                self._SDM630_WP_total_power_active_average.reset()

            if hostname == "ESPAltherma":
                self.m_ESPAltherma_INV_primary_current_average.reset()
                self._SDM630_WP_total_power_active_average.reset()

        if (
            infostate == DeviceState.ERROR.value
            or infostate == DeviceState.UNKNOWN.value
        ):
            self.m_DevicedoProcessing[hostname] = False
            # self.m_mqttDeviceClient.unsubscribeallTopics()

        logger.info(f"notifyInfoStateFunction Device: {hostname} infostate: {infostate}")


    def getProcessValues(self):

        if self.m_SPH_TL3_BH_UP != None and self.m_DevicedoProcessing["SPH_TL3_BH_UP"]:
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

            self._SPH_TL3_BH_UP_Pactogrid_total_average.add(
                self._SPH_TL3_BH_UP_Pactogrid_total
            )

            self._SPH_TL3_BH_UP_Pactouser_total = (
                self.m_SPH_TL3_BH_UP.get_Pactouser_total()
            )

            self._SPH_TL3_BH_UP_PLocalLoad_total = (
                self.m_SPH_TL3_BH_UP.get_PLocalLoad_total()
            )
            self._SPH_TL3_BH_UP_Pdischarge1 = self.m_SPH_TL3_BH_UP.get_Pdischarge1()

            self._SPH_TL3_BH_UP_Pdischarge1_average.add(self._SPH_TL3_BH_UP_Pdischarge1)

            self._SPH_TL3_BH_UP_Pcharge1 = self.m_SPH_TL3_BH_UP.get_Pcharge1()
            self._SPH_TL3_BH_UP_SOC = self.m_SPH_TL3_BH_UP.get_BMS_SOC()
            self._SPH_TL3_BH_UP_SOC_Min = self.m_SPH_TL3_BH_UP.get_SOC_Min()
            self._SPH_TL3_BH_UP_Inverter_Status = (
                self.m_SPH_TL3_BH_UP.get_Inverter_Status()
            )
            self._SPH_TL3_BH_UP_Temp1 = self.m_SPH_TL3_BH_UP.get_Temp1()
            self._SPH_TL3_BH_UP_Temp2 = self.m_SPH_TL3_BH_UP.get_Temp2()

            self._SPH_TL3_BH_UP_Temp3 = self.m_SPH_TL3_BH_UP.get_Temp3()

        if (
            (self.m_SDM630_WP != None)
            and (self.m_SDM630_WR != None)
            and self.m_DevicedoProcessing["SDM630_WP"]
            and self.m_DevicedoProcessing["SDM630_WR"]
        ):
            self._SDM630_WR_total_power_active = (
                self.m_SDM630_WR.get_total_power_active()
            )

            self._SDM630_WP_total_power_active = (
                self.m_SDM630_WP.get_total_power_active()
            )

            self._SDM630_WR_total_power_active_average.add(
                self._SDM630_WR_total_power_active
            )

            self._SDM630_WP_total_power_active_average.add(
                self._SDM630_WP_total_power_active
            )

            self._SDM630_WP_import_energy_active = (
                self.m_SDM630_WP.get_import_energy_active()
            )

            if self._SPH_TL3_BH_UP_Pcharge1 > 0:
                pass

            self._PLocalLoad_Household = (
                self._SPH_TL3_BH_UP_PLocalLoad_total
                - self._SDM630_WP_total_power_active_average.get_avg()
            )

        if self.m_ESPAltherma != None and self.m_DevicedoProcessing["ESPAltherma"]:

            self.m_ESPAltherma_operation_mode = self.m_ESPAltherma.get_Operation_Mode()

            self.m_ESPAltherma_I_U_operation_mode = (
                self.m_ESPAltherma.get_I_U_operation_mode()
            )
            self.m_ESPAltherma_Thermostat_ON_OFF = (
                self.m_ESPAltherma.get_Thermostat_ON_OFF()
            )

            self.m_ESPAltherma_Defrost_Operation = (
                self.m_ESPAltherma.get_Defrost_Operation()
            )

            self.m_ESPAltherma_HPSU_Bypass_valve_position = (
                self.m_ESPAltherma.get_HPSU_Bypass_valve_position()
            )
            self.m_ESPAltherma_HPSU_Tank_valve_position = (
                self.m_ESPAltherma.get_HPSU_Tank_valve_position()
            )
            self.m_ESPAltherma_HPSU_Mixed_leaving_water_R7T_DLWA2 = (
                self.m_ESPAltherma.get_HPSU_Mixed_leaving_water_R7T_DLWA2()
            )
            self.m_ESPAltherma_Water_pump_signal = (
                self.m_ESPAltherma.get_Water_pump_signal()
            )
            self.m_ESPAltherma_Water_pressure = self.m_ESPAltherma.get_Water_pressure()
            self.m_ESPAltherma_Flow_sensor_l_min = (
                self.m_ESPAltherma.get_Flow_sensor_l_min()
            )

            self.m_ESPAltherma_INV_primary_current = (
                self.m_ESPAltherma.get_INV_primary_current()
            )

            self.m_ESPAltherma_Flow_sensor_l_min_average.add(
                self.m_ESPAltherma_Flow_sensor_l_min
            )

            self.m_ESPAltherma_INV_primary_current_average.add(
                self.m_ESPAltherma_INV_primary_current
            )

            self.m_ESPAltherma_DHW_tank_temp_R5T = (
                self.m_ESPAltherma.get_DHW_tank_temp_R5T()
            )
            self.m_ESPAltherma_Inlet_water_temp_R4T = (
                self.m_ESPAltherma.get_Inlet_water_temp_R4T()
            )
            self.m_ESPAltherma_Refrig_Temp_liquid_side_R3T = (
                self.m_ESPAltherma.get_Refrig_Temp_liquid_side_R3T()
            )
            self.m_ESPAltherma_Leaving_water_temp_BUH_R2T = (
                self.m_ESPAltherma.get_Leaving_water_temp_BUH_R2T()
            )
            self.m_ESPAltherma_Leaving_water_temp_BUH_R1T = (
                self.m_ESPAltherma.get_Leaving_water_temp_BUH_R1T()
            )
            self.m_ESPAltherma_DHW_setpoint = self.m_ESPAltherma.get_DHW_setpoint()
            self.m_ESPAltherma_LW_setpoint_main = (
                self.m_ESPAltherma.get_LW_setpoint_main()
            )
            self.m_ESPAltherma_INV_frequency_rps = (
                self.m_ESPAltherma.get_INV_frequency_rps()
            )

            if self.m_ESPAltherma_operation_mode == "Fan Only":
                pass

            if self.m_ESPAltherma_operation_mode == "Heating":
                pass

            if self.m_ESPAltherma_Defrost_Operation == "OFF":
                pass

            if self.m_ESPAltherma_Thermostat_ON_OFF == "ON":
                pass

            doCalculate_Heating: bool = False
            doCalculate_DWH: bool = False
            # self.m_ESPAltherma_Flow_sensor_l_min_average
            if "Heating" in self.m_ESPAltherma_I_U_operation_mode:
                if self.m_ESPAltherma_Thermostat_ON_OFF == "ON":

                    if self.m_ESPAltherma_INV_primary_current == 0:
                        delta_T = (
                            self.m_ESPAltherma_HPSU_Mixed_leaving_water_R7T_DLWA2
                            - self.m_ESPAltherma_Inlet_water_temp_R4T
                        )
                    else:
                        delta_T = (
                            self.m_ESPAltherma_Leaving_water_temp_BUH_R2T
                            - self.m_ESPAltherma_Inlet_water_temp_R4T
                        )

                    self.m_ESPAltherma_INV_Heat_Energy = float(
                        self.m_ESPAltherma_Flow_sensor_l_min_average.get_avg()
                        * 1.16
                        * 60
                        * delta_T
                    )

                    self.m_ESPAltherma_INV_electric_HeatEnergy = float(
                        1.73
                        # 1.0
                        * self.m_ESPAltherma_INV_primary_current_average.get_avg()
                        * self.m_SDM630_WP.get_total_power_factor()
                        * self.m_SDM630_WP.get_voltage_ll()
                    )

                    if self.m_ESPAltherma_INV_primary_current != 0:
                        # if self._SDM630_WP_total_power_active_average.get_avg() != 0:
                        self.m_ESPAltherma_INV_Heat_COP = float(
                            self.m_ESPAltherma_INV_Heat_Energy
                            / self._SDM630_WP_total_power_active_average.get_avg()
                        )
                    else:
                        self.m_ESPAltherma_INV_Heat_COP = float(0.0)
                    doCalculate_Heating = True

            if not doCalculate_Heating:
                self.m_ESPAltherma_INV_Heat_Energy = float(0.0)
                self.m_ESPAltherma_INV_Heat_COP = float(0.0)
                self.m_ESPAltherma_INV_electric_HeatEnergy = float(0.0)

            if "DHW" in self.m_ESPAltherma_I_U_operation_mode:
                if self.m_ESPAltherma_INV_primary_current != 0:
                    delta_T = (
                        self.m_ESPAltherma_Leaving_water_temp_BUH_R2T
                        - self.m_ESPAltherma_Inlet_water_temp_R4T
                    )
                    self.m_ESPAltherma_INV_DHW_Energy = float(
                        self.m_ESPAltherma_Flow_sensor_l_min_average.get_avg()
                        * 1.16
                        * 60
                        * delta_T
                    )
                    self.m_ESPAltherma_INV_electric_DHWEnergy = float(
                        1.73
                        # 1.0
                        * self.m_ESPAltherma_INV_primary_current_average.get_avg()
                        * self.m_SDM630_WP.get_total_power_factor()
                        * self.m_SDM630_WP.get_voltage_ll()
                    )

                    if self._SDM630_WP_total_power_active_average.get_avg() != 0:
                        self.m_ESPAltherma_INV_DHW_COP = float(
                            self.m_ESPAltherma_INV_DHW_Energy
                            / self._SDM630_WP_total_power_active_average.get_avg()
                        )
                    else:
                        self.m_ESPAltherma_INV_DHW_COP = float(0.0)
                    doCalculate_DWH = True

            if not doCalculate_DWH:
                self.m_ESPAltherma_INV_DHW_Energy = float(0.0)
                self.m_ESPAltherma_INV_DHW_COP = float(0.0)
                self.m_ESPAltherma_INV_electric_DHWEnergy = float(0.0)

        # if self.m_DaikinWP != None and self.m_DevicedoProcessing["DaikinWP"]:
        #     self._DaikinWP_CLIMATE_hvac_mode = self.m_DaikinWP.get_CLIMATE_hvac_mode()
        #     self._DaikinWP_WATER_temperature = self.m_DaikinWP.get_WATER_temperature()
        #     self._DaikinWP_WATER_turn_on = self.m_DaikinWP.get_WATER_turn_on()
        #     self._DaikinWP_CLIMATE_turn_on = self.m_DaikinWP.get_CLIMATE_turn_on()
        #     self._DaikinWP_WATER_tank_state = self.m_DaikinWP.get_WATER_tank_state()

        #     self._DaikinWP_WATER_target_temperature = (
        #         self.m_DaikinWP.get_WATER_target_temperature()
        #     )
        #     self._DaikinWP_CLIMATE_target_temperature = (
        #         self.m_DaikinWP.get_CLIMATE_target_temperature()
        #     )
        #     self._DaikinWP_CLIMATE_temperature = (
        #         self.m_DaikinWP.get_CLIMATE_temperature()
        #     )

        #     self._DaikinWP_Sensor_OutsideTemperature = (
        #         self.m_DaikinWP.get_Sensor_OutsideTemperature()
        #     )
        #     self._DaikinWP_Sensor_LeavingWaterTemperatur = (
        #         self.m_DaikinWP.get_Sensor_LeavingWaterTemperature()
        #     )

        if self.m_kebaWallbox != None and self.m_DevicedoProcessing["kebaWallbox"]:

            pass

    def doProcess_KebaWallbox(self):
        if self.m_kebaWallbox != None:
            if not self.m_DevicedoProcessing["kebaWallbox"]:
                return
        pass

    def doUnProcess_SPH_TL3_BH_UP(self):
        self.m_GPIODevice.switch_InverterFan(False)
        self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)
        self.m_GPIODevice.set_enableHeating(False)

    # def doUnProcess_DaikinWP(self):
    #     self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)
    #     self.m_GPIODevice.set_enableHeating(False)
    #     self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

    def doProcess_SPH_TL3_BH_UP(self):
        if self.m_SPH_TL3_BH_UP != None:
            if not self.m_DevicedoProcessing["SPH_TL3_BH_UP"]:
                self.doUnProcess_SPH_TL3_BH_UP()

            else:
                if (
                    self._SPH_TL3_BH_UP_Inverter_Status
                    >= InverterState.WORKING_STATE.value
                ):
                    self.doProcess_InverterTemperature()

                    self.doProcess_InverterState()

    def doProcess_InverterTemperature(self):
        if self.m_SPH_TL3_BH_UP != None:
            # 0 == not in Subscibe List
            if (
                self._SPH_TL3_BH_UP_Temp1 != 0
                or self._SPH_TL3_BH_UP_Temp2 != 0
                or self._SPH_TL3_BH_UP_Temp3 != 0
            ):

                tempArray: list[float] = [
                    self._SPH_TL3_BH_UP_Temp1,
                    self._SPH_TL3_BH_UP_Temp2,
                    self._SPH_TL3_BH_UP_Temp3,
                ]
                fanOn: bool = False
                fanOff: bool = True
                for temp in tempArray:
                    if temp >= self.m_INVERTER_TEMPERATURE_FAN_ON:
                        fanOn = True
                        break
                    # alle Temps müssen geprüft und kleiner sein!!
                    if not (temp <= self.m_INVERTER_TEMPERATURE_FAN_OFF):
                        fanOff = False

                if fanOn:
                    # if self._SPH_TL3_BH_UP_Temp1 >= self.m_INVERTER_TEMPERATURE_FAN_ON:
                    state = self.m_GPIODevice.get_InverterFan()

                    if not state:
                        state = self.m_GPIODevice.switch_InverterFan(True)
                        logger.info(
                            f"doProcess_InverterState: switch_InverterFan(True)"
                        )

                # if self._SPH_TL3_BH_UP_Temp1 <= self.m_INVERTER_TEMPERATURE_FAN_OFF:
                elif fanOff:
                    state = self.m_GPIODevice.get_InverterFan()
                    if state:
                        state = self.m_GPIODevice.switch_InverterFan(False)

                        logger.info(
                            f"doProcess_InverterState: switch_InverterFan(False)"
                        )

    def is_PVSurplus(self):
        if self.m_GPIODevice.is_PVSurplus():

            if (
                self._SPH_TL3_BH_UP_Pactogrid_total_average.get_avg()
                > self.m_PV_Surplus
            ):

                # if self._SPH_TL3_BH_UP_Pactogrid_total > self.m_PV_Surplus:
                return True

        return False

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

                    InverterTimeOn = False
                    if timestamp_sr < timestamp_ss:
                        InverterTimeOn = timestamp_sr <= timestamp <= timestamp_ss
                    else:
                        InverterTimeOn = timestamp >= timestamp_sr

                    # zwischen Sonnenauf und Sonneununtergang oder bei hoher MPPT-Spannung
                    if InverterTimeOn:
                        if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                            self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                            logger.info(f"doProcess_InverterState: set_OnOff(1)")

                    else:
                        if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                            InverterOn = (
                                self._SDM630_WR_total_power_active_average.get_avg()
                                >= 10.0
                            )
                            if not InverterOn:
                                self.m_TimeSpan_InverterState.setActTime(timestamp)
                            else:
                                difference = (
                                    self.m_TimeSpan_InverterState.getTimeSpantoActTime()
                                )

                                difference_secs = self.m_TimeSpan_InverterState.getTimediffernceintoSecs(
                                    difference
                                )
                                # für 10 minuten wird etwas produziert
                                if difference_secs > 600:
                                    self.m_SPH_TL3_BH_UP.set_OnOff(
                                        InverterStateONOff.ON.value
                                    )
                                    logger.info(
                                        f"doProcess_InverterState: set_OnOff(1)"
                                    )

                        elif self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.ON.value:

                            # keine Leistung vom WR
                            if (
                                self._SPH_TL3_BH_UP_Vpv1 < self.m_MPPT_StartVoltage * 2
                            ) and (
                                self._SPH_TL3_BH_UP_Vpv2 < self.m_MPPT_StartVoltage * 2
                            ):
                                if (
                                    self._SPH_TL3_BH_UP_SOC_Min * 0.8
                                    <= self._SPH_TL3_BH_UP_SOC
                                    <= self._SPH_TL3_BH_UP_SOC_Min * 1.2
                                ):
                                    if (
                                        self._SDM630_WR_total_power_active_average.get_avg()
                                        < -3.0
                                    ):
                                        self.m_SPH_TL3_BH_UP.set_OnOff(
                                            InverterStateONOff.OFF.value
                                        )
                                        logger.info(
                                            f"doProcess_InverterState: set_OnOff(0)"
                                        )
                else:
                    if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                        self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                        logger.info(f"doProcess_InverterState: set_OnOff(1)")

            else:
                if self._SPH_TL3_BH_UP_OnOff == InverterStateONOff.OFF.value:
                    self.m_SPH_TL3_BH_UP.set_OnOff(InverterStateONOff.ON.value)
                    logger.info(f"doProcess_InverterState: set_OnOff(1)")

    def is_waterprocessingactive(self) -> bool:

        if self.m_USE_ALTHERMA_API > 0:
            # I_U_operation_mode
            # DHW
            # Heating
            # Stop
            
            ret:bool = True

            if "DHW" in self.m_ESPAltherma_I_U_operation_mode:
                return True

            if "Heating" in self.m_ESPAltherma_I_U_operation_mode:
                return True

            if "Stop" in self.m_ESPAltherma_I_U_operation_mode:
                return False
                # if self._DaikinWP_WATER_turn_onState == SwitchONOff.OFF:
                #     return False
                # else: return True

            return ret
            
        # elif self.m_USE_DAIKIN_API > 0:
        #     if self._DaikinWP_WATER_turn_on:
        #         return True

        return False

    def is_start_Water(self) -> bool:
        start_WaterOn: bool = True
        if self._DaikinWP_WATER_Cancel_from_WP:
            return False

        if (
            self.WP_WATER_consume_energy + self.m_PV_MIN_WATER_CONSUME_ENERGY
            >= self.m_PV_MAX_WATER_CONSUME_ENERGY
        ):
            return False

        if self.m_USE_ALTHERMA_API > 0:
            if self.m_ESPAltherma_DHW_tank_temp_R5T >= self.m_MIN_WATER_TEMPERATURE:
                return False


        return start_WaterOn

    def start_Water_Heating(self):

        if self.m_DAIKIN_USE_SMARTGRID_CONTACTS:
            logger.info(f"doProcess_ControlDaikinWater: activate Smart Grid")
            # self.m_GPIODevice.is_WPClimateOn()
            self.m_GPIODevice.switch_SmartGridWP(state_grid_1=1, state_grid_2=1)

        else:
            if self.m_USE_ALTHERMA_API > 0:
                self._DaikinWP_WATER_target_temperature_Saved = self.m_ESPAltherma_DHW_tank_temp_R5T


        self.m_GPIODevice.set_enableHeating(True)

    def cancel_WaterHeating(self):

        logger.info(
            f"doProcess_ControlDaikinWater: consumed Energy:{self.WP_WATER_consume_energy}"
        )
        if self.m_DAIKIN_USE_SMARTGRID_CONTACTS:
            self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)
            logger.info(f"doProcess_ControlDaikinWater: deactivate Smart Grid")


        self.m_GPIODevice.set_enableHeating(False)

    def check_forCancel_Water_Heating(self) -> bool:
        difference = self.m_TimeSpan_Daikin_Control_Water.getTimeSpantoActTime()
        difference_secs = self.m_TimeSpan_Daikin_Control_Water.getTimediffernceintoSecs(difference)
        doCancel:bool = False

        if self.m_USE_ALTHERMA_API > 0:
            if self.m_ESPAltherma_DHW_tank_temp_R5T >= self.m_MAX_WATER_TEMPERATURE:
                doCancel = False
                logger.info(f"doProcess_ControlDaikinWater: Water-Temp. {self.m_ESPAltherma_DHW_tank_temp_R5T} >= Water-Target-Temp. {self.m_MAX_WATER_TEMPERATURE} -> Cancel")
                self._DaikinWP_WATER_Cancel_from_WP = True

            if doCancel:
                return True

        if self.WP_WATER_consume_energy >= self.m_PV_MAX_WATER_CONSUME_ENERGY:
            doCancel = True
            self._DaikinWP_WATER_Cancel_from_WP = True
            logger.info(
                f"doProcess_ControlDaikinWater: WP already consumed Energy: {self.WP_WATER_consume_energy} > MAX. Consume Energy: {self.m_PV_MAX_WATER_CONSUME_ENERGY} -> Cancel"
            )

        if difference_secs >= self.m_PV_Surplus_Time_On_secs:

            if self._SDM630_WP_total_power_active_average.get_avg() <= 100:
                logger.info(
                    f"doProcess_ControlDaikinWater: switched Off by WP: performance :{self._SDM630_WP_total_power_active_average.get_avg()}  <= 100 Watt -> Cancel"
                )
                self._DaikinWP_WATER_Cancel_from_WP = True
                doCancel = True
            else:
                if self._availablepowerWR < 100:
                    if self.WP_WATER_consume_energy >= self.m_PV_MIN_WATER_CONSUME_ENERGY:
                        doCancel = True
                        logger.info(
                            f"doProcess_ControlDaikinWater: actual available WR Power :{self._availablepowerWR } < 100 Watt -> Cancel"
                        )

        return doCancel

    def doProcess_ControlDaikinWater(self, timestamp):
        is_ProcessingActiv: bool = False
        # self.m_TimeSpan_Daikin_Control_Water
        if self.m_doProcessDaikinControlWater > 0:
            if self.is_waterprocessingactive():
                # if self._DaikinWP_WATER_turn_on or self.m_USE_DAIKIN_API > 0:
                is_ProcessingActiv = True
                if self._DaikinWP_WATER_turn_onState == SwitchONOff.OFF:
                    # PV Überschuss, Tank-Temperatur kleiner Max Temperatur
                    #
                    # wir speisen zur Zeit ein
                    if self.is_PVSurplus():
                        self.m_TimeSpan_Daikin_Control_Water.setActTime(timestamp)
                        # stop_time = timestamp + datetime.timedelta(minutes=10)
                        # self.m_TimeSpan_Daikin_Control_Water.setStopTime(stop_time)
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.Waiting_On
                        logger.info(
                            f"doProcess_ControlDaikinWater: {self._SPH_TL3_BH_UP_Pactogrid_total_average.get_avg()} > {self.m_PV_Surplus} "
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

                    if self.is_PVSurplus():
                        # wir speisen zur Zeit ein
                        if difference_secs >= self.m_PV_Surplus_Time_secs:
                            start_WaterOn: bool = self.is_start_Water()
                            if start_WaterOn:
                                self.start_Water_Heating()

                                self._SDM630_WP_start_import_energy_active = self._SDM630_WP_import_energy_active

                                # self._SDM630_WP_start_import_energy_active = (
                                #     self.WP_WATER_consume_energy
                                #     + self._SDM630_WP_import_energy_active
                                # )

                                self.m_TimeSpan_Daikin_Control_Water.setActTime(
                                    timestamp
                                )
                                self._DaikinWP_WATER_turn_onState = SwitchONOff.ON

                    else:
                        logger.info(
                            f"doProcess_ControlDaikinWater: {self._SPH_TL3_BH_UP_Pactogrid_total_average.get_avg()} < {self.m_PV_Surplus}"
                        )
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

                elif self._DaikinWP_WATER_turn_onState == SwitchONOff.ON:
                    doCancel:bool = False
                    
                    self.WP_WATER_consume_energy = (
                        self._SDM630_WP_import_energy_active
                        - self._SDM630_WP_start_import_energy_active
                    )

                    self._availablepowerWR = (
                        self._SDM630_WR_total_power_active_average.get_avg()
                        - self._SPH_TL3_BH_UP_Pdischarge1_average.get_avg()
                        - self._SDM630_WP_total_power_active_average.get_avg()
                    )

                    doCancel = self.check_forCancel_Water_Heating()

                    if doCancel:
                        self.cancel_WaterHeating()
                        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

        if not is_ProcessingActiv:
            logger.info(f"doProcess_ControlDaikinWater: ProcessingActiv: {is_ProcessingActiv} turn_on_state:{self._DaikinWP_WATER_turn_onState.value} " )
            # disable Smart-Grid
            self.m_GPIODevice.switch_SmartGridWP(state_grid_1=0, state_grid_2=0)
            self.m_GPIODevice.set_enableHeating(False)
            self.doinitialstateDaikinWater()

    def doProcess_ControlDaikinClimate(self, timestamp):
        if self.m_doProcessDaikinControlClimate > 0:
            pass

    def doProcess_ControlDaikinWP(self, timestamp):

        doProcessDaikin: bool = (
            (self.m_USE_ALTHERMA_API > 0 and self.m_DevicedoProcessing["ESPAltherma"])
            and self.m_DevicedoProcessing["SPH_TL3_BH_UP"]
            and self.m_DevicedoProcessing["SDM630_WP"]
            and self.m_DevicedoProcessing["SDM630_WR"]
        )

        if doProcessDaikin:
            self.doProcess_ControlDaikinWater(timestamp)
            # self.doProcess_ControlDaikinClimate(timestamp)
        else:
            pass
            # WP Smart-Grid Process beenden können
            # if self._DaikinWP_WATER_turn_onState != SwitchONOff.ON:
            #     self.doinitialstateDaikinWater()


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

    def doinitialstateDaikinWater(self):
        self._SDM630_WP_start_import_energy_active = 0.0
        self.WP_WATER_consume_energy = 0.0
        self._DaikinWP_WATER_Cancel_from_WP = False
        self._DaikinWP_WATER_turn_onState = SwitchONOff.OFF

    def doProcess(self):
        timestamp = datetime.now(timezone.utc).astimezone()
        difference_act = self.m_TimeSpan.getTimeSpantoActTime()
        hours_actsecs = self.m_TimeSpan.getTimediffernceintoSecs(difference_act)

        # difference_act_Sunrise = self.m_TimeSpan_Sunrise.getTimeSpantoActTime()
        # hours_actsecs_Sunrise = self.m_TimeSpan_Sunrise.getTimediffernceintoHours(
        #     difference_act_Sunrise
        # )

        actualday = timestamp.day

        # all new day get sunrise/sunset time
        if self.m_lastday != actualday:
            #  3 hour after midnight-> time shift between raspi and server
            if timestamp.hour >= 3 and timestamp.hour <= 4:
                self.getsunrise_sunsetTime()
                self.doinitialstateDaikinWater()
                self.m_lastday = actualday
            # self.m_TimeSpan_Sunrise.setActTime(timestamp)

        #  val = 0 if ret == None else ret  # Requires Python version >= 2.5
        if hours_actsecs >= self.m_REFRESHTIME:
            self.getProcessValues()

            self.doProcess_SPH_TL3_BH_UP()

            self.doProcess_ControlDaikinWP(timestamp)

            payload = {
                "CPU_Temperature": self.m_GPIODevice.getCpuTemperature(),
                "is_PVSurplus": self.m_GPIODevice.is_PVSurplus(),
                "is_WPClimateOn": self.m_GPIODevice.is_WPClimateOn(),
                "SPH_TL3_BH_UP_OnOff": self._SPH_TL3_BH_UP_OnOff,
                "DaikinWP_WATER_turn_onState":self._DaikinWP_WATER_turn_onState.value,
                # "DaikinWP_WATER_turn_on": self._DaikinWP_WATER_turn_on,
                # "DaikinWP_CLIMATE_turn_on": self._DaikinWP_CLIMATE_turn_on,
                "SPH_TL3_BH_UP_Inverter_Status": self._SPH_TL3_BH_UP_Inverter_Status,
                # "DaikinWP_WATER_tank_state": self._DaikinWP_WATER_tank_state,
                # "DaikinWP_WATER_temperature": self._DaikinWP_WATER_temperature,
                # "DaikinWP_CLIMATE_temperature": self._DaikinWP_CLIMATE_temperature,
                # "DaikinWP_WATER_target_temperature": self._DaikinWP_WATER_target_temperature,
                # "DaikinWP_CLIMATE_target_temperature": self._DaikinWP_CLIMATE_target_temperature,
                # "DaikinWP_Sensor_OutsideTemperature": self._DaikinWP_Sensor_OutsideTemperature,
                # "DaikinWP_Sensor_LeavingWaterTemperatur": self._DaikinWP_Sensor_LeavingWaterTemperatur,
                "ESPAltherma_INV_Heat_Energy": self.m_ESPAltherma_INV_Heat_Energy,
                "ESPAltherma_INV_DHW_Energy": self.m_ESPAltherma_INV_DHW_Energy,
                "ESPAltherma_INV_Heat_COP": self.m_ESPAltherma_INV_Heat_COP,
                "ESPAltherma_INV_electric_HeatEnergy": self.m_ESPAltherma_INV_electric_HeatEnergy,
                "ESPAltherma_INV_electric_DHWEnergy": self.m_ESPAltherma_INV_electric_DHWEnergy,
                "ESPAltherma_INV_DHW_COP": self.m_ESPAltherma_INV_DHW_COP,
                "ESPAltherma_INV_electric_DHWEnergy": self.m_ESPAltherma_INV_electric_DHWEnergy,
                "SDM630_WP_total_power_active_average": self._SDM630_WP_total_power_active_average.get_avg(),
                "ESPAltherma_I_U_operation_mode": self.m_ESPAltherma_I_U_operation_mode,
                "ESPAltherma_operation_mode": self.m_ESPAltherma_operation_mode,
                "ESPAltherma_Thermostat_ON_OFF": self.m_ESPAltherma_Thermostat_ON_OFF,
                "ESPAltherma_Defrost_Operation": self.m_ESPAltherma_Defrost_Operation,
                "ESPAltherma_HPSU_Bypass_valve_position": self.m_ESPAltherma_HPSU_Bypass_valve_position,
                "ESPAltherma_HPSU_Tank_valve_position": self.m_ESPAltherma_HPSU_Tank_valve_position,
                "ESPAltherma_HPSU_Mixed_leaving_water_R7T_DLWA2": self.m_ESPAltherma_HPSU_Mixed_leaving_water_R7T_DLWA2,
                "ESPAltherma_Water_pump_signal": self.m_ESPAltherma_Water_pump_signal,
                "ESPAltherma_Water_pressure": self.m_ESPAltherma_Water_pressure,
                "ESPAltherma_Flow_sensor_l_min_average": self.m_ESPAltherma_Flow_sensor_l_min_average.get_avg(),
                "ESPAltherma_INV_primary_current_average": self.m_ESPAltherma_INV_primary_current_average.get_avg(),
                "WP_WATER_consume_energy": self.WP_WATER_consume_energy,
                "PV_MIN_WATER_CONSUME_ENERGY": self.m_PV_MIN_WATER_CONSUME_ENERGY,
                "PV_MAX_WATER_CONSUME_ENERGY": self.m_PV_MAX_WATER_CONSUME_ENERGY,
                "sunrise": (
                    ""
                    if self.m_today_sr == None
                    else self.m_today_sr.strftime("%Y-%m-%d, %H:%M:%S")
                ),
                "sunset": (
                    ""
                    if self.m_today_ss == None
                    else self.m_today_ss.strftime("%Y-%m-%d, %H:%M:%S")
                ),
            }

            self.doPublishPayload(payload, retained=True)

            self.m_TimeSpan.setActTime(timestamp)

    def setUsedDevices(self) -> None:
        if "SDM630_WR" in self.m_useddevices:
            self.m_SDM630_WR = self.m_useddevices["SDM630_WR"]

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

        # if "DaikinWP" in self.m_useddevices:
        #     self.m_DaikinWP = self.m_useddevices["DaikinWP"]

        if "ESPAltherma" in self.m_useddevices:
            self.m_ESPAltherma = self.m_useddevices["ESPAltherma"]

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
