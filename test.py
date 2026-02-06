#exemple des trucs dans la bibliothèque
adhérent = {
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

livres = {
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
    }
    
}

def ajouter_livre(isbn, titre, auteur, annee, editeur): # ajout d'un livre dans la bibliothèque
    if isbn in livres:
        livres[isbn]['nb exemplaires'] += 1  # incrémente le nombre d'exemplaires si le livre existe déjà
        print("Un exemplaire supplémentaire a été ajouté pour ce livre.")
    else:
        livres[isbn] = {
            "titre": titre,
            "auteur": auteur,
            "annee": annee,
            "editeur": editeur,
            "nb exemplaires": 1
    }

def afficher_livres(): # affchage de tous les livres dans la bibliothèque
    for isbn, livre in livres.items():
        print(f"{livre['titre']} par {livre['auteur']} ({livre['annee']}) - ISBN: {isbn}, Éditeur: {livre['editeur']}, Exemplaires disponibles: {livre['nb exemplaires']}")

def emprunter_livre(num_adhérent, titre):
    if num_adhérent in adhérent: # vérifie si l'adhérent existe
        for isbn, livre in livres.items(): 
            if livre['titre'] == titre: # vérifie si le livre est dans la bibliothèque
                if livre['nb exemplaires'] <= 0: # vérifie la disponibilité du livre
                    print("Le livre n'est pas disponible actuellement.")
                    return
                nb_emprunt = len(adhérent[num_adhérent]['livres_empruntés']) # verifie le nombre d'emprunts de l'adhérent
                if nb_emprunt >= 5: # si supérieur ou égal à 5, on bloque l'emprunt
                    print("L'adhérent a emprunté sont cota de livres maximum.") 
                    return
                else : 
                    adhérent[num_adhérent]['livres_empruntés'].append(titre) # ajoute le livre à la liste des emprunts
                    livre['nb exemplaires'] -= 1 # décrémente le nombre d'exemplaires disponibles
                    print("Votre emprunt est validé")
                    return
        print("Ce livre n'est pas dans la bibliothèque.") # le livre n'existe pas 
    else:
        print("Adhérent non trouvé, vous n'etes pas inscrit à la bibliothèque.") # l'adherent n'est pas abonné 
        

def rendre_livre(num_adhérent, titre):
    if num_adhérent in adhérent:  # vérifie si l'adhérent existe
        if titre in adhérent[num_adhérent]['livres_empruntés']:  # vérifie si le livre est bien emprunté par l'adhérent
            adhérent[num_adhérent]['livres_empruntés'].remove(titre)  # supprime le livre de la liste des emprunts
            # on remet un exemplaire du livre disponible
            for isbn, livre in livres.items():
                if livre['titre'] == titre:
                    livre['nb exemplaires'] += 1
                    break
            print("Le livre a été rendu avec succès.")
        else:
            print("Cet adhérent n'a pas emprunté ce livre.")
            
    else:
        print("Adhérent non trouvé.")
        

#----------------Exemple d'utilisation-----------------
#ajouter_livre("978-2-266-32382-6", "s'adapter ou mourrir", "Antoine Renand", 2021, "Pocket")

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
        ajouter_livre(isbn, titre, auteur, annee, editeur)
        print("Le livre ajouté !")

    elif action == 2: #emprunt d'un livre
        print("\n--- Emprunt d'un livre ---")
        id_adhérent = input("Entrez votre numéro d'adhérent : ")
        titre_livre = input("Entrez le titre de votre livre : ")
        emprunter_livre(id_adhérent, titre_livre)

    elif action == 3: #rendre un livre
        print("\n--- Rendre un livre ---")
        id_adhérent = input("Entrez votre numéro d'adhérent : ")
        titre_livre = input("Entrez le titre de votre livre à rendre : ")
        rendre_livre(id_adhérent, titre_livre)

    elif action == 4: #affichage des livres
        print("\n--- Livres disponibles dans la bibliothèque ---")
        afficher_livres()
    recommencer = input("Voulez-vous effectuer une autre action ? (oui/non) : ")
    if recommencer == "oui":
        utiliser_bibliotheque()
    else : 
        print("\n Merci d'avoir utilisé la bibliothèque. Au revoir !")

utiliser_bibliotheque()