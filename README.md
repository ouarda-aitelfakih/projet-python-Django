# PreSkool

Application web de gestion scolaire développée avec Django dans le cadre d'un projet de fin d'études (PFE) Bac+3.

---

## Technologies

- Python 3.10+
- Django 4.x
- SQLite (développement) / MySQL (production)
- HTML5, CSS3, Bootstrap
- Git & GitHub

---

## Contexte

PreSkool est une plateforme multi-rôles (Administrateur, Enseignant, Étudiant) qui centralise la gestion d'un établissement scolaire : inscriptions, résultats, emplois du temps et suivi pédagogique.

Le projet est développé en équipe selon un workflow Git collaboratif où chaque développeur travaille sur un module isolé.

---

## Branches GitHub

- `main` — production stable, merge après validation complète
- `python` — branche de développement intégré
- `feature/*` — une branche par module, une personne par branche (ex: `feature/auth`, `feature/exam`)


Règles : pull systématique avant tout développement, merge uniquement après tests, communication obligatoire avant chaque merge vers `python`.

---

## Modèles et fonctionnalités

### CustomUser (home_auth)
Étend AbstractUser de Django. Champs supplémentaires : `is_student`, `is_teacher`, `is_admin`. Un utilisateur ne peut avoir qu'un seul rôle actif.

### Parent (student)
Stocke les informations des parents : nom du père, nom de la mère, numéros de contact, adresse. Lié à un ou plusieurs étudiants.

### Student (student)
Représente un élève : identifiant, nom, prénom, genre, date de naissance, classe, section, numéro d'admission. Lié à un `CustomUser` (OneToOne) et à un `Parent` (ForeignKey).

### Department (department)
Représente un département de l'établissement : nom et responsable. Sert de point d'attache pour les enseignants et les matières.

### Teacher (teacher)
Profil complet d'un enseignant : identifiant, coordonnées, date d'embauche, qualification. Rattaché à un `Department` (la suppression du département ne supprime pas l'enseignant — SET_NULL).

### Subject (subjects)
Matière identifiée par un nom et un code. Associée à un `Department` et à un `Teacher` responsable.

### Exam (exam)
Représente un examen : nom, date, note totale, matière concernée.

### ExamResult (exam)
Note d'un étudiant à un examen : note obtenue, mention, remarques. Contrainte d'unicité : un étudiant ne peut avoir qu'un seul résultat par examen.

### Holiday (holiday)
Jour férié ou période de congé : nom, date de début, date de fin, description. Méthodes : `is_single_day()` et `duration()`.

### TimeTable (timetable)
Créneau horaire : jour (Lundi–Samedi), heure de début, heure de fin, salle, matière et enseignant concernés. Ordonné par jour puis par heure de début.

# les commandes utilisées 

## Installation

1. Cloner le projet :
   
git clone <lien>

3. Aller dans le dossier :
cd school

4. Créer un environnement virtuel :
python -m venv env
env\Scripts\activate

5. Installer les dépendances :
pip install -r requirements.txt

6. Appliquer les migrations :
python manage.py migrate

7. Charger les données :
python manage.py loaddata data.json

8. Lancer le serveur :
python manage.py runserver

## Identifiants de test
admin / admin123

## Lien vidéo
(lien ici)
