"""Gestion des evenements du Bullet Journal."""

from __future__ import annotations

from datetime import date, time
from typing import Any

from bujo.exceptions import DateInvalide
from bujo.modeles.entree import Entree


class Evenement(Entree):
    """Represente un evenement dans le journal."""

    def __init__(
        self,
        nom: str,
        date_evenement: date,
        description: str = "",
        heure: time | None = None,
        date_log: date | None = None,
    ) -> None:
        """Initialise un evenement avec sa date et son heure optionnelle."""
        if not isinstance(date_evenement, date):
            raise DateInvalide("La date est invalide.")

        if heure is not None and not isinstance(heure, time):
            raise DateInvalide("L'heure est invalide.")

        super().__init__(nom=nom, description=description, date_log=date_log)
        self.date_evenement: date = date_evenement
        self.heure: time | None = heure

    def symbole(self) -> str:
        """Retourne le symbole associe a un evenement."""
        return "o"

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'evenement en dictionnaire."""
        donnees = super().to_dict()
        donnees["date_evenement"] = self.date_evenement.isoformat()
        donnees["heure"] = self.heure.isoformat() if self.heure else None
        return donnees
