/*
Ccreation des tables de la base de données
*/
SET client_encoding TO 'LATIN1';

DROP TABLE users    CASCADE;
DROP TABLE projet   CASCADE;
DROP TABLE parcelle CASCADE;
DROP TABLE ville    CASCADE;


CREATE TABLE IF NOT EXISTS users(
    id      serial     CONSTRAINT pkuser PRIMARY KEY,
    name    varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS ville(
    code_postal integer     CONSTRAINT pkVille PRIMARY KEY,
    nom         varchar(50)
);

CREATE TABLE IF NOT EXISTS parcelle(
    parcelle_id integer     CONSTRAINT pkparcelle PRIMARY KEY,
    adresse    varchar(50),
    code_postal    integer,
    surface     integer,
    CONSTRAINT fk_ville  FOREIGN KEY(code_postal)    REFERENCES ville(code_postal)    ON DELETE CASCADE
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

INSERT INTO ville (nom,code_postal) VALUES ('Montreuil',75048);
INSERT INTO ville (nom,code_postal) VALUES ('Paris',75000);

INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (42,12000,'5 rue des Pins',(SELECT code_postal FROM ville WHERE ville.nom = 'Montreuil'));
INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (41,14000,'6 rue des Arbres',(SELECT code_postal FROM ville WHERE ville.nom = 'Paris'));
INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (98,698000,'51 rue de la Soif',(SELECT code_postal  FROM ville WHERE ville.nom = 'Montreuil'));

INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 07, 25)),69420,'en cours', 98, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'toto'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 08, 25)),2,'terminé', 42, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2021, 07, 25)),100000,'en cours', 41, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,users_id) VALUES ((SELECT make_date(2020, 07, 20)),100052,'en cours', 41, (SELECT FIRST_VALUE(id) OVER() FROM users WHERE users.name = 'tata'));
