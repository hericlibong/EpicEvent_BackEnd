# Description de la base de données

La base de données est structurée autour de cinq entités principales : **User**, **Client**, **Contract**, **Event**, et **Department**, chacune avec des relations bien définies :

- **User** représente les utilisateurs, qui appartiennent à un **Department** (relation 1 à plusieurs). Chaque utilisateur peut être un gestionnaire de **Clients**, un responsable des **Contracts**, et un contact de support pour les **Events** (relations plusieurs à plusieurs).

- **Client** correspond aux clients de l'organisation. Chaque client est associé à un responsable commercial (**User**) et peut avoir plusieurs **Contracts**.

- **Contract** représente les contrats signés par les clients. Chaque contrat est associé à un **Client** et à un utilisateur responsable (**User**), et peut planifier plusieurs **Events**.

- **Event** désigne des événements liés à un **Contract**, avec un support assuré par un utilisateur (**User**). Chaque événement est unique à un contrat.

- **Department** représente les départements au sein de l'organisation. Chaque utilisateur (**User**) est assigné à un seul département.

Ces relations permettent de modéliser un système de gestion centralisé, où les rôles des utilisateurs, la gestion des clients et contrats, et les événements sont interconnectés de manière cohérente.