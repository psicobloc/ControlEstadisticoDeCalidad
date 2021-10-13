import pandas as pd
import matplotlib.pyplot as plt
tamano_muestra = 120 #N
bandera_paso = False
iter = 0
lsupAnterior = -5
linfAnterior = -5
licentAnterior = -5
datos = pd.read_csv('data.csv', header=None)
articulos_defectuosos = datos
outLanterior = pd.Series()
outFinal = pd.Series()

while bandera_paso == False:
    iter +=1
    articulos_defectuosos = datos
    numero_muestras = datos.count().loc[0]
    p_barra = datos.sum() / (numero_muestras * tamano_muestra) #
    p_barra = p_barra.loc[0]
    #prints
    print('Iteración:' + str(iter))
    print('Artículos defectuosos:')
    print(articulos_defectuosos)
    print('numero_muestras: ' + str(numero_muestras))
    print('Total de muestras defectuosas: ' + str(datos.sum().loc[0]))
    print('p_barra: ' + str(p_barra))
    desviacion_estandar = ((tamano_muestra * p_barra) * (1 - p_barra))**(1/2)
    #límites
    limite_central = p_barra * tamano_muestra
    limite_superiror = limite_central + (3 * desviacion_estandar)
    limite_inferiror = limite_central - (3 * desviacion_estandar)
    if (limite_inferiror < 0):
        limite_inferiror = 0

    print('Límite Central: ' + str(limite_central))
    print('Límite Superior: ' + str(limite_superiror))
    print('Límite Inferior: ' + str(limite_inferiror))
    #graficar
    plt.figure(iter)
    axs = plt.axes()
    axs.set_title('Carta nP ' + str(iter))
    axs.set(xlabel = 'Número de muestra', ylabel='Artículos defectuosos')
    axs.plot(articulos_defectuosos, marker = 'x', color='black')
    axs.axhline(limite_central, color='green', linestyle='dashdot')
    axs.text(20, (limite_central - 4), ('LCC:' + str(round(limite_central,4))))
    axs.axhline(limite_superiror, color='red', linestyle='dashed')
    axs.text(5, (limite_superiror - 2), ('LSC:' + str(round(limite_superiror,4))))
    axs.axhline(limite_inferiror, color='red', linestyle='dashed')
    axs.text(10, (limite_inferiror + 2), ('LIC:' + str(round(limite_inferiror,4))))
    #mostrar límites de la iteración anterior
    if (lsupAnterior != -5):
        axs.axhline(lsupAnterior, color='pink', linestyle='dashed')
        axs.axhline(linfAnterior, color='pink', linestyle='dashed')
        axs.axhline(licentAnterior, color='blue', linestyle='dashdot')
        axs.plot(outFinal, marker='x', color='blue')

    lsupAnterior = limite_superiror
    linfAnterior = limite_inferiror
    licentAnterior = limite_central
    #outliers
    outliersHi = articulos_defectuosos.loc[articulos_defectuosos[0] >= limite_superiror]
    outliersLow = articulos_defectuosos.loc[articulos_defectuosos[0] <= limite_inferiror]
    outLanterior = pd.concat([outliersHi, outliersLow], axis=0)
    print('Outliers sobre límite superior ')
    print(outliersHi)
    print('Outliers bajo el límite inferior ')
    print(outliersLow)
    outFinal = pd.concat([outFinal, outLanterior], axis=0)
    # print("out df final")
    # print(outFinal)
    datos = datos.loc[articulos_defectuosos[0] < limite_superiror]
    datos = datos.loc[articulos_defectuosos[0] > limite_inferiror]
    if outliersHi.empty == True and outliersLow.empty == True: #ya paso las especificaciones, termina while
        bandera_paso = True
        print('termino en iter= ' + str(iter))
plt. show()
