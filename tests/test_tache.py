"""Tests unitaires pour Entree et Tache."""

from datetime import date, datetime
from uuid import UUID
import pytest

from bujo.modeles.entree import Entree
from bujo.modeles.tache import EtatTache, Tache


def test_entree_est_abstraite_leve_type_error() -> None:
    """Verifie qu'on ne peut pas instancier Entree directement."""
    with pytest.raises(TypeError):
        Entree("Entree abstraite")  # type: ignore[abstract]


def test_tache_creation_et_attributs_par_defaut() -> None:
    """Verifie l'initialisation d'une tache et ses attributs."""
    tache = Tache("Acheter du pain", description="Boulangerie du coin")
    assert isinstance(tache.identifiant, UUID)
    assert tache.nom == "Acheter du pain"
    assert tache.description == "Boulangerie du coin"
    assert isinstance(tache.date_creation, datetime)
    assert tache.date_log == date.today()
    assert tache.etat == EtatTache.A_FAIRE


def test_deux_taches_meme_nom_ont_identifiants_differents() -> None:
    """Verifie l'unicite de l'identifiant meme avec un nom identique."""
    tache_1 = Tache("Faire les courses")
    tache_2 = Tache("Faire les courses")
    assert tache_1.identifiant != tache_2.identifiant


@pytest.mark.parametrize("nom_invalide", ["", "   ", "\t\n"])
def test_nom_vide_ou_espaces_leve_erreur(nom_invalide: str) -> None:
    """Verifie qu'un nom vide ou d'espaces est refuse."""
    with pytest.raises(ValueError):
        Tache(nom_invalide)


def test_terminer_tache_a_faire() -> None:
    """Verifie la transition A_FAIRE -> TERMINEE."""
    tache = Tache("Lire le chapitre 1")
    tache.terminer()
    assert tache.etat == EtatTache.TERMINEE


def test_abandonner_tache_a_faire() -> None:
    """Verifie la transition A_FAIRE -> ABANDONNEE."""
    tache = Tache("Ancienne tache")
    tache.abandonner()
    assert tache.etat == EtatTache.ABANDONNEE


def test_terminer_tache_abandonnee_leve_erreur() -> None:
    """Verifie qu'une transition depuis ABANDONNEE est interdite."""
    tache = Tache("Courses")
    tache.abandonner()
    with pytest.raises(ValueError):
        tache.terminer()


def test_abandonner_tache_terminee_leve_erreur() -> None:
    """Verifie qu'une transition depuis TERMINEE est interdite."""
    tache = Tache("Rapport")
    tache.terminer()
    with pytest.raises(ValueError):
        tache.abandonner()


def test_symbole_selon_etat_tache() -> None:
    """Verifie le symbole retourne pour chaque etat de Tache."""
    tache = Tache("Verifier les mails")
    assert tache.symbole() == "•"

    tache.terminer()
    assert tache.symbole() == "×"

    autre_tache = Tache("Tache abandonnee")
    autre_tache.abandonner()
    assert autre_tache.symbole() == "~"
