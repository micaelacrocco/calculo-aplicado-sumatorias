"""
Sección 2: Propiedad asociativa.
Acá estudiamos la sucesión a_N = suma de (1 + b^k - b^k), que en teoría vale N, pero que al 
implementarla puede dar otra cosa según cómo se agrupen las operaciones.
Las tres asociaciones que probamos son:
  - Asociación 1: (1 + b^k - b^k)
  - Asociación 2: (1 + b^k) - b^k
  - Asociación 3: (1 - b^k) + b^k
Se hace con b de tipo int y de tipo float, y además se repite el experimento para el Bonus 
(b menor o igual a 1 y b negativo).
"""
import os

import matplotlib.pyplot as plt

# Crear carpeta para guardar las figuras si no existe
os.makedirs('figuras', exist_ok=True)

CANTIDAD_DE_TERMINOS = 1000

# Sumas con las tres asociaciones sin usar sum de python

def suma_con_enteros(cantidad_terminos: int, base: int):
    # Con int base ** k se calcula de forma exacta, python usa enteros de precisión arbitraria,
    # así que no hay redondeo ni overflow.
    # k va desde 0 hasta N-1, como cada término vale 1 es equivalente a ir de 1 a N.
    # Devuelve los valores de k y el acumulado de cada asociación en cada paso
    acumulado_asociacion_1 = 0
    acumulado_asociacion_2 = 0
    acumulado_asociacion_3 = 0
    valores_de_k = []
    historial_asociacion_1 = []
    historial_asociacion_2 = []
    historial_asociacion_3 = []
    for k in range(cantidad_terminos):
        potencia = base ** k
        acumulado_asociacion_1 += (1 + potencia - potencia)
        acumulado_asociacion_2 += (1 + potencia) - potencia
        acumulado_asociacion_3 += (1 - potencia) + potencia
        valores_de_k.append(k)
        historial_asociacion_1.append(acumulado_asociacion_1)
        historial_asociacion_2.append(acumulado_asociacion_2)
        historial_asociacion_3.append(acumulado_asociacion_3)
    print(f"[int] b={base}: asociación 1 = {acumulado_asociacion_1}, "
          f"asociación 2 = {acumulado_asociacion_2}, "
          f"asociación 3 = {acumulado_asociacion_3}")
    return (valores_de_k, historial_asociacion_1,
            historial_asociacion_2, historial_asociacion_3)

def suma_con_flotantes(cantidad_terminos: int, base: float):
    # Con float base ** k se redondea a 53 bits  y cuando es muy grande el 1 se pierde al 
    # sumarlo (absorción). Además si base ** k supera 1.8e308 python lanza OverflowError, en 
    # ese caso cortamos la serie en ese k y los k siguientes no se grafican.
    acumulado_asociacion_1 = 0.0
    acumulado_asociacion_2 = 0.0
    acumulado_asociacion_3 = 0.0
    valores_de_k = []
    historial_asociacion_1 = []
    historial_asociacion_2 = []
    historial_asociacion_3 = []
    for k in range(cantidad_terminos):
        try:
            potencia = base ** k
        except OverflowError:
            print(f"b={base}: overflow en k={k}, se corta la serie ahí")
            break
        acumulado_asociacion_1 += (1 + potencia - potencia)
        acumulado_asociacion_2 += (1 + potencia) - potencia
        acumulado_asociacion_3 += (1 - potencia) + potencia
        valores_de_k.append(k)
        historial_asociacion_1.append(acumulado_asociacion_1)
        historial_asociacion_2.append(acumulado_asociacion_2)
        historial_asociacion_3.append(acumulado_asociacion_3)
    print(f"[float] b={base}: asociación 1 = {acumulado_asociacion_1}, "
          f"asociación 2 = {acumulado_asociacion_2}, "
          f"asociación 3 = {acumulado_asociacion_3}")
    return (valores_de_k, historial_asociacion_1,
            historial_asociacion_2, historial_asociacion_3)

# Gráficos

def graficar_resultados(lista_de_bases, usa_flotantes: bool, nombre_archivo: str):
    # Hace una figura con 3 gráficos y una curva por cada valor de b. Se llama con int o con 
    # float según usa_flotantes, y guarda la figura en "figuras/"
    figura, ejes = plt.subplots(3, 1, figsize=(8, 12))
    for base in lista_de_bases:
        if usa_flotantes:
            resultados = suma_con_flotantes(CANTIDAD_DE_TERMINOS, base)
        else:
            resultados = suma_con_enteros(CANTIDAD_DE_TERMINOS, base)
        valores_de_k, historial_1, historial_2, historial_3 = resultados
        ejes[0].plot(valores_de_k, historial_1, label=f'b={base}')
        ejes[1].plot(valores_de_k, historial_2, label=f'b={base}')
        ejes[2].plot(valores_de_k, historial_3, label=f'b={base}')

    ejes[0].set_title('Resultado 1: (1 + b^k - b^k)')
    ejes[1].set_title('Resultado 2: (1 + b^k) - b^k')
    ejes[2].set_title('Resultado 3: (1 - b^k) + b^k')
    for eje in ejes:
        eje.legend()
        eje.set_xlabel('k')
        eje.set_ylabel('a_N')
    plt.tight_layout()
    figura.savefig(f'figuras/{nombre_archivo}')
    plt.close(figura)

# Experimentos

def experimento_enteros_y_flotantes():
    # Consignas 2 y 3: b en {2, 3, 5, 10} con int y luego con float
    print("\n--- Asociatividad con b de tipo int ---")
    graficar_resultados([2, 3, 5, 10], False, 'GraficasInt.png')
    print("\n--- Asociatividad con b de tipo float ---")
    graficar_resultados([2.0, 3.0, 5.0, 10.0], True, 'GraficasFloat.png')

def experimento_bonus():
    # Bonus: Repetimos con b negativo (int y float) y con b menor o igual a 1 (float)
    print("\n--- Bonus: b negativo con int ---")
    graficar_resultados([-2, -3, -5, -10], False, 'BonusNegInt.png')
    print("\n--- Bonus: b negativo con float ---")
    graficar_resultados([-2.0, -3.0, -5.0, -10.0], True, 'BonusNegFloat.png')
    print("\n--- Bonus: b menor o igual a 1 con float ---")
    graficar_resultados([1.0, 0.9, 0.5, 0.1], True, 'BonusMenorUno.png')

if __name__ == "__main__":
    experimento_enteros_y_flotantes()
    experimento_bonus()