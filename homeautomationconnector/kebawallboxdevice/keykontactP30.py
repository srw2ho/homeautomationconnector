from homeautomationconnector.modbusdevicebase import ModBusDeviceBase

from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class KeykontactP30(ModBusDeviceBase):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        super().__init__(deviceKey, mqttDeviceClient)
        # self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        # self.m_deviceKey: str = deviceKey
        # self.m_writewithNotify: bool = True

    # readable HoldingRegisters
    def get_Charging_State(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Charging_State")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Cable_State(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Cable_State")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_EVSE_Error_Code(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("EVSE_Error_Code")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Current_L1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Current_L1")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Current_L2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Current_L2")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Current_L3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Current_L3")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Serial_Number(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Serial_Number")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Product_Type(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Product_Type")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Firmware_Version(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Firmware_Version")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Active_Power(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Active_Power")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Total_Energy(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Total_Energy")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Voltage_U1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Voltage_U1")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Voltage_U2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Voltage_U2")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Voltage_U3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Voltage_U3")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Power_Factor(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Power_Factor")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Max_Charging_Current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Max_Charging_Current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Max_Supported_Current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Max_Supported_Current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_RFID_Card(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("RFID_Card")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Charged_Energy(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Charged_Energy")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Phase_Switching_Source(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Phase_Switching_Source")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Phase_Switching_State(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Phase_Switching_State")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Failsafe_Current_Setting(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Failsafe_Current_Setting")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_Set_Charging_Current(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Set_Charging_Current"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret

    def set_Set_Energy(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Set_Energy"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Unlock_Plug(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Unlock_Plug"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Charging_Station_Enable(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Charging_Station_Enable"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Set_Phase_Switch_Toggle(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Set_Phase_Switch_Toggle"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Trigger_Phase_Switch(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Set_Phase_Switch_Toggle"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Trigger_Phase_Switch(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Trigger_Phase_Switch"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Failsafe_Current(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Failsafe_Current"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Failsafe_Timeout(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Failsafe_Timeout"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def set_Failsafe_Persist(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Failsafe_Persist"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret
