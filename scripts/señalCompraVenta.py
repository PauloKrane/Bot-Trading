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

# Detectar intersecciones
#crossings = ((ema_min > ema_max) & (ema_min.shift(1) < ema_max.shift(1))) | ((ema_min < ema_max) & (ema_min.shift(1) > ema_max.shift(1)))

# Detectar puntos de cruce descendentes (punto "A")
crossings_descendentes= (ema_min < ema_max) & (ema_min.shift(1) > ema_max.shift(1))

# Detectar puntos de cruce ascendentes (punto "B")
crossings_ascendentes = (ema_min > ema_max) & (ema_min.shift(1) < ema_max.shift(1))

# Detectar puntos mínimo entre A Y B (punto "c")
"""
# Iterar sobre los datos de las EMAs (excepto el primer punto, ya que no tiene un punto anterior)
for i in range(1, len(ema_min)):
    if (ema_min < ema_max) & ema_min.shift(1)[i] < ema_max.shift(1)[i]:  
        punto_C_precio = data.index[i].Close
"""

# Obtener fechas de intersecciones
intersection_dates = data.index[crossings_ascendentes]
intersection_dates_A = data.index[crossings_descendentes]

# Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'], label='Precio de cierre', color='brown')
plt.plot(ema_min.index, ema_min, label= 'EMA (' + str(EMA_MIN) + ' días)', color='purple', linestyle='--')
plt.plot(ema_max.index, ema_max, label= 'EMA (' + str(EMA_MAX) + ' días)', color='blue', linestyle='--')
plt.scatter(intersection_dates, data.loc[intersection_dates]['Close'], marker='o', color='green', label='punto B (compra)')
plt.scatter(intersection_dates_A, data.loc[intersection_dates_A]['Close'], marker='o', color='red', label='puto A')
plt.title('Gráfico de Precios y EMAs con Intersecciones')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid(True)
plt.show()
