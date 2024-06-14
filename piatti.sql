DROP TABLE IF EXISTS piatti;
DROP TABLE IF EXISTS ingredienti;
DROP TABLE IF EXISTS collegamenti;
DROP TABLE IF EXISTS utenti;
DROP TABLE IF EXISTS magazzino;
DROP TABLE IF EXISTS oggetti;



CREATE TABLE utenti
(
    id_utente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cognome TEXT,
    mail TEXT,
    compagnia TEXT,
    passwo VARCHAR[255] NOT NULL
    /*
    tabella che racchiude gli utenti iscritti al servizio e i loro dati

    id dell'utente'
    nome utente
    cognome utente
    mail dell'utente'
    azienda per cui lavora
    password criptata con hash


*/
);

CREATE TABLE piatti
(
	piattoId INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtente INT,
	nome TEXT,
    costo DECIMAL (10, 4),
    prezzoVendita DECIMAL (10, 4),
    percentualeFoodCost DECIMAL (10, 4)
    /*
    tabella che racchiude i piatti composti da vari ingredienti ed oggetti, degli utenti iscritti al servizio

    id del piatto 
    id dell'utente
    nome del piatto'
    costo del piatto composto dalla somma di tutti gli ingredienti e gli oggetti che lo compongono
*/

);

CREATE TABLE ingredienti
(
    ingredienteId INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtente INT,
    idPiatto INT,
    nome TEXT,
    prezzoKg DECIMAL (10, 4),
    prezzo DECIMAL (10, 4),
	quantita DECIMAL (10, 4),
    costo DECIMAL(10, 3),
    magazzinoId INTEGER,
    descrizione TEXT,
    unitaDiMisura TEXT,
    quanti DECIMAL(5,3),
    codice TEXT,
    famiglia TEXT,
    sottoFamiglia TEXT,
    fornitore TEXT,
    codFornitore TEXT,
    ordineMinimo INT
    /*
    tabella ingredienti salva i dati degli articoli food e beverage inseriti dall'utente', tutti gli articoli segnano
    tra i dati i piatti in cui vengono utilizzati, il magazzino in cui sono stoccati ed altre informazioni utili a 
    elaborare dati utili al monitoraggio da parte dell'utente e risultati per calcoli come il food cost'

    id dell'ingrediente
    id dell'utente che lo utilizza
    id del piatto in cui   presente (NONE nel caso non fosse utilizzato in nessun piatto)
    nome dell'ingrediente
    prezzo al kg dell'ingrediente
    prezzo riferito all'unit  di misura'
    quantit  dell'ingrediente usata in un piatto
    costo della quantit  rispetto al prezzo al kg'
    id del magazzino in cui   stoccato
    descrizione libera (TEXT)
    unit  di misura adottata
    quantit  dell'ingrediente presente in magazzino
    codice del prodotto
    famiglia del prodotto
    sottofamiglia del prodotto
    fornitore del prodotto
    codice del fornitore
    ordine minimo necessario'

*/
);

CREATE TABLE oggetti
(
    oggettoId INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtente INT,
    idPiatto INT,
    nome TEXT,
    prezzo DECIMAL (10, 4),
	quantita DECIMAL (10, 4),
    costoQuantita DECIMAL(10, 3),
    magazzinoId INTEGER,
    descrizione TEXT,
    unitaDiMisura TEXT,
    quanti DECIMAL(5,3),
    codice TEXT,
    famiglia TEXT,
    sottoFamiglia TEXT,
    fornitore TEXT,
    codFornitore TEXT,
    ordineMinimo INT
    /*
    la tabella oggetti   sostanzialmente uguale a ingredienti solo che racchiude le attrezzature utilizzate dall'utente
    per la opreparazione di un piatto o comunque sostenere l'attivit  quindi piatti, spatole, prodotti delle pulizie ecc
    
    id dell'oggetto'
    id dell'utente
    id del piatto che utlizza l'oggetto
    nome dell'oggetto
    prezzo dell'oggetto
    quantit  dell'oggetto utilizzata per preparare un piatto
    costo della quantit  utilizzata in un piatto
    id del magazzino in cui si trova
    descrizione dell'articolo
    unit  di misura utilizza
    quantit  posseduta dell'oggetto
    codice dell'oggetto
    famiglia dell'oggetto FOOD-BEVERAGE-OBJECT'
    sottoFamiglia
    fornitore dell'oggetyto
    codice del fornitore
    ordine minimo'
*/
);

CREATE TABLE magazzino
(
    magazzinoId INTEGER PRIMARYKEY AUTORINCREMENT,
    idUtente INT,
    nome TEXT,
    descrizione TEXT,
    posizione TEXT,
    valore DECIMAL(5,3)
    /*
    la tabella magazzino racchiude le zone adibite di ogni utente, sarebbe possibile aggiungere le varie stanze, o impostarne
    1 sola di default, inoltre possiede la variabile valore che esprime appunto il valore della merce contennuta in un
    magazzino.

    id del magazzino
    id dell'utente che possiede il magazzino
    nome del magazzino
    descrizione del magazzino
    posizione del magazzino
    valore complessivo della merce presente'
*/
);


CREATE TABLE collegamenti
(   
    piattoId INT,
    ingredienteId INT,
    quantita DECIMAL(10, 4),
    FOREIGN KEY (piattoId) REFERENCES piatti(piattoId),
    FOREIGN KEY (ingredienteId) REFERENCES ingredienti(ingredienteId)
);

