#Initialise la base de données
psql -h localhost -d buildrz -f sql/create_db.sql
psql -h localhost -d buildrz -f sql/functions.sql