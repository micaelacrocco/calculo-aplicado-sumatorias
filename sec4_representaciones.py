"""
Sección 4: Representaciones de una suma.
Acá comparamos formas que matemáticamente son la misma cantidad pero que al implementarlas en 
una computadora pueden dar resultados distintos.
Por ahora implementamos b_N:
  - Forma (1): Suma de 1/(k(k+1))
  - Forma (2): Suma telescópica de (1/k - 1/(k+1))
  - Bonus 1: 1 - 1/(N+1) frente a N/(N+1)
Las dos primeras se comparan contra la fórmula cerrada N/(N+1).
"""
import os
from fractions import Fraction

import numpy as np
import matplotlib.pyplot as plt

# Crear carpeta para guardar las figuras si no existe
os.makedirs('figuras', exist_ok=True)

# Cuando el error es exactamente 0 no se puede dibujar en escala logarítmica así que en los 
# gráficos lo reemplazamos por este valor.
PISO_ERROR_PARA_GRAFICO = 1e-17

# Valor de referencia y error

def valor_exacto_formula_cerrada(cantidad_terminos: int) -> float:
    # Fórmula cerrada de b_N: N / (N + 1) calculada en float.
    return cantidad_terminos / (cantidad_terminos + 1)

def valor_exacto_con_fracciones(cantidad_terminos: int) -> Fraction:
    # Valor exacto de b_N usando fracciones racionales (sin redondeo).
    # Se usa en el Bonus, porque N/(N+1) en float ya tiene un redondeo y no sirve como 
    # referencia para juzgar a la propia fórmula.
    return Fraction(cantidad_terminos, cantidad_terminos + 1)

def error_relativo(valor_numerico: float, valor_de_referencia: float) -> float:
    # Error relativo |numérico - referencia| / |referencia|.
    return abs(valor_numerico - valor_de_referencia) / abs(valor_de_referencia)

def error_relativo_contra_fraccion(valor_numerico: float,
                                   valor_exacto: Fraction) -> float:
    # Error relativo contra un valor exacto dado como Fraction.
    # La resta se hace con fracciones para no introducir redondeos extra.
    diferencia_exacta = abs(Fraction(valor_numerico) - valor_exacto)
    return float(diferencia_exacta / valor_exacto)

# Representaciones de b_N como sumatoria sin usar sum de python

def suma_forma_producto(cantidad_terminos: int) -> float:
    # Forma (1): b_N = suma de 1 / (k * (k + 1)) con k desde 1 hasta N.
    acumulado = 0.0
    for k in range(1, cantidad_terminos + 1):
        acumulado += 1.0 / (k * (k + 1))
    return acumulado

def suma_forma_telescopica(cantidad_terminos: int) -> float:
    # Forma (2): b_N = suma de (1/k - 1/(k+1)), con k desde 1 hasta N.
    # En teoría los términos se cancelan de a pares y queda 1 - 1/(N+1), pero acá se restan dos 
    # floats en cada paso, y eso puede perder precisión.
    acumulado = 0.0
    for k in range(1, cantidad_terminos + 1):
        acumulado += (1.0 / k) - (1.0 / (k + 1))
    return acumulado

# Bonus 1: Dos formas de escribir el resultado cerrado de b_N

def forma_uno_menos_inverso(cantidad_terminos: int) -> float:
    # 1 - 1/(N+1). Resta un número chico a 1, no a otro cercano a él.
    return 1.0 - 1.0 / (cantidad_terminos + 1)


def forma_cociente(cantidad_terminos: int) -> float:
    # N/(N+1). Una sola división un único redondeo.
    return cantidad_terminos / (cantidad_terminos + 1)

# Experimentos

def reemplazar_ceros_para_grafico(lista_errores):
    # Cambia los ceros exactos por un piso para poder usar escala log.
    return [max(error, PISO_ERROR_PARA_GRAFICO) for error in lista_errores]

def experimento_representaciones_de_b():
    # Consigna 2: Para N = 1, 10, 20, ..., 10000 calcula el error relativo de las dos formas de 
    # sumar b_N respecto de N/(N+1) y las grafica.
    valores_de_N = [1] + list(range(10, 10001, 10))
    errores_forma_producto = []
    errores_forma_telescopica = []
    for N in valores_de_N:
        referencia = valor_exacto_formula_cerrada(N)
        errores_forma_producto.append(
            error_relativo(suma_forma_producto(N), referencia))
        errores_forma_telescopica.append(
            error_relativo(suma_forma_telescopica(N), referencia))
    print("\n--- b_N: error relativo de las dos representaciones ---")
    print(f"{'Forma':<28}{'Máximo':>12}{'Media':>12}{'En N=10000':>14}")
    for nombre, errores in [("(1) 1/(k(k+1))", errores_forma_producto),
                            ("(2) 1/k - 1/(k+1)", errores_forma_telescopica)]:
        print(f"{nombre:<28}{np.max(errores):>12.3e}"
              f"{np.mean(errores):>12.3e}{errores[-1]:>14.3e}")
    plt.figure(figsize=(8, 5))
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_forma_producto),
             label='Forma (1): 1/(k(k+1))', alpha=0.8)
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_forma_telescopica),
             label='Forma (2): 1/k - 1/(k+1)', alpha=0.8)
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Error Relativo')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('figuras/error_representaciones_bN.png', dpi=300,
                bbox_inches='tight')
    plt.close()

def experimento_bonus_uno_menos_inverso():
    # Bonus 1: Compara 1 - 1/(N+1) con N/(N+1).
    # Como las dos son iguales en matemática, se miden contra el valor exacto (fracciones) y 
    # además se cuenta en cuántos N dan resultados distintos.
    valores_de_N = list(range(10, 10001, 10))
    errores_uno_menos_inverso = []
    errores_cociente = []
    for N in valores_de_N:
        exacto = valor_exacto_con_fracciones(N)
        errores_uno_menos_inverso.append(
            error_relativo_contra_fraccion(forma_uno_menos_inverso(N), exacto))
        errores_cociente.append(
            error_relativo_contra_fraccion(forma_cociente(N), exacto))
    print("\n--- Bonus 1: 1 - 1/(N+1) frente a N/(N+1) ---")
    print(f"Error máximo de 1 - 1/(N+1): {np.max(errores_uno_menos_inverso):.3e}")
    print(f"Error máximo de N/(N+1):     {np.max(errores_cociente):.3e}")
    # Barrido grande: En cuántos N dan distinto las dos formas?
    cantidad_barrida = 1_000_000
    cantidad_distintos = 0
    for N in range(1, cantidad_barrida + 1):
        if forma_uno_menos_inverso(N) != forma_cociente(N):
            cantidad_distintos += 1
    print(f"N en 1..{cantidad_barrida} donde las dos formas dan distinto: "
          f"{cantidad_distintos}")
    # Para N enormes: Cuando 1/(N+1) queda por debajo de la precisión de 1 las dos formas 
    # terminan valiendo exactamente 1.0
    print("\n   N            1 - 1/(N+1)           N/(N+1)         iguales")
    for exponente in [4, 8, 12, 15, 16, 17]:
        N = 10 ** exponente
        a = forma_uno_menos_inverso(N)
        b = forma_cociente(N)
        print(f"1e{exponente:<3}   {a:<22.17f}{b:<22.17f}{a == b}")
    plt.figure(figsize=(8, 5))
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_uno_menos_inverso),
             label='1 - 1/(N+1)', alpha=0.8)
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_cociente),
             label='N/(N+1)', alpha=0.8)
    plt.yscale('log')
    plt.xlabel('N')
    plt.ylabel('Error Relativo (contra fracción exacta)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('figuras/error_bonus1_bN.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    experimento_representaciones_de_b()
    experimento_bonus_uno_menos_inverso()