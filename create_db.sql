/*
Ccreation des tables de la base de données
*/
SET client_encoding TO 'LATIN1';

DROP TABLE users    CASCADE;
DROP TABLE projet   CASCADE;
DROP TABLE parcelle CASCADE;
DROP TABLE ville    CASCADE;


CREATE TABLE IF NOT EXISTS users(
    name    varchar(40)     CONSTRAINT pkuser PRIMARY KEY
    /*
    possibilité d'ajouter des pass hashés
    */
);

CREATE TABLE IF NOT EXISTS ville(
    code_postal integer     CONSTRAINT pkVille PRIMARY KEY,
    nom         varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS parcelle(
    parcelle_id integer     CONSTRAINT pkparcelle PRIMARY KEY,
    adresse    varchar(50)  NOT NULL,
    code_postal    integer  NOT NULL,
    surface     integer,
    CONSTRAINT fk_ville  FOREIGN KEY(code_postal)    REFERENCES ville(code_postal)    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projet(
    id              serial     CONSTRAINT pkproject PRIMARY KEY,
    date_creation   date,
    chiffre_affaire integer ,
    statut          varchar(10) CONSTRAINT statchk CHECK(statut = 'en cours' OR statut = 'terminé' OR statut = 'abandonné'),
    parcelle_id     integer NOT NULL,
    username        varchar(40) NOT NULL,
    CONSTRAINT fk_parcelle  FOREIGN KEY(parcelle_id)    REFERENCES parcelle(parcelle_id)    ON DELETE CASCADE,
    CONSTRAINT fk_users     FOREIGN KEY(username)       REFERENCES users(name)                ON DELETE CASCADE
);


/* Valeurs de test*/
INSERT INTO users (name) VALUES ('toto');
INSERT INTO users (name) VALUES ('tata');

INSERT INTO ville (nom,code_postal) VALUES ('Montreuil',93100);
INSERT INTO ville (nom,code_postal) VALUES ('Paris',75000);

INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (42,452,'30 rue de Paris',(SELECT code_postal FROM ville WHERE ville.nom = 'Montreuil'));
INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (41,14000,'6 rue de la paix',(SELECT code_postal FROM ville WHERE ville.nom = 'Paris'));
INSERT INTO parcelle (parcelle_id,surface,adresse,code_postal) VALUES (96,698000,'51 rue de la Soif',(SELECT code_postal  FROM ville WHERE ville.nom = 'Montreuil'));

INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT make_date(2020, 07, 25)),69420,'en cours', 96,'toto');
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT make_date(2020, 08, 25)),2,'terminé', 42, 'tata');
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT make_date(2021, 07, 25)),100000,'en cours', 41, 'tata');
INSERT INTO projet (date_creation,chiffre_affaire,statut,parcelle_id,username) VALUES ((SELECT make_date(2020, 07, 20)),100052,'en cours', 41, 'toto');
