# import RPi.GPIO as GPIO
import logging
from gpiozero import (
    Button,
    LED,
    DigitalOutputDevice,
    TimeOfDay,
    PWMOutputDevice,
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

UNIT_TIME = 0.25
PIN = 21
VERBOSE = True
FREQUENCY = 100
PWM_CHANNEL = 1

# Pin-Belegung
# INPUT Relais:
# B1 -> IO27
# B2 -> IO17
# B3 -> IO24
# B4 -> IO16

# 4 fach Relais:
# IN1-> IO07 (WP SmartGrid_0)
# IN2-> IO08 (WP SmartGrid_2)
# IN3-> IO11 (FAN)
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
            self._button_16 = Button(pull_up=None, active_state=False, pin=16)
            self._button_17 = Button(pull_up=None, active_state=False, pin=17)
            self._button_22 = Button(pull_up=None, active_state=False, pin=22)
            self._button_23 = Button(pull_up=None, active_state=False, pin=23)
            self._button_24 = Button(pull_up=None, active_state=False, pin=24)
            self._button_25 = Button(pull_up=None, active_state=False, pin=25)
            self._button_26 = Button(pull_up=None, active_state=False, pin=26)
            # self._button_27 = Button(pull_up=None, active_state=False, pin=27)

            self._button_27 = LED(pin=27)
            self._button_27.blink()
            # 4 fach Relais:
            self._digitalout_07 = DigitalOutputDevice(
                initial_value=False, active_high=False, pin=7
            )
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


            self._tod = TimeOfDay(
                time(hour=self.m_TIMEOFDAY_BEGIN_HOUR, minute=self.m_TIMEOFDAY_BEGIN_MINUTE), time(hour=self.m_TIMEOFDAY_END_HOUR, minute=self.m_TIMEOFDAY_END_MINUTE ), utc=False
            )

            self._tod.when_activated = self.begin_day
            self._tod.when_deactivated = self.end_day

        
            self._cpuTemp = CPUTemperature(
                event_delay=5, min_temp=self.m_CPU_TEMPERATURE_MIN, max_temp=self.m_CPU_TEMPERATURE_MAX, threshold=self.m_CPU_TEMPERATURE_THRESHOLD
            )
          
            self._cpuTemp.when_activated = self.CPUTempActivate
            self._cpuTemp.when_deactivated = self.CPUTempDeactivate

            # self._PingServer = PingServer("google.com", event_delay=10)
            # self._PingServer.when_activated = self.PingServerActivated
            # self._PingServer.when_deactivated = self.PingServerDeactivated

            logger.info(f"CPU-Temperature = {self._cpuTemp.temperature} °C")
            # pause()

        except GPIOZeroError as e:
            logger.error("doBearerRequest-REQUEST FAILED: %s", e)

  
    def getCpuTemperature(self) -> float:
        return self._cpuTemp.temperature
          
    def switch_InverterFan(self, state: bool) -> bool:
        # if not self._digitalout_11.is_active:
        #     self._digitalout_11.on()
        # else:
        #     self._digitalout_11.off()
        # return
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

    def CPUTempActivate(self):
        logger.error(
            f"CPUTempActivate: Temperature:{self._cpuTemp.temperature} °C, % = {self._cpuTemp.value}"
        )
        pass

    def CPUTempDeactivate(self):
        logger.error(
            f"CPUTempDeActivate: Temperature:{self._cpuTemp.temperature} °C, % = {self._cpuTemp.value}"
        )
