from flask import g, render_template
import sqlite3


class database:
    

    def db():
        DATABASE = 'piatti.db'
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db



    def visualizza_tutti_piatti(db, tabella, idUte):
        cursore=db.cursor()

        #cursore.execute(GLOBALEselezionaTuttiPiatti)
        if tabella=='piatti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE idUtente=?", (idUte,))
            piatti=cursore.fetchall()
        elif tabella=='ingredienti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE idUtente=?", (idUte,))
            piatti=cursore.fetchall()
        elif tabella=='utenti':
            cursore.execute(f"SELECT * FROM {tabella} WHERE id_utente=?", (idUte,))
            piatti=cursore.fetchone()


        return piatti

    

    def visualizza_un_piatto(nome):#passa il nome <hidden> in modo da ingrandire piatto in 1 pagina
        """db_ram=db_utenti()
        cursore=db_ram.cursor()

        cursore.execute(query2.GLOBALEselezionaSoloUnPiatto)
        piatto=cursore.fetchone()

        

        return piatto"""


    #------------------------------------------------------------------------


    def elimina_rigaPiatto(db_ram, id, tabella):
        """la funzione non apre il database perchè verrebbe già aperto dalla funzione
        db_utenti, quindi passo l'oggetto come parametro e lo utilizzo direttamente"""
    
        try:
            cursore=db_ram.cursor()

            if tabella=='piatti':
                cursore.execute(f"DELETE FROM {tabella} WHERE piattoId=?", (id,))
                db_ram.commit()
                
  
            elif tabella=='ingredienti':
                cursore.execute(f"DELETE FROM {tabella} WHERE ingredienteId=?", (id,))
                db_ram.commit()
                cursore.close()

            return True

        except Exception as e:
            print(e)
            return False



    def modifica_elemento(db_ram, idUtente, idSpecifico, tabella, colonna, nuovo):
        try:
            cursore=db_ram.cursor()

            if tabella=='piatti':#tabella: piatti, colonna: "nome", nuovo: "", idSpecifi: piattoId
                cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE piattoId=?", (nuovo, idSpecifico))
                db_ram.commit()
            
            elif tabella=='ingredienti':#tabella: ingredienti, colonna: "quella che vuoi", nuovo: "", idSpecifi: ingredienteId
               cursore.execute(f"UPDATE {tabella} SET {colonna}=? WHERE ingredienteId=?", (nuovo, idSpecifico))
               db_ram.commit() 

            return True

        except Exception as e:
            return False

        finally:
            cursore.close()
    #----------------------------------------------------------------------------


    def aggiungi_piatto(db_ram, tabella, idUte, nome, costo):
        try:
            cursore=db_ram.cursor()

            cursore.execute(f"INSERT INTO {tabella} (idUtente, nome, costo) VALUES (?, ?, ?)", (idUte, nome, costo ))
            db_ram.commit()
            

            return render_template("calcolaPrezzo.html")

        except Exception as e:
            return render_template("index.html")


    #---------------------------------------------------------------------------------

    def aggiungi_ingrediente(db, tabella, idUtente, idPiatto, nome, prezzoKg, quanti, costo):
        try:
            cursore = db.cursor()

            cursore.execute(f"INSERT INTO {tabella} (idUtente, idPiatto, nome, prezzoKg, quantita, costo) VALUES (?, ?, ?, ?, ?, ?)", (idUtente, idPiatto, nome, prezzoKg, quanti, costo))
            db.commit()
            

            return render_template("calcolaPrezzo.html")

        except Exception as e:
            print("Si è verificato un'errore:", e)
            return render_template("index.html")



    def cerca_corso(db, rif):
    
        cursore=db.cursor()

        cursore.execute("SELECT * FROM service WHERE id=?", (rif,))
        trovato=cursor.fetchone()
    

        return rif


    #---------------------------------------------------------------------------------

    def visualizza_carrello(db_ram, id, tabella):
        cursore=db_ram.cursor()

        cursore.execute(f"SELECT * FROM {tabella} WHERE id_uten={id}")
        carrello=cursore.fetchall()

        return carrello


    def idPiatto(db, tabella, nome, idUte):
        try:
            cursore = db.cursor()

            cursore.execute(f"SELECT * FROM {tabella} WHERE nome=? AND idUtente=?", (nome, idUte,))
            riga = cursore.fetchall()

            if riga:
                idPiatto = riga[0]
            else:
                idPiatto = None

            

            return idPiatto

        except Exception as e:
            print("Si è verificato un'errore:", e)



    def idIngre(db, tabella, nome, id):
        try:
            cursore = db.cursor()

            cursore.execute(f"SELECT * FROM {tabella} WHERE nome=? AND idUtente=?", (nome, id, ))
            riga = cursore.fetchall()

            if riga:
                idIngre = riga[0]
            else:
                idIngre = None

            

            return idIngre

        except Exception as e:
            print("Si è verificato un'errore:", e)
            


    
    def sommaCosti_ingredienti(db, tabella, idPiatto, idUte, nome):
        try:
            cursore = db.cursor()
            cursore.execute(f"SELECT * FROM {tabella} WHERE idPiatto=? AND idUtente=?", (idPiatto, idUte,))
            risultati = cursore.fetchall()

            tot = 0
            for riga in risultati:
                costo_ingrediente = riga[6]  # sesto elemento della tupla
                tot += float(costo_ingrediente)

            cursore.execute('UPDATE piatti SET costo=? WHERE piattoId=?', (tot, idPiatto))
            db.commit()
            return tot

        except Exception as e:
            print("Si è verificato un'errore:", e)
            return None
