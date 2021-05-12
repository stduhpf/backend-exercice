import psycopg2 as pc2

connexion = pc2.connect("dbname=buildrz user=postgres password=stdRoot")

cursor = connexion.cursor()

cursor.execute("SELECT parcelle.addresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = (SELECT code_postal  FROM ville WHERE ville.nom = 'Montreuil');")

res = cursor.fetchall()

print(res)
