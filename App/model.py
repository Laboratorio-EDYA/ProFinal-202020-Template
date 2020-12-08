"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer(size, loadfactor):
    analyzer = {'companyByTaxis': None,
                'companyByTrips': None,
                'datesByTaxis': None}
    analyzer['companyByTaxis'] = m.newMap(size,
                                        maptype = 'CHAINING',
                                        loadfactor = loadfactor,
                                        comparefunction = compareTaxisIds)
    analyzer['companyByTrips'] = m.newMap(size,
                                        maptype = 'CHAINING',
                                        loadfactor = loadfactor,
                                        comparefunction = compareTripsIds)
    analyzer['datesByTaxis'] = om.newMap(maptype = 'RBT',
                                        comparefunction = compareDatesIds)

    return analyzer

def add(analyzer, actual):
    addTaxis(analyzer, actual)
    addTrips(analyzer, actual)

def addTaxis(analyzer, actual):
    current = m.get(analyzer['companyByTaxis'],actual['company'])
    if current is None:
        mapa = m.newMap()
        m.put(analyzer['companyByTaxis'],actual['company'],mapa)
        current = m.get(analyzer['companyByTaxis'],actual['company'])['value']
        m.put(current, actual['taxi_id'], 1)
    else:
        value = m.get(current['value'], actual['taxi_id'])
        if value is None:
            m.put(current['value'], actual['taxi_id'], 1)
        else:
            m.put(current['value'], actual['taxi_id'], value['value'] + 1)

def addTrips(analyzer, actual):
    current = m.get(analyzer['companyByTrips'],actual['company'])
    if current is None:
        mapa = m.newMap()
        m.put(analyzer['companyByTrips'],actual['company'],mapa)
        current = m.get(analyzer['companyByTrips'],actual['company'])['value']
        m.put(current, actual['trip_id'], 1)
    else:
        value = m.get(current['value'], actual['trip_id'])
        if value is None:
            m.put(current['value'], actual['trip_id'], 1)
        else:
            m.put(current['value'], actual['trip_id'], value['value'] + 1)

def addDate(analyzer, actual):
    current = om.get(analyzer['datesByTaxis'], actual['trip_start_timestamp'])
    if current is None:
        mapa = m.newMap()
        om.put(analyzer['datesByTaxis'],actual['trip_start_timestamp'],mapa)
        current = om.get(analyzer['datesByTaxis'],actual['trip_start_timestamp'])['value']
        money = float(actual['trip_total'])
        millas = float(actual['trip_miles'])
        puntos = millas/money
        om.put(current, actual['taxi_id'], [money,millas,1,puntos])
    else:
        value = om.get(current['value'], actual['taxi_id'])
        if value is None:
            money = float(actual['trip_total'])
            millas = float(actual['trip_miles'])
            puntos = millas/money
            om.put(current, actual['taxi_id'], [money,millas,1,puntos])
        else:
            money = value['value'][0] + float(actual['trip_total'])
            millas = value['value'][1] + float(actual['trip_miles'])
            total = value['value'][2] + 1
            puntos = (millas/money)*total
            om.put(current, actual['taxi_id'], [money,millas,total,puntos])
# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex']),om.height(analyzer['timeIndex'])

def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex']),om.size(analyzer['timeIndex'])

def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])

def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    return lst

def getAccidentsByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    accidentdate = om.get(analyzer['dateIndex'], initialDate)
    if accidentdate['key'] is not None:
        offensemap = me.getValue(accidentdate)['offenseIndex']
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstoffenses'])
        return 0

# ==============================
# Funciones Helper
# ==============================
def gradosAkilometros2(x):
    a=x.split('.')
    try:
        return str(a[0])+'.'+str(a[1])+str(a[2])
    except:
        return str(a[0])+'.'+str(a[1])    

# ==============================
# Requerimientos
# ==============================
def

# ==============================
# Funciones de Comparacion
# ==============================
def compareTaxisIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareTripsIds(trip1, trip2):
    if (trip1 == trip2):
        return 0
    elif trip1 > trip2:
        return 1
    else:
        return -1
def compareDatesIds(date1, date2):
    if (date1 == date2):
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1