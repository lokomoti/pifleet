from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pifleet.db.models import Device as DBDevice
from pifleet.exceptions import DeviceAlreadyExistsError, DeviceNotFoundError
from pifleet.schemas import Device, DeviceAdopt


def register_device(device: Device, session: Session):
    """Register device into the database."""

    new_device = DBDevice(mac_address=device.mac, ip_address=str(device.ip_address))

    try:
        session.add(new_device)
        session.commit()
        session.refresh(new_device)

        return new_device

    except IntegrityError as e:
        raise DeviceAlreadyExistsError(device.mac) from e


def device_adopted(mac, session: Session) -> bool:
    """Check if given MAC address is adopted."""
    stmt = select(DBDevice.id).where(
        DBDevice.mac_address == mac and DBDevice.adopted is True
    )

    return bool(session.scalars(stmt).one_or_none())


def device_exists(mac, session: Session) -> bool:
    """Check if given MAC address exists."""
    stmt = select(DBDevice.id).where(DBDevice.mac_address == mac)

    return bool(session.scalars(stmt).one_or_none())


def get_device(mac, session: Session) -> DBDevice:
    """Check if given MAC address exists."""
    stmt = select(DBDevice).where(DBDevice.mac_address == mac)

    return session.scalars(stmt).one_or_none()


def adopt_device(device_adopt: DeviceAdopt, session: Session):
    """Adopt device with provided ID."""

    stmt = select(DBDevice).where(DBDevice.id == device_adopt.id)

    if device := session.scalars(stmt).one_or_none():
        device.adopted = True
    else:
        raise DeviceNotFoundError(f"Device with ID: '{device_adopt.id}' not found.")
    
    