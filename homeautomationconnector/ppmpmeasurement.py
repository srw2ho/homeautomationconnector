import json


class PPMPHomeMeasurement(object):
    """Class that represents a PPMP Process Payload packet

    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, payload):
        if isinstance(payload, dict):
            self.data = payload
        else:
            self.data = json.loads(payload)

    def hostname(self) -> str:
        """Retrieve device hostname

        Returns:
            [str] -- hostname or device.id
        """
        try:
            return self.data["device"]["additionalData"]["hostname"]
        except KeyError:
            return self.data["device"]["id"]

    def getData(self) -> any:
        return self.data
