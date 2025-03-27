from typing import List, Dict, Optional, Self, Union
from abc import ABC, abstractmethod
from random import random, randrange, randint
from helper_functions import bin_to_float, float_to_bin

import matplotlib.pyplot as plt

class GaPopInterface(ABC):
    @abstractmethod
    def fitness(self)->float:
        pass
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def fitness(self)->float:
        pass
    @abstractmethod
    def uniform(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        pass
    @abstractmethod
    def arithmetric(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        pass
    @abstractmethod
    def crossover(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        pass
    @abstractmethod
    def mutate(self,debug=False)->None:
        pass
class DisplayInterface(ABC):
    # Display the data
    @abstractmethod
    def display(self):
        pass
class GaAlgorithmInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def gen_pop(self, amount:int):
        pass
    # Mutate a small proportion of the population
    @abstractmethod
    def mutate(self):
        pass
    # Main algorithm loop
    @abstractmethod
    def main(self,pop:int,max_iterations=10):
        pass
    @abstractmethod
    def result(self,debug=False):
        pass
    # Gives the ranking of the fitness function of the population.
    @abstractmethod
    def crossover(self,method="tournament"):
        pass
    @abstractmethod
    def display(self):
        pass
    
class MyGaPopInterface(GaPopInterface,DisplayInterface):
    # Generate a random individual
    value:float
    fitness_value:float
    relative_fitness:float
    def __init__(self) -> None:
        self.value=randrange(40,89,1)+random()
        self.fitness_value=self.fitness()
        self.relative_fitness=-1
    # Fitness function
    def fitness(self)->float: # this could just write the fitness value to self.fitness_value. It would have saved me debugging if i created it that way in the first place
        fitness_value=35*(5833.3/(330-2*self.value))+208*(50/(self.value-20))
        return fitness_value
    # Crossover between two individuals
    def uniform(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        binary1=float_to_bin(indiv1.value)
        binary2=float_to_bin(indiv2.value)
        newPop1=GaPopInterface()
        newPop2=GaPopInterface()
        no_good_offspring=True
        while no_good_offspring: #since it is random, it tries as long as it hasent found children that are within the constraints
            while len(binary1)!=len(binary2): #make binary numbers the same length
                if len(binary1)<len(binary2):
                    binary1.insert(0,0)
                if len(binary2)<len(binary1):
                    binary2.insert(0,0)

            newIndiv1=binary1.copy()
            newIndiv2=binary2.copy()

            if debug: 
                print(binary1)
                print(binary2)
            
            for i in range(len(binary1)):
                if random()<0.4:
                    newIndiv1[i]=binary2[i]
                    newIndiv2[i]=binary1[i] 
            if debug: 
                print(newIndiv1)
                print(newIndiv2)
            if not (bin_to_float(newIndiv1)<40 or bin_to_float(newIndiv1)>90) and not (bin_to_float(newIndiv2)<40 or bin_to_float(newIndiv2)>90): #checks if any of the offsprings is outside of valid range, if so, redo (at crossover and random)
                no_good_offspring=False
        newPop1.value=bin_to_float(newIndiv1)
        newPop2.value=bin_to_float(newIndiv2)
        newPop1.fitness_value=newPop1.fitness()
        newPop2.fitness_value=newPop2.fitness()
        return (newPop1,newPop2)
    def arithmetric(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        binary1=float_to_bin(indiv1.value)
        binary2=float_to_bin(indiv2.value)
        newPop1=GaPopInterface()
        newPop2=GaPopInterface()

        while len(binary1)!=len(binary2): #make binary numbers the same length
            if len(binary1)<len(binary2):
                binary1.insert(0,0)
            if len(binary2)<len(binary1):
                binary2.insert(0,0)
        newIndiv1=binary1.copy()
        newIndiv2=binary2.copy()
        if debug: 
            print(binary1)
            print(binary2)
        for i in range(len(binary1)):
            newIndiv1[i]=int(binary1[i] and binary2[i])
            newIndiv2[i]=int(binary1[i] or binary2[i])
        if debug: 
            print(newIndiv1)
            print(newIndiv2)
        # if a determenistic method is chosen and the value is out of bounds (constraints), the parent is taken to the next step
        if bin_to_float(newIndiv1)<40 or bin_to_float(newIndiv1)>90:
            newIndiv1=binary1.copy()
        if bin_to_float(newIndiv2)<40 or bin_to_float(newIndiv2)>90:
            newIndiv2=binary2.copy()
        newPop1.value=bin_to_float(newIndiv1)
        newPop2.value=bin_to_float(newIndiv2)
        newPop1.fitness_value=newPop1.fitness()
        newPop2.fitness_value=newPop2.fitness()
        return (newPop1,newPop2) #returns a list of the two resulting children
    def crossover(indiv1: Self, indiv2: Self,debug=False)->List[Self]:
        binary1=float_to_bin(indiv1.value)
        binary2=float_to_bin(indiv2.value)
        newPop1=MyGaPopInterface()
        newPop2=MyGaPopInterface()
        while len(binary1)!=len(binary2): #make binary numbers the same length
            if len(binary1)<len(binary2):
                binary1.insert(0,0)
            if len(binary2)<len(binary1):
                binary2.insert(0,0)

        newIndiv1=binary1.copy()
        newIndiv2=binary2.copy()

        if debug: 
            print(binary1)
            print(binary2)
        proportion=randint(1,len(binary1)//2) # randomly changes the amount of bits crossed (bits with high impact are rare to make small changes)
        newIndiv1[-proportion:]=binary2[-proportion:]
        newIndiv2[-proportion:]=binary1[-proportion:]
        if debug: 
            print(newIndiv1)
            print(newIndiv2)
        # if a determenistic method of crossover is chosen and the value is out of bounds, the parent is taken to the next step
        if bin_to_float(newIndiv1)<40 or bin_to_float(newIndiv1)>90:
            newIndiv1=binary1.copy()
        if bin_to_float(newIndiv2)<40 or bin_to_float(newIndiv2)>90:
            newIndiv2=binary2.copy()
        newPop1.value=bin_to_float(newIndiv1)
        newPop2.value=bin_to_float(newIndiv2)
        newPop1.fitness_value=newPop1.fitness()
        newPop2.fitness_value=newPop2.fitness()
        return (newPop1,newPop2)
        
    # Mutate the individual
    def mutate(self,debug=False)->None:
        no_good_mutation=True
        if debug: print(self.value)
        while no_good_mutation: # redoes the mutation process if the value is not within the constraints
            binary=float_to_bin(self.value)
            for i in range(len(binary)):
                if random()<0.1: # since most bits only have a small impact, the mutation chance is quite high
                    binary[i]=int(not binary[i])
            mutated_value=bin_to_float(binary)
            if 40 <= mutated_value <= 90:
                no_good_mutation=False
        self.value=bin_to_float(binary)
        self.fitness_value=self.fitness()
        if debug:print(self.value)
    # displays the values for one individuum
    def display(self):
        print(f"The Value is {self.value} and the fitness is {self.fitness_value}")



    
class MyGaAlgorithmInterface(GaAlgorithmInterface,DisplayInterface):
    iter_num: int
    pop: List[GaPopInterface]
    fitness_list=[]
    # Generate initial population
    def __init__(self) -> None:
        self.iter_num=0
        self.pop=[]
    def gen_pop(self, amount:int):
        for i in range(amount):
            self.pop.append(MyGaPopInterface())
    # Mutate a small proportion of the population
    def mutate(self):
        for Individual in self.pop:
            Individual.mutate()
    # Main algorithm loop
    def main(self,pop:int,max_iterations=10):
        best_fitness=float('inf') # minimisation, therefore inf
        best_value=float('inf')
        best_indiv: MyGaPopInterface
        self.gen_pop(pop)
        while self.iter_num<max_iterations: # it is also possible to check for how may iterations no changes were made. At larger solution spaces, a new population can be created in that case
            self.crossover(method="tournament") # tournament is chosen, since it is a minimisation problem
            self.mutate()
            (current_fitness,current_value,best_indiv_pos)=self.result(debug=False)
            self.iter_num+=1
            if current_fitness<best_fitness:
                best_fitness=current_fitness
                best_value=current_value
                best_indiv=self.pop[best_indiv_pos]
            self.fitness_list.append(best_fitness)    
        self.display()
        best_indiv.display()
    # Get the result of the algorithm (best individual)
    def result(self,debug=False):
        bestPop=-1
        best_fitness=float('inf')
        for i,Individual in enumerate(self.pop):
            if Individual.fitness_value<best_fitness:
                best_fitness=Individual.fitness_value
                bestPop=i
        if debug: print(best_fitness)
        best_value=self.pop[bestPop].value
        return (best_fitness,best_value,bestPop)

    # Gives the ranking of the fitness function of the population.
    def crossover(self,method="tournament"):
        new_pop=self.pop.copy()
        if method=="roulett": # only to be used with maximisation problems! (in that case, there need to be some changes in the code and the evaluation function. other than that, it works (and finds the maximal value))
            sum_fitness=0
            for Indiv in self.pop:
                sum_fitness+=1/(1+Indiv.value)
            for Indiv in self.pop:
                Indiv.relative_fitness=(1/(1+Indiv.value))/sum_fitness
            for i in range(0,len(self.pop),2):
                wheel=random()
                father=0
                ball=self.pop[father].relative_fitness
                while ball<wheel:
                    father+=1
                    ball+=self.pop[father].relative_fitness
                mother=0
                wheel=random()
                ball=self.pop[mother].relative_fitness
                while ball<wheel:
                    mother+=1
                    ball+=self.pop[mother].relative_fitness
                offspring=GaPopInterface.crossover(self.pop[father],self.pop[mother],method="crossover")
                new_pop[i]=offspring[0]
                new_pop[i+1]=offspring[1]
            self.pop=new_pop
        elif method=="tournament": # to be used in minimisation and maximisation problems (only need to change the tournament rules)
            population_size=len(self.pop)
            parent_population=[]
            while population_size/2 >len(parent_population):
                first_competitor=randint(0,population_size-1)
                second_competitor=randint(0,population_size-1)
                while second_competitor==first_competitor:
                    second_competitor=randint(0,population_size-1)
                if self.pop[first_competitor].fitness_value<self.pop[second_competitor].fitness_value:
                    parent_population.append(self.pop[first_competitor])
                else:
                    parent_population.append(self.pop[second_competitor])
            for i in range(0,len(self.pop),2):
                father=randint(0,len(parent_population)-1)
                mother=randint(0,len(parent_population)-1)
                while mother==father:
                    mother=randint(0,len(parent_population)-1)
                offspring=MyGaPopInterface.crossover(parent_population[father],parent_population[mother]) # here, the arithmetric or uniform method can be chosen
                #offspring=GaPopInterface.uniform(parent_population[father],parent_population[mother])
                #offspring=GaPopInterface.arithmetric(parent_population[father],parent_population[mother])
                new_pop[i]=offspring[0]
                new_pop[i+1]=offspring[1]
            self.pop=new_pop
    def display(self):
        #for Ind in self.pop:
        #    Ind.displayInd()
        # plots the best element in the process
        plt.plot(self.fitness_list)
        plt.show()

# This solves the example given in the Lecture 5    
MyGAAlgorithm=MyGaAlgorithmInterface()
MyGAAlgorithm.main(8,10)




