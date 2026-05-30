# Application de Gestion des Étudiants - Django

Projet prêt à l'emploi pour le sujet **Application de Gestion des Étudiants**.

## Fonctionnalités couvertes
- CRUD des étudiants
- CRUD des cours
- CRUD des filières et classes
- Gestion des inscriptions des étudiants aux cours
- Liste des étudiants par classe
- Liste des étudiants par cours
- Détail d'un étudiant avec ses inscriptions
- Authentification Django
- Permissions via groupes Django
- Interface responsive avec Bootstrap
- Tableau de bord simple
- Recherche, filtres et pagination
- Tests unitaires de base

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows: .venv\Scriptsctivate
pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap_roles
python manage.py seed_demo_data
python manage.py runserver
```

## Comptes de démonstration
- `admin / Admin12345!`
- `gestionnaire / Gestion12345!`
- `consultation / Consult12345!`

## Structure
- `academics/models.py` : modèles principaux
- `academics/views.py` : vues CRUD, dashboard et rapports
- `templates/academics/` : interfaces HTML
- `academics/management/commands/` : commandes pour rôles et données de démo

## Ce que tu peux montrer dans la vidéo
1. Connexion
2. Ajout d'une filière, classe, étudiant, cours
3. Création d'une inscription
4. Affichage du détail d'un étudiant
5. Rapport étudiants par classe / par cours
6. Dashboard
