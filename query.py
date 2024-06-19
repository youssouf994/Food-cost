from flask import g, render_template
import sqlite3

class database:
    """
    Classe per la gestione del database dell'applicazione.
    """

    @staticmethod
    def db():
        """
        Funzione per ottenere la connessione al database SQLite.
        Se la connessione non esiste, viene creata e memorizzata nell'oggetto globale g.

        Returns:
            db (sqlite3.Connection): Connessione al database.
        """
        DATABASE = 'piatti.db'
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    @staticmethod
    def visualizza_tutti_piatti(db, tabella, idUte):
        """
        Funzione per visualizzare tutti i piatti, ingredienti o utenti dal database per un determinato utente.

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella da cui selezionare i dati.
            idUte (int): ID dell'utente.

        Returns:
            list: Lista dei risultati della query.
        """
        cursore = db.cursor()

        if tabella == 'piatti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE idUtente=?", (idUte,))
            piatti = cursore.fetchall()
        elif tabella == 'ingredienti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE idUtente=?", (idUte,))
            piatti = cursore.fetchall()
        elif tabella == 'utenti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE id_utente=?", (idUte,))
            piatti = cursore.fetchone()
        elif tabella=='oggetti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE idUtente=?", (idUte,))
            piatti = cursore.fetchall()
            

        return piatti

    @staticmethod
    def visualizza_un_piatto(db, tabella, idUte, idEle):
        """
        Funzione per visualizzare un singolo piatto o ingrediente dal database per un determinato utente.

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella da cui selezionare i dati.
            idUte (int): ID dell'utente.
            idEle (int): ID dell'elemento (piatto o ingrediente).

        Returns:
            tuple: Dati dell'elemento selezionato.
        """
        cursore = db.cursor()

        if tabella == 'piatti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE piattoId=?", (idEle,))
            elemento = cursore.fetchone()
        elif tabella == 'ingredienti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE ingredienteId=?", (idEle,))
            elemento = cursore.fetchone()
        elif tabella == 'utenti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE id_utente=?", (idUte,))
            elemento = cursore.fetchone()
        elif tabella=='oggetti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE oggettoId=?", (idEle,))
            elemento = cursore.fetchone()

        return elemento

    @staticmethod
    def elimina_rigaPiatto(db_ram, id, tabella):
        """
        Funzione per eliminare una riga da una tabella del database.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            id (int): ID dell'elemento da eliminare.
            tabella (str): Nome della tabella da cui eliminare l'elemento.

        Returns:
            bool: True se l'operazione ha avuto successo, altrimenti False.
        """
        try:
            cursore = db_ram.cursor()

            if tabella == 'piatti':
                cursore.execute(f"DELETE FROM {tabella} WHERE piattoId=?", (id,))
                db_ram.commit()
            elif tabella == 'ingredienti':
                cursore.execute(f"DELETE FROM {tabella} WHERE ingredienteId=?", (id,))
                db_ram.commit()
                cursore.close()
            elif tabella == 'ingredientiForzata':
                tabella = 'ingredienti'
                cursore.execute(f"DELETE FROM {tabella} WHERE idPiatto=?", (id,))
                db_ram.commit()
                cursore.close()

            return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def modifica_elemento(db_ram, idUtente, idSpecifico, tabella, colonna, nuovo):
        """
        Funzione per modificare un elemento in una tabella del database.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            idUtente (int): ID dell'utente.
            idSpecifico (int): ID dell'elemento da modificare.
            tabella (str): Nome della tabella in cui si trova l'elemento.
            colonna (str): Nome della colonna da modificare.
            nuovo (str): Nuovo valore per la colonna.

        Returns:
            bool: True se l'operazione ha avuto successo, altrimenti False.
        """
        try:
            cursore = db_ram.cursor()

            if tabella == 'piatti':
                cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE piattoId=?", (nuovo, idSpecifico))
                db_ram.commit()
            elif tabella == 'ingredienti':
                cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE ingredienteId=?", (nuovo, idSpecifico))
                db_ram.commit()
            elif tabella=='oggetti':
                cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE oggettoId=?", (nuovo, idSpecifico))
                db_ram.commit()

            

        except Exception as e:
            return False

        finally:
            cursore.close()
            return True

    @staticmethod
    def aggiungi_piatto(db_ram, tabella, idUte, nome, costo, prezzoVendita):
        """
        Funzione per aggiungere un nuovo piatto al database.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella in cui inserire il nuovo piatto.
            idUte (int): ID dell'utente.
            nome (str): Nome del nuovo piatto.
            costo (float): Costo del nuovo piatto.

        Returns:
            None
        """
        try:
            cursore = db_ram.cursor()
            cursore.execute(f"INSERT INTO {tabella} (idUtente, nome, costo, prezzoVendita) VALUES (?, ?, ?, ?)", (idUte, nome, costo, prezzoVendita))
            db_ram.commit()
        except Exception as e:
            return render_template("errore.html")
        
    @staticmethod
    def aggiungi_prezzoVendita(db_ram, tabella, prezzoVendita, idPiatto):
        colonna='prezzoVendita'
        """
        Funzione per aggiungere un nuovo piatto al database.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella in cui inserire il nuovo piatto.
            idUte (int): ID dell'utente.
            nome (str): Nome del nuovo piatto.
            costo (float): Costo del nuovo piatto.

        Returns:
            None
        """
        try:
            cursore = db_ram.cursor()
            cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE piattoId=?", (prezzoVendita, idPiatto))
            db_ram.commit()
        except Exception as e:
            return render_template("errore.html")
        

    @staticmethod
    def aggiungi_percentualeFoodCost(db_ram, tabella, percentuale, idPiatto):
        colonna='percentualeFoodCost'
        """
        Funzione per aggiungere un nuovo piatto al database.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella in cui inserire il nuovo piatto.
            idUte (int): ID dell'utente.
            nome (str): Nome del nuovo piatto.
            costo (float): Costo del nuovo piatto.

        Returns:
            None
        """
        try:
            cursore = db_ram.cursor()
            cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE piattoId=?", (percentuale, idPiatto))
            db_ram.commit()
        except Exception as e:
            return render_template("errore.html")
        


    @staticmethod
    def aggiungi_ingrediente(db, tabella, idUtente, idPiatto, nome, prezzoKg, quanti, costo, udm):
        """
        Funzione per aggiungere un nuovo ingrediente al database (UTILE AL CALCOLO DEL COSTO PIATTO)

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella in cui inserire il nuovo ingrediente.
            idUtente (int): ID dell'utente.
            idPiatto (int): ID del piatto a cui aggiungere l'ingrediente.
            nome (str): Nome del nuovo ingrediente.
            prezzoKg (float): Prezzo al kg del nuovo ingrediente.
            quanti (float): Quantità del nuovo ingrediente.
            costo (float): Costo totale del nuovo ingrediente.

        Returns:
            None
        """
        
        if tabella=='ingredienti':
            try:
                cursore = db.cursor()
                cursore.execute(f"INSERT INTO {tabella} (idUtente, idPiatto, nome, prezzoKg, quantita, costo) VALUES (?, ?, ?, ?, ?, ?)", (idUtente, idPiatto, nome, prezzoKg, quanti, costo))
                db.commit()
            except Exception as e:
                print("Si è verificato un errore:", e)
                return render_template("index.html")
            
        elif tabella=='oggetti':
            try:
                cursore = db.cursor()
                cursore.execute(f"INSERT INTO {tabella} (idUtente, idPiatto, nome, prezzo, quantita, costoQuantita, unitaDiMisura) VALUES (?, ?, ?, ?, ?, ?, ?)", (idUtente, idPiatto, nome, prezzoKg, quanti, costo, udm))
                db.commit()
            except Exception as e:
                print("Si è verificato un errore:", e)
                return render_template("index.html")
        
    @staticmethod
    def aggiungi_ingrediente2(db, tabella, idUtente, nome, prezzoKg, quanti, costo):
        """
        Funzione per aggiungere un nuovo ingrediente al database (UTILE AL CALCOLO DEL COSTO PIATTO)

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella in cui inserire il nuovo ingrediente.
            idUtente (int): ID dell'utente.
            idPiatto (int): ID del piatto a cui aggiungere l'ingrediente.
            nome (str): Nome del nuovo ingrediente.
            prezzoKg (float): Prezzo al kg del nuovo ingrediente.
            quanti (float): Quantità del nuovo ingrediente.
            costo (float): Costo totale del nuovo ingrediente.

        Returns:
            None
        """
        try:
            cursore = db.cursor()
            cursore.execute(f"INSERT INTO {tabella} (idUtente, idPiatto, nome, prezzoKg, quantita, costo) VALUES (?, ?, ?, ?, ?, ?)", (idUtente,  nome, prezzoKg, quanti, costo))
            db.commit()
        except Exception as e:
            print("Si è verificato un errore:", e)
            return render_template("index.html")

    @staticmethod
    def cerca_corso(db, rif):
        """
        Funzione per cercare un corso nel database.

        Args:
            db (sqlite3.Connection): Connessione al database.
            rif (int): ID del corso da cercare.

        Returns:
            rif (int): ID del corso trovato.
        """
        cursore = db.cursor()
        cursore.execute("SELECT * FROM service WHERE id=?", (rif,))
        trovato = cursore.fetchone()
        return rif

    @staticmethod
    def visualizza_carrello(db_ram, id, tabella):
        """
        Funzione per visualizzare il carrello dell'utente.

        Args:
            db_ram (sqlite3.Connection): Connessione al database.
            id (int): ID dell'utente.
            tabella (str): Nome della tabella da cui selezionare i dati.

        Returns:
            list: Lista dei risultati della query.
        """
        cursore = db_ram.cursor()
        cursore.execute(f"SELECT * FROM {tabella} WHERE id_uten={id}")
        carrello = cursore.fetchall()
        return carrello

    @staticmethod
    def idPiatto(db, tabella, nome, idUte):
        """
        Funzione per ottenere l'ID di un piatto nel database.

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella da cui selezionare i dati.
            nome (str): Nome del piatto.
            idUte (int): ID dell'utente.

        Returns:
            tuple: ID del piatto se trovato, altrimenti None.
        """
        
        try:
            cursore = db.cursor()
            cursore.execute(f"SELECT * FROM {tabella} WHERE nome=? AND idUtente=?", (nome, idUte))
            riga = cursore.fetchall()

            if riga:
                idPiatto = riga[0]
            else:
                idPiatto = None

            return idPiatto

        except Exception as e:
            print("Si è verificato un errore:", e)
        

    @staticmethod
    def idIngre(db, tabella, nome, id):
        """
        Funzione per ottenere l'ID di un ingrediente nel database.

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella da cui selezionare i dati.
            nome (str): Nome dell'ingrediente.
            id (int): ID dell'utente.

        Returns:
            tuple: ID dell'ingrediente se trovato, altrimenti None.
        """
        try:
            cursore = db.cursor()
            cursore.execute(f"SELECT * FROM {tabella} WHERE nome=? AND idUtente=?", (nome, id))
            riga = cursore.fetchall()

            if riga:
                idIngre = riga[0]
            else:
                idIngre = None

            return idIngre

        except Exception as e:
            print("Si è verificato un errore:", e)

    @staticmethod
    def sommaCosti_ingredienti(db, tabella, idPiatto, idUte, idOggetto):
        """
        Funzione per calcolare la somma dei costi degli ingredienti di un piatto e aggiornare il costo totale nel database.

        Args:
            db (sqlite3.Connection): Connessione al database.
            tabella (str): Nome della tabella da cui selezionare i dati.
            idPiatto (int): ID del piatto.
            idUte (int): ID dell'utente.
            
            tot_arrotondato (float): arrotondo il risultato
            aggiorno la colonna costo della tabella PIATTI in corrispondenza di piatto Id
            
        Returns:
            float: Totale dei costi degli ingredienti arrotondato a 3 decimali.
        """
        try:
            if tabella=='ingredienti':
                cursore = db.cursor()
                cursore.execute(f"SELECT * FROM {tabella} WHERE idPiatto=? AND idUtente=?", (idPiatto, idUte))
                risultati = cursore.fetchall()
            
                tot = 0
                for riga in risultati:
                    costo_ingrediente = riga[7]  # sesto elemento della tupla
                    tot += float(costo_ingrediente)
                    totArrotondato=round(tot, 3)

            elif tabella=='oggetti':
                cursore = db.cursor()
                cursore.execute(f"SELECT * FROM {tabella} WHERE oggettoId=? AND idUtente=?", (idOggetto, idUte))
                risultati = cursore.fetchall()
            
                tot = 0
                for riga in risultati:
                    costo_ingrediente = riga[6]  # sesto elemento della tupla
                    tot += float(costo_ingrediente)
                    totArrotondato=round(tot, 3)
 
            if tabella=='ingredienti':
                cursore.execute('UPDATE piatti SET costo=? WHERE piattoId=?', (totArrotondato, idPiatto))                
            elif tabella=='oggetti':
                tabella='piatti'
                cursore.execute(f"SELECT * FROM {tabella} WHERE piattoId=?", (idPiatto,))
                elemento = cursore.fetchone()
                tot_piatto=float(elemento[3])
                totArrotondato+=tot_piatto
                
                cursore.execute('UPDATE piatti SET costo=? WHERE piattoId=?', (totArrotondato, idPiatto))
                
            db.commit()
            return totArrotondato

        except Exception as e:
            print("Si è verificato un errore:", e)
            return None
