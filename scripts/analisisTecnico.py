import talib as ta
import matplotlib.pyplot as plt
import yfinance as yf

#Gráfico Bayesian methods for hackers style sheet
plt.style.use('bmh')

#Configuración 
CRYPTO = 'BTC-USD' # Símbolo criptomoneda 
FECHA_INICIO = '2024-02-01' #Fecha de inicio desde la cual se desean descargar los datos
FECHA_FIN = '2024-03-14' #fecha de finalización hasta la cual se desean descargar los datos.
INTERVALO = '5m' #  Intervalo de tiempo de los datos que se están descargando.
EMA_MIN = 9 # Valor mínimo que se utilizará para calcular el promedio móvil exponencial. 
EMA_MAX = 300 # valor máximo que se utilizará para calcular el promedio móvil exponencial. 

# Obtiene la información histórica
data = yf.download(CRYPTO, FECHA_INICIO  ,FECHA_FIN , interval = INTERVALO )

# Obtener la columna "Close"
precios_cierre = data['Close']

# Calcular la EMA_MIN
ema_min = ta.EMA(precios_cierre, timeperiod=EMA_MIN)

# Calcular la EMA_MAX
ema_max = ta.EMA(precios_cierre, timeperiod=EMA_MAX)

# Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(data.index, data.Close, label='Precio', color='green')
plt.plot(data.index, ema_min, label='EMA corta (9 días)', color='red', linestyle='--')
plt.plot(data.index, ema_max, label='EMA larga (300 días)', color='blue', linestyle='--') 
plt.title('Gráfico de Precios y EMAs para' + CRYPTO)
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid(True)
plt.show()

