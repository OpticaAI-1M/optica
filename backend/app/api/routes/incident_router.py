"""
Incident API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.services.incident_service import IncidentService


router = APIRouter(prefix="/incidents", tags=["incidents"])


def get_db():
    """
    Dependency to get DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_incident(
    payload: dict,
    db: Session = Depends(get_db),
):
    service = IncidentService()

    try:
        incident = service.create_incident(db, payload)
        return {"id": str(incident.id)}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Invalid foreign key reference (user or team not found)",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )