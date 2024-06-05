class Calcoli:
    @staticmethod
    def prezzoGrammi(quantiG, prezzoKg):
        return (quantiG/1000)*prezzoKg
    
    @staticmethod
    def calcola_iva(prezzo, aliquota_iva):

        importo_iva = prezzo * (aliquota_iva / 100)
        prezzo_totale = prezzo + importo_iva
        return importo_iva, prezzo_totale

    
