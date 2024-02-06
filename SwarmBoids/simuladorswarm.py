import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Drone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

class SwarmSimulation:
    def __init__(self, num_drones, width, height, params):
        self.drones = [Drone(np.random.rand(2) * [width, height], np.random.rand(2) - 0.5) for _ in range(num_drones)]
        self.leader = self.drones[0]  # Escolhe o primeiro drone como líder
        self.width = width
        self.height = height
        self.params = params  # Parâmetros: [separação, alinhamento, coesão, seguir líder]

    def limit_velocity(self, drone):
        max_velocity = 2.0  # Define a velocidade máxima
        speed = np.linalg.norm(drone.velocity)
        if speed > max_velocity:
            drone.velocity = (drone.velocity / speed) * max_velocity

    def avoid_edges(self, drone):
        margin = 20  # Define uma margem da borda
        turn_factor = 0.5  # Define quão rapidamente o drone vira
        if drone.position[0] < margin:
            drone.velocity[0] += turn_factor
        if drone.position[0] > self.width - margin:
            drone.velocity[0] -= turn_factor
        if drone.position[1] < margin:
            drone.velocity[1] += turn_factor
        if drone.position[1] > self.height - margin:
            drone.velocity[1] -= turn_factor

    def update_positions(self):
        for drone in self.drones:
            separation = np.zeros(2)
            alignment = np.zeros(2)
            cohesion = np.zeros(2)
            neighbor_count = 0

            for other in self.drones:
                if other is drone:
                    continue
                distance = np.linalg.norm(drone.position - other.position)
                if distance < 10 and distance > 0:  # Raio de percepção
                    separation += (drone.position - other.position) / distance
                    alignment += other.velocity
                    cohesion += other.position
                    neighbor_count += 1

            if neighbor_count > 0:
                alignment /= neighbor_count
                cohesion = (cohesion / neighbor_count) - drone.position

                # Aplica os parâmetros
                drone.velocity += (separation * self.params[0] +
                                   alignment * self.params[1] +
                                   cohesion * self.params[2])

            self.limit_velocity(drone)
            self.avoid_edges(drone)

            # Atualiza a posição
            drone.position += drone.velocity
            drone.position = np.clip(drone.position, 0, [self.width, self.height])

def animate(i, sim, scatter):
    sim.update_positions()
    scatter.set_offsets([drone.position for drone in sim.drones])

def main():
    params = [0.1, 0.1, 0.1]  # Valores arbitrários
    sim = SwarmSimulation(num_drones=30, width=500, height=500, params=params)

    fig, ax = plt.subplots()
    scatter = ax.scatter([drone.position[0] for drone in sim.drones],
                         [drone.position[1] for drone in sim.drones])

    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    anim = FuncAnimation(fig, animate, fargs=(sim, scatter), frames=200, interval=50)

    plt.show()

if __name__ == "__main__":
    main()