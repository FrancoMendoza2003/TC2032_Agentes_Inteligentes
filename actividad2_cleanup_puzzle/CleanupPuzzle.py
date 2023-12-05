#---------------------------------------------------------------------------------------------------------------
#    PSA para el problema de Cleanup Puzzle
#---------------------------------------------------------------------------------------------------------------

from simpleai.search import SearchProblem, depth_first, breadth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer

#---------------------------------------------------------------------------------------------------------------
#   Definición del problema
#---------------------------------------------------------------------------------------------------------------

class CleanupPuzzle(SearchProblem):
    """ 
        Clase que es usada para definir el problema. Los estados son representados 
        con .
    """

    def __init__(self, puzzle):
        """ Constructor de la clase para el problema del Cleanup Puzzle. 
            Inicializa el problema de acuerdo al puzzle que se proporciona.
       
            puzzle: El puzzle que se va a resolver
            tamanio: tamanio del puzzle
        """
        self.puzzle = puzzle
        self.tamanio = len(puzzle)
        
        
        # Llama al constructor de su superclase SearchProblem (estado inicial = ).
        estado_inicial = self.puzzle
        SearchProblem.__init__(self, estado_inicial)

        self.goal_state =[]
        for i in range(self.tamanio):
            fila = []
            for x in range(self.tamanio):
                fila.append(0)
            self.goal_state.append(tuple(fila))

        for i in range(self.tamanio):
            self.goal_state[i] = tuple(self.goal_state[i])

        self.goal_state = tuple(self.goal_state)


    def actions(self, state):
        #Las acciones se van a hacer en lista.
        actions = []
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                actions.append([i, j])
                
        return actions

    def result(self, state, action):
        """ 
            Este método regresa el nuevo estado obtenido despues de ejecutar la acción.

            state: ciudad actual.
            action: ciudad a donde voy.
        """
        nuevo = []
        for i in list(state):
            nuevo.append(list(i))
        #Primera parte de la accion es la fila en la que se esta haciendo y la segunda es la columna 3,1 seria la 4ta fila y 2da columna
        fila = action[0]
        columna = action[1]
        # Hacer los cambios en el nuevo estado en los puntos necesarios, dependiendo de los puntos donde se toman las acciones.
        # Se toma en cuenta cuando estan en las orillas de la matriz, para no hacer cambios fuera de la matriz.
        if fila!=0:
            if (state[fila-1][columna]==0):
                nuevo[fila-1][columna] = 1
            else:
                nuevo[fila-1][columna] = 0

        if columna!=0:
            if (state[fila][columna-1]==0):
                nuevo[fila][columna-1] = 1
            else:
                nuevo[fila][columna-1] = 0

        if fila!=self.tamanio-1:
            if (state[fila+1][columna]==0):
                nuevo[fila+1][columna] = 1
            else:
                nuevo[fila+1][columna] = 0

        if columna!=self.tamanio-1:
            if (state[fila][columna+1]==0):
                nuevo[fila][columna+1] = 1
            else:
                nuevo[fila][columna+1] = 0
            
        for i in range(len(nuevo)):
            nuevo[i] = tuple(nuevo[i])
        
        return tuple(nuevo)

    def is_goal(self, state):
        """ 
            This method evaluates whether the specified state is the goal state.

            state: La matriz actual.
        """
        #Se busca una matriz llena de ceros.
        return state == self.goal_state
        
    def cost(self, state, action, state2):
        """ 
            Este método recibe dos estados y una acción, y regresa el costo de 
            aplicar la acción del primer estado al segundo.

            Toda accion cuesta 1, mientras menos acciones cuesta menos.
        """
        #No se pide pero en este caso el costo va a ser = a el numero de clicks que toma
        return 1
        
    def heuristic(self, state):
        #Heuristica, mientras mas 1s haya, es mas alto el costo del puzzle.
        count = 0
        heuristica = list(state)
        for i in heuristica:
            if i==1:
                count+=1
        return count



# Despliega los resultados
def display(result):
    if result is not None:
        for i, (action, state) in enumerate(result.path()):
            if action == None:
                print('Configuración inicial')
            elif i == len(result.path()) - 1:
                print(i,'- Después de click en:',action,"nuevo puzzle:")
                print('¡Meta lograda con costo = ', result.cost,'!')
            else:
                print(i,'- Después de click en:',action,"nuevo puzzle:")
            
            for i in state:
                print('  ', i)
    else:
        print('No se puede resolver')


#---------------------------------------------------------------------------------------------------------------
#   Programa
#---------------------------------------------------------------------------------------------------------------

#my_viewer = None
my_viewer = BaseViewer()       # Solo estadísticas
#my_viewer = ConsoleViewer()    # Texto en la consola
#my_viewer = WebViewer()        # Abrir en un bfilaser en la liga http://localhost:8000
#Puzzle1
# puzzle = ((0, 0, 1, 0),
#         (0, 0, 0, 1),
#         (1, 0, 0, 1),
#         (0, 1, 1, 0))

puzzle = ((0,1,1,0),
          (1,0,1,1),
          (1,1,0,1),
          (0,1,1,0))

# Crea un PSA y lo resuelve con la búsqueda primero en anchura
result = breadth_first(CleanupPuzzle(puzzle), graph_search=True, viewer=my_viewer)
result2= astar(CleanupPuzzle(puzzle),graph_search=True,viewer=my_viewer)
if my_viewer != None:
    print('Stats:')
    print(my_viewer.stats)

print()
print('>> Búsqueda Primero en Anchura <<')
display(result)

print()
print('>> Búsqueda ahora con A* <<')
display(result2)


#---------------------------------------------------------------------------------------------------------------
#   Fin del archivo
#---------------------------------------------------------------------------------------------------------------