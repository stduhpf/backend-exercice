from flask import Flask, render_template
import psycopg2 as pc2

connexion = pc2.connect("dbname=buildrz user=postgres password=stdRoot")
cursor = connexion.cursor()


app = Flask(__name__)


@app.route("/")
def main():
    cursor.execute("SELECT parcelle.addresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.ville = 'Montreuil';")
    res = cursor.fetchall()
    return render_template("template.html")
