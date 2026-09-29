"""
Implementación de algoritmos de sumatoria para el análisis de 
la propiedad conmutativa en números de punto flotante.
"""
import os
import random
import numpy as np
import matplotlib.pyplot as plt

# Crear carpeta para guardar las figuras si no existe
os.makedirs('figuras', exist_ok=True)

def valor_teorico(N: int) -> float:
    """Calcula el valor teórico analítico de la sumatoria b_N."""
    return N / (N + 1)

def error_relativo(valor_numerico: float, valor_teorico: float) -> float:
    """Calcula el error relativo respecto al valor teórico exacto."""
    return abs(valor_numerico - valor_teorico) / abs(valor_teorico)

# Suma de mayor a menor módulo
def suma_mayor_a_menor(N: int) -> float:
    """Suma los términos decrecientes (desde k=1 hasta N)."""
    s = 0.0
    for k in range(1, N + 1):
        s += 1.0 / (k * (k + 1))
    return s

# Suma de menor a mayor módulo
def suma_menor_a_mayor(N: int) -> float:
    """Suma los términos crecientes (desde k=N hasta 1)."""
    s = 0.0
    for k in range(N, 0, -1):
        s += 1.0 / (k * (k + 1))
    return s

# Suma randomizada con múltiples corridas
def suma_randomizada(N: int) -> float:
    """Suma los términos en un orden aleatorio."""
    terminos = [1.0 / (k * (k + 1)) for k in range(1, N + 1)]
    random.shuffle(terminos)
    s = 0.0
    for t in terminos:
        s += t
    return s

# Algoritmo de Kahan
def suma_kahan(N: int) -> float:
    """Suma compensada de Kahan."""
    s = 0.0
    c = 0.0
    for k in range(1, N + 1):
        y = (1.0 / (k * (k + 1))) - c
        t = s + y
        c = (t - s) - y
        s = t
    return s

def evaluar_multiples_corridas(N_fijo: int = 500000, repeticiones: int = 50):
    """Realiza múltiples corridas para la suma randomizada y evalúa la varianza."""
    errores = []
    teorico = valor_teorico(N_fijo)
    for _ in range(repeticiones):
        errores.append(error_relativo(suma_randomizada(N_fijo), teorico))
    
    print("\n--- Resultados Suma Randomizada Múltiples Corridas ---")
    print(f"Error mínimo: {np.min(errores):.4e}")
    print(f"Error máximo: {np.max(errores):.4e}")
    print(f"Desviación estándar: {np.std(errores):.4e}")

def ejecutar_experimentos():
    """Ejecuta los análisis solicitados y exporta las gráficas en alta calidad."""
    
    # Calcular y graficar error relativo E_rel para N de 10 a 10.000
    print("Calculando rango pequeño (N hasta 10.000)...")
    N_10k = np.arange(10, 10001, 10)
    e_mayor_10k = [error_relativo(suma_mayor_a_menor(n), valor_teorico(n)) for n in N_10k]
    e_menor_10k = [error_relativo(suma_menor_a_mayor(n), valor_teorico(n)) for n in N_10k]
    e_rand_10k  = [error_relativo(suma_randomizada(n), valor_teorico(n)) for n in N_10k]
    e_kahan_10k = [error_relativo(suma_kahan(n), valor_teorico(n)) for n in N_10k]

    plt.figure(figsize=(8, 5))
    plt.plot(N_10k, e_mayor_10k, label='Mayor a menor')
    plt.plot(N_10k, e_menor_10k, label='Menor a mayor')
    plt.plot(N_10k, e_rand_10k, label='Randomizada', alpha=0.5)
    plt.plot(N_10k, e_kahan_10k, label='Kahan')
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Error Relativo')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()

    # Exportación en PNG
    plt.savefig('figuras/error_10k.png', dpi=300, bbox_inches='tight') 
    plt.close()

    #Calcular y graficar E_rel para N de 1.000 a 1.000.000
    print("Calculando rango grande (N hasta 1.000.000)...")
    N_1M = np.arange(1000, 1000001, 5000)
    e_mayor_1M = [error_relativo(suma_mayor_a_menor(n), valor_teorico(n)) for n in N_1M]
    e_menor_1M = [error_relativo(suma_menor_a_mayor(n), valor_teorico(n)) for n in N_1M]
    e_rand_1M  = [error_relativo(suma_randomizada(n), valor_teorico(n)) for n in N_1M]
    e_kahan_1M = [error_relativo(suma_kahan(n), valor_teorico(n)) for n in N_1M]

    plt.figure(figsize=(8, 5))
    plt.plot(N_1M, e_mayor_1M, label='Mayor a menor')
    plt.plot(N_1M, e_menor_1M, label='Menor a mayor')
    plt.plot(N_1M, e_rand_1M, label='Randomizada', alpha=0.5)
    plt.plot(N_1M, e_kahan_1M, label='Kahan')
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Error Relativo')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()

    # Exportación en PNG
    plt.savefig('figuras/error_1M.png', dpi=300, bbox_inches='tight') 
    plt.close()

if __name__ == "__main__":
    ejecutar_experimentos()
    evaluar_multiples_corridas()