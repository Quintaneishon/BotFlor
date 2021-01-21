from tabulate import tabulate
import textwrap

class Alumno():
    def __init__( self ):
        self.tareas = list()
    def get_table( self ):
        tabla = tabulate([['\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['nombre'], width=20, replace_whitespace=False)), tarea["puntos"], '\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['retro'], width=20, replace_whitespace=False))] for tarea in self.tareas], ["Actividad", "Puntaje", "Retroalimentación"], tablefmt="grid") 
        return f"{tabla}"
    def get_html( self ):
        tabla = tabulate([['\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['nombre'], width=20, replace_whitespace=False)), tarea["puntos"], '\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['retro'], width=20, replace_whitespace=False))] for tarea in self.tareas], ["Actividad", "Puntaje", "Retroalimentación"], tablefmt="html") 
        return f"{tabla}"
    