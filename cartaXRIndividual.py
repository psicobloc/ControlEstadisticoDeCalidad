import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#factores para cartas individuales (n=2)
factorD2 = 1.128
factorD4 = 3.268
factorD3 = 0

#5 observaciones por grupo (5 atributos por instancia)


datos = pd.read_csv("datos.csv")

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
axs[1].text(3.5,3.5 , ('X Doble Barra= ' + str(round(xDobleBarra, 2))))
axs[1].text(8,3.5 , ('R Barra= ' + str(round(rBarra, 2))))
axs[1].text(11,3.5 , ('LSCx= ' + str(round(LSCx, 2))))
axs[1].text(14,3.5 , ('LICx= ' + str(round(LICx, 2))))
axs[1].text(17,3.5 , ('LSCr= ' + str(round(LSCr, 2))))
axs[1].text(20,3.5 , ('LICr= ' + str(round(LICr, 2))))
axs[1].text(22,3.5 , ('stdX= ' + str(round(stdX, 2))))
axs[1].text(25,3.5 , ('stdR= ' + str(round(stdR, 2))))

plt.show()
