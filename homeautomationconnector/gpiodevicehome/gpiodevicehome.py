# import RPi.GPIO as GPIO
import logging
from gpiozero import (
    Button,
    LED,
    DigitalOutputDevice,
    TimeOfDay,
    # PWMOutputDevice,
    CPUTemperature,
    GPIOZeroError,
    # PingServer,
)

from tomlconfig.tomlutils import TomlParser
from datetime import time
from signal import pause

# import RPi.GPIO
# import time

logger = logging.getLogger("root")


# Pin-Belegung
# INPUT Relais:
# B1 -> IO27
# B2 -> IO17
# B3 -> IO24
# B4 -> IO16

# OutPut-LED -> IO23

# 4 fach Relais:
# IN1-> IO07 (WP SmartGrid_0)
# IN2-> IO08 (WP SmartGrid_1)
# IN3-> IO11 (FAN WR)
# IN4-> IO09


# 8 fach Treiber
# IB-> IO10
# 2B-> IO12
# 3B-> IO13


class GPIODeviceHomeAutomation(object):
    def __init__(
        self,
        devkey: str = "",
        tomlParser: TomlParser = None,
    ):
        self.m_deviceKey = devkey
        self.m_tomlParser = tomlParser

        self._button_16 = None
        self._button_17 = None
        self._button_22 =  None
            # self._button_23 = Button(pull_up=None, active_state=False, pin=23)
        self._button_24 = None
        self._button_25 = None
        self._button_26 = None
        self._button_27 = None

        self._LED_23 = None
  
            # 4 fach Relais:
        self._digitalout_07 = None
        self._digitalout_08 = None
        self._digitalout_09 = None
        self._digitalout_11 = None
            # 8 fach Treiber
            #
        self._digitalout_10 = None
        self._digitalout_12 = None
        self._digitalout_13 = None
        #         CPU_TEMPERATURE_MAX= 55
        # CPU_TEMPERATURE_MIN= 35

        self.m_CPU_TEMPERATURE_MAX = self.m_tomlParser.get(
            "homeautomation.CPU_TEMPERATURE_MAX", 55
        )
        self.m_CPU_TEMPERATURE_MIN = self.m_tomlParser.get(
            "homeautomation.CPU_TEMPERATURE_MIN", 35
        )
        self.m_CPU_TEMPERATURE_THRESHOLD = self.m_tomlParser.get(
            "homeautomation.CPU_TEMPERATURE_THRESHOLD", 42.5
        )

        self.m_TIMEOFDAY_BEGIN_HOUR = self.m_tomlParser.get(
            "homeautomation.TIMEOFDAY_BEGIN_HOUR", 5
        )

        self.m_TIMEOFDAY_BEGIN_MINUTE = self.m_tomlParser.get(
            "homeautomation.TIMEOFDAY_BEGIN_MINUTE", 0
        )

        self.m_TIMEOFDAY_END_HOUR = self.m_tomlParser.get(
            "homeautomation.TIMEOFDAY_END_HOUR", 5
        )

        self.m_TIMEOFDAY_END_MINUTE = self.m_tomlParser.get(
            "homeautomation.TIMEOFDAY_END_MINUTE", 59
        )

        self.initialize_gpio()

    def initialize_gpio(self):
        try:
            # Input to
   

    
            # B4 -> IO16 : (Inverter PACToGrid > 300 Watt as Dry Contact) , first Relais from left
            self._button_16 = Button(pull_up=None, active_state=False, pin=16)
            # self._button_16.when_activated=self.button_16_Activate
            # self._button_16.when_deactivated=self.button_16_Deactivate

  
            
            # B2 -> IO17: last Relais from Right
            self._button_17 = Button(pull_up=None, active_state=False, pin=17)
            # self._button_17.when_activated=self.button_17_Activate
            # self._button_17.when_deactivated=self.button_17_Deactivate
            

            # self._button_23 = Button(pull_up=None, active_state=False, pin=23)
            # B3 -> IO24 : second Relais from Left
            self._button_24 = Button(pull_up=None, active_state=False, pin=24)
            # self._button_24.when_activated=self.button_24_Activate
            # self._button_24.when_deactivated=self.button_24_Deactivate            
            

            # B1 -> IO27: second last from Right
            self._button_27 = Button(pull_up=None, active_state=False, pin=27)
            # self._button_27.when_activated=self.button_27_Activate
            # self._button_27.when_deactivated=self.button_27_Deactivate

            self._button_25 = Button(pull_up=None, active_state=False, pin=25)
            self._button_26 = Button(pull_up=None, active_state=False, pin=26)
            self._button_22 = Button(pull_up=None, active_state=False, pin=22)
            
            self._LED_23 = LED(pin=23)
            self._LED_23.blink()
            # 4 fach Relais:

            # IN1-> IO07 (WP SmartGrid_0)
            self._digitalout_07 = DigitalOutputDevice(
                initial_value=False, active_high=False, pin=7
            )
            # IN2-> IO08 (WP SmartGrid_1)
            self._digitalout_08 = DigitalOutputDevice(
                initial_value=False, active_high=False, pin=8
            )
            self._digitalout_09 = DigitalOutputDevice(
                initial_value=False, active_high=False, pin=9
            )
            self._digitalout_11 = DigitalOutputDevice(
                initial_value=False, active_high=False, pin=11
            )
            # 8 fach Treiber
            #
            self._digitalout_10 = DigitalOutputDevice(
                initial_value=False, active_high=True, pin=10
            )
            self._digitalout_12 = DigitalOutputDevice(
                initial_value=False, active_high=True, pin=12
            )
            self._digitalout_13 = DigitalOutputDevice(
                initial_value=False, active_high=True, pin=13
            )

            # self._led_11.blink()
            # self._PingServer = PingServer("google.com", event_delay=10)
            # self._PingServer.when_activated = self.PingServerActivated
            # self._PingServer.when_deactivated = self.PingServerDeactivated

            # self._tod = TimeOfDay(
            #     time(
            #         hour=self.m_TIMEOFDAY_BEGIN_HOUR,
            #         minute=self.m_TIMEOFDAY_BEGIN_MINUTE,
            #     ),
            #     time(
            #         hour=self.m_TIMEOFDAY_END_HOUR, minute=self.m_TIMEOFDAY_END_MINUTE
            #     ),
            #     utc=False,
            # )

            # self._tod.when_activated = self.begin_day
            # self._tod.when_deactivated = self.end_day

            self._cpuTemp = CPUTemperature(
                event_delay=5,
                min_temp=self.m_CPU_TEMPERATURE_MIN,
                max_temp=self.m_CPU_TEMPERATURE_MAX,
                threshold=self.m_CPU_TEMPERATURE_THRESHOLD,
            )

            # self._cpuTemp.when_activated = self.CPUTempActivate
            # self._cpuTemp.when_deactivated = self.CPUTempDeactivate

            logger.info(f"CPU-Temperature = {self._cpuTemp.temperature} °C")
    

        except GPIOZeroError as e:
            logger.error("initialize_gpio FAILED: %s", e)

    def is_PVSurplus(self) -> bool:
        return self._button_16.is_active
    
    def is_WPClimateOn(self) -> bool:
        return self._button_24.is_active

    def is_Button17On(self) -> bool:
        return self._button_17.is_active
    
    def is_Button27On(self) -> bool:
        return self._button_27.is_active
  
    def getCpuTemperature(self) -> float:
        return self._cpuTemp.temperature

    def switch_SmartGridWP(self, state_grid_1: int = 0, state_grid_2: int = 0) -> bool:
        # IN1-> IO07 (WP SmartGrid_0)
        # IN2-> IO08 (WP SmartGrid_1)
        if state_grid_1 > 0:
            if not self._digitalout_07.is_active:
                self._digitalout_07.on()
        else:
            if self._digitalout_07.is_active:
                self._digitalout_07.off()

        if state_grid_2 > 0:
            if not self._digitalout_08.is_active:
                self._digitalout_08.on()
        else:
            if self._digitalout_08.is_active:
                self._digitalout_08.off()

    def get_InverterFan(self) -> bool:
        return self._digitalout_11.is_active
    
    def switch_InverterFan(self, state: bool) -> bool:
        # if not self._digitalout_11.is_active:
        #     self._digitalout_11.on()
        # else:
        #     self._digitalout_11.off()
        # return
        if self._digitalout_11 == None: return False
        
        if state:
            if not self._digitalout_11.is_active:
                self._digitalout_11.on()
        else:
            if self._digitalout_11.is_active:
                self._digitalout_11.off()

        return self._digitalout_11.is_active

    def initialize_pwm(self):
        pass
        # p = GPIO.PWM(PWM_CHANNEL, FREQUENCY)
        # p.start(100)
        # p.ChangeFrequency(freq)
        # p.ChangeDutyCycle(dc)

    def PingServerActivated(self):
        logger.info(f"PingServerActivated:")
        pass

    def PingServerDeactivated(self):
        logger.info(f"PingServerDeActivated:")
        pass

    def begin_day(self):
        logger.info(f"Start-New Day:")
        pass

    def end_day(self):
        logger.info(f"End-New Day:")

    def begin_day(self):
        logger.info(f"Start-New Day:")
        pass

    def end_day(self):
        logger.info(f"End-New Day:")

    def button_16_Activate(self):
        # B4 -> IO16 : (Inverter PACToGrid >= 300 Watt as Cry Contact) 
        logger.info(
            f"_button_16-Activate: Value:{self._button_16.value}"
        )


    def button_16_Deactivate(self):
        # B4 -> IO16 : (Inverter PACToGrid < 300 Watt as Cry Contact) 
        logger.info(
            f"_button_16-DeActivate: Value:{self._button_16.value}"
        )
        
    def button_17_Activate(self):
        logger.info(
            f"_button_17-Activate: Value:{self._button_17.value}"
        )


    def button_17_Deactivate(self):
        logger.info(
            f"_button_17-DeActivate: Value:{self._button_17.value}"
        )

    def button_27_Activate(self):
        logger.info(
            f"_button_27-Activate: Value:{self._button_27.value}"
        )


    def button_27_Deactivate(self):
        logger.info(
            f"_button_27-DeActivate: Value:{self._button_27.value}"
        )

    def button_24_Activate(self):
        logger.info(
            f"_button_24-Activate: Value:{self._button_24.value}"
        )

    def button_24_Deactivate(self):
        logger.info(
            f"_button_24-DeActivate: Value:{self._button_24.value}"
        )
                                
        
    def CPUTempActivate(self):
        logger.info(
            f"CPUTempActivate: Temperature:{self._cpuTemp.temperature} °C, % = {self._cpuTemp.value}"
        )
        pass

    def CPUTempDeactivate(self):
        logger.info(
            f"CPUTempDeActivate: Temperature:{self._cpuTemp.temperature} °C, % = {self._cpuTemp.value}"
        )
