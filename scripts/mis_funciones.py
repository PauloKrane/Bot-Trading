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

def obtener_take_profit(precios_cierre, a_cruces_descendentes, b_cruces_ascendentes):
    take_profit = []
    stop_loss = None
    indice_stop_loss = None
    en_operacion = False  
    
    for i in range(len(precios_cierre)):
        if a_cruces_descendentes.iloc[i]:
            stop_loss = precios_cierre.iloc[i]
            indice_stop_loss = i
            en_operacion = True
        elif b_cruces_ascendentes.iloc[i] and en_operacion:
            porcentaje = precios_cierre.iloc[i] - stop_loss
            precio_take_profit = precios_cierre.iloc[i] + porcentaje
            take_profit.append((i, precio_take_profit))
            en_operacion = False
       
        if en_operacion and stop_loss is not None:
            precio_cierre = precios_cierre.iloc[i]
            if precio_cierre <= stop_loss:
                stop_loss = precio_cierre
                indice_stop_loss = i

    return take_profit