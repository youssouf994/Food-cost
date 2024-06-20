#from crypt import methods
from tkinter.tix import INTEGER
from flask import Flask, render_template, request, session, redirect, url_for
from piatto import Piatto
from calcoli import Calcoli
from query import database
import query2
import bcrypt
import sqlite3
from functools import wraps



"""
    NOME APPLICAZIONE: SMART RESTOURANT
    
    SCOPO APPLICAZIONE: integrare in un'unica suite quanti più strumenti possibile tra calcolatore food cost,
                        gestione magazzino, visualizzazione giacienze in tempo reale,
                        
    CONTENUTO DEL FILE: route principali di accesso alle pagine e ai servizi delle applicazioni, sono presenti
                        tutte le funzioni di partenza dei vari eventi, potete trovare la spiegazione dettagliata
                        prima delle funzioni presenti sul file
                        
    FILE COLLEGATI:     
"""

app = Flask(__name__)
app.config['SECRET_KEY']='super_secret_key'
piattiUtente=[]

"""with app.app_context():
    dbIstanza=database()
    db=dbIstanza.db()"""


# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app 

#decoratore che impedisce le aperture di pagine che restituiscono dati sensibili senza login
def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'userId' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('crea_utente'))
    return wrapped_view

#ACCESSO AL PROGRAMMA ( vedi esecuzione del server in fondo alla pagina )
@app.route('/')
@app.route('/main')
def main():
   
  
    return render_template('index.html')    



"""
    la funzione ritorna tutti i valori necessari a mostrare una panoramica di tutti i piatti di cui l'utente
    ha voluto calcolare il food cost, in pratica raccoglie dati mirati a generare una dashboard
    
---------------------------------------------------------------------------------------------------------------

    @route calcola totale accetta richieste get e post
    @decoratore LOGIN RICHIESTO
    
    func()
        acquisizione database (vedi classe database nel file cartellaOrigine/query.py)
        acquisizione di tutti i piatti dell'utente passato come parametro
        acquisizione degli ingredienti che compongono i piatti raccolti in precedenza
        acquisizione delle info utente
        chiusura dell'oggetto database creato all'ingresso della route
        return
"""
@app.route('/calcolaTotale', methods=['POST', 'GET'])
@login_required
def calcolaTot():
    db=database.db()
    #idPiatto=database.idPiatto(db, 'piatti', session['userId'])
    #tot2=database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto, session['userId'])

    #(database, nome tabella db, id dell'utente nelle tabelle)
    #RACCOLTA DEI DATI RELATIVI ALL'UTENTE
    piattiUtente=database.visualizza_tutti_piatti(db, 'piatti', session['userId'])
    oggettiUtente=database.visualizza_tutti_piatti(db,'oggetti', session['userId'])
    ingredientiUtente=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    infoUtente=database.visualizza_tutti_piatti(db, 'utenti', session['userId'])
    
    db.close()
    return render_template('calcolaPrezzo.html', piattiUtente=piattiUtente, ingredientiUtente=ingredientiUtente, infoUtente=infoUtente, oggettiUtente=oggettiUtente)

"""
    INFO COMPLETE DI UN SOLO PIATTO SELEZIONATO DA CALCOLAPREZZO.HTML
    la funzione ritorna tutti i valori necessari a mostrare le specifiche di un piatto di cui l'utente
    ha voluto calcolare il food cost, in pratica raccoglie dati mirati a visualizzare dati come la lista
    di ingredienti che compongono un piatto, in che quantità sono presenti, quanto vale la quantità inserita,
    il prezzo al kg, 
    
---------------------------------------------------------------------------------------------------------------

    @route calcola totale accetta richieste get e post, e prende come parametro un intero. questo intero
        serve a tenere traccia del piatto cliccato nella pagina precedente.
        l'utente nella pagina precedente (calcolaPrezzo.html) aveva la carrellata di piatti, in base a quale link
        ha scelto il form nella pag html raccoglie il dato e lo reinvia tramite richiesta post nell'url.
        <int:idPiatto> è il passaggio di variabile da un contesto all'altro
        
    @decoratore LOGIN RICHIESTO
    
    func(idPiatto)
        acquisisco il db ( classe database presente in radice/query.py)
        acquisizione di un solo piatto utente (quello selezionato nella pag calcolaPrezzo.html)
        acquisizione informazioni sull'utente
        chiusura oggetto db
        return

"""
@app.route('/visualizzaDashboardPiatto/<int:idPiatto>', methods=['POST', 'GET'])
@login_required
def visualizzaDashboardPiatto(idPiatto):    
        db=database.db()
        #idPiatto=database.idPiatto(db, 'piatti', session['userId'])
        #tot2=database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto, session['userId'])

        #(db, nome tabella, id utente, id piatto)
        piattiUtente=database.visualizza_un_piatto(db, 'piatti', session['userId'], idPiatto)
    
        #(db, nome tabella, id utente)
        ingredientiUtente=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    
        #(db, nome tabella, id utente)
        infoUtente=database.visualizza_tutti_piatti(db, 'utenti', session['userId'])
        oggettiUtente=database.visualizza_tutti_piatti(db,'oggetti', session['userId'])
        percentualeFoodCost=piattiUtente[5]
            

    
        if request.method=='GET':
            db.close() #chiusura database
        
        elif request.method=='POST':
            prezzoVendita=(request.form.get('prezzoVendita'))
            
            prezzo=float(prezzoVendita)
            prezzo=round(prezzo, 3)
            
        
        
            database.aggiungi_prezzoVendita(db, 'piatti', prezzo, idPiatto)
        
            db.close()
        
        return render_template('infoComplete.html', oggettiUtente=oggettiUtente, ingredientiUtente=ingredientiUtente, infoUtente=infoUtente, piattiUtente=piattiUtente, percentualeFoodCost=percentualeFoodCost)

@app.route('/calcolaFoodCost/<int:idPiatto>', methods=['POST', 'GET'])
@login_required
def calcolaFoodCost(idPiatto):
    if request.method=='POST':
        db=database.db()
        
        piattiUtente=database.visualizza_un_piatto(db, 'piatti', session['userId'], idPiatto)
        
        prezzo=piattiUtente[4]
        sommaCostoIngredienti=database.sommaCosti(db, idPiatto, session['userId'])
        
        if (prezzo==0) or (sommaCostoIngredienti==0):
            percentualeFoodCost=0
            database.aggiungi_percentualeFoodCost(db, 'piatti', percentualeFoodCost, idPiatto)
        else:
            percentualeFoodCost=round(Calcoli.foodCostPIATTO(sommaCostoIngredienti, prezzo), 3)
            database.aggiungi_percentualeFoodCost(db, 'piatti', percentualeFoodCost, idPiatto)

        db.close()
        return redirect(url_for('visualizzaDashboardPiatto', idPiatto=idPiatto))
"""
    la funzione permette all'utente di aggiungere un nuovo piatto alla sua collezione
    
---------------------------------------------------------------------------------------------------------------

    @route /*nuovopiatto accetta metodi get e post
    
    @decoratore LOGIN RICHIESTO
    
    se la richiesta da parte del client è post
    aggiungi alla var nome il testo nel campo input nomePiatto
    
    salva in idU l'id dell'utente
    apri il db
    aggiungi il piatto nel db
    chiudi il db
    
    ritorna la funzione calcolaTot
"""

@app.route('/nuovoPiatto', methods=['POST', 'GET'])
@login_required
def nuovoPiatto():
    if request.method=='POST':
        nome=request.form.get('nomePiatto')
        
        """piatto1=Piatto()
        piatto1.setNome(nome)
        piattiUtente.append(piatto1)"""

        idU=session['userId']

        db=database.db()
        database.aggiungi_piatto(db, 'piatti', idU, nome, 0, 0)
        db.close()
    
    return redirect(url_for('calcolaTot'))
    #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente)



"""
    la funzione permette all'utente di aggiungere un nuovo ingrediente ad un piatto esistente
    
---------------------------------------------------------------------------------------------------------------

    @route /nuovoIngrediente accetta metodi get e post
    
    @decoratore LOGIN RICHIESTO
    
    se la richiesta da parte del client è post
    estrai i dati inviati dal form (nome del piatto, nome dell'ingrediente, prezzo al kg, quantità)
    calcola il costo totale dell'ingrediente in base alla quantità e al prezzo al kg
    salva l'ingrediente nel database associandolo al piatto specificato
    aggiorna il costo totale del piatto
    chiudi il db
    
    ritorna la funzione calcolaTot
"""

@app.route('/nuovoIngrediente/<int:strada>', methods=['POST', 'GET'])
@login_required
def aggiungiIngre(strada):
    try:
        db=database.db()
        if strada==0:
                nomePiatto=str(request.form.get('nomeP'))
                ingrediente=request.form.get('nomeAlimento')
                prezzoKg=float(request.form.get('prezzoAlKg'))
                quanti=float(request.form.get('quantita'))
                tot=0
                prezzo=round(Calcoli.prezzoGrammi(quanti, prezzoKg), 3)

                
                idPiatto=database.idPiatto(db, 'piatti', nomePiatto, session['userId'])
    
                database.aggiungi_ingrediente(db, 'ingredienti', session['userId'], idPiatto[0], ingrediente, prezzoKg, quanti, prezzo, None)
    
                database.sommaCosti(db, idPiatto[0], session['userId'])
                
  
                #piattiUtente=database.visualizza_tutti_piatti(db, 'piatti', session['userId'])
                #for piattoIdenti in piattiUtente:
                    #if piattoIdenti.getNome()==nomePiatto:
                      #  piattoIdenti.aggiungiIngrediente(ingrediente, prezzoKg, quanti)  
                        #break    
                    #tot=piattoIdenti.sommaCosti()
                #del db
  
        elif strada==1:
            
            nomePiatto=str(request.form.get('nomeP'))
            nomeOggetto=str(request.form.get('nomeOggetto'))
            costoOggetto=float(request.form.get('prezzoOggetto'))
            quanti=float(request.form.get('quantita'))
            stradaL2=request.form.get('prezzo')
            
            tot=0
            if stradaL2=='0':
                prezzo=Calcoli.prezzoGrammi(quanti, costoOggetto)
                udm='grammi'
            elif stradaL2=='1':
                prezzo=costoOggetto*quanti
                prezzo=round(prezzo, 3)
                udm='pezzi'

            idPiatto=database.idPiatto(db, 'piatti', nomePiatto, session['userId'])
            
    
            database.aggiungi_ingrediente(db, 'oggetti', session['userId'], idPiatto[0], nomeOggetto, costoOggetto, quanti, prezzo, udm)
            
            #idOggetto=database.idPiatto(db, 'oggetti', nomeOggetto, session['userId'])
            database.sommaCosti(db, idPiatto[0], session['userId'])
        

    except  Exception as e:
        return render_template("errore.html", e=e)
    
    finally:
        db.close()
        idPiatto=int(idPiatto[0])
        return redirect(url_for('visualizzaDashboardPiatto', idPiatto=idPiatto))
        #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente, tot2=tot2)
        
    

"""
    la funzione permette all'utente di modificare un piatto o un ingrediente esistente
    
---------------------------------------------------------------------------------------------------------------

    @route /modifica/<int:sel>/<int:idP>/<int:selCol> accetta metodi get e post
    
    @decoratore LOGIN RICHIESTO
    
    se la richiesta da parte del client è post
    estrai i dati inviati dal form (nome del piatto, nuovo valore)
    seleziona la colonna del database da modificare in base ai parametri della route
    aggiorna il valore nel database
    se l'elemento modificato è un ingrediente, ricalcola il costo totale dell'ingrediente
    chiudi il db
    
    ritorna la funzione calcolaTot
"""
    
@app.route('/modifica/<int:sel>/<int:idP>/<int:selCol>/<int:idE>/<string:udm>', methods=['POST', 'GET'])
@login_required
def modifica(sel, idP, selCol, idE, udm):
    colonne=['nome', 'prezzoKg', 'quantita', 'costo', 'prezzo']
    
    if request.method=='POST': 
        nuovo=request.form.get('nuovo')
        db=database.db()

        if sel==1:
            
            database.modifica_elemento(db, session['userId'], idP, 'piatti', colonne[0], nuovo)
        

        elif sel==2:
            #nuovo=request.form.get('ingre') da eliminare
            database.modifica_elemento(db, session['userId'], idE, 'ingredienti', colonne[selCol], nuovo)
            elemento=database.visualizza_un_piatto(db, 'ingredienti', session['userId'], idE)
            nuovo=Calcoli.prezzoGrammi(float(elemento[6]), float(elemento[4]))
            database.modifica_elemento(db, session['userId'], idE, 'ingredienti', colonne[3], nuovo)
            database.sommaCosti(db, idP, session['userId'])
            
        elif sel==3:
            database.modifica_elemento(db, session['userId'], idE, 'oggetti', colonne[selCol], nuovo)
        
        elif sel==4:
            database.modifica_elemento(db, session['userId'], idE, 'oggetti', colonne[selCol], nuovo)
            elemento=database.visualizza_un_piatto(db, 'oggetti', session['userId'], idE)
            quanti=float(elemento[5])
            nuovo=float(nuovo)
            if udm=='grammi':
                nuovo=Calcoli.prezzoGrammi(quanti, nuovo)
            elif udm=='pezzi':
                nuovo*=quanti
            elif udm=='no':
                return

            database.modifica_elemento(db, session['userId'], idE, 'oggetti', 'costoQuantita', nuovo)
            database.sommaCosti(db, idP, session['userId'])
            
        elif sel==5:
            database.modifica_elemento(db, session['userId'], idE, 'oggetti', colonne[selCol], nuovo)
            elemento=database.visualizza_un_piatto(db, 'oggetti', session['userId'], idE)
            prezzo=float(elemento[4])
            nuovo=float(nuovo)
            if udm=='grammi':
                nuovo=Calcoli.prezzoGrammi(nuovo, prezzo)
            elif udm=='pezzi':
                nuovo*=prezzo
            elif udm=='no':
                return

            database.modifica_elemento(db, session['userId'], idE, 'oggetti', 'costoQuantita', nuovo)
            database.sommaCosti(db, idP, session['userId'])
            

        #piatto.setNome(nome)    
        #da aggiungere modifica specifica ad un solo oggetto dell'array
        #for a in piattiUtente:
        #    nome.append(piatto.getNome())

        db.close()

    return redirect(url_for('calcolaTot'))


"""
    la funzione permette all'utente di cancellare un piatto esistente
    
---------------------------------------------------------------------------------------------------------------

    @route /cancellaX accetta metodi get e post
    
    @decoratore LOGIN RICHIESTO
    
    estrai il nome del piatto da cancellare dal form
    apri il db
    trova l'id del piatto
    elimina tutti gli ingredienti associati al piatto
    elimina il piatto
    chiudi il db
    
    ritorna la funzione calcolaTot
"""

@app.route('/cancellaX', methods=['GET', 'POST'])
@login_required
def cancellaPiatto():
    nome=request.form.get('nomeP')

    db=database.db()
    idPia=database.idPiatto(db, 'piatti', nome, session['userId'])

    ingreElimina=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    oggetElimina=database.visualizza_tutti_piatti(db, 'oggetti', session['userId'])
    
    for e in ingreElimina:
        if e[2] ==idPia[0]:
            database.elimina_rigaPiatto(db, idPia[0], 'ingredientiForzata')
            
    for e in oggetElimina:
        if e[2] ==idPia[0]:
            database.elimina_rigaPiatto(db, idPia[0], 'oggettiForzata')

    database.elimina_rigaPiatto(db, idPia[0], 'piatti')
    db.close()
    return redirect(url_for('calcolaTot'))


"""
    la funzione permette all'utente di cancellare un ingrediente esistente
    
---------------------------------------------------------------------------------------------------------------

    @route /cancellaXy accetta metodi get e post
    
    @decoratore LOGIN RICHIESTO
    
    estrai il nome dell'ingrediente da cancellare dal form
    apri il db
    trova l'id dell'ingrediente
    elimina l'ingrediente
    aggiorna il costo totale del piatto a cui l'ingrediente era associato
    chiudi il db
    
    ritorna la funzione calcolaTot
"""
@app.route('/cancellaXy/<int:strada>', methods=['GET', 'POST'])
@login_required
def cancellaIngre(strada):
    nome=request.form.get('nomeI')

    db=database.db()
    
    if strada==0:
        idIngre=database.idIngre(db, 'ingredienti', nome, session['userId'])
        idP=idIngre[2]
        
        daSottrarre=int(idIngre[7])
        database.elimina_rigaPiatto(db, idIngre[0], 'ingredienti')
        database.sommaCosti(db, idP, session['userId'])
    elif strada==1:
        idOggetto=database.idIngre(db, 'oggetti', nome, session['userId'])
        idP=idOggetto[2]
        database.elimina_rigaPiatto(db, idOggetto[0], 'oggetti')
        database.sommaCosti(db, idP, session['userId'])

    db.close()
    return redirect(url_for('calcolaTot'))

"""
    la funzione permette all'utente di registrarsi al sistema
    
---------------------------------------------------------------------------------------------------------------

    @route /registrazione accetta metodi get e post
    
    se la richiesta da parte del client è post
    estrai i dati inviati dal form (nome, cognome, azienda, mail, password)
    controlla se l'email esiste già nel database
    se esiste, reindirizza alla pagina principale
    se non esiste, codifica la password e salva il nuovo utente nel database
    chiudi il db
    
    ritorna la pagina di login
"""
@app.route('/registrazione', methods=['POST', 'GET'])
def crea_utente():
    if request.method=='POST':
        nome=request.form['nome']
        cognome=request.form['cognome']
        azienda=request.form['azienda']
        mail=request.form['mail']
        passw=request.form['pass']

        db=database.db()
        cursore=db.cursor()


        cursore.execute(query2.SPECIFICOselezionaColonnaMail, (mail,))
        if cursore.fetchone() is not None:
           return redirect(url_for('main'))
        else:
            #-----------CODIFICA VALORI INSERITI--------------
            pass_codificata=bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
            #-----------------------------------------------------------

            cursore.execute(query2.SPECIFICOinserisciNuovoUtente,
                            (nome, cognome, mail, azienda, pass_codificata ))
            
            db.commit()
            db.close()

            return render_template('index.html')

    return render_template('registrazione.html')

"""
    la funzione permette all'utente di effettuare il login
    
---------------------------------------------------------------------------------------------------------------

    @route /login accetta metodi get e post
    
    se la richiesta da parte del client è post
    estrai i dati inviati dal form (utente, password)
    controlla se l'utente esiste nel database e verifica la password
    se corretto, salva l'id utente nella sessione e reindirizza alla dashboard
    se errato, reindirizza alla pagina principale
"""
@app.route('/login', methods=['POST', 'GET'])
def accesso():
    trovato_nome=None
    if request.method=='POST':
        utente=request.form['user']
        passwd=request.form['pass'].encode('UTF-8')

        
        db=database.db()
        cursore=db.cursor()

        cursore.execute(query2.SPECIFICOselezionaColonnaMail, (utente,))
        trovato_nome=cursore.fetchone()
        
        db.close()
        

    if trovato_nome is not None and bcrypt.checkpw(passwd, trovato_nome[5]):
        session['userId']=trovato_nome[0]      
        return redirect(url_for('calcolaTot'))
           
    else:
        trovato_nome=None
        return redirect(url_for('main'))        


"""
    la funzione permette all'utente di effettuare il logout
    
---------------------------------------------------------------------------------------------------------------

    @route /logout
    
    rimuove l'id utente dalla sessione
    reindirizza alla pagina principale
"""

@app.route('/magazzino', methods=['POST', 'GET'])
def dashboardMagazzino():

    db=database.db()
    infoUtente=database.visualizza_tutti_piatti(db, 'utenti', session['userId'])

    return render_template('giacienzeMagazzino.html', infoUtente=infoUtente)

@app.route('/magazzino', methods=['POST'])
def aggiungiArticoloMagazzino():
    idUtente=session['idUtente']
    nome=request.form.get('nome')
    prezzoKg=float(request.form.get('prezzoKg')) 
    prezzo=float(request.form.get('prezzo')) 
    magazzinoId=int(request.form.get('magazzinoId'))
    descrizione=request.form.get('descrizione') 
    unitaDiMisura=request.form.get('unita') 
    quanti=float(request.form.get('quantita')) 
    codice=request.form.get('cod') 
    famiglia=request.form.get('famiglia')
    sottoFamiglia=request.form.get('sottoFam') 
    fornitore=request.form.get('fornitore') 
    codFornitore=request.form.get('codFornitore') 
    ordineMinimo=int(request.form.get('ordineMin')) 
    
    db=database.db()
    
    return redirect(url_for('dashboardMagazzino'))

@app.route('/logout')
def logOut():
    session.pop('userId', None)
    return redirect(url_for('main'))


if __name__ == "__main__":
    # Run the app server on localhost:4449
    app.run(host='0.0.0.0', port=4449)


