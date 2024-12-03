
# Exercices Hyggle

Voici mes réponse au test technique pour la candidature d'alternance au poste de Développeur FullStack.



## Auteur

- [@GuillaumeCAN](https://www.github.com/GuillaumeCAN)


## Installation

**1. Installer python et PIP** :

Afin de pouvoir utilisé le code, assurez-vous d'avoir installé Python 3.12 ou supérieur :

```bash
  sudo apt install python3
  python --version
```
Assurez-vous également d'avoir **PIP** pour installer les dépendances :
```bash
  python get-pip.py
```

**2. Clonez ce repository :**

   ```bash
   git clone https://github.com/GuillaumeCAN/exercicesHyggle.git
   cd exercicesHyggle
   ```

   Installez les dépendances :
   ```bash
   pip install -r requirements.txt
  ```

**3. Exercices 1 & 2 :**

Pour les exercices 1 et 2, il vous suffit de lancer la commande :
  ```bash
   cd exercices1-2
   python3 exercice1.py
   python3 exercice2.py
  ```
  Les fichiers CSV seront télécharger automatiquement.


## Projet Django

Pour le projet Django rendez-vous dans le dossier :
```bash
  cd energetic_dashboard
```
Appliquer les migrations pour creer la base de données :
```bash
  python manage.py migrate
```

Lancer le serveur de développement :
```bash
  python manage.py runserver
```
Rendez-vous sur http://127.0.0.1:8000/ une fois le serveur de développement lancé.
Vous pouvez maintenant navigué sur le projet Django.
    
## API Reference

#### Récupérer toute la collection :

```http
  GET /api/energy-data/
```

#### Récupérer un item spécifique dans la collection :

```http
  GET /api/energy-data/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Requis**. ID de l'item à récupérer |

#### Ajouter un item dans la collection :

```http
  POST /api/energy-data/
```

| Parameter | Type     | Description                            |
| :-------- | :------- | :--------------------------------      |
| `id`      | `int`    | **Auto**. ID de l'item                 |
| `date`    | `string` | **Requis**. date de l'item à récupérer (YYYY-MM-DD) |
| `region`      | `string`    | **Requis**. Region de l'item à récupérer   |
| `consumption_twh`      | `float`    | **Requis**. Consommation de l'item à récupérer   |


#### Modifier un item dans la collection :

```http
  PUT /api/energy-data/${id}
```

| Parameter | Type     | Description                            |
| :-------- | :------- | :--------------------------------      |
| `id`      | `int`    | **Requis**. ID de l'item                 |
| `date`    | `string` | **Requis**. date de l'item à modifier (YYYY-MM-DD) |
| `region`      | `string`    | **Requis**. Region de l'item à modifier  |
| `consumption_twh`      | `float`    | **Requis**. Consommation de l'item à modifier   |


#### Supprimer un item dans la collection :
```http
  DELETE /api/energy-data/${id}
```

| Parameter | Type     | Description                            |
| :-------- | :------- | :--------------------------------      |
| `id`      | `int`    | **Requis**. ID de l'item à supprimer                |
