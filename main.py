"""
Punto de entrada del programa, ejecuta todos los experimentos del trabajo en orden y deja los 
gráficos en la carpeta "figuras/".
Uso: python main.py
"""
import runpy

from utils import crear_carpeta_figuras

SECCIONES = [
    ('Sección 2: propiedad asociativa', 'sec2_asociativa.py'),
    ('Sección 3: propiedad conmutativa', 'sec3_conmutativa.py'),
    ('Sección 4: representaciones de una suma', 'sec4_representaciones.py'),
]

def ejecutar_todo():
    # Corre cada sección como si se hubiera ejecutado por separado.
    crear_carpeta_figuras()
    for titulo, archivo in SECCIONES:
        print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")
        runpy.run_path(archivo, run_name='__main__')
    print("\nPronto! Los gráficos están en la carpeta 'figuras/'.")

if __name__ == "__main__":
    ejecutar_todo()