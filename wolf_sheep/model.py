import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from agents import Sheep, Wolf


class WolfPredationModel(Model):
    def __init__(self, height, width, initial_sheep, sheep_reproduce, initial_wolves, wolf_reproduce,
                 wolf_gain_from_food, sheep_gain_from_food):
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.sheep_reproduce = sheep_reproduce
        self.initial_wolves = initial_wolves
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep((x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves:
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf((x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        self.running = True

    def step(self):
        self.schedule.step()
