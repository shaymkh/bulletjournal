
#Gestion des événements du Bullet Journal.
from datetime import date, time
from .entree import entree 
from .exceptions import DateInvalide


class Evenement(entree):
    #Représente un événement dans le journal.

    def __init__(self, nom, description, date_evenement, heure=None):

        super().__init__(nom, description)

        if not isinstance(date_evenement, date):
            raise DateInvalide("La date est invalide.")

        if heure is not None and not isinstance(heure, time):
            raise DateInvalide("L'heure est invalide.")

        self.date_evenement = date_evenement

        self.heure = heure
