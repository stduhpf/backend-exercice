# test psycopg2

import psycopg2

connexion = psycopg2.connect("dbname=buildrz user=postgres password=stdRoot")

cursor = connexion.cursor()

cursor.execute("SELECT parcelle.adresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = (SELECT code_postal  FROM ville WHERE ville.nom = 'Montreuil');")

res = cursor.fetchall()

print(res)
