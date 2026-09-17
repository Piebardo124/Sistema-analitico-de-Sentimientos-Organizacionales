from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import FeedbackEntry, SentimentAnalysis, Alert
from app.schemas.feedback import FeedbackCreate
from app.services.sanitization import sanitize_text
from app.services.ai_engine import analyze_sentiment_with_ai
from app.core.security import verify_token
import uuid


router = APIRouter()

@router.post("/analyze-feedback")
def analyze_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_db)
):
    try:

        # Limpieza de texto con posibles datos sensibles.
        texto_limpio = sanitize_text(feedback.text_content)

        # Preparador de registros para tabla feedback_entries
        new_feedback = FeedbackEntry(
            id=uuid.uuid4(),
            content_text=texto_limpio,
            is_anonymous=True #Anonimo por defecto, Cambios en futuro.
        )

        # Insercion de datos y guardado en PsotgreSQL
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        # Pasador de texto limpio en motor IA
        ai_results = analyze_sentiment_with_ai(texto_limpio)

        # Logica de guardado de resultados de la IA en sentimen_analysis
        new_analysis = SentimentAnalysis(
            feedback_entry_id=new_feedback.id,
            polarity_score=ai_results["polarity_score"],
            sentiment_label=ai_results["sentiment_label"],
            metadata_ai=ai_results["metadata_ai"]
        )
        db.add(new_analysis)
        db.commit()


        # Funcion para Alertas automaticas (Dichosas banderas rojas)
        
        alerta_id = None
        is_risk = ai_results["metadata_ai"].get("risk_burnout", False)

        if is_risk:
            nueva_alerta = Alert(
                feedback_id=new_feedback.id,
                risk_level="ALTO",
                reason=ai_results["metadata_ai"].get("red_flag_reason", "Riesgo detectado por IA")
            )
            db.add(nueva_alerta)
            db.commit()
            db.refresh(nueva_alerta)

            # En caso de riesgo, actualizador de varibale con el ID real de la base de datos
            alerta_id = nueva_alerta.id

        return {
            "status": "success",
            "message": "Feedback recibido, sanitizado y analizado correctamente",
            "entry_id": new_feedback.id,
            "alert_generated_id": alerta_id,
            "ai_analysis": {
                "label": ai_results["sentiment_label"],
                "polarity": ai_results["polarity_score"],
                "details": ai_results["metadata_ai"]
            }
        }

        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
