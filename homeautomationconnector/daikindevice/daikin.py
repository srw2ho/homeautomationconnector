from homeautomationconnector.modbusdevicebase import ModBusDeviceBase

from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class DaikinDevice(ModBusDeviceBase):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        super().__init__(deviceKey, mqttDeviceClient)
        # self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        # self.m_deviceKey: str = deviceKey
        # self.m_writewithNotify: bool = True

    def get_Sensor_LeavingWaterTemperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.LeavingWaterTemperature")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_TankTemperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.TankTemperature")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_OutsideTemperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.OutsideTemperature")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Daily_CoolEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Daily.CoolEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Daily_HeatEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Daily.HeatEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Weekly_CoolEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Weekly.CoolEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Weekly_HeatEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Weekly.HeatEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Weekly_HeatTankEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Weekly.HeatTankEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Yearly_CoolEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Yearly.CoolEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Yearly_HeatEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Yearly.HeatEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_Yearly_HeatTankEnergyConsumption(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.Yearly.HeatTankEnergyConsumption")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_OperationMode(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.OperationMode")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoSetpointMode(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoSetpointMode")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoControlMode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoControlMode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoisHolidayModeActive(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoisHolidayModeActive")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoisInEmergencyState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoisInEmergencyState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoisInErrorState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoisInErrorState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoisInInstallerState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoisInInstallerState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoisInWarningState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoisInWarningState")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoErrorCode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoErrorCode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_WiFiStrength(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.WiFiStrength")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_WiFiSSID(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.WiFiSSID")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InternalSSID(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InternalSSID")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_MacAddress(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.MacAddress")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_SerialNumber(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.SerialNumber")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankheatupMode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankheatupMode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_TankoperationMode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.TankoperationMode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisHolidayModeActive(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisHolidayModeActive")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisInEmergencyState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisInEmergencyState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisInErrorState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisInErrorState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisInInstallerState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisInInstallerState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisInWarningState(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisInWarningState")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankisPowerfulModeActive(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankisPowerfulModeActive")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Sensor_InfoTankErrorCode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("sensor.Altherma.InfoTankErrorCode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_preset_mode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.preset_mode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_hvac_modes(self) -> list[str]:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.hvac_modes")
        )
        val = [] if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_hvac_mode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.hvac_mode")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_CLIMATE_hvac_mode(self, value) -> bool:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("CLIMATE.hvac_mode"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret

    def get_CLIMATE_temperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.temperature")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_target_temperature_step(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.target_temperature_step")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_target_temperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.target_temperature")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_CLIMATE_target_temperature(self, value) -> bool:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("CLIMATE.target_temperature"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret
    
    def get_CLIMATE_min_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.min_temp")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_CLIMATE_max_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.max_temp")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_CLIMATE_temperature_unit(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.temperature_unit")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_WATER_extra_state_attributes(self) -> dict:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.extra_state_attributes")
        )
        val = {} if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_WATER_temperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.temperature")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    

    def get_WATER_tank_state(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.tank_state")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_WATER_target_temperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.target_temperature")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_WATER_target_temperature(self, value) -> bool:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("WATER.target_temperature"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret


    def set_WATER_tank_state(self, value) -> bool:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("WATER.tank_state"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret

    def get_WATER_min_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.min_temp")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val     

    def get_WATER_max_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.max_temp")
        )
        val = 0.0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_WATER_temperature_unit(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.temperature_unit")
        )
        val = "" if ret == None else ret  # Requires Python version >= 2.5
        return val       

    def get_WATER_operation_list(self) -> list[str]:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.operation_list")
        )
        val = [] if ret == None else ret  # Requires Python version >= 2.5
        return val   
    
    def get_WATER_turn_on(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("WATER.turn_on")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val     
    
    def get_CLIMATE_turn_on(self) -> bool:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("CLIMATE.turn_on")
        )
        val = False if ret == None else ret  # Requires Python version >= 2.5
        return val                                                                                                                                                                                                                                                                                  