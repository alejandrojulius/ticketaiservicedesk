from transformers import pipeline
import spacy

nlp = spacy.load("es_core_news_sm")

# Modelo Zero-Shot (fácil y efectivo)
classifier = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli", 
                     device=-1)  # -1 = CPU

categorias = ["Hardware", "Software", "Redes", "Seguridad", "Solicitud de Acceso", 
              "Impresoras", "Correo Electrónico", "Otros"]

def clasificar_ticket(titulo: str, descripcion: str):
    texto = f"{titulo}. {descripcion}"
    
    resultado = classifier(texto, categorias, multi_label=False)
    categoria = resultado['labels'][0]
    confianza = round(resultado['scores'][0] * 100, 2)
    
    # Lógica de prioridad
    texto_lower = texto.lower()
    if any(p in texto_lower for p in ["ransomware", "phishing", "brecha", "ataque"]):
        prioridad = "Crítica"
    elif any(p in texto_lower for p in ["urgente", "inmediato", "caído", "desesperado"]):
        prioridad = "Alta"
    else:
        prioridad = "Media"
    
    explicacion = f"Clasificado como {categoria} con {confianza}% de confianza."
    
    return {
        "categoria": categoria,
        "prioridad": prioridad,
        "confianza": confianza,
        "explicacion": explicacion
    }