"""
Funciones auxiliares transversales a las secciones del proyecto.
"""
import os

CARPETA_FIGURAS = 'figuras'

def crear_carpeta_figuras() -> str:
    # Crea la carpeta donde se guardan los gráficos si no existe.
    os.makedirs(CARPETA_FIGURAS, exist_ok=True)
    return CARPETA_FIGURAS

def error_relativo(valor_numerico: float, valor_de_referencia: float) -> float:
    # Error relativo |numérico - referencia| / |referencia|.
    return abs(valor_numerico - valor_de_referencia) / abs(valor_de_referencia)