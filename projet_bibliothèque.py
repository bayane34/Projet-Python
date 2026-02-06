class livre: #classe qui représente les livres dans la bibliothèque
    def __init__(self, isbn, titre, auteur, annee, editeur): #constructeur de la classe, qui prend en compte les attributs de base des livres
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.editeur = editeur
        self.nb_exemplaires = 1

class Adhérent: #classe qui représente les adhérents de la bibliothèque
    def __init__(self, num_adherent, nom, prenom): #constructeur de la classe, qui prend en compte les attributs de base des adhérents
        self.num_adherent = num_adherent
        self.nom = nom
        self.prenom = prenom
        self.livres_empruntes = []

class Bibliotheque: #classe qui représente la bibliothèque
    def __init__(self):
        self.livres = {}  # dictionnaire pour stocker les livres avec l'ISBN comme clé
        self.adhérents = {}  # dictionnaire pour stocker les adhérents avec le numéro d'adhérent comme clé

    def ajouter_livre(self, isbn, titre, auteur, annee, editeur): # ajout d'un livre dans la bibliothèque
        if isbn in self.livres:
            self.livres[isbn]['nb exemplaires'] += 1  # incrémente le nombre d'exemplaires si le livre existe déjà
            print("Un exemplaire supplémentaire a été ajouté pour ce livre.")
        else:
            self.livres[isbn] = {
                "titre": titre,
            "auteur": auteur,
            "annee": annee,
            "editeur": editeur,
            "nb exemplaires": 1
    }
    def afficher_livres(self): # affchage de tous les livres dans la bibliothèque
        for isbn, livre in self.livres.items():
            print(f"{livre['titre']} par {livre['auteur']} ({livre['annee']}) - ISBN: {isbn}, Éditeur: {livre['editeur']}, Exemplaires disponibles: {livre['nb exemplaires']}")

    def emprunter_livre(self, num_adhérent, titre):
        if num_adhérent in self.adhérents: # vérifie si l'adhérent existe
            for isbn, livre in self.livres.items(): 
                if livre['titre'] == titre: # vérifie si le livre est dans la bibliothèque
                    if livre['nb exemplaires'] <= 0: # vérifie la disponibilité du livre
                        print("Le livre n'est pas disponible actuellement.")
                        return
                    nb_emprunt = len(self.adhérents[num_adhérent]['livres_empruntés']) # verifie le nombre d'emprunts de l'adhérent
                    if nb_emprunt >= 5: # si supérieur ou égal à 5, on bloque l'emprunt
                        print("L'adhérent a emprunté sont cota de livres maximum.") 
                        return
                    else : 
                        self.adhérents[num_adhérent]['livres_empruntés'].append(titre) # ajoute le livre à la liste des emprunts
                        livre['nb exemplaires'] -= 1 # décrémente le nombre d'exemplaires disponibles
                        print("Votre emprunt est validé")
                        return
            print("Ce livre n'est pas dans la bibliothèque.") # le livre n'existe pas 
        else:
            print("Adhérent non trouvé, vous n'etes pas inscrit à la bibliothèque.") # l'adherent n'est pas abonné 
            

    def rendre_livre(self, num_adhérent, titre):
        if num_adhérent in self.adhérents:  # vérifie si l'adhérent existe
            if titre in self.adhérents[num_adhérent]['livres_empruntés']:  # vérifie si le livre est bien emprunté par l'adhérent
                self.adhérents[num_adhérent]['livres_empruntés'].remove(titre)  # supprime le livre de la liste des emprunts
                # on remet un exemplaire du livre disponible
                for isbn, livre in self.livres.items():
                    if livre['titre'] == titre:
                        livre['nb exemplaires'] += 1
                        break
                print("Le livre a été rendu avec succès.")
            else:
                print("Cet adhérent n'a pas emprunté ce livre.")
                
        else:
            print("Adhérent non trouvé.")

#----------------Initialisation de la bibliothèque-----------------
bibliotheque = Bibliotheque()
bibliotheque.adhérents = {
    "001": {
        "nom": "Dupont",
        "prénom": "Jean",
        "date_inscription": "2020-01-15",
        "livres_empruntés": ["Le Petit Prince"]
    },
    "002": {
        "nom": "Martin",
        "prénom": "Sophie",
        "date_inscription": "2019-11-22",
        "livres_empruntés": []
    }
}

bibliotheque.livres = {
    "978-3-16-148410-0": {
        "titre": "Le Petit Prince",
        "auteur": "Antoine de Saint-Exupéry",
        "annee": 1943,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 3
    },
    "978-2-07-036002-4": {
        "titre": "L'Étranger",
        "auteur": "Albert Camus",
        "annee": 1942,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 2
    },
    "978-2-07-041311-9": {
        "titre": "Les Misérables",
        "auteur": "Victor Hugo",
        "annee": 1862,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 2
    },
    "978-2-253-00001-4": {
        "titre": "Madame Bovary",
        "auteur": "Gustave Flaubert",
        "annee": 1857,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 4
    },
    "978-2-07-040918-1": {
        "titre": "La Peste",
        "auteur": "Albert Camus",
        "annee": 1947,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 3
    },
    "978-2-253-00618-4": {
        "titre": "Germinal",
        "auteur": "Émile Zola",
        "annee": 1885,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 6
    },
    "978-2-07-037924-8": {
        "titre": "Bel-Ami",
        "auteur": "Guy de Maupassant",
        "annee": 1885,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 2
    },
    "978-2-253-06721-5": {
        "titre": "Le Rouge et le Noir",
        "auteur": "Stendhal",
        "annee": 1830,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 3
    },
    "978-2-07-036822-8": {
        "titre": "Candide",
        "auteur": "Voltaire",
        "annee": 1759,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 5
    },
    "978-2-253-00189-9": {
        "titre": "Les Fleurs du mal",
        "auteur": "Charles Baudelaire",
        "annee": 1857,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 4
    },
    "978-2-07-040506-0": {
        "titre": "Huis clos",
        "auteur": "Jean-Paul Sartre",
        "annee": 1944,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 3
    },
    "978-2-253-00427-2": {
        "titre": "Le Père Goriot",
        "auteur": "Honoré de Balzac",
        "annee": 1835,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 2
    },
    "978-2-07-040074-4": {
        "titre": "Antigone",
        "auteur": "Jean Anouilh",
        "annee": 1944,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 6
    },
    "978-2-253-08716-9": {
        "titre": "L’Assommoir",
        "auteur": "Émile Zola",
        "annee": 1877,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 3
    },
    "978-2-07-036085-7": {
        "titre": "La Condition humaine",
        "auteur": "André Malraux",
        "annee": 1933,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 2
    },
    "978-2-253-00258-2": {
        "titre": "Phèdre",
        "auteur": "Jean Racine",
        "annee": 1677,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 4
    },
    "978-2-07-040323-3": {
        "titre": "Le Malade imaginaire",
        "auteur": "Molière",
        "annee": 1673,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 5
    },
    "978-2-253-00699-3": {
        "titre": "Dom Juan",
        "auteur": "Molière",
        "annee": 1665,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 3
    },
    "978-2-07-041573-1": {
        "titre": "La Princesse de Clèves",
        "auteur": "Madame de La Fayette",
        "annee": 1678,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 2
    },
    "978-2-253-00489-0": {
        "titre": "Voyage au centre de la Terre",
        "auteur": "Jules Verne",
        "annee": 1864,
        "editeur": "Éditions Le Livre de Poche",
        "nb exemplaires": 6
    },
    "978-2-07-040233-5": {
        "titre": "Vingt mille lieues sous les mers",
        "auteur": "Jules Verne",
        "annee": 1870,
        "editeur": "Éditions Gallimard",
        "nb exemplaires": 4
    }

}

#----------------Exemple d'utilisation-----------------

def utiliser_bibliotheque():
    print("\n--- Bienvenue dans la bibliothèque ---")
    action = int(input("Que souhaitez-vous faire ? (1: Ajouter un livre, " \
    "2: Emprunter un livre, " \
    "3: Rendre un livre " \
    "4: Afficher les livres de la bibliothèque) : "))

    if action == 1: #ajout d'un livre
        print("\n--- Ajout d'un livre ---")
        isbn = input("Entrez l'ISBN du livre : ")
        titre = input("Entrez le titre du livre : ")
        auteur = input("Entrez l'auteur du livre : ")
        annee = int(input("Entrez l'année de publication du livre : "))
        editeur = input("Entrez l'éditeur du livre : ")
        bibliotheque.ajouter_livre(isbn, titre, auteur, annee, editeur)
        print("Le livre ajouté !")

    elif action == 2: #emprunt d'un livre
        print("\n--- Emprunt d'un livre ---")
        id_adhérent = input("Entrez votre numéro d'adhérent : ")
        titre_livre = input("Entrez le titre de votre livre : ")
        bibliotheque.emprunter_livre(id_adhérent, titre_livre)

    elif action == 3: #rendre un livre
        print("\n--- Rendre un livre ---")
        id_adhérent = input("Entrez votre numéro d'adhérent : ")
        titre_livre = input("Entrez le titre de votre livre à rendre : ")
        bibliotheque.rendre_livre(id_adhérent, titre_livre)

    elif action == 4: #affichage des livres
        print("\n--- Livres disponibles dans la bibliothèque ---")
        bibliotheque.afficher_livres()
    recommencer = input("Voulez-vous effectuer une autre action ? (oui/non) : ")
    if recommencer == "oui":
        utiliser_bibliotheque()
    else : 
        print("\n Merci d'avoir utilisé la bibliothèque. Au revoir !")

utiliser_bibliotheque()

