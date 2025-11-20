# strategies/calculo_notas.py
from abc import ABC, abstractmethod

class EstrategiaCalculo(ABC):
    @abstractmethod
    def calcular(self, lista_notas):
        pass

class PromedioPonderado(EstrategiaCalculo):
    def calcular(self, lista_notas):
        # lista_notas espera diccionarios: {'nota': float, 'porcentaje': float}
        suma_notas = 0
        suma_pesos = 0

        for item in lista_notas:
            nota = float(item['nota'])
            # Asumimos que el porcentaje viene como 40 (para 40%)
            peso = float(item['porcentaje']) 
            
            suma_notas += nota * (peso / 100) # Convertimos 40 a 0.4
            suma_pesos += (peso / 100)
        
        if suma_pesos == 0: return 0.0
        
        # Retornamos redondeado a 2 decimales
        return round(suma_notas / suma_pesos, 2)

class Calculadora:
    def __init__(self, estrategia: EstrategiaCalculo):
        self.estrategia = estrategia

    def obtener_resultado(self, lista_notas):
        return self.estrategia.calcular(lista_notas)