"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

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


@app.route('/nuovoPiatto', methods=['POST', 'GET'])
def nuovoPiatto():
    if request.method=='POST':
        nome=request.form.get('nomePiatto')
        
        """piatto1=Piatto()
        piatto1.setNome(nome)
        piattiUtente.append(piatto1)"""

        id=session['userId']

        db=database.db()
        database.aggiungi_piatto(db, 'piatti', id, nome, 0)
    
    return redirect(url_for('calcolaTot'))
    #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente)

@app.route('/calcolaPrezzo', methods=['POST', 'GET'])
def calcolaPrezzo():
    

    return render_template('calcolaPrezzo.html')

@app.route('/nuovoIngrediente', methods=['POST', 'GET'])
def aggiungiIngre():
    nomePiatto=str(request.form.get('nomeP'))
    ingrediente=request.form.get('nomeAlimento')
    prezzoKg=float(request.form.get('prezzoAlKg'))
    quanti=float(request.form.get('quantita'))
    tot=0
    prezzo=Calcoli.prezzoGrammi(quanti, prezzoKg)

    db=database.db()
    idPiatto=database.idPiatto(db, 'piatti', nomePiatto, session['userId'])
    
    database.aggiungi_ingrediente(db, 'ingredienti', session['userId'], idPiatto[0], ingrediente, prezzoKg, quanti, prezzo)

    tot2=database.sommaCosti_ingredienti(db, 'ingredienti', idPiatto[0], session['userId'], nomePiatto)
  
    #piattiUtente=database.visualizza_tutti_piatti(db, 'piatti', session['userId'])
    #for piattoIdenti in piattiUtente:
        #if piattoIdenti.getNome()==nomePiatto:
          #  piattoIdenti.aggiungiIngrediente(ingrediente, prezzoKg, quanti)  
            #break    
        #tot=piattoIdenti.sommaCosti()

    db.close()
    return redirect(url_for('calcolaTot'))
    #return render_template("calcolaPrezzo.html", piattiUtente=piattiUtente, tot2=tot2)

@app.route('/modifica/<int:sel>/<int:idP>/<int:selCol>', methods=['POST'])
def modifica(sel, idP, selCol):
    colonne=['nome', 'prezzoKg', 'quantita', 'costo']

    nome=request.form.get('nomePiatto')
    nuovo=request.form.get('nuovo')
    db=database.db()

    if sel==1:
        database.modifica_elemento(db, session['userId'], idP, 'piatti', colonne[0], nuovo)
    elif sel==2:
        nuovo=request.form.get('ingre')
        database.modifica_elemento(db, session['userId'], idP, 'ingredienti', colonne[selCol], nuovo)


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

    database.elimina_rigaPiatto(db, idPia[0], 'piatti')

    db.close()
    return redirect(url_for('calcolaTot'))


@app.route('/cancellaXy', methods=['GET', 'POST'])
def cancellaIngre():
    nome=request.form.get('nomeI')

    db=database.db()
    idIngre=database.idIngre(db, 'ingredienti', nome, session['userId'])

    database.elimina_rigaPiatto(db, idIngre[0], 'ingredienti')

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

        data=database.db()
        cursore=data.cursor()


        cursore.execute(query2.SPECIFICOselezionaColonnaMail, (mail,))
        if cursore.fetchone() is not None:
           return redirect(url_for('no'))
        else:
            #-----------CODIFICA VALORI INSERITI--------------
            pass_codificata=bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
            #-----------------------------------------------------------

            cursore.execute(query2.SPECIFICOinserisciNuovoUtente,
                            (nome, cognome, mail, azienda, pass_codificata ))
            
            data.commit()
            data.close()

            return render_template('index.html')

    return render_template('registrazione.html')


@app.route('/login', methods=['POST', 'GET'])
def accesso():
    trovato_nome=None
    if request.method=='POST':
        utente=request.form['user']
        passwd=request.form['pass'].encode('UTF-8')

        database_ram=database.db()
        cursore=database_ram.cursor()

        cursore.execute(query2.SPECIFICOselezionaColonnaMail, (utente,))
        trovato_nome=cursore.fetchone()
        
        database_ram.close()
        

    if trovato_nome is not None and bcrypt.checkpw(passwd, trovato_nome[5]):
        session['userId']=trovato_nome[0]
        return redirect(url_for('calcolaTot'))
           
    else:
        trovato_nome=None
        return redirect(url_for('main'))        

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555 
    app.run(HOST, PORT)
