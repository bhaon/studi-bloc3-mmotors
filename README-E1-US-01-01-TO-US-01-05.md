# COMMIT INITIALE + EPIC 01

## Mise en place du Frontend

### Prototype du Frontend
- Prototype créé en HTML statique -> Fichier: prototypesHTML/m-motors_initial.html.
- Ce prototype sert pour validation avec le PO et les parties prenantes.
- Construction d'une application NextJS 15 avec ce template.
- Mise en place de tests unitaires sur l'intégralité des fichiers.

## Mise en place du Backend minimaliste
- Création de l'application FastAPI minimaliste avec les fonctions CRUD pour les véhicules.
- Création des models et des dépendances pour utiliser la base de données au travers de SQLAlchemy.
- Création d'un script seed.py pour alimenterr la base de données afin de faire les tests visuels.
- Mise en place des tests unitaires et d'intégration avec la base de données

## Mise en place Architecture Production et Staging sur un seul VPS
VPS (1 machine)
├── Traefik (port 80/443) ← reverse proxy unique
├── /opt/mmotors/production/   → stack prod  (domaine : mmotors.fr)
└── /opt/mmotors/staging/      → stack staging (domaine : staging.mmotors.fr)

Déploiement via Kubernetes (manifests `k8s/`).

## Mise en place d'un Pipeline CI Manuel GitHub Actions
- Mise en place d'une pipeline manuelle GitHub Actions pour valider :
    - Modifications du repo
    - Linter Frontend et Backend
    - Tests unitaires Frontend
    - Tests unitaires Backend
    - Tests intégration DB Backend
    - Analyse Sonaqube (sécurité)
    - Notification Slack

# EPIC 01
Tous les Use Cases de l'Epic 01 sont en place et validés avec les étapes de DOD.
Cela permet d'avoir une application opérationnelle avec le stricte minimum :
- Consultation du catalogue des véhicules avec filtrage
- Une API permetante d'ajouter des véhicules (sans espace Back Office)
- Pas d'authentificatiion