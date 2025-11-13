from collections import namedtuple

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """

    if estacion.capacidad == 0:
        return "gray"
    disponibilidad = estacion.bicicletas_disponibles / estacion.capacidad

    if disponibilidad >= 2/3:
        return "green"
    elif disponibilidad >= 1/3:
        return "orange"
    elif disponibilidad > 0:
        return "red"

def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    total_bicicletas_libres = 0
    total_capacidad = 0
    total_estaciones = 0

    for estaciones in estaciones:
        total_bicicletas_libres += estaciones[6]
        total_capacidad += estaciones[4]
        total_estaciones += 1
    
    porcentaje_ocupacion = (1-total_bicicletas_libres/total_capacidad)*100
    
    return total_bicicletas_libres, total_capacidad, porcentaje_ocupacion, total_estaciones

def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    direccion_parcial = direccion_parcial.lower()

    resultado = []
    for est in estaciones:
        direccion_estacion = est.direccion.lower()
        if direccion_parcial in direccion_estacion:
            resultado.append(est)
    return resultado

def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    resultado = []

    for est in estaciones:
        if est.capacidad > 0:
            disponibilidad = est.bicicletas_disponibles / est.capacidad
            if disponibilidad >= min_disponibilidad:
                resultado.append(est)

    return resultado

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea entre los dos puntos
    """
    lat1, lon1 = p1
    lat2, lon2 = p2

    distancia = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    return distancia

def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """ 
    estacion_mas_cercana = None
    distancia_minima = float("inf")

    for est in estaciones:
        if est.bicicletas_disponibles > 0:
            distancia = calcula_distancia((est.latitud, est.longitud), punto)
            if distancia < distancia_minima:
                distancia_minima = distancia
                estacion_mas_cercana = est

    return estacion_mas_cercana

def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    estacion_origen = busca_estacion_mas_cercana(estaciones, origen)

    # Para el destino, buscamos la estación más cercana con al menos un puesto libre
    estaciones_con_puestos = [e for e in estaciones if e.puestos_libres > 0]
    estacion_destino = None
    if estaciones_con_puestos:
        estacion_destino = min(
            estaciones_con_puestos,
            key=lambda e: calcula_distancia((e.latitud, e.longitud), destino)
        )

    return estacion_origen, estacion_destino

