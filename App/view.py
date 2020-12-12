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


import sys
import config
from App import controller as ctrl
from DISClib.ADT import stack
import timeit
assert config
from time import process_time
import controller
from DISClib.DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

taxifile = 'taxi-trips-wrvz-psew-subset-small.csv'
initialStation = None
recursionLimit = 30000

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print('\n')
    print('='*80)
    print('Bienvenido')
    print('1- Inicializar analizador y cargar archivo CSV')
    print('2- Reporte de infomación de compañías y taxis')
    print('3- Sistemas de puntos y premios a taxis')
    print('4- Consultar el mejor horario entre 2 areas comunitarias')
    print('5- Salir')
    print('='*80)

def menu1():
    print('\n')
    print('-'*80)
    print('Reporte de infomación de compañías y taxis')
    print('1- Número total de taxis en los servicios')
    print('2- Número total de compañías con al menos un taxi inscrito')
    print('3- Top M compañías ordenadas por cantidad de taxis afiliados')
    print('4- Top N compañías que prestaron más servicios')
    print('5- Volver al menú principal')
    print('-'*80)

def menu2():
    print('\n')
    print('-'*80)
    print('Sistemas de puntos y premios a taxis')
    print('1- Identificar los N taxis con más puntos en una fecha')
    print('2- Identificar los M taxis con más puntos en un rango de fechas')
    print('3- Volver al menú principal')
    print('-'*80)

# ----------------------------
#     funciones menu 1
# ----------------------------

def totalTaxis(analyzer):
    data = ctrl.parteA1(analyzer)
    print(data, ' taxis tienen servicios reportados')
    
def totalCompañias(analyzer):
    data = ctrl.parteA2(analyzer)
    print(data,' compañías tiene al menos un taxi inscrito')
    
def topM(analyzer, top):
    res = []    
    data = ctrl.parteA3(analyzer)
    print(data)
    for each_data in data:
        res.append(each_data)
        if len(res) >= top:
            break
    print('El top ',top,' de las compañías ordenadas por taxis afiliados es: ')
    for each_data in res:
        print(str(each_data))

def topN(analyzer, top): 
    res = []    
    data = ctrl.parteA3(analyzer)
    print(data)
    for each_data in data:
        res.append(each_data)
        if len(res) >= top:
            break
    print('El top ',top,' de las compañías que más servicios prestaron es: ')
    for each_data in res:
        print(str(each_data))

# ----------------------------
#     funciones menu 2
# ----------------------------

def puntosFecha(analyzer, top, fecha):
    data = ctrl.parteB1(analyzer, top,fecha)
    iterator=it.newIterator(data)
    i=1
    
    print('Los taxis con más puntos según la fecha dada son: ' )
    print('='*50)
    while it.hasNext(iterator):
        print(str(i)+'->','El taxi con la identificación: ',it.next(iterator))
        i+=1
    print('-'*50)

def puntosRango(analyzer, date1, date2, top):
    data = ctrl.parteB2(analyzer, date1, date2, top)
    iterator=it.newIterator(data)
    print('Los taxis con más puntos según el rango de fechas',date1,' y ',date2)
    print('='*50)
    i=1
    while it.hasNext(iterator):
        print(str(i)+'->','El taxi con la identificación: ',it.next(iterator))
        i+=1
    print('='*50)
# Debe existir una funcion en el model que calcule los puntos de cada pinche taksi
"""
El addDate añade cada fecha junto con un taxi y sus puntos, millas y entre otros
"""
# ------------------------------------------------------
def mejorHorario(analyzer):    # Req. 3
    hora_inicio = ''
    hora_fin = ''
    area1 = input('Digita el area comunitaria de inicio: ')
    area2 = input('Digita el area comunitaria final: ')
    inicio_H = int(input('Digita las horas de la hora inicial en formato HH: '))
    inicio_M = int(input('Digita los minutos de la hora inicial en formato MM: '))
    fin_H = int(input('Digita las horas de la hora final en formato HH: '))
    fin_M = int(input('Digita los minutos de la hora final en formato MM: '))
    if inicio_M > 60 or inicio_H > 24 or fin_M > 60 or fin_H > 24:
        print('¡¡ KELLY, UNA HORA TIENE 60 MINUTOS Y UN DÍA 24 HORAS !!')
    else:
        if inicio_M > 0 and inicio_M <= 15:
            inicio_M = '15'
            hora_inicio = str(inicio_H) + ':' + inicio_M
        elif inicio_M > 15 and inicio_M <= 30:    
            inicio_M = '30'
            hora_inicio = str(inicio_H) + ':' + inicio_M
        elif inicio_M > 30 and inicio_M <= 45:
            inicio_M = '45'
            hora_inicio = str(inicio_H) + ':' + inicio_M
        elif inicio_M > 45 and inicio_M <= 60:
            inicio_M = '00'
            inicio_H += 1
            hora_inicio = str(inicio_H) + ':' + inicio_M
        if fin_M > 0 and fin_M <= 15:
            fin_M = '15'
            hora_fin = str(fin_H) + ':' + fin_M
        elif fin_M > 15 and fin_M <= 30:    
            fin_M = '30'
            hora_fin = str(fin_H) + ':' + fin_M
        elif fin_M > 30 and fin_M <= 45:
            fin_M = '45'
            hora_fin = str(fin_H) + ':' + fin_M
        elif fin_M > 45 and fin_M <= 60:
            fin_M = '00'
            fin_H += 1
            hora_fin = str(fin_H) + ':' + fin_M
        data = ctrl.mejorHorario(analyzer, area1, area2, hora_inicio, hora_fin)
    print(data)


def cargarDatos(analyzer):
    print("\nCargando información de taxis de Chicago .....")
    ctrl.loadData(analyzer, taxifile)
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

# Menú principal

def main():
    analyzer = None
    while True:
        printMenu()
        inputs = int(input('Selecciona una opción para continuar\n-> '))
        if inputs == 1:   #Inicio y carga
            t1_start = process_time() #tiempo inicial
            print("\nInicializando.....")
            tamaño = int(input("Digita el tamaño de las tablas de hash: "))
            carga = float(input("Digita el factor de carga: "))
            analyzer = ctrl.init(tamaño, carga)
            cargarDatos(analyzer)
            t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 2:   #Req. 1
            if analyzer == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                while True:
                    menu1()
                    opcion = int(input('Selecciona una opción para continuar\n--> '))
                    if opcion == 1:
                        t1_start = process_time() #tiempo inicial
                        totalTaxis(analyzer)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 2:
                        t1_start = process_time() #tiempo inicial
                        totalCompañias(analyzer)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 3:
                        t1_start = process_time() #tiempo inicial
                        top = int(input('Digita el top límite: '))
                        topM(analyzer, top)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 4:
                        t1_start = process_time() #tiempo inicial
                        top = int(input('Digita el top límite: '))
                        topN(analyzer, top)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 5:
                        break
                    else:
                        print('Opción invalida .....')

        elif inputs == 3:   #Req. 2
            if analyzer == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                while True:
                    menu2()
                    opcion = int(input('Selecciona una opción para continuar\n--> '))
                    if opcion == 1:
                        t1_start = process_time() #tiempo inicial
                        year1 = input('Año: ')
                        month1 = input('Mes: ')
                        day1 = input('Dia: ')
                        date1 = year1 + '-' + month1 + '-' + day1
                        top = int(input('Digita el top límite: '))
                        puntosFecha(analyzer, top, date1)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 2:
                        t1_start = process_time() #tiempo inicial
                        print('Digita la fecha inicial de busqueda con formato YYYY-MM-DD')
                        year1 = input('Año: ')
                        month1 = input('Mes: ')
                        day1 = input('Dia: ')
                        date1 = year1 + '-' + month1 + '-' + day1
                        print('Digita la fecha ifinal de busqueda con formato YYYY-MM-DD')
                        year2 = input('Año: ')
                        month2 = input('Mes: ')
                        day2 = input('Dia: ')
                        date2 = year2 + '-' + month2 + '-' + day2
                        top = int(input('Digita el top límite: '))
                        puntosRango(analyzer, date1, date2, top)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 3:
                        break
                    else:
                        print('Opcion invalida .....')

        elif inputs == 4:
            if analyzer == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                mejorHorario(analyzer)
                t1_stop = process_time() #tiempo final
                print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")

        elif inputs == 5:   #Salir
            print('Cerrando el programa ...')
            sys.exit(0)

        else:
            print('Opción incorrecta .....')
            
main()