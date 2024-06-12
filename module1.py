
import sqlite3

# definisci una funzione lambda per decodificare i byte come stringhe utf8
def utf8_decoder(b):
    return b.decode('utf-8')

# crea la connessione e imposta la funzione di decodifica utf8
connection = sqlite3.connect('piatti.db')
connection.text_factory = utf8_decoder

with open ('piatti.sql', mode='r', encoding='utf-8') as f:
    connection.executescript(f.read())

connection.commit()
connection.close() 