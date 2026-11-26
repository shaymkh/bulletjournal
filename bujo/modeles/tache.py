"""Modele de tache et enumeration de ses etats dans le Bullet Journal."""

from datetime import date
from enum import Enum

from bujo.exceptions import EtatInvalide
from bujo.modeles.entree import Entree


class EtatTache(Enum):
    """Etats possibles d'une tache dans son cycle de vie."""

    A_FAIRE = "a_faire"
    TERMINEE = "terminee"
    MIGREE = "migree"
    PLANIFIEE = "planifiee"
    ABANDONNEE = "abandonnee"


SYMBOLES_TACHE: dict[EtatTache, str] = {
    EtatTache.A_FAIRE: "•",
    EtatTache.TERMINEE: "×",
    EtatTache.MIGREE: ">",
    EtatTache.PLANIFIEE: "<",
    EtatTache.ABANDONNEE: "~",
}

_TRANSITIONS_AUTORISEES: dict[EtatTache, set[EtatTache]] = {
    EtatTache.A_FAIRE: {
        EtatTache.TERMINEE,
        EtatTache.MIGREE,
        EtatTache.PLANIFIEE,
        EtatTache.ABANDONNEE,
    },
    EtatTache.PLANIFIEE: {
        EtatTache.MIGREE,
        EtatTache.ABANDONNEE,
    },
    EtatTache.TERMINEE: set(),
    EtatTache.MIGREE: set(),
    EtatTache.ABANDONNEE: set(),
}


class Tache(Entree):
    """Entree representant une tache avec un cycle de vie."""

    def __init__(
        self,
        nom: str,
        description: str = "",
        date_log: date | None = None,
    ) -> None:
        """Initialise une tache a l'etat A_FAIRE."""
        super().__init__(nom=nom, description=description, date_log=date_log)
        self._etat: EtatTache = EtatTache.A_FAIRE

    @property
    def etat(self) -> EtatTache:
        """Retourne l'etat actuel de la tache."""
        return self._etat

    def _changer_etat(self, nouvel_etat: EtatTache) -> None:
        """Change l'etat de la tache si la transition est autorisee."""
        if nouvel_etat not in _TRANSITIONS_AUTORISEES[self._etat]:
            raise EtatInvalide(
                f"Transition interdite depuis l'etat {self._etat.name} "
                f"vers {nouvel_etat.name}."
            )
        self._etat = nouvel_etat

    def terminer(self) -> None:
        """Marque la tache comme terminee."""
        self._changer_etat(EtatTache.TERMINEE)

    def abandonner(self) -> None:
        """Marque la tache comme abandonnee."""
        self._changer_etat(EtatTache.ABANDONNEE)

    def migrer(self) -> None:
        """Marque la tache comme migree."""
        self._changer_etat(EtatTache.MIGREE)

    def planifier(self) -> None:
        """Marque la tache comme planifiee."""
        self._changer_etat(EtatTache.PLANIFIEE)

    def symbole(self) -> str:
        """Retourne le symbole correspondant a l'etat de la tache."""
        return SYMBOLES_TACHE[self._etat]
