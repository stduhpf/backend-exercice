DROP FUNCTION somme;

CREATE OR REPLACE FUNCTION somme (cp integer, s varchar) RETURNS integer
LANGUAGE SQL
AS $$
    SELECT SUM(projet.chiffre_affaire) FROM projet INNER JOIN parcelle ON parcelle.parcelle_id = projet.parcelle_id WHERE parcelle.code_postal = cp AND projet.statut = s
$$;
