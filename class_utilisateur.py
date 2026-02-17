class Emprunt:
    def __init__(self, adherents, livres):
        self.adherents = adherents
        self.livres = livres

    def emprunter(self, num_adherent, titre):
        if num_adherent not in self.adherents:
            print("Adhérent non trouvé, vous n'êtes pas inscrit à la bibliothèque.")
            return

        adherent = self.adherents[num_adherent]

        # Vérifie le livre
        for isbn, livre in self.livres.items():
            if livre['titre'] == titre:
                if livre['nb exemplaires'] <= 0:
                    print("Le livre n'est pas disponible actuellement.")
                    return

                if len(adherent['livres_empruntés']) >= 5:
                    print("L'adhérent a emprunté son quota maximum de livres.")
                    return

                adherent['livres_empruntés'].append(titre)
                livre['nb exemplaires'] -= 1
                print("Votre emprunt est validé.")
                return

        print("Ce livre n'est pas dans la bibliothèque.")

    def rendre(self, num_adherent, titre):
        
        if num_adherent not in self.adherents:
            print("Adhérent non trouvé.")
            return

        adherent = self.adherents[num_adherent]

        if titre not in adherent['livres_empruntés']:
            print("Cet adhérent n'a pas emprunté ce livre.")
            return

        adherent['livres_empruntés'].remove(titre)

        # Permet de rendre un livre 
        for isbn, livre in self.livres.items():
            if livre['titre'] == titre:
                livre['nb exemplaires'] += 1 
                print("Le livre a été rendu avec succès.") #affiche le message que si la condition est validée
                break #casse la boucle 