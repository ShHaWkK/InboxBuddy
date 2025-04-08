import requests

def query_ollama(prompt, model="mistral", max_tokens=300):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": max_tokens
            }
        })

        data = response.json()
        if "response" in data:
            return data["response"].strip()
        elif "message" in data:
            return data["message"].strip()
        elif "error" in data:
            print("❌ Erreur du modèle :", data["error"])
            return f"Erreur Ollama : {data['error']}"
        else:
            print("❌ Réponse inattendue :", data)
            return "Erreur inconnue avec le modèle"
    except Exception as e:
        print("❌ Exception côté Ollama:", e)
        return "Erreur technique"
