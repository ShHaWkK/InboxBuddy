from agents.summarizer import summarize
from agents.responder import generate_reply
from agents.organizer import classify_mail
from agents.reminder import schedule_reminder
from agents.calendar import create_event
from database.db import save_mail
import datetime
import requests

def call_local_model(prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
    except Exception as e:
        print("❌ Erreur avec Ollama :", e)
        return "['résumé']"

def core_agent_decision(mail):
    prompt = f"""
Tu es un assistant IA. Voici un mail reçu :

Expéditeur : {mail['from']}
Sujet : {mail['subject']}
Contenu : {mail['body'][:500]}

Quelles actions dois-tu faire ?
Choisis dans cette liste :
- résumé
- répondre
- classer
- programmer un rappel
- programmer un rdv

Réponds uniquement sous forme de liste Python : ["résumé", "répondre"]
"""
    response = call_local_model(prompt)
    print("🧠 Réponse brute Mistral:", response)

    try:
        actions = eval(response.strip())
        if isinstance(actions, list):
            return actions
    except:
        pass
    return ["résumé"]

def process_mail(mail):
    actions = core_agent_decision(mail)
    results = {}

    if "résumé" in actions:
        results["résumé"] = summarize(mail["body"])

    if "répondre" in actions:
        results["réponse"] = generate_reply(mail)

    if "classer" in actions:
        results["classement"] = classify_mail(mail)

    if "programmer un rappel" in actions:
        results["rappel"] = schedule_reminder(mail)

    if "programmer un rdv" in actions:
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        results["event"] = create_event("RDV détecté", mail["body"], now)

    save_mail(mail, summary=results.get("résumé"), response=results.get("réponse"))

    return results
