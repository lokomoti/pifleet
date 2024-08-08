from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mac_address: Mapped[str] = mapped_column(unique=True, index=True)
    ip_address: Mapped[str]
    hostname: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    created_date: Mapped[datetime] = mapped_column(server_default=func.now())
    adopted: Mapped[bool] = mapped_column(default=False)
    statuses: Mapped[List["Status"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Device(id={self.id}, mac={self.mac}, ip={self.ip}, "
            f"hostname={self.hostname}, name={self.name}, "
            f"description={self.description})"
        )


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    cpu_temp: Mapped[float]
    disk_space: Mapped[int]
    cpu_usage: Mapped[int] = None
    ram_usage: Mapped[int] = None
    uptime: Mapped[int]
    device: Mapped[Device] = relationship(back_populates="statuses")
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))

    def __repr__(self) -> str:
        return (
            f"Status(id={self.id}, timestamp={self.timestamp}, "
            f"cpu_temp={self.cpu_temp}, disk_space={self.disk_space}, "
            f"uptime={self.uptime}, device_id={self.device_id})"
        )
