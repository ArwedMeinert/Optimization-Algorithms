import random
from typing import List, Tuple,Self
from acoInterface import IAnt, IEnvironment, IRenderer
import random
import math
from typing import Dict
import pygame
import sys
import random
import math
class Environment(IEnvironment):
    def __init__(self, cities: List[Tuple[int, int]], evaporation_rate: float = 0.1):
        self.cities = cities  # Cities are passed in as a list of (x, y) coordinates
        self.pheromones = {}  # Pheromone levels between cities
        self.evaporation_rate = evaporation_rate
        self.distances = self._compute_distances()

    def _compute_distances(self):
        distances = {}
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                if i != j:
                    dist = math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
                    distances[(i, j)] = dist
        return distances

    def get_pheromone_level(self, city1, city2):
        # Ensure city1 is always the smaller index to maintain symmetry
        if city1 > city2:
            city1, city2 = city2, city1

        # Return pheromone level or 1.0 if no pheromone has been laid
        return self.pheromones.get((city1, city2), 1.0)

    def update_pheromone(self, city1, city2, amount):
        # Ensure city1 is always the smaller index to maintain symmetry
        if city1 > city2:
            city1, city2 = city2, city1

        # Update the pheromone level on the edge between city1 and city2
        if (city1, city2) in self.pheromones:
            self.pheromones[(city1, city2)] += amount
        else:
            self.pheromones[(city1, city2)] = amount

    def evaporate_pheromone(self):
        # Evaporate pheromone on all edges by reducing the amount by the evaporation rate
        for edge in self.pheromones:
            self.pheromones[edge] *= (1 - self.evaporation_rate)

    def get_cities(self):
        # Return the list of city indices (0, 1, 2, ...)
        return self.cities

    def get_distance(self, city1, city2):
        # Return the distance between two cities
        return self.distances.get((city1, city2), float('inf'))



class PygameRenderer(IRenderer):
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Ant Colony Optimization - TSP')
        self.width = width
        self.height = height
        self.city_radius = 10

    def render_environment(self, environment):
        self.screen.fill((255, 255, 255))  # Fill background with white
        # Draw pheromone trails (red lines, thickness based on pheromone levels)
        for (city1, city2), pheromone in environment.pheromones.items():
            x1, y1 = environment.cities[city1]
            x2, y2 = environment.cities[city2]
            intensity = min(int(pheromone * 255), 255)  # Clamp pheromone intensity
            color = (255, 0, 0, intensity)  # Red color with varying intensity
            pygame.draw.line(self.screen, color[:3], (x1 * 100, y1 * 100), (x2 * 100, y2 * 100),   max(1, min(20, int(pheromone * 10))))

        # Draw cities (blue circles)
        i=0
        for x, y in environment.cities:
            if i==0:
                rgb=(100,255,255)
            else:
                rgb=(0,0,255)
            pygame.draw.circle(self.screen, rgb, (int(x * 100), int(y * 100)), self.city_radius)
            i+=1

    def render_ants(self, ants: List[IAnt]):
        for ant in ants:
            tour = ant.tour
            if len(tour) < 2:
                continue
            # Draw the path of the ant (green line)
            for i in range(len(tour) - 1):
                city1 = ant.environment.cities[tour[i]]
                city2 = ant.environment.cities[tour[i + 1]]
                pygame.draw.line(self.screen, (0,255,0), (city1[0] * 100, city1[1] * 100), (city2[0] * 100, city2[1] * 100), 2)
    def disp_best_route(self,tour:List,env:Environment):
        for i in range(len(tour) - 1):
            city1 = env.cities[tour[i]]
            city2 = env.cities[tour[i + 1]]
            pygame.draw.line(self.screen, (0, 0, 255), (city1[0] * 100, city1[1] * 100), (city2[0] * 100, city2[1] * 100), 5)

    def update(self):
        pygame.display.flip()  # Update the display with the latest drawing

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

