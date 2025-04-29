import random
import PSO_Enviroment
import numpy as np

class Particle_indiv():
    def __init__(self, solution_space:list,cities:list,shops:list):
        '''
        param solution_space: list of lists that define the dimension (eg [[0,40],[0,40]] for a 2d solution space ranging from 0,0 to 40,40)
        '''
        self.position=[]
        self.momentum=[]
        self.cities=cities
        self.shops=shops
        self.solution_space=solution_space
        #initial position
        for dimension in self.solution_space:
            self.position.append(random.randrange(dimension[0],dimension[1]))
            self.momentum.append(random.random())
        print(self.position)
        self.indiv_optimum=self.position
        self.fitness_current=self.fitness()
        self.fitness_best=self.fitness_current
        self.fitness_best_pos=self.position
        self.movements=0
    
    def fitness(self) -> float:
        closest_shop_dist = min(self.distance(self.position, city) for city in self.cities)
        closest_city_dist = min(self.distance(self.position, shop) for shop in self.shops)
        return -closest_city_dist + closest_shop_dist

    
    def move(self, global_optimum, weights=[0.5, 1.5, 1.5]):  # [inertia, cognitive, social]
        inertia = weights[0]
        cognitive = weights[1]
        social = weights[2]

        if self.movements == 0:
            self.position = [self.position[0] + self.momentum[0], self.position[1] + self.momentum[1]]
            self.fitness_current = self.fitness()
            self.movements += 1
            return

        r1 = random.random()
        r2 = random.random()

        # Update momentum (velocity) using standard PSO rule
        new_momentum = []
        for i in range(2):
            cognitive_term = cognitive * r1 * (self.fitness_best_pos[i] - self.position[i])
            social_term = social * r2 * (global_optimum[i] - self.position[i])
            new_velocity = inertia * self.momentum[i] + cognitive_term + social_term
            new_momentum.append(new_velocity)
        
        self.momentum = new_momentum

        # Update position
        self.position = [self.position[i] + self.momentum[i] for i in range(2)]

        for i in range(2):
            min_bound, max_bound = self.solution_space[i]
            self.position[i] = max(min_bound, min(self.position[i], max_bound))
            
        # Update fitness and personal best
        self.fitness_current = self.fitness()
        if self.fitness_current > self.fitness_best:
            self.fitness_best = self.fitness_current
            self.fitness_best_pos = self.position[:]

        self.movements += 1

        
        
        
        
        
    
    def distance(self,p1,p2):
        return(((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**0.5)
            
class Swarm():
    def __init__(self,particles:int,solution_space:list,cities:list,shops:list):
        self.particles=[]
        self.cities=cities
        self.shops=shops
        self.global_optimum_fitness=float('-inf')
        self.global_optimum_pos=None
        for particle in range(particles):
            self.particles.append(Particle_indiv(solution_space,self.cities,self.shops))
        
        for particle in self.particles:
            if particle.fitness_current>self.global_optimum_fitness:
                self.global_optimum_fitness=particle.fitness_current
                self.global_optimum_pos=particle.position
            
    def move(self,weights=[1,1,1]):
        potential_optimum=self.global_optimum_fitness
        potential_position=[]
        for particle in self.particles:
            particle.move(self.global_optimum_pos,weights)
            if particle.fitness_current>potential_optimum:
                potential_optimum=particle.fitness_current
                potential_position=particle.position.copy()
        if potential_optimum>self.global_optimum_fitness:
            self.global_optimum_fitness=potential_optimum
            self.global_optimum_pos=potential_position
            
if __name__=='__main__':
    solution_space=[[0,40],[0,40]]
    shops=  [[20,20],
            [15,4],
            [35,35],
            [4,10]]
    cities=[[12,23],
            [10,5],
            [39,3],
            [0,0],
            [0,40],
            [40,40],
            [40,0]]
    particleswarm=Swarm(10,solution_space,cities,shops)
    render=PSO_Enviroment.Renderer(solution_space,cities,shops)
    for i in range(50):
        # Linearly decay inertia weight from 1.0 to 0.4
        inertia = 1.0 - (0.6 * (i / 50))  # w from 1.0 to 0.4
        c1 = 1.5  # global influence
        c2 = 1.5  # personal influence

        particleswarm.move([inertia, c1, c2])
        
        render.render_enviroment(particleswarm.particles, particleswarm.global_optimum_pos)
        print(f"Step {i:3}: Best Fitness = {particleswarm.global_optimum_fitness:.3f}")
        render.update(200)  # faster update for smoother visuals
    