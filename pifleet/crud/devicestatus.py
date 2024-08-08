from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pifleet.db.models import Status
from pifleet.exceptions import DeviceStatusInsertError
from pifleet.schemas import DeviceReport


def insert_status(
    device_report: DeviceReport, device_id: int, session: Session
) -> None:
    """Insert device report into the database."""

    new_report = Status(
        device_id=device_id,
        cpu_temp=device_report.cpu_temp,
        disk_space=device_report.disk_space,
        uptime=device_report.uptime,
        cpu_usage=device_report.cpu_usage,
        ram_usage=device_report.ram_usage,
    )

    try:
        session.add(new_report)
        session.commit()
    except IntegrityError as e:
        raise DeviceStatusInsertError from e
