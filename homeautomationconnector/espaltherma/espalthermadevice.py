from homeautomationconnector.modbusdevicebase import ModBusDeviceBase

from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class ESPAltherma(ModBusDeviceBase):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        super().__init__(deviceKey, mqttDeviceClient)
        # self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        # self.m_deviceKey: str = deviceKey
        # self.m_writewithNotify: bool = True

    # readable HoldingRegisters
    def get_O_U_capacity(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("O/U capacity (kW)")
        )
        val = 0.0 if ret == None else ret
        return val

    def get_Operation_Mode(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Operation Mode")
        )
        val = "" if ret == None else ret
        return val

    def get_Thermostat_ON_OFF(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Thermostat ON/OFF")
        )
        val = "" if ret == None else ret
        return val

    def get_Defrost_Operation(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Defrost Operation")
        )
        val = "" if ret == None else ret
        return val
    
    def get_R1T_Outdoor_air_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("R1T-Outdoor air temp.")
        )
        val = 0.0 if ret == None else ret

    def get_O_U_Heat_Exch_Temp_R4T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("O/U Heat Exch. Temp.(R4T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    
    def get_Discharge_pipe_temp_R2T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Discharge pipe temp.(R2T)")
        )
        val = 0.0 if ret == None else ret
        return val
        
    def get_Suction_pipe_temp_R3T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Suction pipe temp.(R3T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Heat_exchanger_mid_temp_R5T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Heat exchanger mid-temp.(R5T)")
        )
        val = 0.0 if ret == None else ret
        return val
        
    def get_Liquid_pipe_temp_R6T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Liquid pipe temp.(R6T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_High_Pressure(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("High Pressure")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_High_Pressure_T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("High Pressure(T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Low_Pressure(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Low Pressure")
        )
        val = 0.0 if ret == None else ret

    def get_Low_Pressure_T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Low Pressure(T)")
        )
        val = 0.0 if ret == None else ret
        return val
        
    def get_INV_primary_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("INV primary current (A)")
        )
        val = 0.0 if ret == None else ret
        return val
        
    def get_INV_secondary_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("INV secondary current (A)")
        )
        val = 0.0 if ret == None else ret

    def get_INV_fin_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("INV fin temp.")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Fan1_Fin_temp(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Fan1 Fin temp.")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Compressor_outlet_temperature(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Compressor outlet temperature")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_INV_frequency_rps(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("INV frequency (rps)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Fan_1_step(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Fan 1 (step)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_DHW_setpoint(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("DHW setpoint")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_LW_setpoint_main(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("LW setpoint (main)")
        )
        val = 0.0 if ret == None else ret

    def get_Solar_input(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Solar input")
        )
        val = "" if ret == None else ret
        return val
    
    def get_SmartGridContact2(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("SmartGridContact2")
        )
        val = "" if ret == None else ret
        return val
    
    def get_SmartGridContact1(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("SmartGridContact1")
        )
        val = "" if ret == None else ret
        return val
    
    def get_Bivalent_Operation(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Bivalent Operation")
        )
        val = "" if ret == None else ret
        return val
    
    def get_BSH(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BSH")
        )
        val = "" if ret == None else ret
        return val
    
    def get_BUH_Step1(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BUH Step1")
        )
        val = "" if ret == None else ret
        return val
    
    def get_BUH_Step2(self) -> str:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BUH Step2")
        )
        val = "" if ret == None else ret
        return val
    
    def get_Leaving_water_temp_BUH_R1T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Leaving water temp. before BUH (R1T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Leaving_water_temp_BUH_R2T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Leaving water temp. after BUH (R2T)")
        )
        val = 0.0 if ret == None else ret
        return val
    
    def get_Refrig_Temp_liquid_side_R3T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Refrig. Temp. liquid side (R3T)")
        )
        val = 0.0 if ret == None else ret
        return val
        
    def get_Inlet_water_temp_R4T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Inlet water temp.(R4T)")
        )
        val = 0.0 if ret == None else ret
        
    def get_DHW_tank_temp_R5T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("DHW tank temp. (R5T)")
        )
        val = 0.0 if ret == None else ret
        return val

                
                                