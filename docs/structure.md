


## Architecture/structure

### Vue (CLI)

Basée sur Click et Rich pour une interface utilisateur interactive et agréable.  
Journalisation des actions utilisateur via Sentry.

### Contrôleurs

Intermédiaires entre les vues, les modèles et les DAO.  
Incluent la logique métier, les validations, et la gestion des droits d'accès.  
Gestion des erreurs spécifiques avec journalisation.

### Modèles

Représentent les entités métier en Python.  
Simples, sans logique métier intégrée.

### DAO (Data Access Object)

Gestion des opérations CRUD et méthodes spécifiques à l'application avec SQLAlchemy.  
Journalisation des exceptions et suivi des requêtes via Sentry.

### Base de Données

PostgreSQL, utilisée pour le stockage persistant des données.

### Alembic

Gestion manuelle des migrations de base de données (phase d'apprentissage).

### Sentry

Intégré pour la journalisation des erreurs critiques et des métriques.  
Captures étendues dans les contrôleurs et DAO.


```markdown
### Schéma

```plaintext
+------------------------+
|        Vue (CLI)       |
|   (Click, Rich)        |
|  (Journalisation des   |
|   actions utilisateur) |
+-----------+------------+
            |
            v
+------------------------+
|      Contrôleurs       |
| (Interagissent avec    |
|  les modèles et DAO)   |
| (Incluent une logique  |
|  métier et des         |
|  validations, avec     |
|  gestion des erreurs)  |
+-----------+------------+
            |
            v
+------------------------+
|        Modèles         | 
| (Classes Python        |
|  représentant les      |
|  entités métier)       |
+-----------+------------+
            |
            v
+------------------------+
|          DAO           |
| (Gestion de l'accès    |
|  aux données avec      |
|  SQLAlchemy, incluant  |
|  des méthodes spécifiques|
|  et journalisation des |
|  exceptions)           |
+-----------+------------+
            |
            v
+------------------------+
|    Base de Données     |
|      (PostgreSQL)      |
+-----------+------------+
            |
            v
+------------------------+
|      Alembic          |
| (Gestion des          |
|  migrations de la     |
|  base de données,     |
|  manuel actuellement) |
+-----------+------------+
            |
            v
+------------------------+
|       Sentry           |
| (Journalisation des   |
|  erreurs critiques    |
|  et métriques via les |
|  DAO et contrôleurs)   |
+------------------------+
```
```
