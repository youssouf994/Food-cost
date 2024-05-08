from calcoli import Calcoli
from query import database

class Elemento:
    def __init__(self, id=0, nome="", posizione="", quanti=0, prezzo_pezzo=0.0, id_magazzino=""):
        self.id = id
        self.nome = nome
        self.posizione = posizione
        self.quanti = quanti
        self.prezzo_pezzo = prezzo_pezzo
        self.id_magazzino = id_magazzino

    def set_prezzo(self, prezzo):
        self.prezzo_pezzo = prezzo

    def set_quanti(self, quanti):
        self.quanti = quanti

    def set_posizione(self, posizione):
        self.posizione = posizione

    def get_prezzo(self):
        return str(self.prezzo_pezzo)

    def get_quanti(self):
        return self.quanti

    def get_id_magazzino(self):
        return self.id_magazzino

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_posizione(self):
        return self.posizione

    def set_nome(self, nome):
        self.nome = nome

    def set_id_magazzino(self, id):
        self.id_magazzino = id
