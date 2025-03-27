import random
from typing import List, Tuple

import pygame


from acoEnv import Environment, PygameRenderer
from acoInterface import IAnt, IAntColonyAlgorithm, IEnvironment, IRenderer

import random

class Ant(IAnt):
    def __init__(self, environment: IEnvironment):
        self.environment = environment
        self.amount_cities = len(self.environment.get_cities())
        self.start_city = 0
        self.current_city = self.start_city
        self.distance_traveled = 0
        self.tour = [self.start_city]  # Initialize with the start city
        self.distances = []
        self.pheromones = []

    def initialize(self):
        self.distance_traveled = 0
        self.tour = [self.start_city]  # Reset the tour and start city
        self.current_city = self.start_city
        self.distances = []  # Clear the previous distances
        self.pheromones = []  # Clear the previous pheromones
        
        # Populate distances and pheromones from the environment
        for city_from in range(self.amount_cities):
            distance_to = []
            pheromones_to = []
            for city_to in range(self.amount_cities):
                distance_to.append(self.environment.get_distance(city_from, city_to))
                pheromones_to.append(self.environment.get_pheromone_level(city_from, city_to))
            self.distances.append(distance_to)
            self.pheromones.append(pheromones_to)
        
    def _calculate_probability(self,current_city:int,alpha=1.0,beta=1.0)->List: # calculates the list of propabilitys where the ant should move next in respect to the current city. if a city already has been visited, the propability is 0
        propabilitys=[]
        sum_edge=0
        for city in range(self.amount_cities): # calculate the sum of probabilities
            if city not in self.tour:
                sum_edge+=self.pheromones[current_city][city]**alpha*self.distances[current_city][city]**beta
        for city in range(self.amount_cities): #creates the propability ist. this is going to be used in the roulett selection
            if city not in self.tour:
                propability=(self.pheromones[current_city][city]**alpha*self.distances[current_city][city]**beta)/sum_edge
                propabilitys.append(propability)
            else:
                propabilitys.append(0)
        #print(propabilitys)
        return propabilitys 


    def move(self,alpha=1,beta=1):
        next_city=0 # next city to move to
        propabilitys=self._calculate_probability(self.current_city,alpha=alpha,beta=beta) #calculate probabilities for the current city
        next_step=random.random() #spin the wheel
        propability_sum=propabilitys[next_city] # initialise the roulett with the probability of the fist city
        while next_step>propability_sum and next_city<self.amount_cities-1: #roulett wheel selection
            next_city+=1
            propability_sum+=propabilitys[next_city]
        if next_city < self.amount_cities and next_city not in self.tour: # check if the city already has been visited (should not be the case, since the probability is 0, but there might be edge cases where 0 is actually 0.00001)
            self.tour.append(next_city)
            self.current_city=next_city
            self.distance_traveled+=self.environment.get_distance(self.tour[-2],self.tour[-1])
        if len(self.tour) == self.amount_cities: # all cities have been visited, the ant should return to the starting city (TSP)
            # Return to the starting city and complete the tour
            self.tour.append(self.start_city)
            self.distance_traveled += self.environment.get_distance(self.tour[-2], self.tour[-1])
        #print(self.tour)


    def has_found_goal(self)->bool:
        if len(self.tour)!=self.amount_cities+1: # check if the ant has reacht the starting location again
            return False
        else:
            return True

    def deposit_pheromone(self):
        amount = 1 / self.distance_traveled
        for i in range(len(self.tour) - 1):
            # get the actual cities from the tour list
            city1 = self.tour[i]
            city2 = self.tour[i + 1]
        
            # calculate the amount of pheromone to deposit
            #amount = 1 / self.environment.get_distance(city1, city2)
        
            # update the pheromone levels between city1 and city2
            self.environment.update_pheromone(city1, city2, amount=amount)

class AntColonyAlgorithm(IAntColonyAlgorithm):
    # added the visualisation variable for easier debugging and faster testing
    def __init__(self, num_ants, cities, num_iterations, evaporation_rate=0.2, step_delay=500,alpha=1,beta=1,visualise=True,visualise_ants=True):
        self.environment = Environment(cities, evaporation_rate)
        self.visualise=visualise
        self.visualise_ants=visualise_ants
        self.ants = [Ant(self.environment) for _ in range(num_ants)]
        if self.visualise: self.renderer = PygameRenderer()
        self.num_iterations = num_iterations
        self.step_delay = step_delay  # Delay between each step (in milliseconds)
        self.shortest_distance=float('inf') # store the shortest distance
        self.best_route=[]
        self.alpha=alpha
        self.beta=beta

    def initialize(self):
        for ant in self.ants:
            ant.initialize()

    def reset_pheromone_levels(self, initial_pheromone: float = 1):
        cities = self.environment.get_cities()
        num_cities = len(cities)

        for i in range(num_cities):
            for j in range(num_cities):
                if i != j:
                    # update the pheromone level between city i and city j
                    self.environment.update_pheromone(i, j, amount=initial_pheromone)

    def run(self):
        for iteration in range(self.num_iterations):
            self.environment.evaporate_pheromone()  # Evaporate pheromones
            self.initialize()  # Initialize ants for a new iteration

            # Move each ant to complete their tour
            for ant in self.ants:
                while not ant.has_found_goal():
                    ant.move(alpha=self.alpha,beta=self.beta)

                    # Render after each ant's move
                    if self.visualise_ants: self.renderer.handle_events()  # Handle window close events
                    if self.visualise_ants: self.renderer.render_environment(self.environment)
                    if self.visualise_ants: self.renderer.render_ants(self.ants)
                    if self.visualise_ants: self.renderer.disp_best_route(self.best_route,self.environment)
                    if self.visualise_ants: self.renderer.update()
                    if self.visualise_ants: pygame.time.delay(self.step_delay)  # Pause for step visualization
        
            if self.visualise: self.renderer.handle_events()  # Handle window close events
            if self.visualise: self.renderer.render_environment(self.environment)
            if self.visualise: self.renderer.disp_best_route(self.best_route,self.environment)
            if self.visualise: self.renderer.update()
            #if self.visualise: pygame.time.delay(self.step_delay)  # Pause for step visualization
            # Update pheromones based on ants' tours
            new_path_discovered=False
            for ant in self.ants:
                ant.deposit_pheromone()
                if ant.distance_traveled<self.shortest_distance:
                    self.shortest_distance=ant.distance_traveled
                    self.best_route=ant.tour.copy()
                    if self.visualise: print(self.shortest_distance)
                    new_path_discovered=True
                    iterations_without_progress=0
            if not new_path_discovered:
                iterations_without_progress+=1
            if iterations_without_progress>3000:
                self.reset_pheromone_levels(0.2)
                if self.visualise: print("pheromones reset")
                iterations_without_progress=0

        if self.visualise: self.renderer.disp_best_route(self.best_route,self.environment)
        if self.visualise: self.renderer.update()
        if self.visualise: print(self.best_route)
        

        # Keep the window open until manually closed
        if self.visualise:
            while True:
                self.renderer.handle_events()
        return self.shortest_distance # can be used to find the best parameters via brute force



def generate_random_cities(num_cities, x_range=(0, 8), y_range=(0, 6)):
    """Generates a list of cities with random (x, y) coordinates."""
    cities = []
    for _ in range(num_cities):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        cities.append((x, y))
    return cities


#this function finds the best values for the parameters. If one is very motivated, this could be a genetic algorithm. but this solutions still gives back decent values
def find_optimal_values(num_cities:int,amount_of_runs:int,amount_ants=10,num_iterations=50):
    cities=generate_random_cities(num_cities)
    shortest_distance=float('inf')
    for i in range(amount_of_runs):
        random.seed()
        num_ants=amount_ants
        num_iterations=num_iterations
        evaporation_rate=random.triangular(0.05,0.9,0.35) # the random numbers are generated with a bias of recommended values by chat gpt
        alpha=random.triangular(0.1,10,1)
        beta=random.triangular(0.4,10,4)
        
        algorithm = AntColonyAlgorithm(num_ants=num_ants, cities=cities, num_iterations=num_iterations,evaporation_rate=evaporation_rate, step_delay=1,alpha=alpha,beta=beta,visualise=False,visualise_ants=False)
        random.seed(19)
        shortest_distance_algorithm=algorithm.run()
        if shortest_distance_algorithm<shortest_distance:
            shortest_distance=shortest_distance_algorithm
            best_evaporation = evaporation_rate
            best_alpha = alpha
            best_beta = beta
    print("The shortest distance was: "+str(shortest_distance)+ ". The best evaporation was: "+str(best_evaporation)+ ". The best alpha value was: "+ str(best_alpha)+". And the best Beta value was: "+str(best_beta))
    return(best_evaporation,best_alpha,best_beta,cities)


#algorithm = AntColonyAlgorithm(num_ants=20, cities=cities, num_iterations=50,evaporation_rate=0.5, step_delay=1,alpha=2,beta=1,visualise=True)
#algorithm.run()
num_cities = 7
num_ants=100
num_iterations=30000

(evaporation_rate,alpha,beta,_)=(0.5,1,1,1)#find_optimal_values(num_cities=num_cities,amount_of_runs=60,amount_ants=num_ants,num_iterations=int(num_iterations/3))

cities = generate_random_cities(num_cities)  # Generate 10 random cities

algorithm = AntColonyAlgorithm(num_ants=num_ants, cities=cities, num_iterations=num_iterations*5,evaporation_rate=evaporation_rate, step_delay=1,alpha=alpha,beta=beta,visualise=True,visualise_ants=False)
random.seed(19)
algorithm.run()