import os
from dotenv import load_dotenv

load_dotenv() # Cargar variables de entorno desde el archivo .env

def analyze_sentiment_with_ai(text: str) -> dict:
    """
    Procesa el texto sanitizado utilizando LangChain y modelos LLM.
    Devuelve polaridad, etiqueta y metadatos de riesgo
    """
    # Logica para conexion entre azureChatOpenAI y LangChain
    # Cambios futuros debido a que son Claves privadas (Utilizar Azure grapas)
    # llm = AzureChatOpenAI(
    #     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    #     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    #     api_version=os.getenv("OPENAI_API_VERSION"),
    #     deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    #     temperature= 0.3
    #)

    # Simulacion para validar la arquitectura.
    texto_lower = text.lower()

    if any(palabra in texto_lower for palabra in ["mal", "pesado", "estrés", "renunciar", "problema"]):
        return {
            "polarity_score": -0.8,
            "sentiment_label": "Negativo",
            "metadata_ai": {"emocion": "frustracion", "riesgo_burnout": True}
        }
    elif any(palabra in texto_lower for palabra in ["bueno", "excelente", "motivador", "bien"]):
        return {
            "polarity_score": 0.8,
            "sentiment_label": "Positivo",
            "metadata_ai": {"emocion": "motivacion", "riesgo_burnout": False}
        }
    else:
        return{
            "polarity_score": 0.1,
            "sentiment_label": "Neutral",
            "metadata_ai": {"emocion": "calma", "riesgo_burnout": False}
        }
