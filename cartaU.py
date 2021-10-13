import pandas as pd
import matplotlib.pyplot as plt

bandera_paso = False
iter = 0
dictFraccDefConIndex = {}
dictFueraDeControl = {}
dictBajoControl ={}
lenDictFueraControl = 0
datos = pd.read_csv('data_U.csv', header=None)

while bandera_paso == False:
    iter +=1
    iterLote = 0
    dictFraccDefConIndex.clear()
    dictBajoControl.clear()
    limSupAnterior = 1.73
    limInfAnterior = 0.35

    numeros_de_defectos= datos.loc[:,0]
    tamanos_de_muestras= datos.loc[:,1]
    u_barra = numeros_de_defectos.sum() / tamanos_de_muestras.sum()

    plt.figure(iter)
    axs = plt.axes()
    axs.set_title('Carta U ' + str(iter))
    axs.set(xlabel = 'Número de lote', ylabel='Fracción defectiva')
    print("Iteración: " + str(iter))
    print("U barra: " + str(u_barra))

    for lote in datos.itertuples():
        #calcular fraccion defectuosa del lote
        fraccion_defectuosa = lote[1]/lote[2]
        dictFraccDefConIndex.update({lote[0]:fraccion_defectuosa})
        #calcular los límites para el lote
        termino_raiz = ((u_barra)/lote[2])**(1/2)
        limite_superiror = u_barra + (3*termino_raiz)
        limite_inferiror = u_barra - (3*termino_raiz)
        if limite_inferiror <0:
            limite_inferiror =0
        print ("lote : " + str(iterLote)  + " fracc def: " + str(fraccion_defectuosa) )
        print("LS: " + str(limite_superiror))
        print("LI: " + str(limite_inferiror))
        #plotear lineas de los límites, verticales:
        axs.plot([(lote[0]-0.5),(lote[0]-0.5)], [limSupAnterior,limite_superiror])
        axs.plot([(lote[0]-0.5),(lote[0]-0.5)], [limInfAnterior,limite_inferiror])
        #lineas horizontales:
        axs.plot([(lote[0]-0.5),(lote[0]+0.5)], [limite_superiror,limite_superiror])
        axs.plot([(lote[0]-0.5),(lote[0]+0.5)], [limite_inferiror,limite_inferiror])
        #guardar limites para la siguiente iteracion
        limSupAnterior = limite_superiror
        limInfAnterior = limite_inferiror

        if fraccion_defectuosa < limite_inferiror or fraccion_defectuosa > limite_superiror:
            print("lote " + str(iterLote) + " fuera de control ")
            #si la fraccion defectuosa del lote esta fuera de los límites, agregar a la lista
            dictFueraDeControl.update({lote[0]:fraccion_defectuosa})
        else:
            #agregar a dict bajo control
            dictBajoControl.update({lote[0]:[lote[1],lote[2]]})

        print()
        iterLote +=1

    fraccDefDataF = pd.DataFrame.from_dict(dictFraccDefConIndex, orient='index')
    df_bajo_control = pd.DataFrame.from_dict(dictBajoControl, orient='index')
    #graficar datos
    axs.plot(fraccDefDataF, marker = 'x', color='black', label='Muestras')
    axs.axhline(u_barra, color='green', linestyle='dashdot')
    #plotear lista fuera de control
    fueraDeControlDF = pd.DataFrame.from_dict(dictFueraDeControl, orient='index')
    axs.plot(fueraDeControlDF, marker='x', color='red', label='fueraControl')
    #mantener solo los datos bajo control para la siguiente iteracion
    datos = df_bajo_control

    if len(dictFueraDeControl) == lenDictFueraControl:
        #si no hay instancias fuera de control nuevas en esta iteración, la carta p ha pasado.
        bandera_paso = True
        print("termino en iteracion: " + str(iter))
    else:
        lenDictFueraControl = len(dictFueraDeControl)

plt. show()
