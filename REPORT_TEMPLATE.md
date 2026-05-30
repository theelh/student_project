# Rapport - Projet Django

## 1. Présentation du projet
Ce projet est une **Application de Gestion des Étudiants** réalisée avec Django.
L'objectif est de gérer les étudiants, les cours, les filières, les classes et les inscriptions,
tout en respectant les exigences de l'énoncé du projet.

## 2. Architecture adoptée
Le projet suit l'architecture standard de Django :
- `models.py` pour les entités métier
- `views.py` pour la logique des pages
- `urls.py` pour le routage
- `templates/` pour l'interface HTML
- `forms.py` pour la validation des formulaires
- `admin.py` pour l'administration

## 3. Modèles utilisés
- **Program** : filière
- **ClassRoom** : classe/niveau
- **Student** : étudiant
- **Course** : cours
- **Enrollment** : inscription d'un étudiant à un cours

## 4. Fonctionnalités implémentées
- CRUD complet des étudiants
- CRUD des cours
- CRUD des filières et classes
- Gestion des inscriptions
- Détail d'un étudiant avec ses cours inscrits
- Liste des étudiants par classe
- Liste des étudiants par cours
- Authentification et autorisations avec Django
- Tableau de bord et recherche

## 5. Choix techniques
- Framework backend : Django
- Base de données : SQLite
- Frontend : Templates Django + Bootstrap
- Validation : ModelForm
- Permissions : Groupes et permissions Django

## 6. Difficultés rencontrées
- Gestion des relations entre étudiants, cours et inscriptions
- Mise en place des permissions
- Gestion du responsive design

## 7. Conclusion
Le projet répond aux exigences minimales du sujet choisi.
Des améliorations peuvent être ajoutées comme l'export CSV/PDF, plus de tests et des statistiques avancées.
