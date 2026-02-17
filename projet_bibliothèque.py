import json
from datetime import datetime, timedelta


# demande à l'utilisateur de saisir un entier, et repose la question si la valeur n'en est pas un
def input_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Veuillez entrer un nombre valide.")


# partie admin
# charge le mot de passe depuis le fichier admin.json
def charger_admin():
    try:
        # ouvre "admin.json" en mode lecture ("r")
        with open("admin.json", "r") as f:
            # on va chercher l'information dans "password"
            return json.load(f)["password"]
    # si le fichier "admin.json" n'existe pas dans notre ordinateur    
    except FileNotFoundError:
        # on renvoit un mot de passe par défaut de secours
        return "admin125"

# on appelle la fonction charger_admin et on stocke le mot de passe dans ADMIN_PASSWORD
ADMIN_PASSWORD = charger_admin()

# on vérifie si l'utilisateur est bien admin
def est_admin():
    # vérifie si le mot de passe entré par l'utilisateur est le bon
    mdp = input("Mot de passe administrateur : ")
    return mdp == ADMIN_PASSWORD


#partie classe

class Livre:
    # initialise la classe livre
    def __init__(self, isbn, titre, auteur, annee, editeur, nb_exemplaires=1):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.editeur = editeur
        self.nb_exemplaires = nb_exemplaires

    # diminue de 1 le stock
    def emprunter(self):
        if self.nb_exemplaires > 0:
            self.nb_exemplaires -= 1
            return True
        return False

    # 
    def retirer(self):
        if self.nb_exemplaires > 0:
            self.nb_exemplaires -= 1
            return True
        return False

    # rajoute 1 dans le stock
    def rendre(self):
        self.nb_exemplaires += 1

    # transforme l'objet livre en dictionnaire
    def to_dict(self):
        return self.__dict__


class Adherent:
    LIMITE_EMPRUNTS = 5
    # initialise la classe adhérent
    def __init__(self, num_adherent, nom, prenom):
        self.num_adherent = num_adherent
        self.nom = nom
        self.prenom = prenom
        self.livres_empruntes = {}

    # vérifie si l'adhérent peut encore emprunter un livre
    def peut_emprunter(self):
        # len permet de compter les éléments d'une liste
        return len(self.livres_empruntes) < self.LIMITE_EMPRUNTS

    # ajoute le livre à la liste des livres empruntés par l'adhérent avec une date de retour (+14 jours) si toutes les conditions sont réunies
    def emprunter(self, livre):
        # vérifie si le livre a déjà été emprunté par l'adhérent
        if livre.isbn in self.livres_empruntes:
            print("Vous avez déjà emprunté ce livre.")
            return False
        # vérifie si le quota est atteint
        if not self.peut_emprunter():
            print("Limite d'emprunts atteinte.")
            return False

        date_emprunt = datetime.now()
        date_limite = date_emprunt + timedelta(days=14)

        self.livres_empruntes[livre.isbn] = {
            "date_emprunt": date_emprunt.strftime("%Y-%m-%d"),
            "date_limite": date_limite.strftime("%Y-%m-%d")
        }

        return True

    # 
    def rendre(self, livre):
        if livre.isbn in self.livres_empruntes:
            del self.livres_empruntes[livre.isbn]
            return True
        return False

    def to_dict(self):
        return {
            "num_adherent": self.num_adherent,
            "nom": self.nom,
            "prenom": self.prenom,
            "livres_empruntes": self.livres_empruntes
        }


class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.adherents = {}

    # -------- SAUVEGARDE --------

    def sauvegarder(self):
        data = {
            "livres": [livre.to_dict() for livre in self.livres.values()],
            "adherents": [adherent.to_dict() for adherent in self.adherents.values()]
        }

        with open("bibliotheque.json", "w") as f:
            json.dump(data, f, indent=4)

    def charger(self):
        try:
            with open("bibliotheque.json", "r") as f:
                data = json.load(f)

            for l in data["livres"]:
                livre = Livre(**l)
                self.livres[livre.isbn] = livre

            for a in data["adherents"]:
                adherent = Adherent(a["num_adherent"], a["nom"], a["prenom"])
                adherent.livres_empruntes = a["livres_empruntes"]
                self.adherents[adherent.num_adherent] = adherent

            print("Bibliothèque chargée !")

        except FileNotFoundError:
            print("Nouvelle bibliothèque créée.")

    # -------- LIVRES --------

    def ajouter_livre(self, isbn, titre, auteur, annee, editeur):

        if isbn in self.livres:
            self.livres[isbn].nb_exemplaires += 1
        else:
            self.livres[isbn] = Livre(isbn, titre, auteur, annee, editeur)

        print("Livre ajouté !")
        self.sauvegarder()

    def retirer_livre(self, isbn):

        livre = self.livres.get(isbn)

        if not livre:
            print("Livre introuvable.")
            return

        if livre.retirer():

            if livre.nb_exemplaires == 0:
                del self.livres[isbn]
                print("Livre supprimé de la bibliothèque.")
            else:
                print("Un exemplaire a été retiré.")

            self.sauvegarder()
        else:
            print("Impossible de retirer ce livre.")

    def afficher_livres(self):
        if not self.livres:
            print("Aucun livre.")
            return

        for livre in self.livres.values():
            print(f"{livre.titre} - {livre.auteur} | Exemplaires: {livre.nb_exemplaires}")

    def trouver_livre_par_titre(self, titre):
        for livre in self.livres.values():
            if livre.titre.lower() == titre.lower():
                return livre
        return None

    # -------- EMPRUNTS --------

    def emprunter_livre(self, num_adherent, titre):
        adherent = self.adherents.get(num_adherent)

        if not adherent:
            print("Adhérent non trouvé.")
            return

        livre = self.trouver_livre_par_titre(titre)

        if not livre:
            print("Livre introuvable.")
            return

        if not livre.emprunter():
            print("Plus d'exemplaires.")
            return

        if not adherent.emprunter(livre):
            livre.rendre()
            return

        infos = adherent.livres_empruntes[livre.isbn]

        print("Emprunt validé !")
        print("Date d'emprunt :", infos["date_emprunt"])
        print("Date limite :", infos["date_limite"])

        self.sauvegarder()

    def rendre_livre(self, num_adherent):
        adherent = self.adherents.get(num_adherent)

        if not adherent or not adherent.livres_empruntes:
            print("Aucun livre à rendre.")
            return

        livres_list = list(adherent.livres_empruntes.items())

        for i, (isbn, infos) in enumerate(livres_list, 1):
            livre = self.livres[isbn]
            date_limite = datetime.strptime(infos["date_limite"], "%Y-%m-%d")

            jours_retard = (datetime.now() - date_limite).days

            if jours_retard > 0:
                amende = jours_retard * 1
                print(f"{i}. EN RETARD - {livre.titre} | Amende : {amende}€")
            else:
                print(f"{i}. {livre.titre} | Limite {infos['date_limite']}")

        choix = input_int("Quel livre rendre ? ") - 1

        livre = self.livres[livres_list[choix][0]]
        adherent.rendre(livre)
        livre.rendre()

        print("Livre rendu !")
        self.sauvegarder()


# -------- INITIALISATION --------

bibliotheque = Bibliotheque()
bibliotheque.charger()


# -------- MENUS --------

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Mode utilisateur")
        print("2. Mode administrateur")
        print("3. Quitter")

        choix = input_int("Choix : ")

        if choix == 1:
            menu_utilisateur()

        elif choix == 2:
            if est_admin():
                menu_admin()
            else:
                print("Mot de passe incorrect.")

        elif choix == 3:
            bibliotheque.sauvegarder()
            break


def menu_utilisateur():
    while True:
        print("\n=== MENU UTILISATEUR ===")
        print("1. Emprunter")
        print("2. Rendre")
        print("3. Voir les livres")
        print("4. Retour")

        choix = input_int("Choix : ")

        if choix == 1:
            bibliotheque.emprunter_livre(input("Num adhérent : "), input("Titre : "))

        elif choix == 2:
            bibliotheque.rendre_livre(input("Num adhérent : "))

        elif choix == 3:
            bibliotheque.afficher_livres()

        elif choix == 4:
            break


def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Ajouter un livre")
        print("2. Retirer un livre")
        print("3. Voir les livres")
        print("4. Retour")

        choix = input_int("Choix : ")

        if choix == 1:

            annee = input_int("Année : ")

            bibliotheque.ajouter_livre(
                input("ISBN : "),
                input("Titre : "),
                input("Auteur : "),
                annee,
                input("Éditeur : ")
            )

        elif choix == 2:
            bibliotheque.retirer_livre(input("ISBN : "))

        elif choix == 3:
            bibliotheque.afficher_livres()

        elif choix == 4:
            break


menu_principal()
