from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.fastapi_app.app.database import get_db
from backend.fastapi_app.app.schemas import ErrorLogCreate, SolutionResponse
from backend.fastapi_app.app.error_service import save_error
from backend.rag_engine.rag_service import rag_service

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/solve", response_model=SolutionResponse)
def solve_incident(error: ErrorLogCreate, db: Session = Depends(get_db)):
    save_error(
        db=db,
        error_message=error.error_message
    )
    answer = rag_service.answer(
        error.error_message
    )

    return {
       "answer": answer
    }