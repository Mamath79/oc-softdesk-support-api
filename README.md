
# Soft Desk Support

Soft Desk Support est une application backend basée sur Django REST Framework qui permet de gérer des projets, de signaler des problèmes (issues) et d'y ajouter des commentaires. 

## Installation et lancement en local

Suivez les étapes ci-dessous pour installer et exécuter le projet en local.

---

### Prérequis

- Python 3.12 ou version supérieure
- Pipenv pour la gestion des dépendances
- Git pour cloner le dépôt

---

### Étapes d'installation

1. **Cloner le dépôt**
   Clonez le dépôt GitHub sur votre machine locale :
   ```bash
   git clone https://github.com/Mamath79/OC_P10_Creez-une-API-securisee-RESTful-en-utilisant-Django-REST.git
   cd Soft_desk_support
   ```

2. **Configurer l'environnement virtuel**
   Utilisez Pipenv pour créer et activer un environnement virtuel :
   ```bash
   pipenv install --python 3.12
   pipenv shell
   ```

3. **Installer les dépendances**
   Installez toutes les dépendances nécessaires :
   ```bash
   pipenv install
   ```

4. **Configurer la base de données**
   Appliquez les migrations pour configurer la base de données SQLite par défaut :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Lancer le serveur local**
   Démarrez le serveur Django pour exécuter le projet localement :
   ```bash
   python manage.py runserver
   ```

   L'application sera accessible à l'adresse suivante : [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

