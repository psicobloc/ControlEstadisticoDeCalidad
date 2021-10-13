import pandas as pd
import matplotlib.pyplot as plt

bandera_paso = False
bandera_variacion_aceptable = False
iter = 0
lsupAnterior = -5
linfAnterior = -5
pBarraAnterior = -5
datos = pd.read_csv('data.csv', header=None)
tamano_prom_muestra = datos.loc[:,1].mean()
diffMaxMean = abs((1-(datos.loc[:,1].max() / tamano_prom_muestra)) * 100)
diffMinMean = abs((1-(datos.loc[:,1].min() / tamano_prom_muestra)) * 100)
print("Tamaño promedio de muestra: " + str(tamano_prom_muestra))
print("Diferencia con mínimo: " + str(diffMinMean) + "%")
print("Diferencia con máximo: " + str(diffMaxMean) + "%")

#si la dif entre el max y el promedio, y entre el min y el promedio  es < a 20%, usamos el promedio
#si variacion es mayor al 20% calculamos los límites de control para cada muestra individualmente
#al graficar los limites no aparece una sola linea recta,
#esta escalonada en cada punto con diferente tamaño de muestra

if diffMaxMean < 20.00 and diffMinMean < 20.00:
    bandera_variacion_aceptable = True
    print("variacion aceptable, menor a 20%")
    tamano_muestra = tamano_prom_muestra

# Primera Opcion, si la variacion es menor a 20%, usamos el promedio de los tamaños de muestra
while bandera_paso == False and bandera_variacion_aceptable == True:
    iter +=1
    fraccion_defectuosa = datos.loc[:,0].divide(tamano_muestra)
    numero_muestras = datos.count().loc[0]
    p_barra = datos.loc[:,0].sum() / (numero_muestras * tamano_muestra)
    termino_raiz = ((p_barra * (1-p_barra))/tamano_muestra)**(1/2) #para no calcular la raiz cuadrada varias veces
    limite_superiror = p_barra + (3*termino_raiz)
    limite_inferiror = p_barra - (3*termino_raiz)
    if (limite_inferiror < 0):
        limite_inferiror = 0

    print('Iteración:' + str(iter))
    print('Fraccion defectuosa:')
    print(fraccion_defectuosa)
    print('numero_muestras: ' + str(numero_muestras))
    print('Total de muestras defectuosas: ' + str(datos.sum().loc[0]))
    print('p_barra: ' + str(p_barra))
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
        axs.axhline(pBarraAnterior, color='#87ff87', linestyle='dashdot')
        axs.plot(outliersHi, marker='x', color='blue', linestyle='none')
        axs.plot(outliersLow, marker='x', color='blue', linestyle='none')

    lsupAnterior = limite_superiror
    linfAnterior = limite_inferiror
    pBarraAnterior = p_barra
    outliersHi = fraccion_defectuosa.loc[fraccion_defectuosa > limite_superiror]
    outliersLow = fraccion_defectuosa.loc[fraccion_defectuosa < limite_inferiror]
    print('Outliers sobre límite superior ')
    print(outliersHi)
    print('Outliers bajo el límite inferior ')
    print(outliersLow)
    #eliminar si fraccion_defectuosa[i] > limite_superiror or fraccion_defectuosa[i] < limite_inferiror
    datos = datos.loc[fraccion_defectuosa <= limite_superiror]
    datos = datos.loc[fraccion_defectuosa >= limite_inferiror]
    if outliersHi.empty == True and outliersLow.empty == True:
        bandera_paso = True #ya pasó, termina while
        print('termino en iter= ' + str(iter))

#Segunda Opcion, calcular los límites de control individualmente por cada lote
listaFraccionesDefectuosas = []
dictFraccDefConIndex = {}
dictFueraDeControl = {}
lenDictFueraControl = 0

while bandera_paso == False and bandera_variacion_aceptable == False:
    iter +=1
    iterLote = 0
    p_barra = datos.loc[:,0].sum() / datos.loc[:,1].sum()
    listaFraccionesDefectuosas.clear()
    dictFraccDefConIndex.clear()
    limSupAnterior = 0.103
    limInfAnterior = 0.006
    plt.figure(iter)
    axs = plt.axes()
    axs.set_title('Carta P ' + str(iter))
    axs.set(xlabel = 'Número de muestra', ylabel='Fracción defectuosa')
    print("Iteración: " + str(iter))
    print("p barra: " + str(p_barra))

    for lote in datos.itertuples():
        #calcular fraccion defectuosa del lote
        fraccion_defectuosa = lote[1]/lote[2]
        #agregar fraccion defectuosa a la lista
        listaFraccionesDefectuosas = listaFraccionesDefectuosas + [fraccion_defectuosa]
        dictFraccDefConIndex.update({lote[0]:fraccion_defectuosa})
        #calcular los límites para el lote
        termino_raiz = ((p_barra * (1-p_barra))/lote[2])**(1/2)
        limite_superiror = p_barra + (3*termino_raiz)
        limite_inferiror = p_barra - (3*termino_raiz)
        print ("lote : " + str(iterLote)  + " fracc def: " + str(fraccion_defectuosa) )
        print("LS: " + str(limite_superiror))
        print("LI: " + str(limite_inferiror))
        #plotear lineas de los límites
        #linea vertical, en y va del limite anterior al limite nuevo, en x va en punto(lote[0]) -0.5
        axs.plot([(lote[0]-0.5),(lote[0]-0.5)], [limSupAnterior,limite_superiror])
        axs.plot([(lote[0]-0.5),(lote[0]-0.5)], [limInfAnterior,limite_inferiror])
        #linea horizontal en y va en el limite nuevo, en x va de lote[0] -0.5 a lote[0] + 0.5
        axs.plot([(lote[0]-0.5),(lote[0]+0.5)], [limite_superiror,limite_superiror])
        axs.plot([(lote[0]-0.5),(lote[0]+0.5)], [limite_inferiror,limite_inferiror])
        #guardar limites para la siguiente iteracion
        limSupAnterior = limite_superiror
        limInfAnterior = limite_inferiror

        if fraccion_defectuosa < limite_inferiror or fraccion_defectuosa > limite_superiror:
            print("lote " + str(iterLote) + " fuera de control ")
            #si la fraccion defectuosa del lote esta fuera de los límites, agregar a la lista
            dictFueraDeControl.update({lote[0]:fraccion_defectuosa})

        print()
        iterLote +=1

    fraccDefDataF = pd.DataFrame.from_dict(dictFraccDefConIndex, orient='index')
    print("dictFueraDeControl")
    print(dictFueraDeControl)

    #graficar datos
    axs.plot(fraccDefDataF, marker = 'x', color='black', label='Muestras')
    axs.axhline(p_barra, color='green', linestyle='dashdot')
    #plotear lista fuera de control
    fueraDeControlDF = pd.DataFrame.from_dict(dictFueraDeControl, orient='index')
    axs.plot(fueraDeControlDF, marker='x', color='red')
    #eliminar las instancias fuera de control para la siguiente iteracion
    datosLimSup = datos.loc[listaFraccionesDefectuosas <= limite_superiror]
    listaFraccionesDefectuosas = list(filter(lambda ratio: ratio <= limite_superiror, listaFraccionesDefectuosas))
    datosLimInf = datosLimSup.loc[listaFraccionesDefectuosas >= limite_inferiror]
    datos = datosLimInf

    if len(dictFueraDeControl) == lenDictFueraControl:
        #si no hay instancias fuera de control nuevas en esta iteración, la carta p ha pasado.
        bandera_paso = True
        print("termino en iteracion: " + str(iter))
    else:
        lenDictFueraControl = len(dictFueraDeControl)

plt. show()
