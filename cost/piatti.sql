DROP TABLE IF EXISTS piatti;
DROP TABLE IF EXISTS ingredienti;
DROP TABLE IF EXISTS collegamenti;
DROP TABLE IF EXISTS utenti;

CREATE TABLE utenti
(
    id_utente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cognome TEXT,
    mail TEXT,
    compagnia TEXT,
    passwo VARCHAR[255] NOT NULL
);

CREATE TABLE piatti
(
	piattoId INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtente INT,
	nome VARCHAR(100),
    costo DECIMAL (10, 4)
);

CREATE TABLE ingredienti
(
    ingredienteId INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtente INT,
    idPiatto INT,
    nome VARCHAR(100),
    prezzoKg DECIMAL (10, 4),
	quantita DECIMAL (10, 4),
    costo DECIMAL(10, 3)
);

CREATE TABLE collegamenti
(   
    piattoId INT,
    ingredienteId INT,
    quantita DECIMAL(10, 4),
    FOREIGN KEY (piattoId) REFERENCES piatti(piattoId),
    FOREIGN KEY (ingredienteId) REFERENCES ingredienti(ingredienteId)
);

