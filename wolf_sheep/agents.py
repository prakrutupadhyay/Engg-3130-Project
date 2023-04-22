import mesa
from wolf_sheep.random_walk import RandomWalker
import numpy as np
import math


class Sheep(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        move_towards_sheep(self, self.model.sheep_clustering)
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

def move_towards_sheep(self, sheep_clustering):
#this function is how the sheep go towards each other
    neighbors = self.model.grid.get_neighbors(self.pos, sheep_clustering, True)


    sheep_neighbors = [agent for agent in neighbors if isinstance(agent, Sheep)]

    if len(sheep_neighbors) == 0:
        self.random_move()
        return

    #Finds center of mass of the nearby sheep!
    center_of_mass = np.mean([sheep.pos for sheep in sheep_neighbors], axis=0)
    center_of_mass = tuple(np.round(center_of_mass).astype(int))

    #Finds the direction towards the center of mass to go near the other sheep
    move_direction = np.array(center_of_mass) - np.array(self.pos)
    move_direction = move_direction / np.linalg.norm(move_direction)
    move_direction = tuple(np.round(move_direction).astype(int))

    #Finds the cell its gonna move to
    new_pos = self.pos + move_direction
    move_to = self.pos
    if (new_pos[0] >= 0 and new_pos[0] < 20 and new_pos[1] >= 0 and new_pos[1] < 20):
        move_to = tuple(np.array(new_pos))


    # If the cell to move to is not valid, move randomly
    if not self.model.grid.is_cell_empty(move_to[:2]):
        self.random_move()
        return

    # Move to the chosen cell
    self.model.grid.move_agent(self, move_to)


def distanceFinder(firstPos, secondPos):
    
    #Calculates distance between two positions

    x1, y1 = firstPos
    x2, y2 = secondPos
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Wolf(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # check if sheep are around
        neighbors = self.model.grid.get_neighbors(self.pos, self.model.near_sheep, True)
        sheep = [agent for agent in neighbors if isinstance(agent, Sheep)]

        # check if cheetah is around
        cheetahs = [agent for agent in neighbors if isinstance(agent, Cheetah)]
        if len(cheetahs) > 0:
            closest_cheetah = cheetahs[0]
            min_distance = distanceFinder(self.pos, closest_cheetah.pos)
            for current in cheetahs[1:]:
                dist = distanceFinder(self.pos, current.pos)
                if dist < min_distance:
                    closest_cheetah = current
                    min_distance = dist

            # if cheetah is too close, run away
            if min_distance < self.model.near_sheep:
                move_direction = np.array(self.pos) - np.array(closest_cheetah.pos)
                move_direction = move_direction / np.linalg.norm(move_direction)
                move_direction = tuple(np.round(move_direction).astype(int))
                new_pos = self.pos + move_direction

                # If cant go to the cell go to random place
                if not self.model.grid.is_cell_empty(new_pos[:2]):
                    self.random_move()
                    return

                # Move away from cheetah
                self.model.grid.move_agent(self, tuple(np.array(new_pos)))

        if len(sheep) > 0:
            # go towards closest sheep
            closest_sheep = sheep[0]
            min_distance = distanceFinder(self.pos, closest_sheep.pos)

            for current in sheep[1:]:
                dist = distanceFinder(self.pos, current.pos)
                if dist < min_distance:
                    closest_sheep = current
                    min_distance = dist

            # Move towards the closest sheep
            move_direction = np.array(closest_sheep.pos) - np.array(self.pos)
            move_direction = move_direction / np.linalg.norm(move_direction)
            move_direction = tuple(np.round(move_direction).astype(int))
            new_pos = self.pos + move_direction

            # If cant go to the cell go to random place
            if not self.model.grid.is_cell_empty(new_pos[:2]):
                self.random_move()
                return

            # Move to cell
            self.model.grid.move_agent(self, tuple(np.array(new_pos)))
        else:
            #  randomly move
            self.random_move()

        # Reduce energy
        self.energy -= 1

        # If there are sheep present, eat one
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

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # check if sheep or wolfs are around
        neighbors = self.model.grid.get_neighbors(self.pos, self.model.near_sheep2, True)
        sheep = [agent for agent in neighbors if isinstance(agent, Sheep)]
        wolfs = [agent for agent in neighbors if isinstance(agent, Wolf)]

        if len(wolfs) > 0:
            # go towards closest wolf
            closest_wolf = wolfs[0]
            min_distance = distanceFinder(self.pos, closest_wolf.pos)

            for current in wolfs[1:]:
                dist = distanceFinder(self.pos, current.pos)
                if dist < min_distance:
                    closest_wolf = current
                    min_distance = dist

            # Move towards the closest wolf
            move_direction = np.array(closest_wolf.pos) - np.array(self.pos)
            move_direction = move_direction / np.linalg.norm(move_direction)
            move_direction = tuple(np.round(move_direction).astype(int))
            new_pos = self.pos + move_direction

            # If cant go to the cell go to random place
            if not self.model.grid.is_cell_empty(new_pos[:2]):
                self.random_move()
                return

            # Move to cell and attempt to attack wolf
            self.model.grid.move_agent(self, tuple(np.array(new_pos)))
            if distanceFinder(self.pos, closest_wolf.pos) <= self.model.wolf_attack_range:
                self.attack(closest_wolf)

        elif len(sheep) > 0:
            # go towards closest sheep
            closest_sheep = sheep[0]
            min_distance = distanceFinder(self.pos, closest_sheep.pos)

            for current in sheep[1:]:
                dist = distanceFinder(self.pos, current.pos)
                if dist < min_distance:
                    closest_sheep = current
                    min_distance = dist

            # Move towards the closest sheep
            move_direction = np.array(closest_sheep.pos) - np.array(self.pos)
            move_direction = move_direction / np.linalg.norm(move_direction)
            move_direction = tuple(np.round(move_direction).astype(int))
            new_pos = self.pos + move_direction

            # If cant go to the cell go to random place
            if not self.model.grid.is_cell_empty(new_pos[:2]):
                self.random_move()
                return

            # Move to cell and attempt to eat sheep
            self.model.grid.move_agent(self, tuple(np.array(new_pos)))
            self.eat(closest_sheep)

        else:
            # randomly move
            self.random_move()

        # Reduce energy
        self.energy -= 1

        # Death
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

    def attack(self, target):
        # Calculate probability of success based on wolf's energy and the target's strength
        prob_success = self.energy / (self.energy + target.strength)
        if random.random() < prob_success:
            self.model.grid.remove_agent(target)
            self.energy += self.model.energy_gain_from_attack

    def eat(self, target):
        self.model.grid.remove_agent(target)
        self.energy += self.model.energy_gain_from_food
