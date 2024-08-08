class DeviceError(Exception):
    pass


class DeviceAlreadyExistsError(DeviceError):
    def __init__(self, mac: str):
        self.mac = mac
        self.message = f"Device with MAC address {mac} already exists."
        super().__init__(self.message)


class DeviceStatusInsertError(DeviceError):
    pass


class DeviceNotFoundError(DeviceError):
    pass