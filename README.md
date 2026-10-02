# Cálculo Aplicado - Implementación de Sumatorias

Trabajo práctico de la asignatura Cálculo Aplicado (Facultad de Ingeniería y Tecnología, UCU) sobre optimización numérica en una dimensión: se estudian fenómenos de error numérico (asociatividad, conmutatividad y representaciones equivalentes de una suma) al implementar sumatorias en Python.

## Estructura del repositorio

```
.
├── figuras/                   # Gráficos generados
├── main.py                    # Punto de entrada: ejecuta todo
├── requirements.txt
├── sec2_asociativa.py         # Sección 2: propiedad asociativa
├── sec3_conmutativa.py        # Sección 3: propiedad conmutativa
├── sec4_representaciones.py   # Sección 4: representaciones de una suma
└── utils.py                   # Funciones auxiliares
```

## Contenido de cada sección

- **Sección 2 — Propiedad asociativa:** implementación de `a_N = Σ(1 + b^k − b^k)` con tres asociaciones distintas de los términos, comparando resultados con `b` de tipo `int` y `float`.
- **Sección 3 — Propiedad conmutativa:** cuatro algoritmos de suma (mayor a menor módulo, menor a mayor módulo, orden aleatorio y suma de Kahan) para `b_N = Σ 1/(k(k+1))`, comparando el error relativo respecto al valor teórico `N/(N+1)`.
- **Sección 4 — Representaciones de una suma:** comparación de formas matemáticamente equivalentes pero numéricamente distintas para `b_N` y `c_N`, incluyendo el análisis de cancelación catastrófica.

## Instalación

1. Cloná el repositorio:
```bash
   git clone https://github.com/micaelacrocco/calculo-aplicado-sumatorias.git
   cd calculo-aplicado-sumatorias
```

2. (Recomendado) Creá un entorno virtual:
```bash
   python -m venv venv
```

3. Activá el entorno virtual según tu sistema operativo:

   | Sistema | Comando |
   |---|---|
   | Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
   | Windows (CMD) | `venv\Scripts\activate.bat` |
   | Linux / macOS | `source venv/bin/activate` |

   > En PowerShell, si aparece un error de ejecución de scripts, corré antes
   > `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

4. Instalá las dependencias:
```bash
   pip install -r requirements.txt
```

## Ejecución

Para correr todos los experimentos y generar los gráficos:

```bash
python main.py
```
> **Nota:** la ejecución completa puede tardar varios minutos principalmente por la Sección 3 > (cuatro algoritmos con hasta 1.000.000 de términos).

También se puede ejecutar cada sección de forma independiente:

```bash
python sec2_asociativa.py
python sec3_conmutativa.py
python sec4_representaciones.py
```

## Integrantes

- Emilio Rodriguez
- Micaela Crocco
- Nicolas Márquez
- Gonzalo Juarez

