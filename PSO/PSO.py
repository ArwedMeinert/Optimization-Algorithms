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
        #initial position
        for dimension in solution_space:
            self.position.append(random.randrange(dimension[0],dimension[1]))
            self.momentum.append(random.random())
        print(self.position)
        self.indiv_optimum=self.position
        self.fitness_current=self.fitness()
        self.fitness_best=self.fitness_current
        self.fitness_best_pos=self.position
        self.movements=0
    
    def fitness(self)->float:
        closest_shop_dist = min(np.linalg.norm(self.distance(self.position,city)) for city in self.cities)
        closest_city_dist = min(np.linalg.norm(self.distance(self.position,shop)) for shop in self.shops)
        return(-closest_city_dist+closest_shop_dist)
    
    def move(self,global_optimum:float,wheigts=[0.1,0.1,1]):
        def direction(p1:list,p2:list)->list:
            norm=self.distance(p1,p2)
            return [(p2[0]-p1[0])/norm,(p2[1]-p1[1])/norm]
        
        if self.movements==0:
            self.position=[self.position[0]+self.momentum[0],self.position[0]+self.momentum[0]]
            self.fitness()
            self.movements+=1
            return
        direction_global=direction(self.position,global_optimum)
        direction_local=direction(self.position,self.fitness_best_pos)
        x_vector=direction_global[0]*wheigts[0]+direction_local[0]*wheigts[1]*self.momentum[0]*wheigts[2]
        y_vector=direction_global[1]*wheigts[0]+direction_local[1]*wheigts[1]*self.momentum[1]*wheigts[2]
        norm=((x_vector**2)+(y_vector**2))**0.5
        self.momentum=[x_vector/norm,y_vector/norm]
        self.position=[self.position[0]+self.momentum[0],self.position[0]+self.momentum[0]]
        self.movements+=1
        self.fitness()
        
        
        
        
        
    
    def distance(self,p1,p2):
        return((((p2[0]-p1[0])**2+p2[1]-p1[1])**2)**0.5)
            
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
            
    def move(self):
        for particle in self.particles:
            particle.move(self.global_optimum_pos)
            
            
if __name__=='__main__':
    solution_space=[[0,40],[0,40]]
    shops=  [[20,20],
            [15,4],
            [35,35],
            [4,10]]
    cities=[[12,23],
            [10,5],
            [39,3]]
    particleswarm=Swarm(5,solution_space,cities,shops)
    for i in range(100):
        particleswarm.move()
        render=PSO_Enviroment.Renderer(solution_space,cities,shops)
        render.render_enviroment(particleswarm.particles)
        render.update()
    