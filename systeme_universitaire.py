import json
import os
import hashlib
from datetime import datetime, timedelta

# CONFIGURATION fsd
#Test1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIBLIO_FILE = os.path.join(BASE_DIR, "bibliotheque.json")
SALLES_FILE = os.path.join(BASE_DIR, "salles.json")
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# OUTILS 

def input_int(msg):
    while True:
        try:
            val = int(input(msg))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Entier positif requis.")

def input_text(msg):
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("Champ vide interdit.")

def input_date(msg):
    while True:
        val = input(msg).strip()
        try:
            datetime.strptime(val, "%d-%m-%Y")
            return val
        except ValueError:
            print("Format invalide (DD-MM-YYYY).")

def auth_admin():
    for _ in range(3):
        if hashlib.sha256(input("Mot de passe admin : ").encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            return True
        print("Incorrect.")
    print("Accès refusé.")
    return False

def charger_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def sauvegarder_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# SALLES 

class Salle:
    def __init__(self, numero, capacite, disponible=True):
        self.numero = numero
        self.capacite = capacite
        self.disponible = disponible

    def to_dict(self):
        return self.__dict__

class GestionSalles:
    def __init__(self):
        self.salles = {}
        self.reservations = []
        self.charger()

    def charger(self):
        data = charger_json(SALLES_FILE, {"salles": [], "reservations": []})
        for s in data["salles"]:
            self.salles[s["numero"]] = Salle(**s)
        self.reservations = data["reservations"]

    def sauvegarder(self):
        sauvegarder_json(SALLES_FILE, {
            "salles": [s.to_dict() for s in self.salles.values()],
            "reservations": self.reservations
        })

    def afficher(self):
        if not self.salles:
            print("Aucune salle.")
            return
        for s in self.salles.values():
            print(f"Salle {s.numero} | Capacité {s.capacite}")

    def afficher_reservations(self):
        if not self.reservations:
            print("Aucune réservation.")
            return
        for r in self.reservations:
            print(f"{r['nom']} - Salle {r['numero']} - {r['date']}")

    def reserver(self):
        nom = input_text("Nom : ")
        numero = input_text("Numéro salle : ")
        date = input_date("Date (DD-MM-YYYY) : ")

        if numero not in self.salles:
            print("Salle introuvable.")
            return

        if any(r["numero"] == numero and r["date"] == date for r in self.reservations):
            print("Déjà réservée.")
            return

        self.reservations.append({"nom": nom, "numero": numero, "date": date})
        self.sauvegarder()
        print("Réservation confirmée.")

    def liberer(self):
        numero = input_text("Numéro salle : ")
        date = input_date("Date (DD-MM-YYYY) : ")

        self.reservations = [
            r for r in self.reservations
            if not (r["numero"] == numero and r["date"] == date)
        ]
        self.sauvegarder()
        print("Réservation annulée.")

    def ajouter(self):
        numero = input_text("Numéro salle : ")
        if numero in self.salles:
            print("Existe déjà.")
            return
        self.salles[numero] = Salle(numero, input_int("Capacité : "))
        self.sauvegarder()
        print("Salle ajoutée.")

    def supprimer(self):
        numero = input_text("Numéro salle : ")
        if numero not in self.salles:
            print("Introuvable.")
            return
        del self.salles[numero]
        self.sauvegarder()
        print("Salle supprimée.")

# BIBLIOTHEQUE 

class Livre:
    def __init__(self, isbn, titre, auteur, annee, editeur, nb_exemplaires=1):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.editeur = editeur
        self.nb_exemplaires = nb_exemplaires

    def to_dict(self):
        return self.__dict__

class Adherent:
    LIMITE_EMPRUNTS = 5

    def __init__(self, num_adherent, nom, prenom):
        self.num_adherent = num_adherent
        self.nom = nom
        self.prenom = prenom
        self.livres_empruntes = {}
        self.historique = []

    def to_dict(self):
        return self.__dict__

class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.adherents = {}
        self.charger()

    def charger(self):
        data = charger_json(BIBLIO_FILE, {"livres": [], "adherents": []})
        for l in data["livres"]:
            self.livres[l["isbn"]] = Livre(**l)
        for a in data["adherents"]:
            adh = Adherent(a["num_adherent"], a["nom"], a["prenom"])
            adh.livres_empruntes = a.get("livres_empruntes", {})
            adh.historique = a.get("historique", [])
            self.adherents[a["num_adherent"]] = adh

    def sauvegarder(self):
        sauvegarder_json(BIBLIO_FILE, {
            "livres": [l.to_dict() for l in self.livres.values()],
            "adherents": [a.to_dict() for a in self.adherents.values()]
        })

    def afficher(self):
        if not self.livres:
            print("Aucun livre.")
            return
        for l in self.livres.values():
            print(f"\nAuteur: {l.auteur}")
            print(f"Titre: {l.titre}")
            print(f"ISBN: {l.isbn}")
            print(f"Année: {l.annee}")
            print(f"Éditeur: {l.editeur}")
            print(f"Stock: {l.nb_exemplaires}")

    def trouver_livre(self, titre, auteur):
        for l in self.livres.values():
            if l.titre.lower() == titre.lower() and l.auteur.lower() == auteur.lower():
                return l

    def ajouter(self):
        isbn = input_text("ISBN : ")
        self.livres[isbn] = Livre(
            isbn,
            input_text("Titre : "),
            input_text("Auteur : "),
            input_int("Année : "),
            input_text("Éditeur : "),
            input_int("Nombre d'exemplaires : ")
        )
        self.sauvegarder()
        print("Livre ajouté.")

    def supprimer_livre(self):
        isbn = input_text("ISBN : ")
        if isbn not in self.livres:
            print("Introuvable.")
            return
        del self.livres[isbn]
        self.sauvegarder()
        print("Livre supprimé.")

    def ajouter_adherent(self):
        num = input_int("Numéro adhérent : ")
        self.adherents[num] = Adherent(num, input_text("Nom : "), input_text("Prénom : "))
        self.sauvegarder()
        print("Adhérent ajouté.")

    def supprimer_adherent(self):
        num = input_int("Numéro adhérent : ")
        if num not in self.adherents:
            print("Introuvable.")
            return
        del self.adherents[num]
        self.sauvegarder()
        print("Adhérent supprimé.")

    def emprunter(self):
        num = input_int("Num adhérent : ")
        if num not in self.adherents:
            print("Adhérent introuvable.")
            return

        livre = self.trouver_livre(input_text("Titre : "), input_text("Auteur : "))
        if not livre or livre.nb_exemplaires <= 0:
            print("Livre indisponible.")
            return

        adherent = self.adherents[num]

        if len(adherent.livres_empruntes) >= Adherent.LIMITE_EMPRUNTS:
            print("Limite atteinte (5 livres).")
            return

        date_emprunt = datetime.now()
        date_limite = date_emprunt + timedelta(days=14)

        livre.nb_exemplaires -= 1

        adherent.livres_empruntes[livre.isbn] = {
            "date_emprunt": date_emprunt.strftime("%d-%m-%Y"),
            "date_limite": date_limite.strftime("%d-%m-%Y")
        }

        adherent.historique.append(
            f"{date_emprunt.strftime('%d-%m-%Y')} - Emprunt : {livre.titre}"
        )

        self.sauvegarder()
        print("Emprunt validé.")
        print("Date limite :", date_limite.strftime("%d-%m-%Y"))

    def rendre(self):
        num = input_int("Num adhérent : ")
        if num not in self.adherents:
            print("Adhérent introuvable.")
            return

        livre = self.trouver_livre(input_text("Titre : "), input_text("Auteur : "))
        adherent = self.adherents[num]

        if not livre or livre.isbn not in adherent.livres_empruntes:
            print("Livre non emprunté.")
            return

        del adherent.livres_empruntes[livre.isbn]
        livre.nb_exemplaires += 1

        adherent.historique.append(
            f"{datetime.now().strftime('%d-%m-%Y')} - Retour : {livre.titre}"
        )

        self.sauvegarder()
        print("Livre rendu.")

    def voir_historique(self):
        num = input_int("Num adhérent : ")
        if num not in self.adherents:
            print("Introuvable.")
            return
        for h in self.adherents[num].historique:
            print(h)

# MENU 

def menu(titre, options):
    while True:
        print(f"\n=== {titre} ===")
        for i, (txt, _) in enumerate(options, 1):
            print(f"{i}. {txt}")
        choix = input_int("Choix : ")
        if 1 <= choix <= len(options):
            if options[choix-1][1]():
                break

biblio = Bibliotheque()
salles = GestionSalles()

def menu_utilisateur():
    menu("ESPACE UTILISATEUR", [
        ("Voir livres", biblio.afficher),
        ("Emprunter", biblio.emprunter),
        ("Rendre", biblio.rendre),
        ("Historique", biblio.voir_historique),
        ("Réserver salle", salles.reserver),
        ("Libérer salle", salles.liberer),
        ("Voir salles", salles.afficher),
        ("Voir réservations", salles.afficher_reservations),
        ("Retour", lambda: True)
    ])

def menu_admin():
    if not auth_admin():
        return
    menu("ESPACE ADMIN", [
        ("Ajouter livre", biblio.ajouter),
        ("Supprimer livre", biblio.supprimer_livre),
        ("Ajouter adhérent", biblio.ajouter_adherent),
        ("Supprimer adhérent", biblio.supprimer_adherent),
        ("Ajouter salle", salles.ajouter),
        ("Supprimer salle", salles.supprimer),
        ("Voir salles", salles.afficher),
        ("Voir réservations", salles.afficher_reservations),
        ("Retour", lambda: True)
    ])

def menu_principal():
    menu("SYSTÈME UNIVERSITAIRE", [
        ("Utilisateur", menu_utilisateur),
        ("Admin", menu_admin),
        ("Quitter", lambda: True)
    ])

if __name__ == "__main__":
    menu_principal()
