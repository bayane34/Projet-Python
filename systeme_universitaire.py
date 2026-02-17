import json
import os
import hashlib
from datetime import datetime, timedelta

# CONFIGURATION

# On a differente constantes global utilisé dans tout le fichier 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier où se trouve le fichier Python.
BIBLIO_FILE = os.path.join(BASE_DIR, "bibliotheque.json")  # Crée un chemin complet vers le fichier bibliotheque.json.
SALLES_FILE = os.path.join(BASE_DIR, "salles.json")  # Crée un chemin complet vers le fichier salles.json.
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # Stocke le hash du mot de passe admin.

# OUTILS 
# Ces fonctions gèrent les entrées utilisateur et la manipulation de fichiers JSON.

def input_int(msg): # Cette fonction demande à l'utilisateur de saisir un entier positif. Elle continue à demander une entrée jusqu'à ce qu'une valeur valide soit fournie. Si l'utilisateur saisit une valeur non entière ou un entier négatif, un message d'erreur est affiché et la fonction redemande une entrée.
    while True:     
        try:
            val = int(input(msg))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Entier positif requis.")
# Les fonctions ci-dessus assurent que les entrées sont valides (entiers positifs, texte non vide, dates au format correct) et gèrent l'authentification admin de manière sécurisée. Les fonctions de chargement et de sauvegarde JSON permettent de persister les données des salles et de la bibliothèque.

def input_text(msg):
    while True:
        val = input(msg).strip()
        if val:
            return val
        print("Champ vide interdit.")

# La fonction input_date vérifie que l'entrée correspond au format de date attendu (DD-MM-YYYY) et continue à demander une entrée jusqu'à ce qu'elle soit valide. L'authentification admin utilise un hash pour éviter de stocker le mot de passe en clair, et permet trois tentatives avant de refuser l'accès. Les fonctions charger_json et sauvegarder_json facilitent la lecture et l'écriture des données dans des fichiers JSON, avec une gestion des erreurs pour les fichiers manquants.

def input_date(msg):
    while True:
        val = input(msg).strip()
        try:
            datetime.strptime(val, "%d-%m-%Y")
            return val
        except ValueError:
            print("Format invalide (DD-MM-YYYY).")

# La fonction auth_admin demande à l'utilisateur de saisir le mot de passe admin, le hash de l'entrée est comparé au hash stocké pour vérifier l'authenticité. Si l'utilisateur échoue trois fois, l'accès est refusé.

def auth_admin():
    for _ in range(3):
        if hashlib.sha256(input("Mot de passe admin : ").encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            return True
        print("Incorrect.")
    print("Accès refusé.")
    return False

#charger_json retourne une valeur par défaut si le fichier n'existe pas, tandis que sauvegarder_json écrit les données formatées dans le fichier spécifié.

def charger_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

# La fonction sauvegarder_json prend un chemin de fichier et des données, et les écrit dans le fichier au format JSON avec une indentation pour une meilleure lisibilité.

def sauvegarder_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# SALLES

# La classe Salle représente une salle avec un numéro, une capacité et une disponibilité. La classe GestionSalles gère les salles et les réservations, permettant d'afficher les salles, de réserver ou libérer une salle, et d'ajouter ou supprimer des salles. Les données sont chargées et sauvegardées dans un fichier JSON pour persister les informations entre les sessions.

class Salle:
    def __init__(self, numero, capacite, disponible=True):
        self.numero = str(numero)
        self.capacite = capacite
        self.disponible = disponible

# La méthode to_dict retourne un dictionnaire représentant l'objet Salle.
    
    def to_dict(self):
        return self.__dict__

# La classe GestionSalles contient des méthodes pour gérer les salles et les réservations. Le constructeur initialise les structures de données et charge les informations depuis le fichier JSON. Les méthodes permettent d'afficher les salles, de gérer les réservations, et de modifier la liste des salles disponibles.

class GestionSalles:
    def __init__(self):
        self.salles = {}
        self.reservations = []
        self.charger()

# La méthode charger lit les données des salles et des réservations à partir du fichier JSON. Si le fichier n'existe pas, elle initialise les structures de données avec des valeurs par défaut.
    def charger(self):
        data = charger_json(SALLES_FILE, {"salles": [], "reservations": []})
        for s in data["salles"]:
            self.salles[str(s["numero"])] = Salle(**s)
        self.reservations = data["reservations"]

# La méthode sauvegarder écrit les données actuelles des salles et des réservations dans le fichier JSON, en convertissant les objets Salle en dictionnaires pour la sérialisation.
    def sauvegarder(self):
        sauvegarder_json(SALLES_FILE, {
            "salles": [s.to_dict() for s in self.salles.values()],
            "reservations": self.reservations
        })
# La méthode afficher affiche la liste des salles disponibles avec leur numéro et leur capacité. Si aucune salle n'est disponible, elle affiche un message approprié.
    def afficher(self):
        if not self.salles:
            print("Aucune salle.")
            return
        for s in self.salles.values():
            print(f"Salle {s.numero} | Capacité {s.capacite}")

# La méthode afficher_reservations affiche la liste des réservations actuelles, montrant le nom de la personne qui a réservé, le numéro de la salle et la date de réservation. Si aucune réservation n'est présente, elle affiche un message indiquant qu'il n'y en a aucune.
    def afficher_reservations(self):
        if not self.reservations:
            print("Aucune réservation.")
            return
        for r in self.reservations:
            print(f"{r['nom']} - Salle {r['numero']} - {r['date']}")

# La méthode reserver permet à un utilisateur de réserver une salle en fournissant son nom, le numéro de la salle et la date souhaitée. Elle vérifie que la salle existe et n'est pas déjà réservée pour cette date avant d'ajouter la réservation à la liste.
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

# La méthode liberer permet à un utilisateur d'annuler une réservation en fournissant le numéro de la salle et la date de la réservation. Elle filtre la liste des réservations pour supprimer celle qui correspond aux critères spécifiés.
    def liberer(self):
        numero = input_text("Numéro salle : ")
        date = input_date("Date (DD-MM-YYYY) : ")

        self.reservations = [
            r for r in self.reservations
            if not (r["numero"] == numero and r["date"] == date)
        ]
        self.sauvegarder()
        print("Réservation annulée.")

# Les méthodes ajouter et supprimer permettent à un administrateur d'ajouter une nouvelle salle ou de supprimer une salle existante. Lors de l'ajout, il vérifie que le numéro de la salle n'existe pas déjà, et lors de la suppression, il vérifie que la salle existe avant de la supprimer.
    def ajouter(self):
        numero = input_text("Numéro salle : ")
        if numero in self.salles:
            print("Existe déjà.")
            return
        self.salles[numero] = Salle(numero, input_int("Capacité : "))
        self.sauvegarder()
        print("Salle ajoutée.")

# La méthode supprimer vérifie si la salle existe avant de la supprimer de la liste des salles. Si la salle n'est pas trouvée, elle affiche un message d'erreur.
    def supprimer(self):
        numero = input_text("Numéro salle : ")
        if numero not in self.salles:
            print("Introuvable.")
            return
        del self.salles[numero]
        self.sauvegarder()
        print("Salle supprimée.")


# BIBLIOTHEQUE

# La classe Livre représente un livre avec des attributs tels que l'ISBN, le titre, l'auteur, l'année de publication, l'éditeur et le nombre d'exemplaires disponibles. La classe Adherent représente un adhérent de la bibliothèque avec un numéro d'adhérent, un nom, un prénom, une liste de livres empruntés et un historique des emprunts. La classe Bibliotheque gère les livres et les adhérents, permettant d'afficher les livres disponibles, de gérer les emprunts et les retours, et de maintenir un historique des activités des adhérents.
class Livre:
    def __init__(self, isbn, titre, auteur, annee, editeur, nb_exemplaires=1):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.editeur = editeur
        self.nb_exemplaires = nb_exemplaires

# La méthode to_dict retourne un dictionnaire représentant l'objet Livre, ce qui facilite la conversion en JSON lors de la sauvegarde des données.
    def to_dict(self):
        return self.__dict__

# La classe Adherent contient une constante LIMITE_EMPRUNTS qui définit le nombre maximum de livres qu'un adhérent peut emprunter en même temps. Le constructeur initialise les attributs de l'adhérent, y compris un dictionnaire pour les livres empruntés et une liste pour l'historique des activités.
class Adherent:
    LIMITE_EMPRUNTS = 5

 # La méthode to_dict retourne un dictionnaire représentant l'objet Adherent, ce qui facilite la conversion en JSON lors de la sauvegarde des données. Les attributs incluent le numéro d'adhérent, le nom, le prénom, les livres empruntés (avec les dates d'emprunt et de retour) et l'historique des activités.
    def __init__(self, num_adherent, nom, prenom):
        self.num_adherent = str(num_adherent)
        self.nom = nom
        self.prenom = prenom
        self.livres_empruntes = {}
        self.historique = []

# La méthode to_dict retourne un dictionnaire représentant l'objet Adherent, ce qui facilite la conversion en JSON lors de la sauvegarde des données. Les attributs incluent le numéro d'adhérent, le nom, le prénom, les livres empruntés (avec les dates d'emprunt et de retour) et l'historique des activités.
    def to_dict(self):
        return self.__dict__

# La classe Bibliotheque gère les livres et les adhérents, permettant d'afficher les livres disponibles, de gérer les emprunts et les retours, et de maintenir un historique des activités des adhérents. Le constructeur initialise les structures de données et charge les informations depuis le fichier JSON. Les méthodes permettent d'afficher les livres, de trouver un livre par titre et auteur, d'ajouter ou supprimer des livres et des adhérents, de gérer les emprunts et les retours, et de voir l'historique d'un adhérent.
class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.adherents = {}
        self.charger()

# La méthode charger lit les données des livres et des adhérents à partir du fichier JSON. Si le fichier n'existe pas, elle initialise les structures de données avec des valeurs par défaut. Les livres sont stockés dans un dictionnaire avec l'ISBN comme clé, tandis que les adhérents sont stockés dans un dictionnaire avec le numéro d'adhérent comme clé.
    def charger(self):
        data = charger_json(BIBLIO_FILE, {"livres": [], "adherents": []})
        for l in data["livres"]:
            self.livres[l["isbn"]] = Livre(**l)

# La méthode charger lit les données des livres et des adhérents à partir du fichier JSON. Si le fichier n'existe pas, elle initialise les structures de données avec des valeurs par défaut. Les livres sont stockés dans un dictionnaire avec l'ISBN comme clé, tandis que les adhérents sont stockés dans un dictionnaire avec le numéro d'adhérent comme clé.
       
        for a in data["adherents"]:
            adh = Adherent(a["num_adherent"], a["nom"], a["prenom"])
            adh.livres_empruntes = a.get("livres_empruntes", {})
            adh.historique = a.get("historique", [])
            self.adherents[str(a["num_adherent"])] = adh

# La méthode sauvegarder écrit les données actuelles des livres et des adhérents dans le fichier JSON, en convertissant les objets Livre et Adherent en dictionnaires pour la sérialisation.

    def sauvegarder(self):
        sauvegarder_json(BIBLIO_FILE, {
            "livres": [l.to_dict() for l in self.livres.values()],
            "adherents": [a.to_dict() for a in self.adherents.values()]
        })
# La méthode afficher affiche la liste des livres disponibles avec leurs détails (auteur, titre, ISBN, année, éditeur et stock). Si aucun livre n'est disponible, elle affiche un message approprié.
  
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

# La méthode trouver_livre recherche un livre dans la bibliothèque en fonction du titre et de l'auteur fournis. Elle parcourt la liste des livres et compare les titres et les auteurs de manière insensible à la casse. Si un livre correspondant est trouvé, il est retourné ; sinon, la méthode retourne None.
  
    def trouver_livre(self, titre, auteur):
        for l in self.livres.values():
            if l.titre.lower() == titre.lower() and l.auteur.lower() == auteur.lower():
                return l
            
# La méthode ajouter permet à un administrateur d'ajouter un nouveau livre à la bibliothèque en fournissant les détails du livre (ISBN, titre, auteur, année, éditeur et nombre d'exemplaires). Le livre est ajouté au dictionnaire des livres avec l'ISBN comme clé, et les données sont sauvegardées dans le fichier JSON.
    
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

# La méthode supprimer_livre vérifie si un livre avec l'ISBN fourni existe dans la bibliothèque. Si le livre est trouvé, il est supprimé du dictionnaire des livres, les données sont sauvegardées dans le fichier JSON, et un message de confirmation est affiché. Si le livre n'est pas trouvé, un message d'erreur est affiché.
   
    def supprimer_livre(self):
        isbn = input_text("ISBN : ")
        if isbn not in self.livres:
            print("Introuvable.")
            return
        del self.livres[isbn]
        self.sauvegarder()
        print("Livre supprimé.")

# La méthode ajouter_adherent permet à un administrateur d'ajouter un nouvel adhérent à la bibliothèque en fournissant le numéro d'adhérent, le nom et le prénom. L'adhérent est ajouté au dictionnaire des adhérents avec le numéro d'adhérent comme clé, et les données sont sauvegardées dans le fichier JSON.
   
    def ajouter_adherent(self):
        num = input_text("Numéro adhérent : ")
        self.adherents[num] = Adherent(num, input_text("Nom : "), input_text("Prénom : "))
        self.sauvegarder()
        print("Adhérent ajouté.")
# La méthode supprimer_adherent vérifie si un adhérent avec le numéro d'adhérent fourni existe dans la bibliothèque. Si l'adhérent est trouvé, il est supprimé du dictionnaire des adhérents, les données sont sauvegardées dans le fichier JSON, et un message de confirmation est affiché. Si l'adhérent n'est pas trouvé, un message d'erreur est affiché.
    
    def supprimer_adherent(self):
        num = input_text("Numéro adhérent : ")
        if num not in self.adherents:
            print("Introuvable.")
            return
        del self.adherents[num]
        self.sauvegarder()
        print("Adhérent supprimé.")
# La méthode emprunter permet à un adhérent d'emprunter un livre en fournissant son numéro d'adhérent, le titre et l'auteur du livre. Elle vérifie que l'adhérent existe, que le livre est disponible, et que l'adhérent n'a pas atteint la limite d'emprunts. Si toutes les conditions sont remplies, le livre est marqué comme emprunté, les dates d'emprunt et de retour sont enregistrées, et les données sont sauvegardées dans le fichier JSON.
    
    def emprunter(self):
        num = input_text("Num adhérent : ")
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
        num = input_text("Num adhérent : ")
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
        num = input_text("Num adhérent : ")
        if num not in self.adherents:
            print("Introuvable.")
            return
        for h in self.adherents[num].historique:
            print(h)

# ================================
# MENU
# ================================

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
