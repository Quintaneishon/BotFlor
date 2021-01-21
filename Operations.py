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

def isNaN(num):
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
    alumno = Alumno()
    aux = 0
    tarea = dict()
    for idx,key in enumerate(dic.keys()):
        if idx == 0:
            alumno.nombre = dic[key][alumnos[0]]
        elif idx == 1:
            alumno.nombre += f" {dic[key][alumnos[0]]}"
        elif idx > 2:
            if aux == 0: 
                tarea.update({"nombre":key})
                aux = 1
            elif aux == 1:
                tarea.update({"puntos":dic[key][alumnos[0]]})
                aux = 2
            elif aux == 2:
                tarea.update({"retro":"" if isNaN(dic[key][alumnos[0]]) else dic[key][alumnos[0]]})
                alumno.tareas.append(tarea.copy()) 
                tarea.clear()
                aux = 0
    return alumno
