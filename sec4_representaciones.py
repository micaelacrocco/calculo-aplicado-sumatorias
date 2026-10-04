"""
Sección 4: Representaciones de una suma.
Acá comparamos formas que matemáticamente son la misma cantidad pero que al implementarlas en 
una computadora pueden dar resultados distintos.
Se trabaja con dos sucesiones:
  - b_N: Forma (1) suma de 1/(k(k+1)), Forma (2) suma telescópica de (1/k - 1/(k+1)).
    Las dos se comparan contra la fórmula cerrada N/(N+1).
    Bonus 1: 1 - 1/(N+1) frente a N/(N+1).
  - c_N: Forma (1) suma de 1/(sqrt(k^2+1) + k), Forma (2) suma de (sqrt(k^2+1) - k).
    No tiene fórmula cerrada, así que se compara contra un valor de referencia calculado con 
    Decimal (50 dígitos). Además se grafica la diferencia absoluta D_N entre las dos formas.
    Bonus 2: términos sueltos de c_N y a partir de qué k se pierde precisión.
"""
import math
import os
from decimal import Context, Decimal
from fractions import Fraction

import numpy as np
import matplotlib.pyplot as plt

# Crear carpeta para guardar las figuras si no existe
os.makedirs('figuras', exist_ok=True)

# Cuando el error es exactamente 0 no se puede dibujar en escala logarítmica así que en los 
# gráficos lo reemplazamos por este valor.
PISO_ERROR_PARA_GRAFICO = 1e-17

# Precisión (en dígitos decimales) del valor de referencia de c_N. Es mucho mayor que los ~16 
# dígitos de un float, así que el error de la referencia es despreciable frente al de las sumas.
PRECISION_DECIMAL = 50
CONTEXTO_DECIMAL = Context(prec=PRECISION_DECIMAL)

# Umbrales de error relativo para decir "la pérdida de precisión ya es apreciable" (Bonus 2)
UMBRALES_PERDIDA_DE_PRECISION = [1e-12, 1e-8, 1e-4, 1e-2]

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

# Referencia con Decimal y error relativo (para c_N, que no tiene fórmula cerrada)

def termino_c_exacto_decimal(k: int) -> Decimal:
    # Término k de c_N con 50 dígitos. Se usa la forma 1/(sqrt(k^2+1) + k), que no resta números
    # parecidos, y k^2 + 1 se calcula como entero exacto.
    raiz = CONTEXTO_DECIMAL.sqrt(Decimal(k * k + 1))
    return CONTEXTO_DECIMAL.divide(Decimal(1), CONTEXTO_DECIMAL.add(raiz, Decimal(k)))

def valores_exactos_c_con_decimal(valores_de_N) -> dict:
    # Valor de referencia de c_N para cada N pedido. Como c_N es una suma acumulada alcanza con 
    # una sola pasada hasta el N más grande, guardando el acumulado en los N que se necesitan.
    pedidos = set(valores_de_N)
    acumulado = Decimal(0)
    exactos = {}
    for k in range(1, max(valores_de_N) + 1):
        acumulado = CONTEXTO_DECIMAL.add(acumulado, termino_c_exacto_decimal(k))
        if k in pedidos:
            exactos[k] = acumulado
    return exactos

def error_relativo_contra_decimal(valor_numerico: float, valor_exacto: Decimal) -> float:
    # Error relativo contra un valor exacto dado como Decimal.
    # La resta se hace en Decimal para no introducir redondeos extra.
    diferencia_exacta = CONTEXTO_DECIMAL.abs(
        CONTEXTO_DECIMAL.subtract(Decimal(valor_numerico), valor_exacto))
    return float(CONTEXTO_DECIMAL.divide(diferencia_exacta, valor_exacto))

# Representaciones de c_N como sumatoria sin usar sum de python

def termino_c_forma_inversa(k: int) -> float:
    # Forma (1): 1 / (sqrt(k^2 + 1) + k). Es una suma de dos positivos, así que no hay cancelación.
    return 1.0 / (math.sqrt(float(k) * k + 1.0) + k)

def termino_c_forma_resta(k: int) -> float:
    # Forma (2): sqrt(k^2 + 1) - k. Para k grande son dos números casi iguales y al restarlos se
    # cancelan casi todos los dígitos significativos (cancelación catastrófica).
    return math.sqrt(float(k) * k + 1.0) - k

def suma_c_forma_inversa(cantidad_terminos: int) -> float:
    # c_N con la forma (1): suma de 1 / (sqrt(k^2 + 1) + k) con k desde 1 hasta N.
    acumulado = 0.0
    for k in range(1, cantidad_terminos + 1):
        acumulado += termino_c_forma_inversa(k)
    return acumulado

def suma_c_forma_resta(cantidad_terminos: int) -> float:
    # c_N con la forma (2): suma de (sqrt(k^2 + 1) - k) con k desde 1 hasta N.
    acumulado = 0.0
    for k in range(1, cantidad_terminos + 1):
        acumulado += termino_c_forma_resta(k)
    return acumulado

# Experimentos de c_N

def experimento_representaciones_de_c():
    # Consigna 3: Para N = 1, 10, 20, ..., 10000 calcula el error relativo de las dos formas de 
    # sumar c_N (contra la referencia en Decimal), la diferencia absoluta D_N entre las dos 
    # formas, y grafica las dos cosas.
    valores_de_N = [1] + list(range(10, 10001, 10))
    exactos = valores_exactos_c_con_decimal(valores_de_N)
    errores_forma_inversa = []
    errores_forma_resta = []
    diferencias_D = []
    for N in valores_de_N:
        c_inversa = suma_c_forma_inversa(N)
        c_resta = suma_c_forma_resta(N)
        errores_forma_inversa.append(error_relativo_contra_decimal(c_inversa, exactos[N]))
        errores_forma_resta.append(error_relativo_contra_decimal(c_resta, exactos[N]))
        diferencias_D.append(abs(c_inversa - c_resta))
    print("\n--- c_N: error relativo de las dos representaciones (contra Decimal) ---")
    print(f"{'Forma':<28}{'Máximo':>12}{'Media':>12}{'En N=10000':>14}")
    for nombre, errores in [("(1) 1/(sqrt(k^2+1)+k)", errores_forma_inversa),
                            ("(2) sqrt(k^2+1) - k", errores_forma_resta)]:
        print(f"{nombre:<28}{np.max(errores):>12.3e}"
              f"{np.mean(errores):>12.3e}{errores[-1]:>14.3e}")
    print("\n--- c_N: diferencia absoluta D_N entre las dos formas ---")
    print(f"Máximo: {np.max(diferencias_D):.3e}   Media: {np.mean(diferencias_D):.3e}   "
          f"En N=10000: {diferencias_D[-1]:.3e}")
    print(f"N en la lista donde las dos formas dan exactamente lo mismo (D_N = 0): "
          f"{sum(1 for d in diferencias_D if d == 0)} de {len(valores_de_N)}")
    plt.figure(figsize=(8, 5))
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_forma_inversa),
             label='Forma (1): 1/(sqrt(k^2+1)+k)', alpha=0.8)
    plt.plot(valores_de_N,
             reemplazar_ceros_para_grafico(errores_forma_resta),
             label='Forma (2): sqrt(k^2+1) - k', alpha=0.8)
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Error Relativo (contra Decimal)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('figuras/error_representaciones_cN.png', dpi=300,
                bbox_inches='tight')
    plt.close()
    plt.figure(figsize=(8, 5))
    plt.plot(valores_de_N, reemplazar_ceros_para_grafico(diferencias_D),
             label='D_N = |c_N(1) - c_N(2)|', color='tab:red', alpha=0.8)
    plt.yscale('log')
    plt.xlabel('Cantidad de términos (N)')
    plt.ylabel('Diferencia absoluta D_N')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('figuras/diferencia_DN_cN.png', dpi=300, bbox_inches='tight')
    plt.close()

def primer_k_con_error_mayor(valores_de_k, errores, umbral: float):
    # Primer k de la lista cuyo error relativo supera el umbral (None si ninguno lo supera).
    for k, error in zip(valores_de_k, errores):
        if error > umbral:
            return k
    return None

def experimento_bonus_terminos_de_c():
    # Bonus 2: Compara los dos términos individuales de c_N, sqrt(k^2+1) - k y 
    # 1/(sqrt(k^2+1) + k), cuando k crece. Se mide el error de cada uno contra Decimal y la 
    # diferencia absoluta entre ellos, y se busca desde qué k la pérdida de precisión es apreciable.
    # Los k van de 1 a 10^9 espaciados en escala logarítmica.
    valores_de_k = sorted({int(round(10 ** e)) for e in np.linspace(0, 9, 400)})
    errores_forma_inversa = []
    errores_forma_resta = []
    diferencias = []
    for k in valores_de_k:
        exacto = termino_c_exacto_decimal(k)
        t_inversa = termino_c_forma_inversa(k)
        t_resta = termino_c_forma_resta(k)
        errores_forma_inversa.append(error_relativo_contra_decimal(t_inversa, exacto))
        errores_forma_resta.append(error_relativo_contra_decimal(t_resta, exacto))
        diferencias.append(abs(t_inversa - t_resta))
    print("\n--- Bonus 2: términos de c_N, error relativo de cada forma ---")
    print(f"{'k':<8}{'sqrt(k^2+1) - k':>22}{'1/(sqrt(k^2+1)+k)':>22}"
          f"{'Error forma (2)':>18}{'Error forma (1)':>18}")
    for exponente in range(0, 10):
        k = 10 ** exponente
        t_inversa = termino_c_forma_inversa(k)
        t_resta = termino_c_forma_resta(k)
        exacto = termino_c_exacto_decimal(k)
        print(f"1e{exponente:<5}{t_resta:>22.12e}{t_inversa:>22.12e}"
              f"{error_relativo_contra_decimal(t_resta, exacto):>18.3e}"
              f"{error_relativo_contra_decimal(t_inversa, exacto):>18.3e}")
    print("\nPrimer k donde el error relativo de la forma (2) supera cada umbral:")
    for umbral in UMBRALES_PERDIDA_DE_PRECISION:
        k_umbral = primer_k_con_error_mayor(valores_de_k, errores_forma_resta, umbral)
        print(f"  error > {umbral:.0e}: k = {k_umbral}")
    print(f"Error máximo de la forma (1) en todo el rango: "
          f"{np.max(errores_forma_inversa):.3e}")
    figura, ejes = plt.subplots(2, 1, figsize=(8, 10))
    ejes[0].plot(valores_de_k, reemplazar_ceros_para_grafico(errores_forma_resta),
                 label='Forma (2): sqrt(k^2+1) - k', alpha=0.8)
    ejes[0].plot(valores_de_k, reemplazar_ceros_para_grafico(errores_forma_inversa),
                 label='Forma (1): 1/(sqrt(k^2+1)+k)', alpha=0.8)
    ejes[0].set_ylabel('Error Relativo (contra Decimal)')
    ejes[1].plot(valores_de_k, reemplazar_ceros_para_grafico(diferencias),
                 label='|forma (1) - forma (2)|', color='tab:red', alpha=0.8)
    ejes[1].set_ylabel('Diferencia absoluta entre las dos formas')
    for eje in ejes:
        eje.set_xscale('log')
        eje.set_yscale('log')
        eje.set_xlabel('k')
        eje.legend()
        eje.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    figura.savefig('figuras/error_bonus2_terminos_cN.png', dpi=300,
                   bbox_inches='tight')
    plt.close(figura)

if __name__ == "__main__":
    experimento_representaciones_de_b()
    experimento_bonus_uno_menos_inverso()
    experimento_representaciones_de_c()
    experimento_bonus_terminos_de_c()