"""Gestion des notes du Bullet Journal."""

from __future__ import annotations

from datetime import date

from bujo.modeles.entree import Entree


class Note(Entree):
    """Represente une note dans le journal."""

    def __init__(
        self,
        nom: str,
        description: str = "",
        date_log: date | None = None,
    ) -> None:
        """Initialise une note."""
        super().__init__(nom=nom, description=description, date_log=date_log)

    def symbole(self) -> str:
        """Retourne le symbole associe a une note."""
        return "-"
