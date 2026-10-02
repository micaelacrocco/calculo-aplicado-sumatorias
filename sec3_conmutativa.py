"""
Sección 3: Propiedad conmutativa.
Acá estudiamos cómo el orden de los términos (y el algoritmo de suma) afecta el
resultado de b_N = suma de 1/(k(k+1)), cuyo valor exacto es N/(N+1).
Los cuatro algoritmos que comparamos son:
  - Suma de mayor a menor módulo
  - Suma de menor a mayor módulo
  - Suma en orden aleatorio
  - Suma compensada de Kahan
Se mide el error relativo contra la fórmula cerrada en dos rangos de N, y
además se repite la suma aleatoria varias veces para un N grande.
"""
import os
import random

import numpy as np
import matplotlib.pyplot as plt

# Crear carpeta para guardar las figuras si no existe
os.makedirs('figuras', exist_ok=True)

# Cuando el error es exactamente 0 no se puede dibujar en escala logarítmica, así que en los
# gráficos lo reemplazamos por este valor (un poco menor a eps).
PISO_ERROR_PARA_GRAFICO = 1e-17

# Parámetros del análisis de la suma randomizada con múltiples corridas
N_FIJO_PARA_CORRIDAS = 500000
CANTIDAD_DE_REPETICIONES = 50

# Valor de referencia y error

def valor_teorico(cantidad_terminos: int) -> float:
    # Fórmula cerrada de b_N: N / (N + 1)
    return cantidad_terminos / (cantidad_terminos + 1)

def error_relativo(valor_numerico: float, valor_de_referencia: float) -> float:
    # Error relativo |numérico - referencia| / |referencia|.
    return abs(valor_numerico - valor_de_referencia) / abs(valor_de_referencia)

# Los cuatro algoritmos de suma (sin usar sum de python)

def suma_mayor_a_menor(cantidad_terminos: int) -> float:
    # Los términos 1/(k(k+1)) decrecen con k, así que ir de k=1 a N es de mayor a menor módulo.
    acumulado = 0.0
    for k in range(1, cantidad_terminos + 1):
        acumulado += 1.0 / (k * (k + 1))
    return acumulado

def suma_menor_a_mayor(cantidad_terminos: int) -> float:
    # Ahora se recorre de k=N hasta 1 o sea de menor a mayor módulo. Los términos chicos se
    # acumulan entre sí antes de sumarse a los grandes
    acumulado = 0.0
    for k in range(cantidad_terminos, 0, -1):
        acumulado += 1.0 / (k * (k + 1))
    return acumulado

def suma_orden_aleatorio(cantidad_terminos: int) -> float:
    # Se arma la lista de términos y se mezcla con shuffle y se suma en ese orden.
    # El resultado cambia de una corrida a otra.
    lista_de_terminos = [1.0 / (k * (k + 1)) for k in range(1, cantidad_terminos + 1)]
    random.shuffle(lista_de_terminos)
    acumulado = 0.0
    for termino in lista_de_terminos:
        acumulado += termino
    return acumulado

def suma_kahan(cantidad_terminos: int) -> float:
    # Suma compensada de Kahan: la variable compensacion guarda lo que se perdió por redondeo
    # en el paso anterior y se lo vuelve a restar al próximo término
    acumulado = 0.0
    compensacion = 0.0
    for k in range(1, cantidad_terminos + 1):
        termino_corregido = (1.0 / (k * (k + 1))) - compensacion
        nuevo_acumulado = acumulado + termino_corregido
        compensacion = (nuevo_acumulado - acumulado) - termino_corregido
        acumulado = nuevo_acumulado
    return acumulado

# Cálculo de errores y gráfico

def reemplazar_ceros_para_grafico(lista_errores):
    # Cambia los ceros exactos por un piso para poder usar escala log.
    return [max(error, PISO_ERROR_PARA_GRAFICO) for error in lista_errores]

def calcular_errores_de_los_cuatro_algoritmos(valores_de_N):
    # Para cada N calcula el error relativo de cada algoritmo contra N/(N+1).
    # Devuelve cuatro listas, una por algoritmo, en el mismo orden que valores_de_N
    errores_mayor_a_menor = []
    errores_menor_a_mayor = []
    errores_orden_aleatorio = []
    errores_kahan = []
    for N in valores_de_N:
        referencia = valor_teorico(N)
        errores_mayor_a_menor.append(error_relativo(suma_mayor_a_menor(N), referencia))
        errores_menor_a_mayor.append(error_relativo(suma_menor_a_mayor(N), referencia))
        errores_orden_aleatorio.append(error_relativo(suma_orden_aleatorio(N), referencia))
        errores_kahan.append(error_relativo(suma_kahan(N), referencia))
    return (errores_mayor_a_menor, errores_menor_a_mayor,
            errores_orden_aleatorio, errores_kahan)

def graficar_errores(valores_de_N, errores_por_algoritmo, nombre_archivo: str):
    # Grafica el error relativo de los cuatro algoritmos en función de N, en escala log.
    (errores_mayor_a_menor, errores_menor_a_mayor,
     errores_orden_aleatorio, errores_kahan) = errores_por_algoritmo
    plt.figure(figsize=(8, 5))
    plt.plot(valores_de_N, reemplazar_ceros_para_grafico(errores_mayor_a_menor),
             label='Mayor a menor')
    plt.plot(valores_de_N, reemplazar_ceros_para_grafico(errores_menor_a_mayor),
             label='Menor a mayor')
    plt.plot(valores_de_N, reemplazar_ceros_para_grafico(errores_orden_aleatorio),
             label='Randomizada', alpha=0.5)
    plt.plot(valores_de_N, reemplazar_ceros_para_grafico(errores_kahan),
             label='Kahan')
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Error Relativo')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figuras/{nombre_archivo}', dpi=300, bbox_inches='tight')
    plt.close()

# Experimentos

def experimento_rango_chico():
    # Consigna 3: N = 10, 20, ..., 10000
    print("Calculando rango pequeño (N hasta 10.000)...")
    valores_de_N = np.arange(10, 10001, 10)
    errores = calcular_errores_de_los_cuatro_algoritmos(valores_de_N)
    graficar_errores(valores_de_N, errores, 'error_10k.png')

def experimento_rango_grande():
    # Consigna 4: N desde 1.000 hasta 1.000.000. Para que no tarde demasiado se toma un paso de
    # 5.000 en lugar de 1.000 (son 4 algoritmos con hasta un millón de términos cada uno).
    print("Calculando rango grande (N hasta 1.000.000)...")
    valores_de_N = np.arange(1000, 1000001, 5000)
    errores = calcular_errores_de_los_cuatro_algoritmos(valores_de_N)
    graficar_errores(valores_de_N, errores, 'error_1M.png')

def experimento_multiples_corridas():
    # Consigna 5: Repite la suma aleatoria varias veces con el mismo N grande para ver cuánto
    # varía el error entre una corrida y otra
    referencia = valor_teorico(N_FIJO_PARA_CORRIDAS)
    errores_de_las_corridas = []
    for _ in range(CANTIDAD_DE_REPETICIONES):
        resultado = suma_orden_aleatorio(N_FIJO_PARA_CORRIDAS)
        errores_de_las_corridas.append(error_relativo(resultado, referencia))
    print("\n--- Resultados Suma Randomizada Múltiples Corridas ---")
    print(f"N = {N_FIJO_PARA_CORRIDAS}, {CANTIDAD_DE_REPETICIONES} ejecuciones")
    print(f"Error mínimo: {np.min(errores_de_las_corridas):.4e}")
    print(f"Error máximo: {np.max(errores_de_las_corridas):.4e}")
    print(f"Media del error: {np.mean(errores_de_las_corridas):.4e}")
    print(f"Desviación estándar: {np.std(errores_de_las_corridas):.4e}")

if __name__ == "__main__":
    experimento_rango_chico()
    experimento_rango_grande()
    experimento_multiples_corridas()