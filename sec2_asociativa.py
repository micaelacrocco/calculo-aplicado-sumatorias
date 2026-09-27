import matplotlib.pyplot as plt
from typing import List, Union

def sumaInt(N:int, b:int):
    """Sumatoria solo con valores int. 
    Imprime los resultados y genera png de las graficas.
    """
    resultado1 = resultado2 =resultado3 = 0
    k1=k2=k3=0
    x=[]
    y1=[]
    y2=[]
    y3=[]
    while k1<N:
        resultado1 += (1 + b**k1 - b **k1)
        x.append(k1)
        y1.append(resultado1)
        k1+=1
    while k2<N:
        resultado2 += (1 + b**k2) - b **k2
        y2.append(resultado2)
        k2+=1
    while k3<N:
        resultado3 += (1 - b**k3) + b **k3
        y3.append(resultado3)
        k3+=1
    print(f"Resultado 1:{resultado1}\nResultado 2:{resultado2}\nResultado 3:{resultado3}")
    return x,y1,y2,y3

def sumaFloat(N:float, b:float)->float:
    """Sumatoria solo con valores float. 
    Imprime los resultados y genera png de las graficas. """
    resultado1 = resultado2 =resultado3 = 0
    k1=k2=k3=0
    x=[]
    y1=[]
    y2=[]
    y3=[]
    try:
        while k1<N:
            resultado1 += (1 + b**k1 - b **k1)
            x.append(k1)
            y1.append(resultado1)
            k1+=1
    except OverflowError:
        print(f"b={b}: overflow en k={k1}, se corta la serie ahí")
    try:
        while k2<N:
            resultado2 += (1 + b**k2) - b **k2
            y2.append(resultado2)
            k2+=1
    except OverflowError:
            print(f"b={b}: overflow en k={k2}, se corta la serie ahí")
    try:
        while k3<N:
            resultado3 += (1 - b**k3) + b **k3
            y3.append(resultado3)
            k3+=1
    except OverflowError:
           print(f"b={b}: overflow en k={k3}, se corta la serie ahí")
    print(f"Resultado 1:{resultado1}\nResultado 2:{resultado2}\nResultado 3:{resultado3}")
    return x,y1,y2,y3

def graficar(arrayNumeros:Union[List[int], List[float]],floatBool:bool):
    """Grafica segun el array de numeros, toma tanto array de int como de float. """
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))
    for b in arrayNumeros:
        x, y1, y2, y3 = sumaFloat(1000,b) if floatBool is True else sumaInt(1000,b)
        axes[0].plot(x, y1, label=f'b={b}')
        axes[1].plot(x, y2, label=f'b={b}')
        axes[2].plot(x, y3, label=f'b={b}')

    axes[0].set_title('Resultado 1: (1 + b^k - b^k)')
    axes[1].set_title('Resultado 2: (1 + b^k) - b^k')
    axes[2].set_title('Resultado 3: (1 - b^k) + b^k')

    for ax in axes:
        ax.legend()
        ax.set_xlabel('k')
        ax.set_ylabel('a_N')
    plt.tight_layout()
    fig.savefig('./figuras/GraficasFloat.png') if floatBool is True else fig.savefig('./figuras/GraficasInt.png')
    plt.close(fig)
graficar([2,3,5,10],False)
graficar([2.0,3.0,5.0,10.0],True)