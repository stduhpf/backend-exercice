SELECT parcelle.addresse, parcelle.surface, projet.date_creation, projet.chiffre_affaire FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.ville = 'Montreuil';

CREATE OR REPLACE FUNCTION somme_ca (v varchar, s varchar) RETURNS integer
LANGUAGE SQL
AS $$
SELECT SUM(projet.chiffre_affaire) FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.ville = v AND projet.statut = s
$$;

SELECT somme_ca('Montreuil','terminé');
SELECT somme_ca('Paris','en cours');