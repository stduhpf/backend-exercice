/*
Ccreation des tables de la base de données
*/

DROP TABLE users    CASCADE;
DROP TABLE projet   CASCADE;
DROP TABLE parcelle CASCADE;


CREATE TABLE IF NOT EXISTS users(
    id      serial     CONSTRAINT pkuser PRIMARY KEY,
    name    varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS parcelle(
    parcelle_id integer     CONSTRAINT pkparcelle PRIMARY KEY,
    addresse    varchar(50),
    ville       varchar(50),
    surface     integer 
);

CREATE TABLE IF NOT EXISTS projet(
    id              serial     CONSTRAINT pkproject PRIMARY KEY,
    date_creation   date,
    chiffre_affaire integer,
    statut          varchar(10) CONSTRAINT statchk CHECK(statut = 'en cours' OR statut = 'terminé' OR statut = 'abandonné'),
    parcelle_id     integer,
    users_id        integer,
    CONSTRAINT fk_parcelle  FOREIGN KEY(parcelle_id)    REFERENCES parcelle(parcelle_id)    ON DELETE CASCADE,
    CONSTRAINT fk_users     FOREIGN KEY(users_id)       REFERENCES users(id)                ON DELETE CASCADE
);


/* Valeurs de test*/
INSERT INTO users (name) VALUES ('toto');
INSERT INTO users (name) VALUES ('tata');

INSERT INTO parcelle (parcelle_id,surface,addresse,ville) VALUES (42,12000,'5 rue des Pins','Montreuil');
INSERT INTO parcelle (parcelle_id,surface,addresse,ville) VALUES (41,14000,'6 rue des Arbres','Paris');
INSERT INTO parcelle (parcelle_id,surface,addresse,ville) VALUES (98,698000,'51 rue de la Soif','Montreuil');

INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 07, 25)),69420,'en cours', 98, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'toto'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 08, 25)),2,'terminé', 42, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2021, 07, 25)),100000,'en cours', 41, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 07, 20)),100052,'en cours', 41, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
