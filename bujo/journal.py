"""Gestion globale des entrees du Bullet Journal et persistance JSON."""

from __future__ import annotations

import json
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from uuid import UUID

from bujo.exceptions import EntreeIntrouvable
from bujo.modeles.entree import Entree
from bujo.modeles.evenement import Evenement
from bujo.modeles.note import Note
from bujo.modeles.tache import EtatTache, Tache


class Journal:
    """Conteneur principal des entrees du Bullet Journal."""

    def __init__(self, nom: str = "Mon Bullet Journal") -> None:
        """Initialise un journal vide."""
        self.nom = nom
        self._entrees: dict[UUID, Entree] = {}

    def __len__(self) -> int:
        """Retourne le nombre d'entrees presentes dans le journal."""
        return len(self._entrees)

    def ajouter(self, entree: Entree) -> UUID:
        """Ajoute une entree au journal et retourne son identifiant."""
        if not isinstance(entree, Entree):
            raise TypeError(
                "L'objet ajoute doit etre une instance d'Entree."
            )
        self._entrees[entree.identifiant] = entree
        return entree.identifiant

    def obtenir(self, identifiant: UUID | str) -> Entree:
        """Recupere une entree ou leve EntreeIntrouvable."""
        uid = UUID(str(identifiant))
        if uid not in self._entrees:
            raise EntreeIntrouvable(f"Aucune entree avec l'id {uid}.")
        return self._entrees[uid]

    def supprimer(self, identifiant: UUID | str) -> None:
        """Supprime une entree ou leve EntreeIntrouvable."""
        uid = UUID(str(identifiant))
        if uid not in self._entrees:
            raise EntreeIntrouvable(f"Aucune entree avec l'id {uid}.")
        del self._entrees[uid]

    def lister(
        self,
        type_entree: type[Entree] | None = None,
    ) -> list[Entree]:
        """Retourne la liste des entrees, optionnellement filtree par type."""
        entrees = list(self._entrees.values())
        if type_entree is not None:
            entrees = [e for e in entrees if isinstance(e, type_entree)]
        return entrees

    def daily_log(self, jour: date) -> list[Entree]:
        """Retourne les entrees associees a une date precise."""
        return [e for e in self._entrees.values() if e.date_log == jour]

    def monthly_log(self, annee: int, mois: int) -> list[Entree]:
        """Retourne les entrees d'une annee et d'un mois donnes."""
        return [
            e
            for e in self._entrees.values()
            if e.date_log.year == annee and e.date_log.month == mois
        ]

    def future_log(self, depuis: date | None = None) -> list[Entree]:
        """Retourne les entrees planifiees apres une date de reference."""
        reference = date.today() if depuis is None else depuis
        return [e for e in self._entrees.values() if e.date_log > reference]

    def to_dict(self) -> dict[str, Any]:
        """Serialise le journal et ses entrees en dictionnaire."""
        entrees_serialisees: list[dict[str, Any]] = []
        for entree in self._entrees.values():
            donnees: dict[str, Any] = {
                "type": type(entree).__name__,
                "identifiant": str(entree.identifiant),
                "date_creation": entree.date_creation.isoformat(),
                "nom": entree.nom,
                "description": entree.description,
                "date_log": entree.date_log.isoformat(),
            }
            if isinstance(entree, Tache):
                donnees["etat"] = entree.etat.value
            elif isinstance(entree, Evenement):
                donnees["date_evenement"] = entree.date_evenement.isoformat()
                donnees["heure"] = (
                    entree.heure.isoformat() if entree.heure else None
                )
            entrees_serialisees.append(donnees)
        return {"nom": self.nom, "entrees": entrees_serialisees}

    @classmethod
    def from_dict(cls, donnees: dict[str, Any]) -> Journal:
        """Reconstruit un Journal depuis un dictionnaire."""
        journal = cls(nom=donnees.get("nom", "Mon Bullet Journal"))
        for item in donnees.get("entrees", []):
            type_nom = item.get("type")
            nom = item["nom"]
            description = item.get("description", "")
            date_log = date.fromisoformat(item["date_log"])

            entree: Entree
            if type_nom == "Tache":
                tache = Tache(
                    nom=nom, description=description, date_log=date_log
                )
                if "etat" in item:
                    tache._etat = EtatTache(item["etat"])
                entree = tache
            elif type_nom == "Evenement":
                date_evt = date.fromisoformat(item["date_evenement"])
                heure_raw = item.get("heure")
                heure_evt = (
                    time.fromisoformat(heure_raw) if heure_raw else None
                )
                entree = Evenement(
                    nom=nom,
                    date_evenement=date_evt,
                    description=description,
                    heure=heure_evt,
                    date_log=date_log,
                )
            elif type_nom == "Note":
                entree = Note(
                    nom=nom, description=description, date_log=date_log
                )
            else:
                raise ValueError(f"Type d'entree inconnu : {type_nom}")

            entree._identifiant = UUID(item["identifiant"])
            if "date_creation" in item:
                entree._date_creation = datetime.fromisoformat(
                    item["date_creation"]
                )
            journal.ajouter(entree)
        return journal

    def sauvegarder(self, chemin: str | Path) -> None:
        """Sauvegarde le journal dans un fichier JSON."""
        fichier = Path(chemin)
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def charger(cls, chemin: str | Path) -> Journal:
        """Charge un journal depuis un fichier JSON."""
        contenu = Path(chemin).read_text(encoding="utf-8")
        return cls.from_dict(json.loads(contenu))
