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

import config as cf
from App import model
import csv
import datetime 

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init(tamaño, carga):
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer(tamaño, carga)
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadData(analyzer, file):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for actual in input_file:
        model.add(analyzer, actual)
    return analyzer
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def accidentsSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentsSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)

def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

# _______________________________________
#      Funciones entre View y Model
# _______________________________________

def parteA1(analyzer):
    return model.parteA1(analyzer)

def parteA2(analyzer):
    return model.parteA2(analyzer)

def parteA3(analyzer):
    return model.parteA3(analyzer)

def parteA4(analyzer, top): 
    return model.parteA4(analyzer, top)

def parteB1(analyzer, top, fecha):
    fecha = datetime.datetime.strptime(fecha,'%Y-%m-%d').date()
    return model.parteB1(analyzer, top, fecha)

def parteB2(analyzer, keylo, keyhi, top):
    keylo = datetime.datetime.strptime(keylo,'%Y-%m-%d').date()
    keyhi = datetime.datetime.strptime(keyhi,'%Y-%m-%d').date()
    return model.parteB2(analyzer, keylo, keyhi, top)

  
#datetime.datetime.strptime(hora,'%Y-%m-%d')
#datetime.datetime.strptime(hora,'%H:%M')

def parteC(analyzer, area1, area2, hora_inicio, hora_fin):
    return model.mejorHorario(analyzer, area1, area2, hora_inicio, hora_fin)
