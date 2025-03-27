from typing import List, Tuple


class IEnvironment:
    def get_pheromone_level(self, city1: Tuple[int, int], city2: Tuple[int, int]) -> float:
        """Returns the pheromone level at a given position."""
        pass

    def update_pheromone(self, city1: Tuple[int, int], city2: Tuple[int, int], amount: float):
        """Updates the pheromone level at a specific position by adding an amount."""
        pass

    def evaporate_pheromone(self, evaporation_rate: float):
        """Simulates evaporation by reducing pheromone levels across the environment."""
        pass
    def get_distance(self, city1, city2):
        """Return the distance between two cities"""
        pass
    def get_cities(self):
        """Return the list of cityies"""

class IAnt:
    def initialize(self):
        pass

    def move(self):
        """Moves the ant to a new position based on local pheromone information."""
        pass

    def deposit_pheromone(self):
        """Deposits pheromone at the current position."""
        pass

    def has_found_goal(self) -> bool:
        """Returns whether the ant has reached the goal."""
        pass

class IRenderer:
    def render_environment(self, environment: IEnvironment):
        """Renders the environment and pheromone trails."""
        pass

    def render_ants(self, ants: List[IAnt]):
        """Renders the ants in the environment."""
        pass

    def update(self):
        """Updates the visual display."""
        pass
class IAntColonyAlgorithm:
    def initialize(self):
        """Initializes the environment, ants, and other required components."""
        pass

    def run(self):
        """Runs the ACO algorithm, updating ant positions, pheromone trails, and rendering."""
        pass


