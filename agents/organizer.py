def classify_mail(mail):
    if "facture" in mail["subject"].lower():
        return "Facture"
    elif "rdv" in mail["body"].lower():
        return "Calendrier"
    else:
        return "Autre"
