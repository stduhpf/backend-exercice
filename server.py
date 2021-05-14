from flask import Flask, render_template, request, redirect
from flask.globals import session
import json as jn
import psycopg2
import psycopg2.extras


class DatetimeEncoder(jn.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


connexion = psycopg2.connect("dbname=buildrz user=postgres password=stdRoot")

app = Flask(__name__)
app.secret_key = 'fgjklwsdhwsxjkl'


@app.route("/", methods=['GET'])
def main():
    cursor = connexion.cursor()

    postcode = None
    statut = None

    if request.method == "GET":
        postcode = request.args.get("code_postal")
        statut = request.args.get("statut")

    res = []
    somme = 0
    if postcode != None:
        cursor.execute("SELECT parcelle.adresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire, projet.statut, projet.id FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = %s;", (postcode,))
        res = cursor.fetchall()
    if (postcode != None) & (statut != None):
        cursor.execute("SELECT somme(%s, %s);", (postcode, statut,))
        somme = cursor.fetchall()[0][0]
    if somme == None:
        somme = 0

    cursor.execute("SELECT code_postal,nom FROM ville ORDER BY code_postal")
    postcodesList = cursor.fetchall()
    if postcode == None:
        postcode = ""
    if statut == None:
        statut = "en cours"
    return render_template("template.html", res=res, somme=somme, postcode=postcode, statut=statut, postcodesList=postcodesList)


@app.route("/getJson/", methods=['GET'])
def json():
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)

    postcode = None

    if request.method == "GET":
        postcode = request.args.get("code_postal")

    res = dict()
    if postcode != None:
        cursor.execute("SELECT parcelle.adresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire, projet.statut FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = %s;", (postcode,))
    else:
        cursor.execute("SELECT parcelle.adresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire, projet.statut FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id")
    res = cursor.fetchall()

    jsonStr = jn.dumps(res, cls=DatetimeEncoder)
    return connexion.encoding + jsonStr


@app.route("/changeStatut/", methods=['POST'])
def statut():
    cursor = connexion.cursor()
    id = request.form.get("id")
    statut = request.form.get("statut")
    if id != None:
        cursor.execute(
            "SELECT statut FROM projet WHERE id = %s", (id,))
        res = cursor.fetchall()[0][0]
        if(res != statut):
            if res != "en cours":
                return "Erreur: il est interdit de change le statut de " + res + " a " + statut, 400
            cursor.execute(
                "UPDATE projet SET statut = %s WHERE id = %s", (statut, id,))
            connexion.commit()
    else:
        return "Erreur: Pas d'identifiant", 400
    return redirect(request.referrer)


@app.route("/addProject/", methods=['GET', 'POST'])
def projectList():
    postcode = None
    parcelles = None
    if request.method == "GET":
        postcode = request.args.get("code_postal")

    if postcode != None:
        if str(postcode).isdigit():
            cursor = connexion.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                "SELECT * FROM parcelle WHERE parcelle.code_postal = %s", (postcode,))
            parcelles = cursor.fetchall()
            return render_template("create_project.html", parcelles=parcelles, login=session.get('login'))

    if request.method == "POST":
        login = session.get('login')
        parcelle_id = request.form.get("parcelle_id")
        ca = request.form.get("ca")
        if login == None:
            return "Veuillez vous connecter", 401
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT NOW()),%s,'en cours', %s,%s);", (ca, parcelle_id, login,))
        connexion.commit()
    return render_template("ask_code.html")


@app.route("/addParcelle/", methods=['GET', 'POST'])
def createParcelle():
    selected = None
    if request.method == "POST":
        code_postal = request.form.get('code_postal')
        surface = request.form.get('surface')
        adresse = request.form.get('adresse')
        parcelle_id = request.form.get('parcelle_id')
        try:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM parcelle WHERE parcelle_id = %s", (parcelle_id,))
            if(len(cursor.fetchall()) != 0):
                return "Erreur, identifiant non unique", 400

            cursor.execute(
                "INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (%s, %s, %s, %s)", (parcelle_id, surface, adresse, code_postal,))
            connexion.commit()
        except Exception as e:
            return "Erreur, impossible d'insérer la nouvelle parcelle "+code_postal + ' '+surface+' '+adresse+' '+parcelle_id + ' (' + str(e) + ')', 400

    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM ville")
    villes = cursor.fetchall()
    if request.method == 'GET':
        selected = request.args.get('selected')
    return render_template("create_parcelle.html", villes=villes, selected=selected)


@app.route("/addVille/", methods=['GET', 'POST'])
def createVille():
    if request.method == "POST":
        code_postal = request.form.get('code_postal')
        nom = request.form.get('nom')
        try:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM ville WHERE code_postal = %s", (code_postal,))
            if(len(cursor.fetchall()) != 0):
                return "Erreur, code postal non unique", 400

            cursor.execute(
                "INSERT INTO ville (code_postal,nom) VALUES (%s, %s)", (code_postal, nom,))
            connexion.commit()
        except Exception as e:
            return "Erreur, impossible de créer la nouvelle ville"+code_postal + ' ' + nom + ' (' + str(e) + ')', 400

    return render_template("create_ville.html")


@app.route("/login")
def loginPage():
    cursor = connexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("login.html", users=users)


@app.route("/loginValidate", methods=['POST'])
def login():
    login = request.form['login']
    session['login'] = login
    return redirect("/")
