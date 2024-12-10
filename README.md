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

1. Cloner le dépôt :

    ```bash
    git clone https://github.com/<votre-compte-github>/epicevents-crm.git
    cd epicevents-crm
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

4. Configurer les variables d’environnement :

    Créez un fichier `.env` à la racine du projet pour y stocker les informations sensibles (clés secrètes, identifiants de base de données, DSN Sentry, etc.) :

    ```env
    DATABASE_URL=postgresql://user:password@localhost/epicevents
    SECRET_KEY=une_cle_secrete_pour_les_jwt
    SENTRY_DSN=votre_dsn_sentry
    ```

    Adaptez ces informations à vos besoins.

5. Initialiser la base de données :

    L’application utilise Alembic (si intégré) pour les migrations. Exécutez les migrations initiales (ou directement le `create_all` si encore à l’étape de développement) :

    ```bash
    alembic upgrade head
    ```

    Sinon, si vous êtes au stade de développement initial :

    ```bash
    python main.py init-db
    ```

    (Cette commande dépend de votre implémentation ; assurez-vous d'avoir un point d’entrée pour créer les tables.)

## Utilisation

L’application se pilote via la ligne de commande. Une fois installée et configurée, vous pouvez lancer :

```bash
python main.py --help
```

Cela affichera la liste des commandes disponibles et leurs options.

### Exemples de Commandes

- **Authentification** :

    ```bash
    python main.py login
    ```

    Saisissez votre nom d’utilisateur et mot de passe. Un jeton d’authentification sera généré et stocké (selon votre implémentation) pour les prochaines commandes.

- **Gestion des clients** :

    ```bash
    python main.py create-client --name "Kevin Casey" --email "kevin@startup.io" --phone "+67812345678" --company "Cool Startup LLC"
    ```

    Cette commande crée un nouveau client dans la base.

- **Liste des clients** :

    ```bash
    python main.py list-clients
    ```

    Affiche tous les clients. Vous pouvez ajouter des options pour filtrer ou trier.

- **Contrats & Événements** :

    Des commandes similaires existent pour créer, modifier et lister les contrats et les événements. Consultez l’aide intégrée :

    ```bash
    python main.py create-contract --help
    python main.py list-events --help
    ```

## Tests

Les tests unitaires et d’intégration sont placés dans le répertoire `tests/`. Pour les exécuter :

```bash
pytest
```

Vous pouvez également générer un rapport de couverture de code :

```bash
pytest --cov=epicevents
```

## Qualité du Code

Pour analyser la qualité du code :

```bash
flake8 --format=html --htmldir=flake8_report
```

Ouvrez `flake8_report/index.html` dans votre navigateur pour consulter le rapport.

## Contribuer

- **Branching model** : Utilisez des branches nommées de manière explicite pour chaque nouvelle fonctionnalité ou correction de bug.
- **Pull requests** : Envoyez des pull requests claires, avec une description des modifications apportées.
- **Tests et Documentation** : Ajoutez ou mettez à jour les tests et la documentation lorsque vous apportez une modification.

## Sécurité et Clés Sensibles

- Ne commitez jamais vos clés sensibles ou mots de passe dans le dépôt.
- Stockez les clés dans le fichier `.env` qui n’est pas versionné (à lister dans `.gitignore`).

## Auteurs

[Votre Nom ou le Nom de l’Équipe]

## Licence

Ce projet est interne à Epic Events. Contactez l’administrateur du projet pour plus d’informations sur les droits d’utilisation.