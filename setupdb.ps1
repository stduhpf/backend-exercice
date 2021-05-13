#Initialize la base de données
psql -h localhost -d buildrz -f create_db.sql
psql -h localhost -d buildrz -f functions.sql