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

# Detectar puntos de cruce descendentes (A)
a_cruces_descendentes= (ema_corta < ema_larga) & (ema_corta.shift(1) > ema_larga.shift(1))

# Detectar puntos de cruce ascendentes (B)
b_cruces_ascendentes = (ema_corta > ema_larga) & (ema_corta.shift(1) < ema_larga.shift(1))

# Detectar puntos C entre A Y B (stop_loss)
stop_loss = cf.obtener_stop_loss(precios_cierre, a_cruces_descendentes, b_cruces_ascendentes)

# Detectar puntos D (take_profit)
take_profit = cf.obtener_take_profit(precios_cierre, a_cruces_descendentes, b_cruces_ascendentes)

#Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'], label='Precio de cierre', color='brown')
plt.plot(ema_corta.index, ema_corta, label= 'EMA (' + str(EMA_CORTA) + ' días)', color='purple', linestyle='dashed')
plt.plot(ema_larga.index, ema_larga, label= 'EMA (' + str(EMA_LARGA) + ' días)', color='blue', linestyle='dotted')
plt.scatter(data.index[a_cruces_descendentes], precios_cierre[a_cruces_descendentes], color='red', marker='v', label='Punto A')
plt.scatter(data.index[b_cruces_ascendentes], precios_cierre[b_cruces_ascendentes], color='green', marker='^', label='Punto B (compra)')
plt.scatter([data.index[i[0]] for i in stop_loss], [i[1] for i in stop_loss], marker='o', color='yellow', label='Punto C (stop loss)')
plt.scatter([data.index[i[0]] for i in take_profit], [i[1] for i in take_profit], marker='o', color='orange', label='Punto D (Take_profit)')
plt.title(f'EMA({EMA_CORTA}) vs EMA({EMA_LARGA}) - {CRYPTO}')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid(True)
for i in range(len(data.index[b_cruces_ascendentes])):
    plt.text(data.index[b_cruces_ascendentes][i], precios_cierre[b_cruces_ascendentes][i], f'({precios_cierre[b_cruces_ascendentes][i]:.2f})', fontsize=8, ha='right')
for i , close in stop_loss:
    plt.text(data.index[i], close, f'({close:.2f})', fontsize=8, ha='right')
for i, valor in take_profit:
    plt.text(data.index[i], valor, f'({valor:.2f})', fontsize=8, ha='right')
plt.show()

