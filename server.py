from flask import Flask, render_template, request, redirect
from flask.globals import session
import json as jn
import psycopg2
import psycopg2.extras


# permet d'éviter les "TypeError" de sérialisation Json des dates (trouvé sur stackoverflow)
class DatetimeEncoder(jn.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


# penser a adapter le mot de passe et l'user a votre base de données
connexion = psycopg2.connect("dbname=buildrz user=postgres password=stdRoot")

app = Flask(__name__)
app.secret_key = 'fgjklwsdhwsxjkl'


# route principale (affichage de tous les projets d'une ville, ainsi que le total du ca des projets avec un certain statut)
@app.route("/", methods=['GET'])
def main():
    # création d'un curseur permettant l'utilisation de dictionnaires
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)
    postcode = None
    statut = None

    if request.method == "GET":
        postcode = request.args.get("code_postal")
        statut = request.args.get("statut")

    projets = []
    somme = 0
    if postcode != None:
        # récuperation des la liste des projets correspondants
        cursor.execute("SELECT parcelle.adresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire, projet.statut, projet.id FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = %s;", (postcode,))
        projets = cursor.fetchall()
    if (postcode != None) & (statut != None):
        # calcul de la somme a l'aide d'une fonction SQL
        cursor.execute("SELECT somme(%s, %s);", (postcode, statut,))
        somme = cursor.fetchall()[0]['somme']
    if somme == None:
        somme = 0

    # récuperation de la liste des codes postaux
    cursor.execute("SELECT code_postal,nom FROM ville ORDER BY code_postal")
    postcodesList = cursor.fetchall()

    # valeurs par défaut en cas de requte GET incomplete ou invalide
    if postcode == None:
        postcode = ""
    if statut == None:
        statut = "en cours"
    return render_template("template.html", projets=projets, somme=somme, postcode=postcode, statut=statut, postcodesList=postcodesList)


# route permettant de récupérer la liste des projets au format Json
@app.route("/getJson/", methods=['GET'])
def json():
    # création d'un curseur permettant l'utilisation de dictionnaires
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)

    postcode = None

    if request.method == "GET":
        postcode = request.args.get("code_postal")

    projets = dict()
    if postcode != None:
        cursor.execute(
            "SELECT * FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = %s;", (postcode,))
    else:
        cursor.execute(
            "SELECT * FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id")
    projets = cursor.fetchall()

    # utilisation du DatetimeEncoder pour sérialiser les dates
    jsonStr = jn.dumps(projets, cls=DatetimeEncoder)
    return jsonStr


# route pour changer le statut d'un projet
@app.route("/changeStatut/", methods=['POST'])
def statut():
    cursor = connexion.cursor()
    id = request.form.get("id")
    statut = request.form.get("statut")
    if id != None:
        cursor.execute(
            "SELECT statut FROM projet WHERE id = %s", (id,))
        try:
            res = cursor.fetchall()[0][0]
        except:
            # en cas d'exception ici, cela signifie que l'identifiant demandé n'existe pas
            return "Erreur: Identifiant invalide", 400
        if(res != statut):
            # verification que la modification est autorisée (les projets abandonnés ou terminés ne peuvent plus changer de statut)
            if res != "en cours":
                return "Erreur: il est interdit de change le statut de " + res + " a " + statut, 400
            try:
                cursor.execute(
                    "UPDATE projet SET statut = %s WHERE id = %s", (statut, id,))
                connexion.commit()
            except:
                return "Erreur: Impossible de modifier le projet", 500
    else:
        return "Erreur: Pas d'identifiant", 400
    # retour a la page précédante
    return redirect(request.referrer)


# Route permettant de créer un nouveau projet (avec interface)
@app.route("/addProject/", methods=['GET', 'POST'])
def projectList():
    postcode = None
    parcelles = None
    if request.method == "GET":
        postcode = request.args.get("code_postal")

    if postcode != None:
        if str(postcode).isdigit():
            # création d'un curseur permettant l'utilisation de dictionnaires
            cursor = connexion.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                "SELECT * FROM parcelle WHERE parcelle.code_postal = %s", (postcode,))
            parcelles = cursor.fetchall()
            # affichage de la liste des parcelles
            return render_template("create_project.html", parcelles=parcelles, code_postal=postcode)

    if request.method == "POST":
        login = session.get('login')
        parcelle_id = request.form.get("parcelle_id")
        ca = request.form.get("ca")
        if login == None:
            return "Veuillez vous connecter", 401
        try:
            cursor = connexion.cursor()
            # ajout de la nouvelle parcelle
            cursor.execute(
                "INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT NOW()),%s,'en cours', %s,%s);", (ca, parcelle_id, login,))
            connexion.commit()
        except:
            return "Erreur: Impossible de créer le projet", 500
    # en cas de code postal non spécifié, ou apres ajout réussi, retour au formulaire pour demander un code postal
    return render_template("ask_code.html")


# Route permettant de créer une nouvelle parcelle (avec interface)
@app.route("/addParcelle/", methods=['GET', 'POST'])
def createParcelle():
    selected = None
    if request.method == "POST":
        # création de la nouvelle parcelle
        code_postal = request.form.get('code_postal')
        surface = request.form.get('surface')
        adresse = request.form.get('adresse')
        parcelle_id = request.form.get('parcelle_id')
        try:
            cursor = connexion.cursor()
            # verification de l'unicité de l'identifiant
            cursor.execute(
                "SELECT * FROM parcelle WHERE parcelle_id = %s", (parcelle_id,))
            if(len(cursor.fetchall()) != 0):
                return "Erreur, identifiant non unique", 400
            cursor.execute(
                "INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (%s, %s, %s, %s)", (parcelle_id, surface, adresse, code_postal,))
            connexion.commit()
        except Exception as e:
            return "Erreur, nouvelle parcelle invalide : "+code_postal + ' '+surface+' '+adresse+' '+parcelle_id + ' (' + str(e) + ')', 400

    # création d'un curseur permettant l'utilisation de dictionnaires
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)

    # récuperation de la liste des villes
    cursor.execute("SELECT * FROM ville")
    villes = cursor.fetchall()
    if request.method == 'GET':
        selected = request.args.get('selected')
    return render_template("create_parcelle.html", villes=villes, selected=selected)


# Route permettant d'ajouter une nouvelle ville a la base de données (avec interface)
@app.route("/addVille/", methods=['GET', 'POST'])
def createVille():
    if request.method == "POST":
        code_postal = request.form.get('code_postal')
        nom = request.form.get('nom')
        try:
            cursor = connexion.cursor()
            # verification de l'unicité du code postal
            cursor.execute(
                "SELECT * FROM ville WHERE code_postal = %s", (code_postal,))
            if(len(cursor.fetchall()) != 0):
                return "Erreur, code postal non unique", 400

            cursor.execute(
                "INSERT INTO ville (code_postal,nom) VALUES (%s, %s)", (code_postal, nom,))
            connexion.commit()
        except Exception as e:
            return "Erreur, impossible de créer la nouvelle ville : "+code_postal + ' ' + nom + ' (' + str(e) + ')', 400

    return render_template("create_ville.html")


# route pour sélectionner l'utilisateur connecté (sans mots de passe)
@app.route("/login")
def loginPage():
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("login.html", users=users)


# création de session
@app.route("/loginValidate", methods=['POST'])
def login():
    login = request.form['login']
    session['login'] = login
    return redirect("/")


# déconnexion
@app.route("/logout")
def logout():
    session.pop('login')
    return redirect("/")


# retourne le nom de l'utilisateur connecté
@app.route("/showlogin")
def showlogin():
    try:
        return str(session['login'])
    except:
        return 'Pas connecté'
