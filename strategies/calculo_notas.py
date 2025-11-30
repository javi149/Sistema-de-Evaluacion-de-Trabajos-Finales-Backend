# strategies/calculo_notas.py
from abc import ABC, abstractmethod

class EstrategiaCalculo(ABC):
    @abstractmethod
    def calcular(self, lista_notas):
        pass

class PromedioPonderado(EstrategiaCalculo):
    """
    Calcula el promedio ponderado respetando el formato almacenado en la BD.
    Soporta pesos expresados como porcentaje (0-100) o como fracción (0-1).
    """

    def calcular(self, lista_notas):
        if not lista_notas:
            return 0.0

        suma_notas = 0.0
        suma_pesos = 0.0

        for item in lista_notas:
            nota = float(item.get('nota', 0))
            peso = self._normalizar_peso(item)
            if peso == 0:
                continue

            suma_notas += nota * peso
            suma_pesos += peso

        if suma_pesos == 0:
            return 0.0

        return round(suma_notas / suma_pesos, 2)

    @staticmethod
    def _normalizar_peso(item):
        """
        Permite recibir claves distintas desde la consulta SQL
        (porcentaje, ponderacion, peso, etc.) y normaliza el valor.
        """
        peso = item.get('ponderacion', item.get('porcentaje', item.get('peso')))
        if peso is None:
            return 0.0

        peso = float(peso)
        if peso > 1:
            return peso / 100
        return peso

class Calculadora:
    def __init__(self, estrategia: EstrategiaCalculo):
        self.estrategia = estrategia

    def obtener_resultado(self, lista_notas):
        return self.estrategia.calcular(lista_notas)