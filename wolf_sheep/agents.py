import mesa
from wolf_sheep.random_walk import RandomWalker
import numpy as np


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # self.random_move()
        self.move_away_from()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [
                obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.sheep_reproduce:
            # Create a new sheep:
            if self.model.grass:
                self.energy /= 2
            lamb = Sheep(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)

    def move_away_from(self):
        """
            Move away from the nearest agent of class agent_class.
        """
        neighbors = self.model.grid.get_neighbors(self.pos, self.moore, True)
        wolf_neighbors = []

        # Find all wolf neighbors
        for neighbor in neighbors:

            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            wolf = [obj for obj in this_cell if isinstance(obj, Wolf)]

            if len(wolf) > 0:
                wolf_neighbors.append(neighbor)
        # # If there are no wolf neighbors, move randomly
        if not wolf_neighbors:
            self.random_move()
            return

        # Get the position of the nearest wolf neighbor
        nearest_wolf_pos = min(wolf_neighbors, key=lambda wolf: np.linalg.norm(
            np.array(self.pos) - np.array(wolf.pos))).pos

        # Find the direction away from the nearest wolf neighbor
        move_direction = np.array(self.pos) - np.array(nearest_wolf_pos)
        move_direction = move_direction / np.linalg.norm(move_direction)
        move_direction = tuple(np.round(move_direction).astype(int))

        # Find the cell to move to
        # print(move_direction)
        new_pos = self.pos + move_direction
        move_to = self.pos
        if (new_pos[0] >= 0 and new_pos[0] < 20 and new_pos[1] >= 0 and new_pos[1] < 20):

            move_to = tuple(np.array(new_pos))  # self.pos

        # If the cell to move to is not valid, move randomly
        if not self.model.grid.is_cell_empty(move_to[:2]):
            self.random_move()
            return

        # Move to the chosen cell
        self.model.grid.move_agent(self, move_to)

        # if agents:
        #     # Move directly away from the nearest agent of class agent_class
        #     agent_distances = [self.model.grid.get_distance(
        #         agent.pos, self.pos) for agent in agents]
        #     agent_to_flee = agents[agent_distances.index(min(agent_distances))]
        #     x, y = self.pos
        #     dx = x - agent_to_flee.pos[0]
        #     dy = y - agent_to_flee.pos[1]
        #     new_x, new_y = x + dx, y + dy
        #     if self.model.grid.is_cell_empty((new_x, new_y)):
        #         self.model.grid.move_agent(self, (new_x, new_y))
        #     else:
        #         self.random_move()
        # else:
        #     self.random_move()


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid.remove_agent(sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(mesa.Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1


class Cheetah(RandomWalker):
    """
    A cheetah that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid.remove_agent(sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.cheetah_reproduce:
                # Create a new cheetah cub
                self.energy /= 2
                cub = Cheetah(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
