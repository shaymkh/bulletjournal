[![CI](https://github.com/shaymkh/bulletjournal/actions/workflows/ci.yml/badge.svg)](https://github.com/shaymkh/bulletjournal/actions/workflows/ci.yml)

# bujo — Bullet Journal en Python

Bibliothèque Python qui modélise un Bullet Journal : tâches, événements
et notes, avec le système de symboles du *rapid logging*.

## Installation

    git clone https://github.com/shaymkh/bulletjournal.git
    cd bulletjournal
    conda create -n bujo python=3.12
    conda activate bujo
    pip install -r requirements.txt

## Utilisation

    from bujo.modeles.tache import Tache

    tache = Tache("Acheter du pain")
    print(tache)            # • Acheter du pain
    tache.terminer()
    print(tache)            # × Acheter du pain

## Tests et qualité du code

    pytest                  # lance les tests
    pytest --cov=bujo       # avec la couverture
    flake8 bujo tests       # style PEP 8 et docstrings

## Licence

MIT
