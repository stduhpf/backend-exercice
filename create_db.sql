/*
Ccreation des tables de la base de données
*/

DROP TABLE users;
DROP TABLE projet;
DROP TABLE parcelle;


CREATE TABLE IF NOT EXISTS users(
    id      serial     CONSTRAINT pkuser PRIMARY KEY,
    name    varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS parcelle(
    id          integer     CONSTRAINT pkparcelle PRIMARY KEY,
    addresse    varchar(50),
    ville       varchar(50),
    codepostal  integer,
    surface     integer 
);

CREATE TABLE IF NOT EXISTS projet(
    id              serial     CONSTRAINT pkproject PRIMARY KEY,
    date_creation   date,
    chiffre_affaire integer,
    statut          varchar(10) CONSTRAINT statchk CHECK(statut = 'en cours' OR statut = 'terminé' OR statut = 'abandonné'),
    parcelle_id     integer,
    users_id        integer,
    CONSTRAINT fk_parcelle  FOREIGN KEY(parcelle_id)    REFERENCES parcelle(id),
    CONSTRAINT fk_users     FOREIGN KEY(users_id)       REFERENCES users(id)
);