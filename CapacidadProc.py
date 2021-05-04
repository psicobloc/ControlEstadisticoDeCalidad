import numpy as np
import pandas as pd
#import scipy.stats as stats
import matplotlib.pyplot as plt
#factores (constantes) para grupos de 4 observaciones
factorA2 = 0.729
factorD4 = 2.282
factorD3 = 0
#6 observaciones, 24 instancias
arrayDatos = np.array([[1010,991,985,986],
    [995,996,1009,1001],
    [990,1003,994,997],
    [1015,1020,998,981],
    [1013,1019,997,999],
    [994,1001,1009,1011],
    [989,992,1021,1000],
    [1001,986,1005,987],
    [1006,989,999,982],
    [992,1007,996,979],
    [996,1006,1009,989],
    [1019,996,978,999],
    [981,991,1000,1017],
    [1015,993,980,1009],
    [1023,1008,1000,998],
    [993,1011,987,998],
    [998,998,996,997],
    [999,995,1009,1000],
    [1020,1023,998,978],
    [1018,1016,990,983],
    [989,998,1010,999],
    [992,997,1023,1003],
    [988,1015,992,987],
    [1009,1011,1009,983],
    [991,996,980,972],
    [1000,989,990,994],
    [990,987,999,1008],
    [993,1001,1018,1020],
    [991,1017,988,999],
    [1020,999,987,1011]])
datos = pd.DataFrame(arrayDatos)
#calculo de rangos y promedios
rangos = datos.max(axis=1) - datos.min(axis=1) #axis=1 -> filas
rBarra = rangos.mean()
xBarra = datos.mean(axis=1)
xDobleBarra = xBarra.mean()
stdX = xBarra.std()
stdR = rangos.std()
# Valores carta R
#Limite superior de control
LSCr = factorD4 * rBarra
#Limite inferior de control = D3 * rBarra
LICr = factorD3 * rBarra
#Valores carta X
# Limite superior de control
LSCx = xDobleBarra + (factorA2 * rBarra)
# limite inferior de control
LICx = xDobleBarra - (factorA2 * rBarra)
fig, axs = plt.subplots(2, figsize = (21,21))
#Grafico carta X
axs[0].set_title('Carta X')
axs[0].set(xlabel='Número de muestra', ylabel = 'Promedio del diámetro')
axs[0].plot(xBarra, marker = 'x' , color = 'cyan')
axs[0].axhline(xDobleBarra, color='green', linestyle = 'dashdot')
axs[0].axhline(LSCx, color='red', linestyle='dashed')
axs[0].axhline(LICx, color='red', linestyle='dashed')
#Grafico carta R
axs[1].set_title('Carta R')
axs[1].set(xlabel='Número de muestra', ylabel = 'Rango del diámetro')
axs[1].plot(rangos, marker = 'x' , color = 'cyan')
axs[1].axhline(rBarra, color='green', linestyle = 'dashdot')
axs[1].axhline(LSCr, color='red', linestyle='dashed')
axs[1].axhline(LICr, color='red', linestyle='dashed')
#agregar textos
axs[1].text(0.5,3 , ('X Doble Barra= ' + str(round(xDobleBarra, 2))))
axs[1].text(4,3 , ('R Barra= ' + str(round(rBarra, 2))))
axs[1].text(8,3 , ('LSCx= ' + str(round(LSCx, 2))))
axs[1].text(12,3 , ('LICx= ' + str(round(LICx, 2))))
axs[1].text(17,3 , ('LSCr= ' + str(round(LSCr, 2))))
axs[1].text(20,3 , ('LICr= ' + str(round(LICr, 2))))
axs[1].text(24,3 , ('stdX= ' + str(round(stdX, 2))))
axs[1].text(28,3 , ('stdR= ' + str(round(stdR, 2))))
#Indice de capacidad potencial del proceso (Cp) PRIMER PROCESO
indCapacidadProc = (LSCx - LICx) / (6 * round(stdX, 2))
print('cp= ' + str(indCapacidadProc))
#indice de capacidad real (Cpk)
indCapacidadReal = min( ((LSCx - xDobleBarra) / (3 * round(stdX, 2))), ((xDobleBarra - LICx) / (3 * round(stdX, 2))))
print('cpk= ' + str(indCapacidadReal))
#densidad
distribucion = pd.DataFrame(xBarra).plot(kind='density', title='Capacidad de proceso')
#textos
distribucion.annotate('μ', xy=(xDobleBarra, 0.025), xytext=(xDobleBarra+1, 0.01))
distribucion.annotate('LIC', xy=(LICx, 0.01), xytext=(LICx-3, 0.04))
distribucion.annotate('LSC', xy=(LSCx, 0.01), xytext=(LSCx+1, 0.04))
distribucion.annotate('μ+3σ', xy=((xDobleBarra + (3*stdX)), 0.01), xytext=((xDobleBarra + (3*stdX))-4, 0.02))
distribucion.annotate('μ-3σ', xy=((xDobleBarra - (3*stdX)), 0.01), xytext=((xDobleBarra - (3*stdX))+0.5, 0.02))
# lineas
plt.axvline(LICx, linestyle='dotted', linewidth=1, color='red')
plt.axvline(xDobleBarra, linestyle='dashdot', linewidth=1, color='green')
plt.axvline((xDobleBarra + (3*stdX)), linestyle='dashdot', linewidth=1, color='#ef3df5')
plt.axvline((xDobleBarra - (3*stdX)), linestyle='dashdot', linewidth=1, color='#ef3df5')
plt.axvline(LSCx, linestyle='dotted', linewidth=1, color='red')
# mostrar todo
plt.show()
