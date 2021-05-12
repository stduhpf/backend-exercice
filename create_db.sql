/*
Ccreation des tables de la base de données
*/

CREATE TABLE IF NOT EXISTS user(
    id      integer     CONSTRAINT pkuser PRIMARY KEY,
    name    varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS projet(
    id              integer     CONSTRAINT pkproject PRIMARY KEY,
    date_creation   date,
    chiffre_affaire integer,
    statut          varchar(10) CONSTRAINT statchk CHECK(statut = 'en cours' OR statut = 'terminé' OR statut = 'abandonné')
);

CREATE TABLE IF NOT EXISTS parcelle(
    id          integer     CONSTRAINT pkparcelle PRIMARY KEY,
    addresse    varchar(50),
    ville       varchar(50),
    codepostal  integer,
    surface     integer 
);