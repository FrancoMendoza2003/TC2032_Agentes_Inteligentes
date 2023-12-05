from simpleai.search import SearchProblem, depth_first, breadth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer
import numpy as np
import time 

mapa = np.load('mars_map.npy')
nr,nc = mapa.shape
scale = 10
t0 = time.time()


class MarsRover(SearchProblem):
    def __init__(self,initial_state, final_state,alt_max):
        SearchProblem.__init__(self,initial_state)
        self.goal_state = final_state
        self.alt_max = alt_max

    def actions(self,state):
        xf,yf = state
        x_map = nr - round(yf/scale)
        y_map = round(xf/scale)
        z = mapa[x_map][y_map]

        actions=[]
        n = [(x_map +1, y_map), (x_map, y_map + 1), (x_map - 1, y_map ), (x_map, y_map -1), (x_map + 1,y_map + 1 ),(x_map - 1, y_map -1), (x_map +1, y_map -1), (x_map - 1, y_map + 1)]
        for x,y in n:
            z_n= mapa[x][y]
            if(z_n!= -1 and abs(z - z_n) <= self.alt_max):
                actions.append(((x_map - x)*scale, (y_map - y)*scale))

    
        return actions
    
    def result(self, state, action):
        x,y = state
        xf,yf =action
        new_state = x+xf,y+yf
        return new_state
    

    def heuristic(self, state):
        x,y = state
        xf,yf = self.goal_state
        xf = nr - round(yf/scale)
        yf = round(xf/scale)

        x = nr - round(y/scale)
        y = round(x/scale)
        return np.sqrt((xf - x)**2+ (yf-y)**2)
    
    def cost(self, state, action, statef):
        return 1
    
    def is_goal(self, state):
        return state==self.goal_state



def display(result):
    if result is not None:
        for i, (action, state) in enumerate(result.path()):
            if action is None:
                print('Inicio')
            elif i == len(result.path()) - 1:
                print(i,'Después', action)
                print('Meta lograda con un costo de', result.cost)
            else:
                print('Movimiento:',i,'- ', action)

            print('  ', state)
    else:
        print('Mala configuración del problema')



result = astar(MarsRover((4450,10500),(6000,5000),0.25),graph_search=True)
# result = greedy(MarsRover((2850,6400),(3150,6800),0.25),graph_search=True)
# result = breadth_first(MarsRover((2850,6400),(3150,6800),0.25),graph_search=True)
# result = uniform_cost(MarsRover((2850,6400),(3150,6800),0.25),graph_search=True)
tf = time.time()
tiempo = tf - t0


print('\n ---------------------------------------------- \n>> Búsqueda A* <<')
display(result)
print("El algoritmo se tardo: ", round(tiempo,5), " segundos.")