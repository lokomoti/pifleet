import re
from typing import Optional

from pydantic import BaseModel, IPvAnyAddress, field_validator


class Device(BaseModel):
    mac: str
    ip_address: IPvAnyAddress
    hostname: Optional[str] = None

    @field_validator("mac")
    def validate_mac(cls, v):
        mac_regex = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
        if not mac_regex.match(v):
            raise ValueError("Invalid MAC address format")
        return v


class DeviceReport(Device):
    cpu_temp: float
    cpu_usage: float
    ram_usage: float
    uptime: int
    disk_space: int  # Remaining disk space


class DeviceAdopt(BaseModel):
    id: int