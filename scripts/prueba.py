import talib as ta
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import configuracion as cf

#Configuración 
CRYPTO = cf.CRYPTO 
FECHA_INICIO = cf.FECHA_INICIO
FECHA_FIN = cf.FECHA_FIN
INTERVALO = cf.INTERVALO
EMA_CORTA = cf.EMA_CORTA
EMA_LARGA = cf.EMA_LARGA

#Gráfico Bayesian methods for hackers style sheet
plt.style.use('bmh')

# Obtiene la información histórica
data = yf.download(CRYPTO, FECHA_INICIO  ,FECHA_FIN , interval = INTERVALO )

# Obtener la columna "Close"
precios_cierre = data['Close']

# Calcular la EMA_CORTA
ema_corta = ta.EMA(precios_cierre, timeperiod=EMA_CORTA)

# Calcular la EMA_LARGA
ema_larga = ta.EMA(precios_cierre, timeperiod=EMA_LARGA)

# Detectar puntos de cruce descendentes (punto "A")
a_cruces_descendentes= (ema_corta < ema_larga) & (ema_corta.shift(1) > ema_larga.shift(1))

# Detectar puntos de cruce ascendentes (punto "B")
b_cruces_ascendentes = (ema_corta > ema_larga) & (ema_corta.shift(1) < ema_larga.shift(1))

# Detectar puntos mínimo entre A Y B (punto "c")

def obtener_stop_loss(precios_cierre, a_cruces_descendentes, b_cruces_ascendentes):
    
    stop_loss = []
    min_stop_loss = None
    indice_stop_loss = None
    bandera = False  
    
    for i in range(len(precios_cierre)):
        if a_cruces_descendentes.iloc[i]:
            min_stop_loss = precios_cierre.iloc[i]
            indice_stop_loss = i
            bandera = True
        elif b_cruces_ascendentes.iloc[i]:
            stop_loss.append((indice_stop_loss, min_stop_loss))
            bandera = False
       
        if bandera and min_stop_loss is not None:
            close_price = precios_cierre.iloc[i]
            if close_price <= min_stop_loss:
                min_stop_loss = close_price
                indice_stop_loss = i

    return stop_loss 

stop_loss = obtener_stop_loss(precios_cierre, a_cruces_descendentes, b_cruces_ascendentes)

#Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'], label='Precio de cierre', color='brown')
plt.plot(ema_corta.index, ema_corta, label= 'EMA (' + str(EMA_CORTA) + ' días)', color='purple', linestyle='dashed')
plt.plot(ema_larga.index, ema_larga, label= 'EMA (' + str(EMA_LARGA) + ' días)', color='blue', linestyle='--')
plt.scatter(data.index[a_cruces_descendentes], precios_cierre[a_cruces_descendentes], color='red', marker='v', label='Punto A')
plt.scatter(data.index[b_cruces_ascendentes], precios_cierre[b_cruces_ascendentes], color='green', marker='^', label='Punto B (compra)')
plt.scatter([data.index[i[0]] for i in stop_loss], [i[1] for i in stop_loss], marker='o', color='yellow', label='Punto C (stop loss)')
plt.title(f'EMA({EMA_CORTA}) vs EMA({EMA_LARGA}) - {CRYPTO}')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid(True)
plt.show()

