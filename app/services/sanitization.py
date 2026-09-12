import re

def sanitize_text(text: str) -> str:
    """
    Filtra informacion de identificacion personal basica antes de persistir el texto o enviarlo a la IA
    """

    if not text:
        return ""

    # Enmarcar correos electronicos
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[CORREO OCULTO]', text)

    # Enmarcar numeros de telefono
    text = re.sub(r'\b\d{8,12}\b', '[TELEFONO OCULTO]', text)

    return text
