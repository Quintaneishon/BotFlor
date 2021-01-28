from tabulate import tabulate
import textwrap

class Alumno():
    def __init__( self, llave ):
        self.tareas = list()
        self.llave = llave
        self.total = 0
    def get_table( self ):
        tabla = tabulate([['\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['nombre'], width=20, replace_whitespace=False)), tarea["puntos"], '\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['retro'], width=20, replace_whitespace=False))] for tarea in self.tareas], ["Actividad", "Puntaje", "Retroalimentación"], tablefmt="grid") 
        return f"{tabla}"
    def get_html( self ):
        tabla = tabulate([['\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['nombre'], width=20, replace_whitespace=False)), tarea["puntos"], '\n'.join(texto.ljust(20) for texto in textwrap.wrap(tarea['retro'], width=20, replace_whitespace=False))] for tarea in self.tareas], ["Actividad", "Puntaje", "Retroalimentación"], tablefmt="html") 
        return f"{tabla}"
    def get_ranking( self, ranking ):
        ordenados = list(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
        tpl = next(x for x in ordenados if x[0] == self.llave)
        self.ranking = f"___{ordenados.index(tpl)+ 1}___ de ___{len(ordenados)}___"
        self.promedio = f"___{tpl[1]}___ de ___{self.total}___"