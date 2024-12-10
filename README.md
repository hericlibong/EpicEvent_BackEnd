# EpicEvents CRM - Backend Application

## Présentation

EpicEvents CRM est une application interne permettant à l’entreprise Epic Events de gérer plus efficacement ses clients, contrats et événements. Développée en Python, cette application met l’accent sur la sécurité, la maintenabilité et l’évolutivité. Elle propose une interface en ligne de commande (CLI) pour permettre aux collaborateurs (commerciaux, gestion, support) de travailler sur les données internes du CRM sans interface graphique, mais de manière simple et structurée.

L’application utilise des composants et bibliothèques de référence :

- **Base de Données** : PostgreSQL, pour sa robustesse, sa stabilité et ses capacités avancées.
- **ORM** : SQLAlchemy, pour interagir de manière sécurisée avec la base de données et éviter l’usage de requêtes SQL brutes.
- **Architecture** : Design patterns MVC et DAO pour une séparation claire des responsabilités, facilitant la maintenance et les évolutions futures.
- **Interface Utilisateur** : Click & Rich, permettant une expérience en ligne de commande plus ergonomique, avec des tables, des couleurs et des messages d’aide.
- **Sécurité & Authentification** : Passlib pour le hachage des mots de passe, PyJWT pour la gestion des tokens, Pydantic pour la validation des données.
- **Journalisation & Suivi des Erreurs** : Intégration à Sentry pour la capture des erreurs et le suivi des exceptions.
- **Qualité & Tests** : pytest pour les tests, flake8 + flake8-html pour s’assurer du respect des bonnes pratiques et du style de code.

## Fonctionnalités Principales

- Gestion des utilisateurs et authentification (commerciaux, gestion, support) avec permissions adaptées à chaque rôle.
- Création, mise à jour et consultation des clients.
- Création, mise à jour et consultation des contrats (avec statut, montants, etc.).
- Création, assignation et mise à jour des événements (associés aux clients via les contrats).
- Filtrage et recherche avancés (par exemple, rechercher tous les événements sans support, contrats non signés, etc.).
- Interface en ligne de commande ergonomique, avec aide intégrée.

## Prérequis

- Python 3.9+
- PostgreSQL installé sur votre machine ou accessible via un serveur distant.
- Un environnement virtuel Python (recommandé) pour isoler les dépendances.

## Installation

1. Cloner le repo :

    ```bash
    git clone https://github.com/hericlibong/EpicEvent_BackEnd.git
    cd EpicEvent_Backend
    ```

2. Créer et activer un environnement virtuel (optionnel mais recommandé) :

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Linux/MacOS
    venv\Scripts\activate     # Sur Windows
    ```

3. Installer les dépendances :

    ```bash
    pip install -r requirements.txt
    ```
4. Aller dans l'application
    ```bash
    cd epicevents
    ```



    ### Configuration de la Base de Données

    #### Connexion au Super-Utilisateur PostgreSQL

    Ouvrez une console (PowerShell, CMD sous Windows ou un terminal sous Linux/macOS) et connectez-vous à PostgreSQL en tant que super-utilisateur postgres :

    ```bash
    psql -U postgres
    ```

    Saisissez le mot de passe postgres si nécessaire.

    #### Création de la Base de Données et de l’Utilisateur

    Dans le prompt psql, exécutez :

    ```sql
    CREATE DATABASE epicevents_db;
    CREATE USER epicenvents_user WITH PASSWORD 'M0tD3P4ss3';
    GRANT ALL PRIVILEGES ON DATABASE epicevents_db TO epicenvents_user;
    \q
    ```

    **Conseil** : Utilisez des identifiants simples, sans accents ni caractères spéciaux complexes. Par exemple :

    - Utilisateur : `epicenvents_user`
    - Mot de passe : `MySecurePassword123` (pas d’accents, pas d’espaces)

    #### Configurer le Fichier .env

    Renommez le fichier d’exemple  fourni :

    ```bash
    cp .env_sample .env
    ```

    Ouvrez le fichier `.env` (situé dans le répertoire epicevents) et mettez à jour les variables :

    ```env
    DB_USER=epicenvents_user
    DB_PASSWORD=MySecurePassword123
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=epicevents_db

    SECRET_KEY=my_secret_key
    SENTRY_DSN=
    ```

    Assurez-vous que le fichier `.env` est bien dans le répertoire epicevents et qu’il ne contient aucun caractère accentué ou problème d’encodage. Assurez-vous également que ce fichier n’est pas versionné (il doit être listé dans `.gitignore`).

    #### Initialiser la Base de Données avec Alembic

    Depuis le répertoire epicevents (là où se trouvent `alembic.ini` et le dossier `alembic`), lancez :

    ```bash
    alembic upgrade head
    ```

    Cette commande applique les migrations définies dans `alembic/versions` et crée les tables nécessaires dans la base de données `epicevents_db`.

## Utilisation

L’application se pilote via la ligne de commande. Une fois installée et configurée, vous pouvez lancer :

    ```
    python main.py --help
    ```


Exemple d'affichage d'aide :


    ```
        Usage: main.py [OPTIONS] COMMAND [ARGS]...

    Interface en ligne de commande pour Epic Events.

    Options:
    --help  Show this message and exit.

    Commands:
    clients         Commandes pour gérer les clients.
    contracts       Commandes pour gérer les contrats.
    events          Commandes pour gérer les événements.
    sample-command  Commande d'exemple avec journalisation.
    users           Commandes pour gérer les utilisateurs.
    ```

Cela affichera la liste des commandes disponibles et leurs options.

### Exemples de Commandes

- **Authentification** :

    ```bash
    python main.py users login
    ```

    Saisissez votre nom d’utilisateur et mot de passe. Un jeton d’authentification sera généré et stocké (selon votre implémentation) pour les prochaines commandes.

- **Gestion des clients** :

    ```bash
    python main.py clients create-clients
    ```

    Cette commande crée un nouveau client dans la base.

- **Liste des clients** :

    ```bash
    python main.py clients list-clients
    ```

    Affiche tous les clients. Vous pouvez ajouter des options pour filtrer ou trier.

- **Contrats & Événements** :

    Des commandes similaires existent pour créer, modifier et lister les contrats et les événements. Consultez l’aide intégrée :

    ```bash
    python main.py create-contract --help
    python main.py list-events --help
    ```



