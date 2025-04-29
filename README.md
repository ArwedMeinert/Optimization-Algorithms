# Optimization-Algorithms
Optimization algorithms created in the Manufacturing Optimization Course at HV.
All algorithms were implemented in Python.

## Simplex Algorithm
The Simplex algorithm solves simple linear optimization problems. The implementation is done from scratch without the use of any additional libraries. 

```python
objective = SimplexObjective(name='objective', inputEquation=[1,1,2], maximise=True)
eq1 = SimplexEquation(name='eq1', inputEquation=[2,1,1,50], smaller=True)
eq2 = SimplexEquation(name='eq2', inputEquation=[2,1,0,36], smaller=False)
eq3 = SimplexEquation(name='eq3', inputEquation=[1,0,1,10], smaller=False)
```

The objective and the constraints can be added. The solver then iteratively solves the problem with the following commands:

```python
equations = SimplexDataComposite('equations')
equations.add(eq1)
equations.add(eq2)
equations.add(eq3)
simplexdata = SimplexDataComposite('Data')
simplexdata.add(objective)
simplexdata.add(equations)

simplexdata.input()
simplexdata.display()
DataFormatted = simplexdata.format()
## DataFormatted.display()
SolveTable = SimplexTable(name="SolveTable")
SolveTable.addEquations(DataFormatted)
SolveTable.addObjective(objective)
SolveTable.display()
SolveTable.solveSimplex(debug=False)
SolveTable.display()
```

The solution is shown in the terminal:

<img src="https://github.com/user-attachments/assets/40e8117f-b47f-462f-9643-700cedc28fe0" width="30%" />

## Genetic Algorithm

It solves a problem iteratively by encoding the potential solutions in binary genomes. Multiple generations are created with random solutions in the solution space. They are evaluated based on a fitness function. The best variants are combined using different methods, and with a small probability, they are mutated. This method runs for multiple generations until no improvement for the fitness function is detected. 
The tournament and roulette selection are implemented as well.

The problem is taken from the lecture, and the fitness function is defined like this:

```python
def fitness(self) -> float:
    # This could just write the fitness value to self.fitness_value.
    # It would have saved me debugging if I had created it that way in the first place.
    fitness_value = 35 * (5833.3 / (330 - 2 * self.value)) + 208 * (50 / (self.value - 20))
    return fitness_value
```

The converting solution improves gradually:

<img src="https://github.com/user-attachments/assets/96e2e324-8781-49c3-9acb-288757a1b645" width="50%" />

## Ant Colony Algorithm

The last implemented algorithm aims to solve the TSP by simulating an ant colony. The ants deposit pheromones on the paths between cities based on the length of the full path the ant had to travel to reach all cities. Ants in the next generation are more likely to follow a path with more pheromones on it. After a few iterations, an optimal path is generated. 

```python
num_cities = 30
num_ants = 1000
num_iterations = 20

(evaporation_rate, alpha, beta, _) = find_optimal_values(num_cities=num_cities, amount_of_runs=60, amount_ants=num_ants, num_iterations=int(num_iterations/3))

cities = generate_random_cities(num_cities) 

algorithm = AntColonyAlgorithm(
    num_ants=num_ants, 
    cities=cities, 
    num_iterations=num_iterations * 5,
    evaporation_rate=evaporation_rate, 
    step_delay=1,
    alpha=alpha,
    beta=beta,
    visualise=True,
    visualise_ants=False
)
random.seed(19)
algorithm.run()
```

The number of cities and the number of ants can be defined. The algorithm runs for the specified number of iterations. For easier debugging, a seed can be defined. The same seed results in the generation of the same actions of the ants. 
The amount of pheromones is visualized by the thickness of a line between two cities. 
Since the tuning of the alpha, beta, and evaporation parameters proved to be challenging, a function was created that finds good values that can be used for the optimizer.

<img src="https://github.com/user-attachments/assets/0e5f345d-a3bc-4bb2-8616-466e6ea653c6" width="30%" />

The blue dot represents the start city. All other dots need to be visited, and the ant needs to return to the start city. The optimal order as well as the distance is returned.

## Particle Swarm Optimization

Finally, I have implemented a PSO algorithm that simulates the movement of individual particles based on global and individual knowledge. This was not part of the assignment, but I did it in my free time. 
The problem that was solved was shown in this video: [Video](https://youtu.be/bFbJhl9W89Q?si=o27CDPnp-Ao8EZTF)
The goal is to find the optimal location of a warehouse that should be as close as possible to the shops and as far away to the cities. The fitness function is defined like this:
```python
def fitness(self) -> float:
        closest_shop_dist = min(self.distance(self.position, city) for city in self.cities)
        closest_city_dist = min(self.distance(self.position, shop) for shop in self.shops)
        return -closest_city_dist + closest_shop_dist
```
While the solution was shown in the video, the complete program was written by myself. 

<img src="https://github.com/user-attachments/assets/ab0406d7-8916-4072-a470-798f34c5f9ab" width="30%" />

This is the start of the algorithm. Ten particles are placed random with random initial momentums. After a few iterations, the solution converges to the optimum:

<img src="https://github.com/user-attachments/assets/d4a69265-7e50-40a2-b99c-e18ad259ebd4" width="30%" />

The algorithm works fast and finds reliable solutions. 


