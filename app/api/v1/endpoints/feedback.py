from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import FeedbackEntry
from app.schemas.feedback import FeedbackCreate
import uuid

router = APIRouter()

@router.post("/analyze-feedback")
def analyze_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        #Preparador de registros para tabla feedback_entries
        new_feedback = FeedbackEntry(

            id=uuid.uuid4(),
            content_text=feedback.text_content,
            is_anonymous=True #Anonimo por defecto, Cambios en futuro.
        )

        #Insercion de datos y guardado en PsotgreSQL
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        #Retorno de confirmacion
        return {
            "status": "success",
            "message": "Feedback recibido y analizado correctamente",
            "feedback_id": new_feedback.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
