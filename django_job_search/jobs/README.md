# Préparer les views pour l'APIView

**On se pose les questions suivantes :**

1. Quelles sont les informations que l'on souhaite avoir sur la page d'accueil ?

- Résultats d'une recherche par Pays et par type de travail pour plusieurs sites
- Résultats des recherches passées lorsque l'on est connecté

2. Comment accéder à ces informations ?

Si aucune recherche dans la base de donnée ne correspond à ce qui est entré dans le formulaire, on lance le script.

Si une recherche est déjà lancée et contient des informations de moins d'un mois, on affiche ses informations
mais on lance également le script pour ajouter des informations plus fraîches.