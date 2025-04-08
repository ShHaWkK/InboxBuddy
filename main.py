from core.core_agent import process_mail
from mails.imap import fetch_latest_mails
from database.db import save_mail

print("📬 InboxBuddy CLI - Assistant Mail")
mails = fetch_latest_mails(1)

for mail in mails:
    print(f"\n🔵 Sujet : {mail['subject']}\n🧾 Contenu :\n{mail['body'][:500]}")
    input("↩️ Appuie sur Entrée pour laisser l'IA agir...")

    results = process_mail(mail)

    print("\n🤖 Résultats de l'agent :")
    for k, v in results.items():
        print(f"{k.upper()}:\n{v}\n")

    save_mail(mail, summary=results.get("résumé"), response=results.get("réponse"))
