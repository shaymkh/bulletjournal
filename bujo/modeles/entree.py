"""Classe abstraite de base pour les entrees du Bullet Journal."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from uuid import UUID, uuid4


class Entree(ABC):
    """Base commune a toutes les entrees du journal."""

    def __init__(
        self,
        nom: str,
        description: str = "",
        date_log: date | None = None,
    ) -> None:
        """Initialise une entree avec un identifiant unique."""
        self._identifiant: UUID = uuid4()
        self._date_creation: datetime = datetime.now()
        self.nom = nom
        self._description: str = ""
        self.description = description
        self._date_log: date = date.today()
        self.date_log = date.today() if date_log is None else date_log

    @property
    def identifiant(self) -> UUID:
        """Retourne l'identifiant unique en lecture seule."""
        return self._identifiant

    @property
    def date_creation(self) -> datetime:
        """Retourne la date et l'heure de creation de l'entree."""
        return self._date_creation

    @property
    def nom(self) -> str:
        """Retourne le nom de l'entree."""
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        """Definit le nom apres verification qu'il n'est pas vide."""
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError(
                "Le nom d'une entree ne peut pas etre vide."
            )
        self._nom = valeur.strip()

    @property
    def description(self) -> str:
        """Retourne la description de l'entree."""
        return self._description

    @description.setter
    def description(self, valeur: str) -> None:
        """Definit la description de l'entree."""
        self._description = valeur

    @property
    def date_log(self) -> date:
        """Retourne la date du log associe a l'entree."""
        return self._date_log

    @date_log.setter
    def date_log(self, valeur: date) -> None:
        """Definit la date du log apres verification de son type."""
        if not isinstance(valeur, date) or isinstance(valeur, datetime):
            raise ValueError(
                "La date du log doit etre une instance de date valide."
            )
        self._date_log = valeur

    @abstractmethod
    def symbole(self) -> str:
        """Retourne le symbole de rapid logging associe a l'entree."""
