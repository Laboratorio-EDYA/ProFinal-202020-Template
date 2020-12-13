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
from DISClib.Algorithms.Graphs import dfs
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
import operator as o 
import datetime 

from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as q

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
    if actual['company'] == '':
        company = 'Independent Owner'
    else:
        company = actual['company']
    current = m.get(analyzer['companyByTaxis'],company)
    if current is None:
        mapa = m.newMap(comparefunction=compareTaxis)
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
    if actual['company'] == '':
        company = 'Independent Owner'
    else:
        company = actual['company']
    current = m.get(analyzer['companyByTrips'],company)
    if current is None:
        mapa = m.newMap(comparefunction=compareTrips)
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
    date = getDateTimeTaxiTrip(actual['trip_start_timestamp'])[0]
    current = om.get(analyzer['datesByTaxis'], date)
    if current is None:
        mapa = m.newMap(comparefunction=compareDatesValues)
        om.put(analyzer['datesByTaxis'],date,mapa)
        current = om.get(analyzer['datesByTaxis'],date)['value']
        money = float(actual['trip_total'])
        millas = float(actual['trip_miles'])
        if money > 0:
            puntos = millas/money
        else: 
            puntos = 0
        m.put(current, actual['taxi_id'], [money,millas,1,puntos])
    else:
        value = m.get(current['value'], actual['taxi_id'])
        if actual['trip_total'] != '':
            money = float(actual['trip_total'])
        else:
            money = 0
        if actual['trip_miles'] != '':
            millas = float(actual['trip_miles'])
        else:
            millas = 0
        if value is None:
            if money > 0:
                puntos = millas/money  
            else: 
                puntos = 0
            m.put(current['value'], actual['taxi_id'], [money,millas,1,puntos])
        else:
            money = value['value'][0] + money
            millas = value['value'][1] + millas
            total = value['value'][2] + 1
            if money > 0:
                puntos = (millas/money)*total
            else: 
                puntos = 0
            m.put(current['value'], actual['taxi_id'], [money,millas,total,puntos])

def addCommunity(analyzer, actual):
    start = actual['trip_start_timestamp']
    end = actual['trip_end_timestamp']
    if start != '' and end != '':
        vertexA = (actual['pickup_community_area'],getDateTimeTaxiTrip(start)[1])
        vertexB = (actual['dropoff_community_area'],getDateTimeTaxiTrip(end)[1])
        if vertexA != vertexB:
            addVertex(analyzer, vertexA)
            addVertex(analyzer, vertexB)
            if (actual['trip_seconds']) != '':
                time = float(actual['trip_seconds'])
            else:
                time = 0
            addConnection(analyzer, vertexA, vertexB, time)

def addVertex(analyzer,vertex):
    try:
        if not gr.containsVertex(analyzer['graph'],vertex):
            gr.insertVertex(analyzer['graph'], vertex)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addVertex')

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is not None:
        edge['pesos'] += duration
        edge['size'] += 1
        edge['weight'] = round((edge['pesos']/edge['size']),2)
    else:
        gr.addEdge(analyzer['graph'], origin, destination, duration)
        edge = gr.getEdge(analyzer['graph'], origin, destination)
        edge['pesos'] += duration
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

# ==============================
# Funciones Helper
# ==============================
def gradosAkilometros2(x):
    a=x.split('.')
    try:
        return str(a[0])+'.'+str(a[1])+str(a[2])
    except:
        return str(a[0])+'.'+str(a[1])    
def getDateTimeTaxiTrip(taxitrip):

    """

    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).

    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'

    Los datos date se pueden comparar con <, >, <=, >=, ==, !=

    Los datos time se pueden comparar con <, >, <=, >=, ==, !=

    """
    taxitripdatetime = datetime.datetime.strptime(taxitrip, '%Y-%m-%dT%H:%M:%S.%f')

    return taxitripdatetime.date(), taxitripdatetime.time()


# ==============================
# Requerimientosta
# ==============================

def parteA1(analyzer):
    answer = 0
    companies = m.keySet(analyzer['companyByTaxis'])
    iterator = it.newIterator(companies)
    while it.hasNext(iterator):
        company = it.next(iterator)
        value = m.get(analyzer['companyByTaxis'], company)['value']
        answer += m.size(value)
    return answer

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
    ms.mergesort(lista, compareTaxisValues)
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
    ms.mergesort(lista, compareTripsValues)
    return lista

def parteB1(analyzer,top,fecha):
    mapTaxis = om.get(analyzer['datesByTaxis'],fecha)
    taxis = m.keySet(mapTaxis['value'])
    iterator = it.newIterator(taxis)
    dictRes = {}
    while it.hasNext(iterator):
        taxi = it.next(iterator)
        value = m.get(mapTaxis['value'],taxi)['value']
        puntos = value[3]
        dictRes[taxi] = puntos
    sortedDict = sorted(dictRes.items(), key = o.itemgetter(1), reverse = True)
    listIds = lt.newList()
    for i in range(top):
        lt.addLast(listIds,sortedDict[i])
    return listIds

def parteB2(analyzer,keylo,keyhi,top):
    dates = om.keys(analyzer['datesByTaxis'],keylo,keyhi)
    iterator = it.newIterator(dates)
    dictRes = {}
    while it.hasNext(iterator):
        date = it.next(iterator)
        mapTaxis = om.get(analyzer['datesByTaxis'],date)['value'] #map
        taxis = m.keySet(mapTaxis)
        iterator2 = it.newIterator(taxis)
        while it.hasNext(iterator2):
            taxi = it.next(iterator2)
            value = m.get(mapTaxis,taxi)['value']
            puntos = value[3]
            dictRes[taxi] = puntos
    sortedDict = sorted(dictRes.items(), key = o.itemgetter(1), reverse = True)
    listIds = lt.newList()
    for i in range(top):
        lt.addLast(listIds,sortedDict[i])
    return listIds
        
def parteC(analyzer, area1, area2, hora_inicio, hora_fin):
    area1 = float(area1)
    area2 = float(area2)
    inicio = datetime.datetime.strptime(hora_inicio, '%H:%M').time()
    final = datetime.datetime.strptime(hora_fin, '%H:%M').time()
    vertices = gr.vertices(analyzer['graph'])
    iterator = it.newIterator(vertices)
    vertices_area1 = lt.newList()
    vertices_area2 = lt.newList()
    menor = [0,0,0,0]
    while it.hasNext(iterator):
        actual = it.next(iterator)
        if actual[0] != "" and float(actual[0].strip()) == area1 and actual[1] > inicio:
            lt.addLast(vertices_area1, actual)
        elif actual[0] != "" and float(actual[0].strip()) == area2 and actual[1] < final:
            lt.addLast(vertices_area2, actual)
    iterator = it.newIterator(vertices_area1)
    while it.hasNext(iterator):
        actual = it.next(iterator)
        diks = djk.Dijkstra(analyzer['graph'],actual)
        iterator2 = it.newIterator(vertices_area2)
        while it.hasNext(iterator2):
            current = it.next(iterator2)
            cost = djk.distTo(diks, current)
            if menor[0] == 0:
                menor[0] = cost
                menor[1] = actual
                menor[2] = current
                menor[3] = djk.pathTo(diks, current)
            elif cost < menor[0]:
                menor[0] = cost
                menor[1] = actual
                menor[2] = current
                menor[3] = djk.pathTo(diks, current)
    return menor





# ==============================
# Funciones de Comparacion
# ==============================
def compareTaxisValues(company1, company2):
    return company1['value'] > company2['value']

def compareTripsValues(trip1, trip2):
    return trip1['value'] > trip2['value']

def compareTaxis(company1, company2):
    if (company1 == company2['key']):
        return 0
    elif (company1) > (company2['key']):
        return 1
    else:
        return -1

def compareTrips(company1, company2):
    if (company1) == (company2['key']):
        return 0
    elif (company1) > (company2['key']):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1
def compareDatesValues(date1, date2):
    if date1 == date2['key']:
        return 0
    elif date1 > date2['key']:
        return 1
    else:
        return -1

def compareCommunity(community1, community2):
    if community1 == community2['key']:
        return 0
    elif community1 > community2['key']:
        return 1
    else:
        return -1