#Gestion des notes du Bullet Journal."""

from entree import Entree


class Note(Entree):

    def __init__(objet, nom, description):
        super().__init__(nom, description)