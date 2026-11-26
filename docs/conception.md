# Conception du Bullet Journal (Semaine 1)

## 1. Glossaire

* **Entree** : element de base du journal partageant des attributs communs (identifiant unique, nom, description, date de creation et date du log) et definissant un symbole de *rapid logging*.
* **Tache** : entree representant une action a accomplir qui suit un cycle de vie (a faire, terminee, migree, planifiee ou abandonnee).
* **Evenement** : entree liee a une date precise, et eventuellement a une heure, correspondant a un rendez-vous ou un fait marquant.
* **Note** : entree descriptive permettant de conserver une information, une observation ou un rappel sans cycle de tache.
* **Daily Log** : journal quotidien regroupant les entrees saisies au fil de la journee.
* **Monthly Log** : vue mensuelle combinant un calendrier du mois et une liste de taches ou d'evenements mensuels.
* **Future Log** : vue sur les mois a venir permettant de planifier des taches et evenements futurs.
* **Migration** : action consistant a reporter ou reorienter une tache non terminee (vers un autre jour, un mois suivant ou le Future Log, ou l'abandonner).
* **Signifiant** : marqueur visuel ajoute devant un symbole pour mettre en avant une information (par exemple la priorite ou une idee).

## 2. Symboles du rapid logging

| Symbole | Signification | Symbole | Signification |
| --- | --- | --- | --- |
| `•` | Tache a faire | `~` | Tache abandonnee |
| `×` | Tache terminee | `○` | Evenement |
| `>` | Tache migree | `–` | Note |
| `<` | Tache planifiee (Future Log) | `*` / `!` | Signifiants : priorite / idee |

## 3. Tableau des transitions d'une tache

Legende : **autorise** ou **interdit** (leve `ErreurTransitionInterdite`).

| Etat actuel | `terminer()` | `abandonner()` | `migrer()` | `planifier()` |
| --- | --- | --- | --- | --- |
| `A_FAIRE` | autorise | autorise | autorise | autorise |
| `TERMINEE` | interdit | interdit | interdit | interdit |
| `MIGREE` | interdit | interdit | interdit | interdit |
| `PLANIFIEE` | interdit | autorise | autorise | interdit |
| `ABANDONNEE` | interdit | interdit | interdit | interdit |
