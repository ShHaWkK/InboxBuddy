import requests

def generate_reply(mail):
    prompt = f"""Voici un mail :
Sujet : {mail['subject']}
Contenu : {mail['body'][:800]}

Rédige une réponse courte, polie et professionnelle.
"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        data = response.json()
        if "response" in data:
            return data["response"].strip()
        elif "message" in data:
            return data["message"].strip()
        else:
            return "Réponse générée (texte brut)."
    except Exception as e:
        print("X Erreur dans generate_reply:", e)
        return "Réponse impossible à générer."
