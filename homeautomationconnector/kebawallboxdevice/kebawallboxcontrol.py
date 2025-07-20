# import RPi.GPIO as GPIO
import datetime
from enum import Enum
import json
import logging
from threading import RLock
from time import timezone


from tomlconfig.tomlutils import TomlParser
from datetime import time
from signal import pause

from homeautomationconnector.kebawallboxdevice import keykontactP30
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


logger = logging.getLogger("root")


class WalboxState(Enum):
    Waiting_for_Plugged_In = 0
    PV_Loading = 1
    BOOST_Loading = 2

    Phase_Switching = 3
    no_Loading = 4
    Waiting_for_Plugged_Out = 5

    def __getstate__(self):
        return self.value

class WalboxPhaseChanging(Enum):
    Waiting_for_Switching = 0
    Switch_to_3_phase = 2
    Switch_to_1_phase = 1


    def __getstate__(self):
        return self.value


class WalboxLED(Enum):
    Loading_Ative = 0
    Waiting_ForUnlugged = 1
    PV_Loading = 2  
    BOOST_Loading = 3
    Error_Loading = 4

    def __getstate__(self):
        return self.value

class KebaWallboxControl(object):
    def __init__(
        self,
        devkey: str = "",
        tomlParser: TomlParser = None,
        keykontactP30:keykontactP30=None
    ):

        self.m_deviceKey = devkey
        self.m_tomlParser = tomlParser
        self.m_keykontactP30 = keykontactP30

        self.m_Lock = RLock()
        self.m_logger = logging.getLogger("root.KebaWallboxControl")

        self.m_state = WalboxState.Waiting_for_Plugged_In.value
        self.m_state_phase_changing = WalboxPhaseChanging.Waiting_for_Switching.value
      
        self.m_switch_to=0
        self.m_switch_to_set=0
        self.m_charge_current = 0.0
        # Initialize phase change timestamp to None; set when phase switching starts
        self.m_phase_change_timestamp = None
        self.m_lights = {}
        
        self.m_lights[0] = {"id": 0, "name": "light:0", "output": False}
        self.m_lights[1] = {"id": 1, "name": "light:1", "output": False}
        self.m_lights[2] = {"id": 2, "name": "light:2", "output": False}
        self.m_lights[3] = {"id": 3, "name": "light:3", "output": False}
        self.m_lights[4] = {"id": 4, "name": "light:4", "output": False}
        
        self.m_inputs = {}  
        self.m_inputs[0] = {"id": 0, "name": "input:0", "state": False}
        self.m_inputs[1] = {"id": 1, "name": "input:1", "state": False}
        self.m_inputs[2] = {"id": 2, "name": "input:2", "state": False}
        self.m_inputs[3] = {"id": 3, "name": "input:3", "state": False}
        self.m_inputs[4] = {"id": 4, "name": "input:4", "state": False}
        
        self._P_MAX_KW = self.m_tomlParser.get(
            "kebap30.P_MAX_KW", 10.0
        )
        self._COMMUNICATION_LOST_P_MAX_KW = self.m_tomlParser.get(
            "kebap30.COMMUNICATION_LOST_P_MAX_KW", 10.0
        )
        self._P_MIN_KW = self.m_tomlParser.get(
            "kebap30.P_MIN_KW",4.14
        )

        self._P_MIN_PV_KW_PERCENT = self.m_tomlParser.get(
            "kebap30.P_MIN_PV_KW_PERCENT", 100
        )

        self._PV_BOOST_LOAD_DURATION_min = self.m_tomlParser.get(
            "kebap30.PV_BOOST_LOAD_DURATION_min", 10
        )


        self._SHELLY_TOPIC = self.m_tomlParser.get(
            "kebap30.SHELLY_TOPIC", "shellyprorgbwwpm-ece334edc0f8"
        )
        self._I_MIN_A = self.m_tomlParser.get(
            "kebap30.I_MIN_A", 6.0
        )
        self._E_MIN_KWH = self.m_tomlParser.get(
            "kebap30.E_MIN_KWH", 1.0
        )
             
        self.E_MAX_KWH = self.m_tomlParser.get(
            "kebap30.E_MAX_KWH", 10.0
        )
            
        self._P_MIN_3_Phase_KW = self.m_tomlParser.get(
            "kebap30.P_MIN_3_Phase_KW", 4.14
        )
             




    def set_KebaWallboxDeviceClient(self, keykontactP30:keykontactP30):
        """
        Set the MQTT device client for the Keba Wallbox.

        Args:
            mqttDeviceClient (MQTTServiceDeviceClient): The MQTT client to set.
        """
        self.m_keykontactP30 = keykontactP30
        self.m_mqttDeviceClient = keykontactP30.getMQTTServiceDeviceClient() if keykontactP30 else None
        # subscribe to Shelly RGBWWPM 
        self.m_mqttDeviceClient.getMQTTClient().subscribe( f"{self._SHELLY_TOPIC}/status", self.device_Shelly_RGBWWPM_consumer)

        
    def device_Shelly_RGBWWPM_consumer(self, topic: str, payload: any):
        """
        Handles incoming MQTT messages for Shelly RGBWWPM devices.

        Args:
            topic (str): The MQTT topic.
            payload (any): The message payload (expected to be JSON).
        """
        if not payload:
            return

        try:
            action = json.loads(payload)
        except Exception as e:
            self.m_logger.error(
                f"KebaWallboxControl.device_Shelly_RGBWWPM_consumer: JSON decode error for ({topic}): {e}"
            )
            return

        if not isinstance(action, dict):
            self.m_logger.warning(
                f"KebaWallboxControl.device_Shelly_RGBWWPM_consumer: Payload is not a dict for ({topic})"
            )
            return

        with self.m_Lock:
            for key, device in action.items():
                if key.startswith("light") and isinstance(device, dict):
                    device_id = device.get("id")
                    if device_id in self.m_lights:
                        self.m_lights[device_id].update(device)
                elif key.startswith("input") and isinstance(device, dict):
                    device_id = device.get("id")
                    if device_id in self.m_inputs:
                        self.m_inputs[device_id].update(device)
                        
    def get_input(self, id: int) -> dict:
        """
        Retrieve the state of an input by its ID.

        Args:
            id (int): The ID of the input.

        Returns:
            dict: The input state dictionary. If the input does not exist, returns a default dict.
        """
        with self.m_Lock:
            input_state = self.m_inputs.get(id)
            if input_state is not None:
                # Return a copy to prevent accidental modification
                return input_state.copy()
            else:
                return {"id": id, "name": f"input:{id}", "state": False}
            
    def get_light(self, id: int) -> dict:
        """
        Retrieve the state of a light by its ID.

        Args:
            id (int): The ID of the light.

        Returns:
            dict: The light state dictionary. If the light does not exist, returns a default dict.
        """
        with self.m_Lock:
            light_state = self.m_lights.get(id)
            if light_state is not None:
                # Return a copy to prevent accidental modification
                return light_state.copy()
            else:
                return {"id": id, "name": f"light:{id}", "output": False}
            
    def set_light(self, id: int, state: bool, brightness: int, transition_duration: int, toggle_after: int) -> bool:
        """
        Set the state and properties of a light by its ID.

        Args:
            id (int): The ID of the light.
            state (bool): Desired state (True for on, False for off).
            brightness (int): Brightness level.
            transition_duration (int): Duration for transition (seconds).
            toggle_after (int): Time after which to toggle (seconds).

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        with self.m_Lock:
            light = self.m_lights.get(id)
            if light is None:
                self.m_logger.error(f"Light with ID {id} does not exist.")
                return False

            # Only send command if there is a change
            if (
                light.get("output") != state or
                light.get("brightness", 0) != brightness or
                light.get("transition_duration", 0) != transition_duration or
                light.get("toggle_after", 0) != toggle_after
            ):
                # Update internal state
                light["output"] = state
                light["brightness"] = brightness
                light["transition_duration"] = transition_duration
                light["toggle_after"] = toggle_after

                # Build command string
                command_parts = [
                    "set",
                    str(state).lower(),
                    str(brightness)
                ]
                # Always include transition_duration and toggle_after for clarity
                command_parts.append(str(transition_duration))
                command_parts.append(str(toggle_after))
                command = ",".join(command_parts)

                try:
                    self.m_mqttDeviceClient.getMQTTClient().publish(
                        f"{self._SHELLY_TOPIC}/command/light:{id}", command
                    )
                    self.m_logger.info(
                        f"Light {id} set to {'on' if state else 'off'}, brightness={brightness}, "
                        f"transition={transition_duration}, toggle_after={toggle_after}."
                    )
                    return True
                except Exception as e:
                    self.m_logger.error(f"Failed to publish light command for ID {id}: {e}")
                    return False
            else:
                self.m_logger.debug(f"No change for light {id}, skipping command.")
                return True
            
    def request_state(self) -> bool:
        # shellyprorgbwwpm-ece334edc0f8/command
        self.m_mqttDeviceClient.getMQTTClient().publish(
                    f"{self._SHELLY_TOPIC}/command","status_update"  )
        return True
   
   
    def get_phase_state(self) -> int:
        """
        Determines the current phase state and updates m_switch_to_set accordingly.

        Returns:
            int: The current phase (1 for 1-phase, 3 for 3-phase, -1 if unknown).
        """
        Phase_Switching_State = self.m_keykontactP30.get_Phase_Switching_State()
        Phase_Switching_Source = self.m_keykontactP30.get_Phase_Switching_Source()

        if Phase_Switching_State == 0:
            self.m_switch_to_set = 1
            return 1
        elif Phase_Switching_State == 1:
            self.m_switch_to_set = 3
            return 3
        else:
            self.m_logger.warning(
                f"Unknown Phase_Switching_State: {Phase_Switching_State} (Source: {Phase_Switching_Source})"
            )
            self.m_switch_to_set = -1
            return -1
        
    def do_process_phase_changing(self) -> bool:
        """
        Handles the phase switching logic for the wallbox.

        Returns:
            bool: True if phase switching is complete, False otherwise.
        """
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        Phase_Switching_State = self.m_keykontactP30.get_Phase_Switching_State()
        Phase_Switching_Source = self.m_keykontactP30.get_Phase_Switching_Source()
        # Initialize timestamp if not set
        if self.m_phase_change_timestamp is None:
            self.m_phase_change_timestamp = now
        elapsed = (now - self.m_phase_change_timestamp).total_seconds()

        MIN_PHASE_CHANGE_INTERVAL = 300  # seconds

        def reset_phase_switch_source():
            if Phase_Switching_Source != 3:
                self.m_keykontactP30.set_Set_Phase_Switch_Source(3)
                self.m_logger.info("Phase switch source set to external control (3).")

        def trigger_phase_switch(target_state: int, phase_name: str):
            self.m_keykontactP30.set_Trigger_Phase_Switch(target_state)
            self.m_logger.info(f"Initiating switch to {phase_name}-phase mode.")
            self.m_phase_change_timestamp = now

        # Main state machine for phase changing
        match self.m_state_phase_changing:
            case WalboxPhaseChanging.Waiting_for_Switching.value:
                if elapsed > MIN_PHASE_CHANGE_INTERVAL:
                    reset_phase_switch_source()
                    if self.m_switch_to == 1 and Phase_Switching_State != 0:
                        self.m_state_phase_changing = WalboxPhaseChanging.Switch_to_1_phase.value
                        trigger_phase_switch(0, "1")
                    elif self.m_switch_to == 3 and Phase_Switching_State != 1:
                        self.m_state_phase_changing = WalboxPhaseChanging.Switch_to_3_phase.value
                        trigger_phase_switch(1, "3")
                    else:
                        # Already in desired phase, update m_switch_to_set
                        if Phase_Switching_State == 0:
                            self.m_switch_to_set = 1
                        elif Phase_Switching_State == 1:
                            self.m_switch_to_set = 3
            case WalboxPhaseChanging.Switch_to_1_phase.value:
                if Phase_Switching_State == 0:
                    self.m_state_phase_changing = WalboxPhaseChanging.Waiting_for_Switching.value
                    self.m_logger.info("Switch to 1-phase mode completed.")
                    self.m_switch_to_set = 1
                elif elapsed > MIN_PHASE_CHANGE_INTERVAL:
                    self.m_state_phase_changing = WalboxPhaseChanging.Waiting_for_Switching.value
                    self.m_logger.warning("Timeout while switching to 1-phase mode.")
                    self.m_phase_change_timestamp = now

            case WalboxPhaseChanging.Switch_to_3_phase.value:
                if Phase_Switching_State == 1:
                    self.m_state_phase_changing = WalboxPhaseChanging.Waiting_for_Switching.value
                    self.m_logger.info("Switch to 3-phase mode completed.")
                    self.m_switch_to_set = 3
                elif elapsed > MIN_PHASE_CHANGE_INTERVAL:
                    self.m_state_phase_changing = WalboxPhaseChanging.Waiting_for_Switching.value
                    self.m_logger.warning("Timeout while switching to 3-phase mode.")
                    self.m_phase_change_timestamp = now

            case _:
                self.m_logger.debug("Unknown phase changing state encountered.")

        # Return True if phase switching is complete
        return self.m_switch_to_set == self.m_switch_to
    
    def is_in_loading_state(self) -> bool:
        Charging_State = self.m_keykontactP30.get_Charging_State()
        return Charging_State in [ 2, 3, 4, 5]
  
    def is_in_error_state(self) -> bool:
        """
        Check if the charging station is in an error state.

        Returns:
            bool: True if in error state, False otherwise.
        """
        Charging_State = self.m_keykontactP30.get_Charging_State()
        return Charging_State == 4
    
    def is_in_interrupted_state(self) -> bool:
        """
        Check if the charging station is in an interrupted state (e.g., due to high temperature or suspended mode).

        Returns:
            bool: True if in interrupted state, False otherwise.
        """
        Charging_State = self.m_keykontactP30.get_Charging_State()
        # State 5: Charging temporarily interrupted (e.g., high temperature or suspended)
        return Charging_State == 5
    
    def is_not_inloading_state(self) -> bool:
        """
        Check if the charging station is not in a loading state.

        Returns:
            bool: True if the charging station is not loading (startup or not ready), False otherwise.
        """
        Charging_State = self.m_keykontactP30.get_Charging_State()
        return Charging_State in [0,1]
    
    
    def is_waiting_for_vehicle_reaction(self) -> bool:
        """
        Check if the charging station is waiting for a reaction from the electric vehicle.

        Returns:
            bool: True if waiting for vehicle reaction, False otherwise.
        """
        Charging_State = self.m_keykontactP30.get_Charging_State()
        return Charging_State == 2
                
    def is_cable_not_plugged(self) -> bool:
        Cable_State = self.m_keykontactP30.get_Cable_State()
        return Cable_State in [0,1,3]
    
    def is_cable_plugged(self) -> bool:
        Cable_State = self.m_keykontactP30.get_Cable_State()
        return Cable_State in [5,7]
    
    def calculate_charge_current(self, pv_P_available: float) -> float:
        """
        Calculate the optimal charging current based on available PV power and voltage.

        Args:
            pv_P_available (float): Available PV power in kW.

        Returns:
            float: Calculated charging current (A), clamped to supported range.
        """
        def find_closest(supported_powers, target_power):
            # Find the closest supported power value to the target
            return min(supported_powers, key=lambda x: abs(x - target_power))

        # Define supported charging powers for each phase mode (in kW)
        supported_3phase = [round(x * 0.5, 2) for x in range(int(self._P_MIN_3_Phase_KW / 0.5), int(32.0 / 0.5) + 1)]
        supported_1phase = [round(x * 0.5, 2) for x in range(int((self._P_MIN_3_Phase_KW/3) / 0.5), int(7.36 / 0.5) + 1)]
        
        supported_3phase.insert(0, 0)  # Ensure 4.14 kW is included for 3-phase
        supported_1phase.insert(0, 0)  # Ensure 4.14/3 kW is included for 3-phase
        
        # voltage = self.m_keykontactP30.get_Voltage_U1()
        voltage = 230 # Assuming a standard voltage of 230V for calculations
        
        if voltage <= 0:
            self.m_logger.error("Voltage U1 is zero or negative, cannot calculate charge current.")
            return 0.0

        # Select supported power list based on phase mode
        if self.m_switch_to_set == 1:
            closest_power = find_closest(supported_1phase, pv_P_available)
            current = closest_power * 1000 / voltage
        elif self.m_switch_to_set == 3:
            closest_power = find_closest(supported_3phase, pv_P_available)
            current = closest_power * 1000 / voltage / 3.0
        else:
            self.m_logger.warning("Unknown phase mode for charge current calculation.")
            return 0.0

        # Clamp current to allowed range
        min_current =  self._I_MIN_A
        max_supported = self.m_keykontactP30.get_Max_Supported_Current()
        current = max(min_current, min(current, max_supported))

        self.m_logger.debug(
            f"Calculated charge current: {current:.2f} A (phase: {self.m_switch_to_set}, "
            f"closest_power: {closest_power} kW, voltage: {voltage} V, max_supported: {max_supported} A)"
        )

        return round(current, 2)
    
    def is_pvcharging_active(self, pv_P_available: float) -> bool:
        """
        Determine if PV charging should be considered active based on available PV power.

        Args:
            pv_P_available (float): Available PV power in kW.

        Returns:
            bool: True if PV charging is active, False otherwise.
        """
        threshold_kw = (self._P_MIN_PV_KW_PERCENT / 100.0) * self._P_MIN_KW
        is_active = pv_P_available >= threshold_kw
        self.m_logger.debug(
            f"is_pvcharging_active: pv_P_available={pv_P_available:.2f} kW, "
            f"threshold={threshold_kw:.2f} kW, active={is_active}"
        )
        return is_active
      
    def calculate_charge_power(self, pv_P_available: float) -> float:
        """
        Calculate the effective charge power, ensuring it stays within allowed limits.

        Args:
            pv_P_available (float): Available PV power in kW.

        Returns:
            float: The charge power to use (capped between _P_MIN_KW and _P_MAX_KW).
        """
        # Clamp the available power between minimum and maximum allowed values
        charge_power = max(self._P_MIN_KW, min(pv_P_available, self._P_MAX_KW))
        return charge_power
              
        
         
    def set_charge_current(self) -> bool:
        """
        Set the charging current on the wallbox if it differs from the current setting.

        Returns:
            bool: True if the charging current was updated, False otherwise.
        """
        current_setting = self.m_keykontactP30.get_Max_Charging_Current()
        if abs(self.m_charge_current - current_setting) > 0.01:
            if self.m_charge_current >= self._I_MIN_A:
                self.m_keykontactP30.set_Set_Charging_Current(self.m_charge_current)
                self.m_logger.info(f"Setting charge current to {self.m_charge_current:.2f} A.")
                return True
            else:
                self.m_logger.warning(
                    f"Requested charge current {self.m_charge_current:.2f} A is below minimum allowed ({self._I_MIN_A} A)."
                )
        return False


                                  
    def do_process(self, pv_P_available: float) -> bool:
        """
        Main process loop for PV and BOOST load management.

        Args:
            pv_P_available (float): Available PV power in kW.

        Returns:
            bool: True if processing was performed.
        """
        # Read input states
        pv_loading = self.m_inputs[2].get("state", True)
        boost_loading = self.m_inputs[3].get("state", True)

        # Gather current wallbox and EV states
        Charging_State = self.m_keykontactP30.get_Charging_State()
        Cable_State = self.m_keykontactP30.get_Cable_State()
        EVSE_Error_Code = self.m_keykontactP30.get_EVSE_Error_Code()
        Active_Power = self.m_keykontactP30.get_Active_Power()
        self.get_phase_state()

        def switch_to_phase(target_phase: int):
            if self.m_switch_to_set != target_phase:
                self.m_switch_to = target_phase
                self.do_process_phase_changing()
                self.m_state = WalboxState.Phase_Switching.value
                self.m_logger.info(f"Switching to {target_phase}-phase loading.")

        def reset_loading_state(reason: str):
            self.m_state = WalboxState.Waiting_for_Plugged_Out.value
            self.m_logger.info(f"{reason}, resetting loading.")

        match self.m_state:
            case WalboxState.Waiting_for_Plugged_In.value:
                if self.is_cable_plugged():
                    if self.is_in_loading_state():
                        if self.is_in_error_state():
                            reset_loading_state("Cable plugged in, but in error state")
                            return False
                        if self.is_in_interrupted_state():
                            self.m_keykontactP30.set_Charging_Station_Enable(1)
                            self.m_logger.info("Cable plugged in, interrupted state, enabling charging station.")
                            return False
                        if self.is_waiting_for_vehicle_reaction():
                            self.m_keykontactP30.set_Charging_Station_Enable(1)
                            self.m_logger.info("Cable plugged in, waiting for vehicle reaction, enabling charging station.")
                            return False
                        if EVSE_Error_Code != 0:
                            reset_loading_state(f"EVSE Error Code {EVSE_Error_Code} detected")
                            return False
                        if Active_Power > 10.0:
                            reset_loading_state("Active Power > 0")
                            self.set_charge_current()
                            if pv_loading:
                                self.m_state = WalboxState.PV_Loading.value
                                self.m_logger.info("Switching to PV loading mode.")
                            elif boost_loading:
                                self.m_state = WalboxState.BOOST_Loading.value
                                self.m_logger.info("Switching to BOOST loading mode.")
                            else:
                                self.m_state = WalboxState.no_Loading.value
                                self.m_keykontactP30.set_Charging_Station_Enable(0)
                                self.m_logger.info("Defaulting to no_Loading.")
                        else:
                            reset_loading_state("No Active Power detected")
                            return False
                    elif self.is_not_inloading_state():
                        pass
                elif self.is_cable_not_plugged():
                    if self.m_switch_to_set != 1:
                        switch_to_phase(1)
                        self.m_logger.info("Cable not plugged, switching to 1-phase loading.")
                    if self.m_charge_current != self._I_MIN_A:
                        self.m_charge_current = self._I_MIN_A
                else:
                    reset_loading_state("Cable state unknown")

            case WalboxState.PV_Loading.value:
                if boost_loading:
                    self.m_state = WalboxState.Waiting_for_Plugged_In.value
                    self.m_logger.info("BOOST loading requested, switching state.")
                else:
                    is_pvcharging_active = self.is_pvcharging_active(pv_P_available)
                    charge_power = self.calculate_charge_power(pv_P_available)
                    if self.is_cable_plugged():
                        if self.is_in_loading_state():
                            self.set_light(0, True, 50, 0, 0)
                            self.m_pv_P_available = charge_power
                            if self.is_in_error_state():
                                reset_loading_state("PV: Error state detected")
                            elif self.is_waiting_for_vehicle_reaction():
                                pass
                            elif self.is_in_interrupted_state() and is_pvcharging_active:
                                self.m_keykontactP30.set_Charging_Station_Enable(1)
                                self.m_logger.info("PV: Interrupted state but PV charging active, enabling charging station.")
                            elif not self.is_in_interrupted_state() and not is_pvcharging_active:
                                self.m_keykontactP30.set_Charging_Station_Enable(0)
                                self.m_logger.info("PV: Not interrupted and PV charging not active, disabling charging station.")
                            else:
                                if charge_power > self._P_MIN_3_Phase_KW:
                                    switch_to_phase(3)
                                    self.m_logger.info("PV: Switching to 3-phase loading.")
                                else:
                                    switch_to_phase(1)
                                    self.m_logger.info("PV: Switching to 1-phase loading.")
                                charge_current = self.calculate_charge_current(charge_power)
                                if self.m_charge_current != charge_current:
                                    self.m_charge_current = charge_current
                                    self.m_state = WalboxState.Phase_Switching.value
                                    self.m_logger.info("PV: Charge current changed, switching phase.")
                        elif self.is_not_inloading_state():
                            reset_loading_state("PV: Error/interrupted state detected")
                    elif self.is_cable_not_plugged():
                        reset_loading_state("PV: Cable not plugged")

            case WalboxState.BOOST_Loading.value:
                if pv_loading:
                    self.m_state = WalboxState.Waiting_for_Plugged_In.value
                    self.m_logger.info("PV loading requested, switching state.")
                else:
                    if self.is_cable_plugged():
                        if self.is_in_loading_state():
                            self.m_pv_P_available = self._P_MAX_KW
                            target_phase = 3 if self._P_MAX_KW >= self._P_MIN_3_Phase_KW else 1
                            switch_to_phase(target_phase)
                            charge_current = self.calculate_charge_current(self.m_pv_P_available)
                            if self.m_charge_current != charge_current:
                                self.m_charge_current = charge_current
                                self.m_state = WalboxState.Phase_Switching.value
                                self.m_logger.info("BOOST: Charge current changed, switching phase.")
                        elif self.is_not_inloading_state():
                            self.m_keykontactP30.set_Charging_Station_Enable(1)
                            self.m_logger.info("BOOST: Cable plugged, enabling charging station.")
                        elif self.is_in_error_state() or self.is_in_interrupted_state():
                            reset_loading_state("BOOST: Error/interrupted state detected")
                        elif self.is_waiting_for_vehicle_reaction():
                            reset_loading_state("BOOST: Waiting for vehicle reaction")
                    elif self.is_cable_not_plugged():
                        reset_loading_state("BOOST: Cable not plugged")

            case WalboxState.Phase_Switching.value:
                phase_switch_complete = self.do_process_phase_changing()
                if phase_switch_complete:
                    self.m_logger.info(f"Phase switching to {self.m_switch_to}-phase completed.")
                    self.set_charge_current()
                    if pv_loading:
                        self.m_state = WalboxState.PV_Loading.value
                        self.m_logger.info("Returning to PV loading mode after phase switch.")
                    elif boost_loading:
                        self.m_state = WalboxState.BOOST_Loading.value
                        self.m_logger.info("Returning to BOOST loading mode after phase switch.")
                    else:
                        self.m_state = WalboxState.no_Loading.value
                        self.m_logger.info("Phase switching complete, no loading requested.")
                else:
                    self.m_logger.debug("Phase switching in progress, waiting for completion.")

            case WalboxState.no_Loading.value:
                self.set_light(0, False, 50, 0, 0)
                self.set_light(1, False, 50, 0, 0)
                if pv_loading:
                    self.m_state = WalboxState.PV_Loading.value
                    self.m_logger.info("Switching to PV loading mode.")
                elif boost_loading:
                    self.m_state = WalboxState.BOOST_Loading.value
                    self.m_logger.info("Switching to BOOST loading mode.")

            case WalboxState.Waiting_for_Plugged_Out.value:
                if self.is_cable_plugged():
                    self.set_light(1, True, 50, 0, 0)
                elif self.is_cable_not_plugged():
                    if self.m_charge_current != self._I_MIN_A:
                        self.m_charge_current = self._I_MIN_A
                        self.set_charge_current()
                    if self.m_switch_to_set != 1:
                        switch_to_phase(1)
                        self.m_logger.info("Cable not plugged, switching to 1-phase loading.")
                    else:
                        phase_setting = self.do_process_phase_changing()
                        if phase_setting:
                            self.m_logger.info("Cable not plugged, resetting state to Waiting_for_Plugged_In.")
                            self.m_state = WalboxState.Waiting_for_Plugged_In.value

        self.request_state()
        return True
