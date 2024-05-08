"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from cmath import log
from flask import Flask, render_template, request, session, redirect, url_for
from piatto import Piatto
from calcoli import Calcoli
from query import database
import query2
import bcrypt
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='super_secret_key'
piattiUtente=[]

"""with app.app_context():
    dbIstanza=database()
    db=dbIstanza.db()"""


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
@app.route('/main')
def main():
    """Renders a sample page."""
  
    return render_template('index.html')    

@app.route('/login')
def login():
    
    return render_template('login.html') 

@app.route('/calcolaTotale', methods=['POST', 'GET'])
def calcolaTot():
    db=database.db()
    #idPiatto=database.idPiatto(db, 'piatti', session['userId'])
    #tot2=database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto, session['userId'])

    piattiUtente=database.visualizza_tutti_piatti(db, 'piatti', session['userId'])
    ingredientiUtente=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    infoUtente=database.visualizza_tutti_piatti(db, 'utenti', session['userId'])
    db.close()
    return render_template('calcolaPrezzo.html', piattiUtente=piattiUtente, ingredientiUtente=ingredientiUtente, infoUtente=infoUtente)


@app.route('/visualizzaDashboardPiatto/<int:idPiatto>', methods=['POST', 'GET'])
def visualizzaDashboardPiatto(idPiatto):
    db=database.db()
    #idPiatto=database.idPiatto(db, 'piatti', session['userId'])
    #tot2=database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto, session['userId'])

    piattiUtente=database.visualizza_un_piatto(db, 'piatti', session['userId'], idPiatto)
    ingredientiUtente=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    infoUtente=database.visualizza_tutti_piatti(db, 'utenti', session['userId'])
    db.close()
    return render_template('infoComplete.html', ingredientiUtente=ingredientiUtente, infoUtente=infoUtente, piattiUtente=piattiUtente)

@app.route('/nuovoPiatto', methods=['POST', 'GET'])
def nuovoPiatto():
    if request.method=='POST':
        nome=request.form.get('nomePiatto')
        
        """piatto1=Piatto()
        piatto1.setNome(nome)
        piattiUtente.append(piatto1)"""

        idU=session['userId']

        db=database.db()
        database.aggiungi_piatto(db, 'piatti', idU, nome, 0)
        db.close()
    
    return redirect(url_for('calcolaTot'))
    #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente)

@app.route('/calcolaPrezzo', methods=['POST', 'GET'])
def calcolaPrezzo():
    

    return render_template('calcolaPrezzo.html')

@app.route('/nuovoIngrediente', methods=['POST', 'GET'])
def aggiungiIngre():
    try:
        nomePiatto=str(request.form.get('nomeP'))
        ingrediente=request.form.get('nomeAlimento')
        prezzoKg=float(request.form.get('prezzoAlKg'))
        quanti=float(request.form.get('quantita'))
        tot=0
        prezzo=round(Calcoli.prezzoGrammi(quanti, prezzoKg), 3)

        db=database.db()
        idPiatto=database.idPiatto(db, 'piatti', nomePiatto, session['userId'])
    
        database.aggiungi_ingrediente(db, 'ingredienti', session['userId'], idPiatto[0], ingrediente, prezzoKg, quanti, prezzo)
    

        database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto[0], session['userId'])
  
        #piattiUtente=database.visualizza_tutti_piatti(db, 'piatti', session['userId'])
        #for piattoIdenti in piattiUtente:
            #if piattoIdenti.getNome()==nomePiatto:
              #  piattoIdenti.aggiungiIngrediente(ingrediente, prezzoKg, quanti)  
                #break    
            #tot=piattoIdenti.sommaCosti()
        
        
        db.close()
        #del db
        
        return redirect(url_for('calcolaTot'))
        #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente, tot2=tot2)
    except  Exception as e:
        return render_template("errore.html", e=e)
    
@app.route('/modifica/<int:sel>/<int:idP>/<int:selCol>', methods=['POST', 'GET'])
def modifica(sel, idP, selCol):
    colonne=['nome', 'prezzoKg', 'quantita', 'costo']
    
    if request.method=='POST':
        nome=request.form.get('nomePiatto')
        nuovo=request.form.get('nuovo')
        db=database.db()

        if sel==1:
            database.modifica_elemento(db, session['userId'], idP, 'piatti', colonne[0], nuovo)
        

        elif sel==2:
            #nuovo=request.form.get('ingre') da eliminare
            database.modifica_elemento(db, session['userId'], idP, 'ingredienti', colonne[selCol], nuovo)
            elemento=database.visualizza_un_piatto(db, 'ingredienti', session['userId'], idP)
            nuovo=Calcoli.prezzoGrammi(float(elemento[5]), float(elemento[4]))
            database.modifica_elemento(db, session['userId'], idP, 'ingredienti', colonne[3], nuovo)

        #piatto.setNome(nome)    
        #da aggiungere modifica specifica ad un solo oggetto dell'array
        #for a in piattiUtente:
        #    nome.append(piatto.getNome())

        db.close()

    return redirect(url_for('calcolaTot'))



@app.route('/cancellaX', methods=['GET', 'POST'])
def cancellaPiatto():
    nome=request.form.get('nomeP')

    db=database.db()
    idPia=database.idPiatto(db, 'piatti', nome, session['userId'])

    ingreElimina=database.visualizza_tutti_piatti(db, 'ingredienti', session['userId'])
    
    for e in ingreElimina:
        if e[2] ==idPia[0]:
            database.elimina_rigaPiatto(db, idPia[0], 'ingredientiForzata')

    database.elimina_rigaPiatto(db, idPia[0], 'piatti')
    db.close()
    return redirect(url_for('calcolaTot'))


@app.route('/cancellaXy', methods=['GET', 'POST'])
def cancellaIngre():
    tot=0
    nome=request.form.get('nomeI')

    db=database.db()
    idIngre=database.idIngre(db, 'ingredienti', nome, session['userId'])

    daSottrarre=int(idIngre[2])
    database.elimina_rigaPiatto(db, idIngre[0], 'ingredienti')
    database.sommaCosti_ingredienti(db, 'ingredienti', daSottrarre, session['userId'])

    db.close()
    return redirect(url_for('calcolaTot'))


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




if __name__ == "__main__":
    # Run the app server on localhost:4449
    app.run(host='0.0.0.0')


