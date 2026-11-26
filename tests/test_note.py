"""Tests unitaires pour le modele Note."""

from datetime import date

import pytest

from bujo.exceptions import NomVide
from bujo.modeles.note import Note


def test_note_creation_et_symbole() -> None:
    """Verifie l'initialisation et le symbole d'une note."""
    date_log = date(2026, 11, 26)
    note = Note(
        nom="Idee projet",
        description="Ajouter l'export JSON",
        date_log=date_log,
    )
    assert note.nom == "Idee projet"
    assert note.description == "Ajouter l'export JSON"
    assert note.date_log == date_log
    assert note.symbole() == "-"


@pytest.mark.parametrize("nom_invalide", ["", "   ", "\t\n"])
def test_note_nom_vide_leve_erreur(nom_invalide: str) -> None:
    """Verifie qu'un nom vide ou d'espaces leve NomVide."""
    with pytest.raises(NomVide):
        Note(nom=nom_invalide)
