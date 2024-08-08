from fastapi import FastAPI

from pifleet.api.v1.endpoints import router
from pifleet.db.models import Base
from pifleet.db.session import engine

# Create database tables if they don't exist
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PiFleet API")

# Include the API router
app.include_router(router, prefix="/v1")
