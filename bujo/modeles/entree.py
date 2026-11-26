#Classe de base des entrées du Bullet Journal.

from datetime import datetime


class Entree:

    prochain_id = 1

    def __init__(self, nom, description):
        self.id = Entree.prochain_id
        Entree.prochain_id += 1
        self.nom = nom
        self.description = description
        self.date_creation = datetime.now()