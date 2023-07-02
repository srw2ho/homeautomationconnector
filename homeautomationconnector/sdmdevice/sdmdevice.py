from homeautomationconnector.modbusdevicebase import ModBusDeviceBase

from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class SDM630Device(ModBusDeviceBase):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        super().__init__(deviceKey,mqttDeviceClient)
        # self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        # self.m_deviceKey: str = deviceKey
        # self.m_writewithNotify: bool = True

    # def getKeyByDeviceName(self, key) -> str:
    #     return f"@{self.m_deviceKey}.{key}"

    def get_l1_voltage(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_voltage")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_voltage(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_voltage"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_voltage(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l3_voltage"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l1_current"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_current"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l3_current"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l1_power_active"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_power_active"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l3_power_active"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_power_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l1_power_apparent"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_power_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_power_apparent"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_power_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l3_power_apparent"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_power_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l1_power_reactive"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_power_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_power_reactive"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_power_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l3_power_reactive"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_power_factor(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_power_factor")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_power_factor(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_power_factor")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_power_factor(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_power_factor")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_phase_angle(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_phase_angle")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_phase_angle(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l2_phase_angle"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_phase_angle(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_phase_angle")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_voltage_ln(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("voltage_ln")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_current_ln(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("current_ln"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_line_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("total_line_current"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("total_power_active"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_power_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_power_apparent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_power_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_power_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_power_factor(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_power_factor")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_phase_angle(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_phase_angle")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_frequency(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("frequency")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_import_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("import_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_export_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("export_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_import_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("import_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_export_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("export_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_energy_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_energy_apparent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_import_demand_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_import_demand_power_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_import_demand_power_apparent(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_import_demand_power_apparent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_import_demand_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("import_demand_power_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_import_demand_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_import_demand_power_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_export_demand_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("export_demand_power_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_export_demand_power_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_export_demand_power_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_demand_power_apparent(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_demand_power_apparent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_demand_power_apparent(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_demand_power_apparent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_neutral_demand_current(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("neutral_demand_current"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_neutral_demand_current(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_neutral_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l12_voltage(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("l12_voltage"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l23_voltage(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l23_voltage")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l31_voltage(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l31_voltage")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_voltage_ll(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("voltage_ll")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_neutral_current(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("neutral_current"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1n_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1n_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2n_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2n_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l3n_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3n_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l1_current_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_current_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val



    def get_l2_current_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_current_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val



    def get_l3_current_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_current_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val



    def get_voltage_ln_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("voltage_ln_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_current_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("current_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_pf(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_pf")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_l1_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_l1_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_l2_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_l2_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_maximum_l3_demand_current(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("maximum_l3_demand_current")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l12_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l12_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l23_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l23_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l31_voltage_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l31_voltage_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    

    def get_voltage_ll_thd(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("voltage_ll_thd")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_total_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("total_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_import_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_import_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_import_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_import_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_import_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_import_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_export_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_export_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l2_export_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_export_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_export_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_export_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l1_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_energy_active(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_energy_active")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l1_import_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_import_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l2_import_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_import_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l3_import_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_import_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l1_export_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_export_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l2_export_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_export_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l3_export_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_export_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_l1_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l1_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l2_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l2_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_l3_energy_reactive(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("l3_energy_reactive")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val




    # HoldingRegisters

    def get_demand_time(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("demand_time"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_demand_time(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("demand_time"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret

    def get_demand_period(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("demand_period")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_demand_period(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("demand_period"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret



    def get_meter_id(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("meter_id")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_meter_id(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("meter_id"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret


    def get_system_power(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("system_power")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_system_power(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("system_power"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret



    def get_serial_number(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("serial_number")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_serial_number(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("serial_number"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret


