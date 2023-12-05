import random
import math
import matplotlib.pyplot as plt
import numpy as np

class RecocidoSimulado:
    def __init__(self, x_data, y_data, initial_theta, t0, alpha, step_size):
        self.x_data = x_data
        self.y_data = y_data
        self.initial_theta = initial_theta
        self.t0 = t0
        self.alpha = alpha
        self.step_size = step_size

    def f(self, x, theta):
        a, b, c = theta
        return math.cos(a * x) + b * x - c * x ** 2

    def calculate_max_error(self, theta):
        max_error = 0
        for x, y in zip(self.x_data, self.y_data):
            error = abs(y - self.f(x, theta))
            max_error = max(max_error, error)
        return max_error

    def neighbor(self, theta):
        new_theta = [x + random.uniform(-self.step_size, self.step_size) for x in theta]
        return new_theta

    def solve(self):
        theta = self.initial_theta
        best_theta = theta
        best_error = self.calculate_max_error(theta)

        t = self.t0
        step = 0

        while t > 0.005 and best_error > 0:
            t = self.t0 * math.pow(self.alpha, step)
            step += 1

            new_theta = self.neighbor(theta)
            new_error = self.calculate_max_error(new_theta)

            if new_error < best_error:
                best_theta = new_theta
                best_error = new_error

            print(f"Iteración: {step}, Error máximo absoluto: {best_error}, Temperatura: {t}")

            p = math.exp(-(new_error - best_error) / t)
            if random.random() < p:
                theta = new_theta
                best_error = new_error

        return best_theta, best_error

# Definir los datos de entrada
x_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
y_data = [1.0, 1.0, 2.0, 4.0, 5.0, 4.0, 4.0, 5.0, 6.0, 5.0]

# Parámetros iniciales
initial_theta = [random.uniform(0, 15), random.uniform(0, 15), random.uniform(0, 15)]
t0 = 0.6
alpha = 0.01
step_size = 0.1

rs = RecocidoSimulado(x_data, y_data, initial_theta, t0, alpha, step_size)
best_theta, best_error = rs.solve()

print("\nMejor solución encontrada:")
print("a:", best_theta[0])
print("b:", best_theta[1])
print("c:", best_theta[2])
print("Error máximo absoluto:", best_error)
print("Temperatura inicial:",t0)
print("Alpha:",alpha)

valores_x = np.linspace(min(x_data), max(x_data), 100)
y_original = [rs.f(x, initial_theta) for x in valores_x]
y_ajustado = [rs.f(x, best_theta) for x in valores_x]

plt.figure(figsize=(6, 5))
plt.scatter(x_data, y_data, label='Datos de entrada', color='blue')
plt.plot(valores_x, y_original, label='Función Original', linestyle='--', color='green')
plt.plot(valores_x, y_ajustado, label='Función Ajustada', color='red')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste de Función con Recocido Simulado')
plt.grid(True)
plt.show()