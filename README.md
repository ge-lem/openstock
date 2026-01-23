# Open Stock

Ceci est un site d'annonce minimaliste.

Les fonctionnalités:
- Recherche d'annonces
- Gestion des annonces par organisations
- Compression automatique des images
- Création de compte et authentification soit par invitation soit par système CAS
- PAS de messagerie interne, prise de contact par affichage de l'adresse email.

### Les organisations
Une annonce est rattachée à une organisation et non à une personne. Cependant chaque personne possède une organisation qui lui est propre dite *Personnelle*.

Ensuite une personne peut créer des organisations auquelles elle pourra ajouter des manageurs. Ceci permet de gerer à plusieurs une même organisation.

### Les annonces

Afin de limité la taille de la base de donnée, une seule annonce à l'état de brouillon est authorisée par organisation.

Les annonces ont une date d'expiration. Elles sont définitivement supprimées du système 30 jours après leur expiration.
Il est possible de retirer la date d'expiration mais cela n'est pas conseillé. Il vaut mieux mettre une date d'expiration très longue comme 1 an voir plus.

## Aspects techniques

### Technos

- Python django
- Vue JS

### Installation

A executer dans le dossier du dépot
```
# configurer un environement virtuel python
cp .env.local.example .env.local
cp openstock/local_settings.py.example openstock/local_settings.py
edit openstock/local_settings.py
edit openstock/settings.py
# Vous devez générer une nouvelle clé secrète !!!
sudo edit /etc/django_secret_key.txt
pip install -r requirements.txt
python manage.py migrate
# if not CAS authentication, create first user
python manage.py createsuperuser

./init.sh
cd frontend
edit .env
edit src/views/HomeView.vue
edit src/views/AboutView.vue
edit src/views/LegalsView.vue
npm install
npm run build
```

Si vous utiliser LDAP
```
sudo apt-get install libsasl2-dev libldap2-dev libssl-dev
pip install django-auth-ldap
```

### Tester en local

Une fois les étapes de build ou d'installation ci-dessus effectuées, vous pouvez lancer et tester le résultat par exemple en

1. Ajoutant `http://localhost:5173` aux `CORS_ALLOWED_ORIGINS` de votre fichier `openstock/local_settings.py`
2. Démarrant le backend sur le port 8000 avec `python manage.py runserver`
3. Démarrant le frontend sur le port 5173 en exécutant `npm run dev` depuis le dossier `frontend`

### Déploiement

Si vous utilisez un reverse proxy type nginx, les deux dossiers à servir en statique sont `staticfiles` et `media`

## Exemple d'instances déployées

* openstock.fr est une plateforme de don de pièces détachées entre différentes entités de Grenoble, pour favoriser l’utilisation de composants de seconde main ! 

## Licensing

The source code is licensed under GPL v3. License is available [here](/LICENSE).
