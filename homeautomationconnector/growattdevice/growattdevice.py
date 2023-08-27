from homeautomationconnector.modbusdevicebase import ModBusDeviceBase

# from homeautomationconnector.processbase import ProcessBase
from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class GrowattDevice(ModBusDeviceBase):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        super().__init__(deviceKey, mqttDeviceClient)
        # self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        # self.m_deviceKey: str = deviceKey
        # self.m_writewithNotify: bool = True

    # def getKeyByDeviceName(self, key) -> str:
    #     return f"@{self.m_deviceKey}.{key}"

    def get_Inverter_Status(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Inverter_Status")
        )
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Ppv(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Ppv"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vpv1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vpv1"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_PV1Curr(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("PV1Curr"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Ppv1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Ppv1"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vpv2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vpv2"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_PV2Curr(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("PV2Curr"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Ppv2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Ppv2"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pac(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Pac"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Fac(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Fac"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vac1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac1"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Iac1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Iac1"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pac1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Pac1"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vac2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac2"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Iac2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Iac2"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pac2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Pac2"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vac3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac3"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Iac3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Iac3"))
        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pac3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Pac3"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_Vac_RS(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac_RS"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_Vac_ST(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac_ST"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vac_TR(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vac_TR"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Eactoday(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Eactoday"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Eactotal(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Eactotal"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Epv1_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Epv1_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Epv1_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Epv1_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Epv2_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Epv2_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Epv2_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Epv2_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Temp1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Temp1"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Temp2(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Temp2"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_Temp3(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Temp3"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
        
    def get_uwSysWorkMode(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("uwSysWorkMode")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pdischarge1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pdischarge1")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pcharge1(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Pcharge1"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Vbat(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("Vbat"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_SOC(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("SOC"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactouser_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactouser_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactouser_R(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactouser R")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactouser_S(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactouser S")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactouser_T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactouser T")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactogrid_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactogrid_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_PLocalLoad_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("PLocalLoad_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactogrid_R(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactogrid_R")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Pactogrid_S(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactogrid_S")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_Pactogrid_T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Pactogrid_T")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_PLocalLoad_R(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("PLocalLoad_R")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_PLocalLoad_S(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("PLocalLoad_S")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    def get_PLocalLoad_T(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("PLocalLoad_T")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val
    
    
                
    def get_Etouser_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Etouser_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Etouser_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Etouser_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Etogrid_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Etogrid_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Etogrid_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Etogrid_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Edischarge1_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Edischarge1_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Edischarge1_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Edischarge1_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Echarge1_today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Echarge1_today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_Echarge1_total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Echarge1_total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_ELocalLoad_Today(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("ELocalLoad_Today")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_ELocalLoad_Total(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("ELocalLoad_Total")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_dwExportLimitApparentPower(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("dwExportLimitApparentPower")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_StatusOld(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_StatusOld")
        )

    def get_BMS_ErrorOld(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_ErrorOld")
        )

    def get_BMS_Status(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_Status")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_Error(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_Error")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_SOC(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("BMS_SOC"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_BatteryVolt(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_BatteryVolt")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_SOH(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("BMS_SOH"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_BatteryVolt(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_BatteryVolt")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_BatteryCurrent(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_BatteryCurrent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_BatteryTemp(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_BatteryCurrent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_BMS_MaxCurrent(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("BMS_MaxCurrent")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val


    def get_BMS_SOH(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("BMS_SOH"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_uwMaxCellVolt(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("uwMaxCellVolt")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def get_uwMinCellVolt(self) -> float:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("uwMaxCellVolt")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    # HoldingRegisters

    def get_OnOff(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("OnOff"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_OnOff(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("OnOff"),
            value=value,
            withNotify=self.m_writewithNotify,
        )
        return ret

    def get_PF_CMD_memory_state(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("PF_CMD_memory_state")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_PF_CMD_memory_state(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("PF_CMD_memory_state"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    # 0-100 or 255 : power is not be limited

    def get_Active_P_Rate(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Active_P_Rate")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_Active_P_Rate(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Active_P_Rate"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    # -100-100 or 255 : power is not be limited

    # ExportLimit enable,
    # 0: Disable exportLimit;
    # 1: Enable 485 exportLimit;
    # 2: Enable 232 exportLimit;
    # 3: Enable CT exportLimit

    def get_ExportLimit_EN_Dis(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("ExportLimit_EN_Dis")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_ExportLimit_EN_Dis(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("ExportLimit_EN_Dis"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    # -1000~+1000

    def get_ExportLimitPowerRate(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("ExportLimitPowerRate")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_ExportLimitPowerRate(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("ExportLimitPowerRate"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def get_SOC_Min(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("SOC_Min"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_SOC_Min(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("SOC_Min"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    def get_Load_Priority(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(
            self.getKeyByDeviceName("Load_Priority")
        )

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    # ForceChrEn/ForceDischrEn
    # Load first=0
    # bat first=1
    # grid first=3

    def set_Load_Priority(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("Load_Priority"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret

    # 2:METER
    # 1:cWirele ssCT
    # 0:cWiredCT

    def get_bCTMode(self) -> int:
        ret = self.m_mqttDeviceClient.getValueByKey(self.getKeyByDeviceName("bCTMode"))

        val = 0 if ret == None else ret  # Requires Python version >= 2.5
        return val

    def set_bCTMode(self, value) -> int:
        ret = self.m_mqttDeviceClient.writeValueByKey(
            key=self.getKeyByDeviceName("bCTMode"),
            value=value,
            withNotify=self.m_writewithNotify,
        )

        return ret
