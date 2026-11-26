"""Gestion des erreurs du Bullet Journal."""


class ErreurBulletJournal(Exception):
    """Erreur generale du journal."""


class NomVide(ErreurBulletJournal, ValueError):
    """Le nom est vide."""


class EntreeIntrouvable(ErreurBulletJournal, LookupError):
    """L'entree n'existe pas."""


class DateInvalide(ErreurBulletJournal, ValueError):
    """La date ou l'heure est incorrecte."""


class EtatInvalide(ErreurBulletJournal, ValueError):
    """L'etat est incorrect."""
