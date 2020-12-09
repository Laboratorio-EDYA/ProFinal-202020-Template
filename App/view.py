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
from App import controller
from DISClib.ADT import stack
import timeit
assert config
from time import process_time

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

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print('\n')
    print('-'*80)
    print('Bienvenido')
    print('1- Inicializar analizador y cargar archivo CSV')
    print('2- Reporte de infomación de compañías y taxis')
    print('3- Sistemas de puntos y premios a taxis')
    print('4- Consultar el mejor horario entre 2 areas comunitarias')
    print('5- Salir')
    print('-'*80)

def menu1():
    print('\n')
    print('Reporte de infomación de compañías y taxis')
    print('1- Número total de taxis en los servicios')
    print('2- Número total de compañías con al menos un taxi inscrito')
    print('3- Top M compañías ordenadas por cantidad de taxis afiliados')
    print('4- Top N compañías que prestaron más servicios')
    print('5- Volver al menú principal')

def menu2():
    print('\n')
    print('Sistemas de puntos y premios a taxis')
    print('1- Identificar los N taxis con más puntos en una fecha')
    print('2- Identificar los M taxis con más puntos en un rango de fechas')
    print('3- Volver al menú principal')

# ----------------------------
#     funciones menu 1
# ----------------------------

# def totalTaxis(analyzer):
# def totalCompañias(analyzer):
# def topM(analyzer, name, top):
# def topN(analyzer, name, top): 

# ----------------------------
#     funciones menu 2
# ----------------------------

# def puntosFecha(analyzer, date, top):
# def puntosRango(analyzer, date1, date2, top):
# Debe existir una funcion en el model que calcule los puntos de cada pinche taksi
# ------------------------------------------------------
# def mejorHorario(analyzer, area1, area2):    Req. 3
"""if initialHourM < 15:
            initialHourM = '00'
            initialHour = str(initialHourH) + ':' + initialHourM
        elif (initialHourM >= 15 and initialHourM <= 45) or initialHourM == 30:    
            initialHourM = '30'
            initialHour = str(initialHourH) + ':' + initialHourM
        elif initialHourM <= 60:
            initialHourM = '00'
            initialHourH += 1
            initialHour = str(initialHourH) + ':' + initialHourM
        if finalHourM < 15:
            finalHourM = '00'
            finalHour = str(finalHourH) + ':' + finalHourM
        elif (finalHourM >= 15 and finalHourM <= 45) or finalHourM == 30:
            finalHourM = '30'
            finalHour = str(finalHourH) + ':' + finalHourM
        elif finalHourM <= 60:
            finalHourM = '00'
            finalHourH += 1
            finalHour = str(finalHourH) + ':' + finalHourM"""

# def cargarDatos(analyzer):

"""
Menu principal
"""

def main():
    analyzer = True
    while True:
        printMenu()
        inputs = int(input('Selecciona una opción para continuar\n-> '))
        if inputs == 1:   #Inicio y carga
            t1_start = process_time() #tiempo inicial
            print("\nInicializando.....")
            analyzer = controller.init()
            # cargaDatos(analyzer)
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
                        name = input('Digita el nombre de la compañía: ')
                        top = int(input('Digita el top límite: '))
                        topM(analyzer, name, top)
                        t1_stop = process_time() #tiempo final
                        print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
                    elif opcion == 4:
                        t1_start = process_time() #tiempo inicial
                        name = input('Digita el nombre de la compañía: ')
                        top = int(input('Digita el top límite: '))
                        topN(analyzer, name, top)
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
                        print('Digita la fecha de busqueda con formato YYYY-MM-DD')
                        year = input('Año: ')
                        month = input('Mes: ')
                        day = input('Dia: ')
                        date = year + '-' + month + '-' + day
                        top = int(input('Digita el top límite: '))
                        puntosFecha(analyzer, date, top)
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
                        puntosRango(analyzer, date, top)
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
                area1 = input('Digita el area comunitaria de inicio: ')
                area2 = input('Digita el area comunitaria final: ')
                mejorHorario(analyzer, area1, area2)
                t1_stop = process_time() #tiempo final
                print("Esta función se ejecutó en ",t1_stop-t1_start," segundos ")
        elif inputs == 5:   #Salir
            print('Cerrando el programa ...')
            sys.exit(0)
        else:
            print('Opción incorrecta .....')
main()