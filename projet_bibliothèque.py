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

    # diminue de 1 le stock
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

        # demande à l'ordinateur la date et l'heure exacte
        date_emprunt = datetime.now()
        # calcul de date, date ajourd'hui + 14 jours
        date_limite = date_emprunt + timedelta(days=14)

        # enregistrement dans le dossier de l'adhérent
        self.livres_empruntes[livre.isbn] = {
            "date_emprunt": date_emprunt.strftime("%Y-%m-%d"),
            "date_limite": date_limite.strftime("%Y-%m-%d")
        }

        return True

    # retire le livre de la liste des livres empruntés par l'adhérent
    def rendre(self, livre):
        if livre.isbn in self.livres_empruntes:
            del self.livres_empruntes[livre.isbn]
            return True
        return False

    # transforme les informations de l'adhérent en dictionnaire pour faciliter la sauvegarde en json
    def to_dict(self):
        return {
            "num_adherent": self.num_adherent,
            "nom": self.nom,
            "prenom": self.prenom,
            "livres_empruntes": self.livres_empruntes
        }


class Bibliotheque:
    # initialisation de la classe bibliothèque 
    def __init__(self):
        self.livres = {}
        self.adherents = {}
   
# partie sauvegarde 
    # prend toutes les données en mémoire et les écrit dans un fichier JSON
    def sauvegarder(self):
        # on créait un grand dictionnaire qui va contenir toutes nos données converties
        data = {
            # on parcourt chaque livre on le transforme en dictionnaire (avec to_dict) et on le met dans une liste
            "livres": [livre.to_dict() for livre in self.livres.values()],
            # pareil pour les adhérents
            "adherents": [adherent.to_dict() for adherent in self.adherents.values()]
        }

        # on ouvre le fichier "bibliotheque.json" en mode écriture ("w" pour write)
        with open("bibliotheque.json", "w") as f:
            json.dump(data, f, indent=4)

    # lit le fichier de sauvegarde au démarrage pour recréer tous les objets (livres et adhérents)
    def charger(self):
        try:
            # on essaie d'ouvrir le fichier en mode lecture ("r" pour read)
            with open("bibliotheque.json", "r") as f:
                # on lit le contenu et on le met dans la variable "data"
                data = json.load(f)

            # recrée les objets Livre
            for l in data["livres"]:
                livre = Livre(**l)
                self.livres[livre.isbn] = livre

            # recrée les objets Adherent et restaure leurs emprunts
            for a in data["adherents"]:
                adherent = Adherent(a["num_adherent"], a["nom"], a["prenom"])
                adherent.livres_empruntes = a["livres_empruntes"]
                self.adherents[adherent.num_adherent] = adherent

            print("Bibliothèque chargée !")

        # si c'est la toute première ouverture du programme (aucun fichier de sauvegarde n'existe)
        except FileNotFoundError:
            print("Nouvelle bibliothèque créée.")

# partie livre

    # ajoute un exemplaire si le livre existe déjà sinon crée une nouvelle fiche "produit"
    def ajouter_livre(self, isbn, titre, auteur, annee, editeur):

        if isbn in self.livres:
            self.livres[isbn].nb_exemplaires += 1
        else:
            self.livres[isbn] = Livre(isbn, titre, auteur, annee, editeur)

        print("Livre ajouté !")
        self.sauvegarder()

    # supprime un exemplaire du stock et retire le livre du catalogue s'il n'en reste plus
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

    # parcourt tout le catalogue pour afficher les titres et le nombre d'exemplaires restants
    def afficher_livres(self):
        if not self.livres:
            print("Aucun livre.")
            return

        for livre in self.livres.values():
            print(f"{livre.titre} - {livre.auteur} | Exemplaires: {livre.nb_exemplaires}")

    # cherche un livre par son titre (sans tenir compte des majuscules) pour faciliter l'emprunt
    def trouver_livre_par_titre(self, titre):
        for livre in self.livres.values():
            if livre.titre.lower() == titre.lower():
                return livre
        return None

# partie emprunts

    # vérifie l'adhérent et le stock puis valide l'emprunt en affichant la date limite de retour
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
            # annule l'emprunt côté livre si l'adhérent a déjà trop de livres
            livre.rendre()
            return

        infos = adherent.livres_empruntes[livre.isbn]

        print("Emprunt validé !")
        print("Date d'emprunt :", infos["date_emprunt"])
        print("Date limite :", infos["date_limite"])

        self.sauvegarder()

    # liste les livres de l'adhérent, calcule les éventuelles amendes de retard et enregistre le retour
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


# partie initialisation
# on met la classe dans une variable
bibliotheque = Bibliotheque()
# on charge la bibliothèque
bibliotheque.charger()


# partie menus

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Mode utilisateur")
        print("2. Mode administrateur")
        print("3. Quitter")

        # récupère le choix
        choix = input_int("Choix : ")

        if choix == 1:
            # lance le menu classique pour emprunter ou rendre des livres
            menu_utilisateur()

        elif choix == 2:
            # vérifie le mot de passe avant de donner accès au menu administrateur
            if est_admin():
                menu_admin()
            else:
                print("Mot de passe incorrect.")

        elif choix == 3:
            # sauvegarde toutes les données dans le fichier JSON avant de fermer
            bibliotheque.sauvegarder()
            # casse la boucle 
            break

# affiche le panneau de contrôle de l'utilisateur
def menu_utilisateur():
    while True:
        print("\n=== MENU UTILISATEUR ===")
        print("1. Emprunter")
        print("2. Rendre")
        print("3. Voir les livres")
        print("4. Retour")

        # récupère le choix
        choix = input_int("Choix : ")

        if choix == 1:
            # demande le numéro de l'adhérent et le titre à l'utilisateur puis lance le processus d'emprunt
            bibliotheque.emprunter_livre(input("Num adhérent : "), input("Titre : "))

        elif choix == 2:
            # demande le numéro de l'adhérent à l'utilisateur pour lister ses livres et gérer le retour
            bibliotheque.rendre_livre(input("Num adhérent : "))

        elif choix == 3:
            # affiche simplement le catalogue complet de la bibliothèque
            bibliotheque.afficher_livres()

        elif choix == 4:
            # casse la boucle pour quitter ce menu et revenir au menu principal
            break

# affiche le panneau de contrôle de l'administrateur
def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Ajouter un livre")
        print("2. Retirer un livre")
        print("3. Voir les livres")
        print("4. Retour")

        # récupère le choix
        choix = input_int("Choix : ")

        if choix == 1:
            # on utilise la fonction input_int pour vérifier si la valeur entrée est un entier
            annee = input_int("Année : ")

            # on ajoute un livre à la bibliothèque 
            bibliotheque.ajouter_livre(
                input("ISBN : "),
                input("Titre : "),
                input("Auteur : "),
                annee,
                input("Éditeur : ")
            )

        elif choix == 2:
            # demande l'identifiant (ISBN) et supprime l'exemplaire correspondant
            bibliotheque.retirer_livre(input("ISBN : "))

        elif choix == 3:
            # affiche la liste de tous les livres disponibles
            bibliotheque.afficher_livres()

        elif choix == 4:
            # casse la boucle pour quitter le menu administrateur et revenir au menu principal
            break


menu_principal()
