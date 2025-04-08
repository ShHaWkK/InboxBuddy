import requests
from utils.ollama_client import query_ollama
def summarize(text):
    prompt = f"Résume ce mail en une seule phrase :\n\n{text[:800]}"
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        data = response.json()
        # Vérification de la réponse
        if "response" in data:
            return data["response"].strip()
        elif "message" in data:
            return data["message"].strip()
        elif isinstance(data, dict):
            return str(data)
        else:
            return "Résumé indisponible."
        
    except Exception as e:
        print("❌ Erreur dans summarize:", e)
        return "Résumé indisponible."
