"""
    GLOBALE=POSSIBILE UTILIZZO DA PARTE DI QUALUNQUE TABELLA

    SPECIFICO=DA USARE SOLO CON DETERMINATE TABELLE 
"""


GLOBALEselezionaTuttiPiatti='SELECT * FROM piatti'
GLOBALEselezionaTuttiPiatti2='SELECT p.* FROM piatti p JOIN utenti u ON p.id_utente = u.id_utente WHERE u.id_utente = <ID_UTENTE>;'

GLOBALEselezionaSoloUnPiatto='SELECT * FROM piatti WHERE IdPiatto=?'
GLOBALEselezionaSoloUnPiatto2='SELECT p.* FROM piatti p JOIN utenti u ON p.id_utente = u.id_utente WHERE u.id_utente = <ID_UTENTE> LIMIT 1;'


SPECIFICOselezionaColonnaMail='SELECT * FROM utenti WHERE mail=?'
SPECIFICOinserisciNuovoUtente='INSERT INTO utenti (nome, cognome, mail, compagnia, passwo) VALUES (?, ?, ?, ?, ?)'