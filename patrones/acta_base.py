from abc import ABC, abstractmethod

class ActaBase(ABC):
    # Este es el "Molde". Define los pasos obligatorios.
    
    def generar_acta(self, datos, evaluaciones):
        # Esta funcion es el "Template Method".
        # Llama a los pasos uno por uno en orden.
        self.texto = ""
        self.crear_encabezado(datos)
        self.crear_cuerpo(datos, evaluaciones)
        self.crear_firmas(evaluaciones)
        return self.obtener_resultado()

    # --- Pasos que se deben rellenar (obligatorios) ---
    @abstractmethod
    def crear_encabezado(self, datos):
        pass

    @abstractmethod
    def crear_cuerpo(self, datos, evaluaciones):
        pass

    @abstractmethod
    def crear_firmas(self, evaluaciones):
        pass

    @abstractmethod
    def obtener_resultado(self):
        pass