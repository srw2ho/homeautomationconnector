from mqttconnector.MQTTServiceDevice import MQTTServiceDeviceClient


class ModBusDeviceBase(object):
    def __init__(
        self, deviceKey: str = "", mqttDeviceClient: MQTTServiceDeviceClient = None
    ):
        self.m_mqttDeviceClient: MQTTServiceDeviceClient = mqttDeviceClient
        self.m_deviceKey: str = deviceKey
        self.m_writewithNotify: bool = True

    def getKeyByDeviceName(self, key) -> str:
        return f"@{self.m_deviceKey}.{key}"
