class Emprunt:
    # initialisation
    def __init__(self, adherents, livres):
        self.adherents = adherents
        self.livres = livres

    def emprunter(self, num_adherent, titre):
        # vérifie si l'adhérent existe sinon message erreur
        if num_adherent not in self.adherents:
            print("Adhérent non trouvé, vous n'êtes pas inscrit à la bibliothèque.")
            return

        adherent = self.adherents[num_adherent]

        # vérifie la disponibilité du livre
        for isbn, livre in self.livres.items():
            if livre['titre'] == titre:
                # si le nombre d'exemplaires est "inférieur" ou égal à 0 il n'est pas disponible
                if livre['nb exemplaires'] <= 0:
                    print("Le livre n'est pas disponible actuellement.")
                    return

                # len permet de compter le nombre d'éléments (ici une liste)
                # on compte le nombre de livres empruntés et si c'est supérieur ou égal à 5, l'adhérent ne peut plus emprunter
                if len(adherent['livres_empruntés']) >= 5:
                    print("L'adhérent a emprunté son quota maximum de livres.")
                    return

                # on ajoute le livre dans la liste des livres empruntés par l'adhérent
                adherent['livres_empruntés'].append(titre)
                livre['nb exemplaires'] -= 1
                print("Votre emprunt est validé.")
                return

        print("Ce livre n'est pas dans la bibliothèque.")

    def rendre(self, num_adherent, titre):
        # vérifie si l'adhérent existe sinon message d'erreur
        if num_adherent not in self.adherents:
            print("Adhérent non trouvé.")
            return

        adherent = self.adherents[num_adherent]

        # vérifie si le livre a été emprunté par l'adhérent
        if titre not in adherent['livres_empruntés']:
            print("Cet adhérent n'a pas emprunté ce livre.")
            return

        # retire le livre de la liste des livres empruntés par l'adhérent
        adherent['livres_empruntés'].remove(titre)

        # permet de "rendre" le livre dans l'inventaire 
        for isbn, livre in self.livres.items():
            if livre['titre'] == titre:
                livre['nb exemplaires'] += 1 
                print("Le livre a été rendu avec succès.") #affiche le message que si la condition est validée
                break #casse la boucle 