from calcoli import Calcoli
from query import database

class Magazzino:
    def __init__(self, id=0, nome=""):
        self.id = id
        self.nome = nome

    def set_id(self, id):
        self.id = id

    def set_nome(self, nome):
        self.nome = nome

    def to_string(self):
        return "Magazzino: " + self.nome + "\nId: " + str(self.id)

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome
