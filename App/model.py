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
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om

import datetime 

from DISClib.Algorithms.Sorting import mergesort as ms

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""
#datetime.datetime.strptime(hora,'%Y-%m-%d')
#datetime.datetime.strptime(hora,'%H:%M')
# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer(size, loadfactor):
    analyzer = {'companyByTaxis': None,
                'companyByTrips': None,
                'datesByTaxis': None,
                'graph':None}
    analyzer['companyByTaxis'] = m.newMap(size,
                                        maptype = 'CHAINING',
                                        loadfactor = loadfactor,
                                        comparefunction = compareTaxis)
    analyzer['companyByTrips'] = m.newMap(size,
                                        maptype = 'CHAINING',
                                        loadfactor = loadfactor,
                                        comparefunction = compareTrips)
    analyzer['datesByTaxis'] = om.newMap(omaptype = 'RBT',
                                        comparefunction = compareDates)
    analyzer['graph'] = gr.newGraph(datastructure = "ADJ_LIST",
                                    size = size,
                                    comparefunction = compareCommunity)
    return analyzer

def add(analyzer, actual):
    addTaxis(analyzer, actual)
    addTrips(analyzer, actual)
    addDate(analyzer, actual)
    addCommunity(analyzer, actual)

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

def addCommunity(analyzer, actual):
    addVertex(analyzer, actual['pickup_community_area'])
    addVertex(analyzer, actual['dropoff_community_area'])
    addConnection(analyzer, actual['pickup_community_area'],actual['dropoff_community_area'], actual['trip_seconds'])

def addVertex(analyzer,vertex):
    try:
        if not gr.containsVertex(analyzer['graph'],vertex):
            gr.insertVertex(analyzer['graph'], vertex)
        return analyzer
    except Excveption as exp:
        error.reraise(exp, 'model:addVertex')

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is not None:
        edge['pesos'] += round((duration / 60),2)
        edge['size'] += 1
        edge['weight'] = round((edge['pesos']/edge['size']),2)
    else:
        gr.addEdge(analyzer['graph'], origin, destination, round((duration / 60),2))
        edge = gr.getEdge(analyzer['graph'], origin, destination)
        edge['pesos'] += round((duration / 60),2)
        edge['size'] += 1
        edge['weight'] = round((edge['pesos']/edge['size']),2)

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
    de un tipo especifico.w
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
# Requerimientosta
# ==============================

def mostTaxis(analyzer):
    dates = m.keySet(analyzer['datesByTaxis'])
    iterator=it.newIterator(dates)
    Max=0
    while it.hasNext(iterator):
        key=it.next(iterator)
        value=m.get(analyzer['datesByTaxis'], key)

        

        





def parteA1(analyzer):
    answer = 0
    companies = m.keySet(analyzer['companyByTaxis'])
    iterator = it.newIterator(companies)
    while it.hasNext(iterator):
        company = it.next(iterator)
        value = m.get(analyzer['companyByTaxis'], company)['value']
        answer += m.size(value)

def parteA2(analyzer):
    answer = 0
    companies = m.keySet(analyzer['companyByTaxis'])
    iterator = it.newIterator(companies)
    while it.hasNext(iterator):
        company = it.next(iterator)
        value = m.get(analyzer['companyByTaxis'], company)['value']
        size = m.size(value)
        if size > 0:
            answer += 1
    return answer

def parteA3(analyzer):
    lista = lt.newList()
    companies = m.keySet(analyzer['companyByTaxis'])
    iterator = it.newIterator(companies)
    while it.hasNext(iterator):
        company = it.next(iterator)
        value = m.get(analyzer['companyByTaxis'], company)['value']
        size = m.size(value)
        data = {'key': company, 'value': size}
        lt.addLast(lista, data)
    ms.mergesort(lista, compareTaxis)
    return lista
    
def parteA4(analyzer):
    lista = lt.newList()
    companies = m.keySet(analyzer['companyByTrips'])
    iterator = it.newIterator(companies)
    while it.hasNext(iterator):
        company = it.next(iterator)
        value = m.get(analyzer['companyByTrips'], company)['value']
        size = m.size(value)
        data = {'key': company, 'value': size}
        lt.addLast(lista, data)
    ms.mergesort(lista, compareTrips)
    return lista


# ==============================
# Funciones de Comparacion
# ==============================
def compareTaxis(company1, company2):
    if (company1['value'] == company2['value']):
        return 0
    elif company1['value'] > company2['value']:
        return 1
    else:
        return -1
def compareTrips(trip1, trip2):
    if (trip1['value'] == trip2['value']):
        return 0
    elif trip1['value'] > trip2['value']:
        return 1
    else:
        return -1
def compareDates(date1, date2):
    if (lt.size(date1) == lt.size(date2)):
        return 0
    elif lt.size(date1) > lt.size(date2):
        return 1
    else:
        return -1
def compareCommunity(community1, community2):
    if community1 == community2:
        return 0
    elif community1 > community2:
        return 1
    else:
        return -1