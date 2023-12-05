import numpy as np
import random
import math

# Cargar el mapa del cráter de Marte
mapa = np.load('mars_crater_map.npy')
nr, nc = mapa.shape
pixel_size = 10.045  # Cada píxel representa un área de 10.045 metros x 10.045 metros

# Función para encontrar el vecino con la menor profundidad que cumple con la diferencia de alturas
def find_best_neighbor(x, y, current_depth, max_diff):
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                 (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]

    best_neighbor = (x, y)
    best_depth = current_depth

    for nx, ny in neighbors:
        if 0 <= nx < nr and 0 <= ny < nc:
            neighbor_depth = mapa[nx][ny]
            depth_diff = current_depth - neighbor_depth

            if 0 <= depth_diff <= max_diff and neighbor_depth < best_depth:
                best_neighbor = (nx, ny)
                best_depth = neighbor_depth

    return best_neighbor if best_neighbor != (x, y) else None

# Función para encontrar un vecino aleatorio que cumpla con la diferencia de alturas
def find_random_neighbor(x, y, current_depth, max_diff):
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                 (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]

    valid_neighbors = []

    for nx, ny in neighbors:
        if 0 <= nx < nr and 0 <= ny < nc:
            neighbor_depth = mapa[nx][ny]
            depth_diff = current_depth - neighbor_depth

            if 0 <= depth_diff <= max_diff:
                valid_neighbors.append((nx, ny))

    return random.choice(valid_neighbors) if valid_neighbors else None

# Búsqueda Codiciosa
def greedy_search(start_x, start_y, max_depth_diff=2.0):
    current_x, current_y = start_x, start_y
    current_depth = mapa[start_x][start_y]
    path = [(current_x, current_y)]

    while True:
        neighbor = find_best_neighbor(current_x, current_y, current_depth, max_depth_diff)

        if neighbor:
            current_x, current_y = neighbor
            current_depth = mapa[current_x][current_y]
            path.append((current_x, current_y))
        else:
            break

    return path

# Recocido Simulado
def simulated_annealing_search(start_x, start_y, max_depth_diff=2.0, initial_temperature=1000, cooling_rate=0.995):
    current_x, current_y = start_x, start_y
    current_depth = mapa[start_x][start_y]
    path = [(current_x, current_y)]

    best_x, best_y = current_x, current_y
    best_depth = current_depth
    best_path = path.copy()

    temperature = initial_temperature

    while temperature > 1:
        neighbor = find_random_neighbor(current_x, current_y, current_depth, max_depth_diff)

        if neighbor:
            new_x, new_y = neighbor
            new_depth = mapa[new_x][new_y]

            if new_depth <= current_depth:
                current_x, current_y = new_x, new_y
                current_depth = new_depth
                path.append((current_x, current_y))

                if len(path) < len(best_path):
                    best_x, best_y = current_x, current_y
                    best_depth = current_depth
                    best_path = path.copy()
            else:
                # Prueba la regla de recocido simulado
                if random.random() < acceptance_probability(current_depth, new_depth, temperature):
                    current_x, current_y = new_x, new_y
                    current_depth = new_depth
                    path.append((current_x, current_y))

        temperature *= cooling_rate

    return best_path

# Función para calcular la probabilidad de aceptar un movimiento peor en el recocido simulado
def acceptance_probability(current_depth, new_depth, temperature):
    if new_depth < current_depth:
        return 1.0
    return math.exp((current_depth - new_depth) / temperature)

# Pruebas con coordenadas válidas
for i in range(5):
    start_x = random.randint(0, nr - 1)
    start_y = random.randint(0, nc - 1)

    print(f"Prueba {i+1} - Posición inicial: ({start_x}, {start_y})")

    # Búsqueda Codiciosa
    greedy_path = greedy_search(start_x, start_y)
    greedy_depth_reached = mapa[greedy_path[-1]]
    greedy_length_of_path = len(greedy_path) * pixel_size

    print(f"Búsqueda Codiciosa - Profundidad alcanzada: {greedy_depth_reached}, Longitud del camino (metros): {greedy_length_of_path}")

    # Recocido Simulado
    sa_path = simulated_annealing_search(start_x, start_y)
    sa_depth_reached = mapa[sa_path[-1]]
    sa_length_of_path = len(sa_path) * pixel_size

    print(f"Recocido Simulado - Profundidad alcanzada: {sa_depth_reached}, Longitud del camino (metros): {sa_length_of_path}")
    print()
