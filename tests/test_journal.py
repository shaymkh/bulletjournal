"""Tests unitaires pour la classe Journal et la persistance JSON."""

from datetime import date, time
from pathlib import Path

import pytest

from bujo.exceptions import EntreeIntrouvable, EtatInvalide
from bujo.journal import Journal
from bujo.modeles.evenement import Evenement
from bujo.modeles.note import Note
from bujo.modeles.tache import EtatTache, Tache


def test_journal_ajout_recuperation_et_suppression() -> None:
    """Verifie l'ajout, la lecture et la suppression d'une entree."""
    journal = Journal(nom="Journal Perso")
    tache = Tache(nom="Preparer la demo", date_log=date(2026, 11, 26))
    uid = journal.ajouter(tache)

    assert len(journal) == 1
    assert journal.obtenir(uid) is tache

    journal.supprimer(uid)
    assert len(journal) == 0

    with pytest.raises(EntreeIntrouvable):
        journal.obtenir(uid)

    with pytest.raises(EntreeIntrouvable):
        journal.supprimer(uid)


def test_journal_vues_et_filtrage() -> None:
    """Verifie daily_log, monthly_log, future_log et le filtrage par type."""
    journal = Journal()
    t1 = Tache(nom="Tache 1", date_log=date(2026, 11, 26))
    n1 = Note(nom="Note 1", date_log=date(2026, 11, 26))
    e1 = Evenement(
        nom="Evt futur",
        date_evenement=date(2026, 12, 10),
        heure=time(10, 0),
        date_log=date(2026, 12, 10),
    )

    journal.ajouter(t1)
    journal.ajouter(n1)
    journal.ajouter(e1)

    assert len(journal.daily_log(date(2026, 11, 26))) == 2
    assert len(journal.monthly_log(2026, 11)) == 2
    assert len(journal.future_log(depuis=date(2026, 11, 26))) == 1
    assert len(journal.lister(type_entree=Note)) == 1


def test_journal_persistance_json(tmp_path: Path) -> None:
    """Verifie la sauvegarde et le rechargement JSON avec etats et types."""
    journal = Journal(nom="Bujo Test")
    tache = Tache(nom="Relire PR", date_log=date(2026, 11, 26))
    tache.terminer()
    evt = Evenement(
        nom="Reunion",
        date_evenement=date(2026, 11, 27),
        heure=time(15, 30),
        date_log=date(2026, 11, 26),
    )
    note = Note(
        nom="Rappel",
        description="Verifier CI",
        date_log=date(2026, 11, 26),
    )

    journal.ajouter(tache)
    journal.ajouter(evt)
    journal.ajouter(note)

    fichier = tmp_path / "journal.json"
    journal.sauvegarder(fichier)
    recharge = Journal.charger(fichier)

    assert recharge.nom == "Bujo Test"
    assert len(recharge) == 3

    tache_rechargee = recharge.obtenir(tache.identifiant)
    assert isinstance(tache_rechargee, Tache)
    assert tache_rechargee.etat == EtatTache.TERMINEE

    evt_recharge = recharge.obtenir(evt.identifiant)
    assert isinstance(evt_recharge, Evenement)
    assert evt_recharge.heure == time(15, 30)


def test_transitions_tache_selon_conception() -> None:
    """Verifie les transitions autorisees et interdites d'une tache."""
    tache = Tache(nom="Planifier sprint")
    tache.planifier()
    assert tache.etat == EtatTache.PLANIFIEE

    tache.migrer()
    assert tache.etat == EtatTache.MIGREE

    with pytest.raises(EtatInvalide):
        tache.terminer()
