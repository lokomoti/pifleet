from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from pifleet.api import deps
from pifleet.crud import device as d
from pifleet.crud import devicestatus as ds
from pifleet.schemas import DeviceReport

router = APIRouter()


@router.post(
    "/report/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Device was registered."},
        status.HTTP_200_OK: {"description": "Device received, device not adopted."},
        status.HTTP_202_ACCEPTED: {
            "description": "Device status was successfully stored."
        },
    },
)
def handle_device_report(
    device_report: DeviceReport, db: Session = Depends(deps.get_db)
):
    """Handle incoming device report."""

    if device := d.get_device(device_report.mac, db):
        if device.adopted:
            ds.insert_status(device_report, device.id, db)
        else:
            return status.HTTP_200_OK

    else:
        d.register_device(device_report, db)


# @router.patch("/device/", response_model=)