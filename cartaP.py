import math
import pandas as pd
import matplotlib.pyplot as plt
tamano_muestra = 100
bandera_paso = False
iter = 0
lsupAnterior = -5
linfAnterior = -5
pBarraAnterior = -5
datos = pd.read_csv('data.csv', header=None)
fraccion_defectuosa = datos.divide(tamano_muestra)
while bandera_paso == False:
    iter +=1
    fraccion_defectuosa = datos.divide(tamano_muestra)
    numero_muestras = datos.count().loc[0] #alfredo no cambia esto, se mantiene 25 en todas las iteraciones
    p_barra = datos.sum() / (numero_muestras * tamano_muestra) #
    p_barra = p_barra.loc[0]
    print('Iteración:' + str(iter))
    print('Fraccion defectuosa:')
    print(fraccion_defectuosa)
    print('numero_muestras: ' + str(numero_muestras))
    print('Total de muestras defectuosas: ' + str(datos.sum().loc[0]))
    print('p_barra: ' + str(p_barra))
    termino_raiz = ((p_barra * (1-p_barra))/tamano_muestra)**(1/2) #variable auxiliar para no calcular la raiz cuadrada varias veces
    limite_superiror = p_barra + (3*termino_raiz)
    limite_inferiror = p_barra - (3*termino_raiz)
    if (limite_inferiror < 0):
        limite_inferiror = 0
    print('Límite superior: ' + str(limite_superiror))
    print('Límite inferior: ' + str(limite_inferiror))
    #graficar
    plt.figure(iter)
    axs = plt.axes()
    axs.set_title('Carta P ' + str(iter))
    axs.set(xlabel = 'Número de muestra', ylabel='Fracción defectuosa')
    axs.plot(fraccion_defectuosa, marker = 'x', color='black')
    axs.axhline(p_barra, color='green', linestyle='dashdot')
    axs.axhline(limite_superiror, color='red', linestyle='dashed')
    axs.text(10, (limite_superiror - 0.007), ('LSC:' + str(round(limite_superiror,4))))
    axs.axhline(limite_inferiror, color='red', linestyle='dashed')
    axs.text(5, (limite_inferiror + 0.004), ('LIC:' + str(round(limite_inferiror,4))))
    #mostrar límites y p_barra de la iteración anterior
    if (lsupAnterior != -5):
        axs.axhline(lsupAnterior, color='pink', linestyle='dashed')
        axs.axhline(linfAnterior, color='pink', linestyle='dashed')
        axs.axhline(pBarraAnterior, color='green', linestyle='dashdot') #cambiar a verde claro
        axs.plot(outliersHi, marker='x', color='blue', linestyle='none')
        axs.plot(outliersLow, marker='x', color='blue', linestyle='none')
    lsupAnterior = limite_superiror
    linfAnterior = limite_inferiror
    pBarraAnterior = p_barra
    outliersHi = fraccion_defectuosa.loc[fraccion_defectuosa[0] > limite_superiror]
    outliersLow = fraccion_defectuosa.loc[fraccion_defectuosa[0] < limite_inferiror]
    print('Outliers sobre límite superior ')
    print(outliersHi)
    print('Outliers bajo el límite inferior ')
    print(outliersLow)
    #eliminar si fraccion_defectuosa[i] > limite_superiror or fraccion_defectuosa[i] < limite_inferiror
    datos = datos.loc[fraccion_defectuosa[0] <= limite_superiror]
    datos = datos.loc[fraccion_defectuosa[0] >= limite_inferiror]
    if outliersHi.empty == True and outliersLow.empty == True:
        bandera_paso = True #ya pasó, termina while
        print('termino en iter= ' + str(iter))
plt. show()
