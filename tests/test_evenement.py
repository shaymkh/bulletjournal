"""Tests unitaires pour le modele Evenement."""

from datetime import date, time

import pytest

from bujo.exceptions import DateInvalide, NomVide
from bujo.modeles.evenement import Evenement


def test_evenement_creation_avec_et_sans_heure() -> None:
    """Verifie l'initialisation d'un evenement avec ou sans heure."""
    date_evt = date(2026, 12, 1)
    evt_sans_heure = Evenement(
        nom="Reunion equipe",
        date_evenement=date_evt,
        description="Point hebdo",
    )
    assert evt_sans_heure.nom == "Reunion equipe"
    assert evt_sans_heure.description == "Point hebdo"
    assert evt_sans_heure.date_evenement == date_evt
    assert evt_sans_heure.heure is None
    assert evt_sans_heure.symbole() == "o"

    heure_evt = time(14, 30)
    evt_avec_heure = Evenement(
        nom="Dentiste",
        date_evenement=date_evt,
        heure=heure_evt,
    )
    assert evt_avec_heure.heure == heure_evt


def test_evenement_to_dict() -> None:
    """Verifie la serialisation d'un evenement en dictionnaire."""
    evt = Evenement(
        nom="Conference",
        date_evenement=date(2026, 11, 28),
        heure=time(9, 0),
    )
    donnees = evt.to_dict()
    assert donnees["type"] == "Evenement"
    assert donnees["nom"] == "Conference"
    assert donnees["date_evenement"] == "2026-11-28"
    assert donnees["heure"] == "09:00:00"


@pytest.mark.parametrize("nom_invalide", ["", "   ", "\t\n"])
def test_evenement_nom_vide_leve_erreur(nom_invalide: str) -> None:
    """Verifie qu'un nom vide ou d'espaces leve NomVide."""
    with pytest.raises(NomVide):
        Evenement(nom=nom_invalide, date_evenement=date(2026, 12, 1))


def test_evenement_date_ou_heure_invalide_leve_erreur() -> None:
    """Verifie qu'une date ou une heure invalide leve DateInvalide."""
    with pytest.raises(DateInvalide):
        Evenement(
            nom="Atelier",
            date_evenement="2026-12-01",  # type: ignore[arg-type]
        )

    with pytest.raises(DateInvalide):
        Evenement(
            nom="Atelier",
            date_evenement=date(2026, 12, 1),
            heure="10:00",  # type: ignore[arg-type]
        )
