import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field
from typing import List

load_dotenv() # Cargar variables de entorno desde el archivo .env

# Definicion de Contrato de salida
class AIAnalysisResult(BaseModel):
    polarity_score: float = Field (..., description="Puntuacion de -1.0 (muy negativo) a 1.0 (muy positivo)")
    sentiment_label: str = Field(..., description = "Positivo, Negativo o Neutral")
    emotionsdetected: List[str] = Field(..., description = "Lista de emociones detectadas, ej: frustración, alegría")
    organizational_axes: List[str] = Field(..., description = "Ejes afectados. Solo usa: Liderazgo y management, Carga de trabajo, Ambiente laboral, Compensaciones, Herramientas")
    risk_burnout: bool = Field(..., description="True si hay indicios de burnout, estrés extremo, acoso o renuncia")
    red_flag_reason: str = Field(default="", description="Breve justificación si risk_burnout es True, de lo contrario vacío")




def analyze_sentiment_with_ai(text: str) -> dict:
    """
    Procesa el texto sanitizado utilizando LangChain y modelos LLM.
    evalua polaridad, ejes organizacionales y banderas rojas de riesgo.
    """

    # Verificacion de credenciales en .env; en caso de no, usa fallback
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        return _fallback_simulation(text)

    try:
        # Configuracion del LLM
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION", "2023-05-15"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPOYMENT_NAME"),
            temperature=0.1
        )

        # Obligando para que el modelo respete la estructura de Pydantic
        structured_llm = llm.with_structured_output(AIAnalysisResult)

        # Prompt de Ingenieria
        prompt = f"""
        Eres un analista experto de Recursos Humanos. Analiza el siguiente comentario de un empleado.
        Clasifícalo en los ejes organizacionales y detecta posibles banderas rojas como acoso o intenciones de renuncia.
        
        Comentario: {text}
        """

        # Ejecucion de IA
        result = structured_llm.invoke(prompt)

        # Mapeado de salida para encajar en endpoint de FastAPI
        return {
            "polarity_score": result.polarity_score,
            "sentiment:label": result.sentiment_label,
            "metadata_ai": {
                "emotions": result.emotions_detected,
                "organizational_axes": result.organizational_axes,
                "risk_burnout": result.risk_burnout,
                "red_flag_reason": result.red_flag_reason
            }
        }
    except Exception as e:
        print (f"Error con Azure OpenAI: {e}")
        return _fallback_simulation(text)

    def _fallback_simulation(text: str) -> dict:
        """
        Simulacion de respaldo en caso de no tener API Keys activas o fallas de red.
        """

        texto_lower = text.lower()

        if any(palabra in texto_lower for palabra in ["mal", "pesado", "estrés", "renunciar", "problema"]):
            return {
                "polarity_score": -0.8,
                "sentiment_label": "Negativo",
                "metadata_ai": {
                    "emotions": ["frustración", "cansancio"],
                    "organizational_axes": ["Carga de trabajo"],
                    "risk_burnout": True,
                    "red_flag_reason": "Se detectó lenguaje asociado a estrés o renuncia"
                }
            }
        
        return {
            "polarity_score": 0.8,
            "sentiment_label": "Positivo",
            "metadata_ai": {
                "emotions": ["motivación"],
                "organizational_axes": ["Ambiente laboral"],
                "risk_burnout": False,
                "red_flag_reason": ""
            }
        }
            
