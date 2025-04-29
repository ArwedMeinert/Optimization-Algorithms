import pygame
import sys
import PSO
import numpy as np

class Renderer():
    def __init__(self,solution_space,cities,shops):
        pygame.init()
        self.solution_space=solution_space
        self.cities=cities
        self.shops=shops
        self.scale=10
        pygame.display.set_caption('PSO Optimisation')
        self.width=self.solution_space[0][1]-self.solution_space[0][0]
        self.height=self.solution_space[1][1]-self.solution_space[1][0]
        self.screen = pygame.display.set_mode((self.width*self.scale, self.height*self.scale))
        
        self.fitness_surface = pygame.Surface((self.width, self.height)).convert()
    
        self.display_fitness()
        self.blit_scaled_fitness()
        pygame.display.flip()
    
    def blit_scaled_fitness(self):
        # Scale up the fitness surface to screen size
        scaled = pygame.transform.scale(self.fitness_surface, (self.width * self.scale, self.height * self.scale))
        self.screen.blit(scaled, (0, 0))
    
    def render_enviroment(self,particles:list=None):
        for city in self.cities:
            color = (255, 0, 0)
            pygame.draw.circle(self.screen,color,[city[0]*self.scale,city[1]*self.scale],2)
        for shop in self.shops:
            color = (0, 255, 0)
            pygame.draw.circle(self.screen,color,[shop[0]*self.scale,shop[1]*self.scale],2)
            
        if particles is not None:
            for particle in particles:
                x=particle.position[0]*self.scale
                y=particle.position[1]*self.scale
                pygame.draw.circle(self.screen,(0,0,255),[x,y],2)
                
                
                
    def update(self,delay=500):
        pygame.display.flip()
        pygame.time.delay(delay)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                
    def display_fitness(self):
        min_fitness = float('inf')
        max_fitness = float('-inf')

        for x in range(self.width):
            for y in range(self.height):    
                fitness = self.fitness_function(x, y)
                if fitness < min_fitness:
                    min_fitness = fitness
                if fitness > max_fitness:
                    max_fitness = fitness

        for x in range(self.width):
            for y in range(self.height):
                fitness = self.fitness_function(x, y)
                color = map_color_by_scalar(fitness, min_fitness, max_fitness, [255, 0, 0], [0, 255, 0])
                self.fitness_surface.set_at((x, y), color)
 

        
    def fitness_function(self,x,y):
        closest_shop_dist = min(np.linalg.norm(self.distance([x,y],city)) for city in self.cities)
        closest_city_dist = min(np.linalg.norm(self.distance([x,y],shop)) for shop in self.shops)
        return(-closest_city_dist+closest_shop_dist)

    def distance(self,p1,p2):
        return((((p2[0]-p1[0])**2+p2[1]-p1[1])**2)**0.5)

def map_color_by_scalar(x, in_min, in_max, color_min, color_max):
    # Avoid division by zero
    if in_max == in_min:
        return color_min

    # Clamp x to input range
    x = max(in_min, min(in_max, x))

    # Interpolation factor
    t = (x - in_min) / (in_max - in_min)

    # Interpolate each RGB channel
    return [        int(color_min[i] + t * (color_max[i] - color_min[i]))
        for i in range(3)
    ]