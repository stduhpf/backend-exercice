from flask import Flask, render_template, request
from flask.helpers import flash
import psycopg2 as pc2

connexion = pc2.connect("dbname=buildrz user=postgres password=stdRoot")
cursor = connexion.cursor()


app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    if request.method == "GET":
        return (request.args.get("code_postal"))

    cursor.execute("SELECT parcelle.addresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.ville = 'Montreuil';")
    res = cursor.fetchall()

    cursor.execute("SELECT somme_ca('Paris','en cours');")
    somme = cursor.fetchall()[0][0]

    return render_template("template.html", res=res, somme=somme)
