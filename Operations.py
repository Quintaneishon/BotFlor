import unicodedata
from os import listdir
from os.path import isfile, join
import pandas
from Alumno import Alumno

# Funcion que quita los acentos de un string
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text).lower()

def validar_mensaje(text):
    return len(text.split(' ')) > 6 or 4 > len(text.split(' '))

def regresa_archivo(materia):
    archivos = [f for f in listdir('Recursos') if isfile(join('Recursos', f))]
    return next((file for file in archivos if materia in strip_accents(file)), None)

def is_nan(num):
    return num != num

def bitacora_alumno(archivo, nombre):
    apellidos = ' '.join(nombre[-2:])
    workbook = pandas.read_excel(f"Recursos/{archivo}", engine='openpyxl')
    dic = workbook.to_dict()
    alumnos = [key for key in dic['Last Name'].keys() if str(dic['Last Name'][key]).lower() == apellidos]
    if len(alumnos) == 0:
        return None
    if len(alumnos) > 1:
        nombres = nombre[:-2]
        alumnos = [llave for llave in alumnos if dic['First Name'] == nombres]
    alumno = Alumno(alumnos[0])
    alumno.nombre = f"{dic['First Name'][alumno.llave]} {dic['Last Name'][alumno.llave]}"
    llaves = list(dic.keys())
    ranking = dict()
    for i in range (3, len(llaves[2:]), 3):
        alumno.tareas.append(dict({"nombre":llaves[i], "puntos":f"{'0' if is_nan(dic[llaves[i]][alumno.llave]) else str(dic[llaves[i]][alumnos[0]])}/{str(dic[llaves[i+1]][alumnos[0]])}", "retro": "" if is_nan(dic[llaves[i+2]][alumnos[0]]) else dic[llaves[i+2]][alumnos[0]]}))
        alumno.total += dic[llaves[i+1]][alumnos[0]]
        for n in dic[llaves[i]]:
            puntaje = 0 if is_nan(dic[llaves[i]][n]) else dic[llaves[i]][n]
            if n in ranking:
                ranking[n] += puntaje
            else:
                ranking[n] = puntaje
    alumno.get_ranking(ranking)
    return alumno
