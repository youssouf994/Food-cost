from calcoli import Calcoli

class Piatto:
    _alimento=[]

    def __init__(self, nome):
        self._nomePiatto=nome
        self._alimento=[]
        

    def __init__(self):
        pass

    def setNome(self, nome):
        self._nomePiatto=nome

    def getNome(self):
        return self._nomePiatto

    def aggiungiIngrediente(self, ingre, kg, quanti):
        costo=Calcoli.prezzoGrammi(quanti, kg)
        self._alimento.append([ingre, kg, quanti, costo])
      
    def getGrammi(self, x):
        return self._alimento[x][2] 
    
    def getPrezzoKg(self, x):
        return self._alimento[x][1] 
 
    def getCosto(self, x):
        return self._alimento[x][3] 

    def getDizionario(self):
        ingredienti_formattati = []
        if len(self._alimento)>=1:
            for ingrediente in self._alimento:
                ingrediente_formattato = {
                    'Nome': ingrediente[0],
                    'PrezzoKg': float(ingrediente[1]),
                    'Quantita': float(ingrediente[2]),
                    'Costo': float(ingrediente[3])
                }
                ingredienti_formattati.append(ingrediente_formattato)
            return ingredienti_formattati
        else:
            return {}

 
    def sommaCosti(self):
        tot=0
        x=0
        if len(self._alimento)>=1:
            for i in self._alimento:           
                tot+=self._alimento[x][3]
                x+=1
        else:
            return {}

        return tot

    