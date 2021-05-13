from flask import Flask, render_template, request, redirect
from flask.helpers import flash
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
                return "Erreur: il est interdit de change le statut de " + res + " a " + statut
            cursor.execute(
                "UPDATE projet SET statut = %s WHERE id = %s", (statut, id,))
            connexion.commit()
    else:
        return "Erreur: Pas d'identifiant"
    return redirect(request.referrer)
