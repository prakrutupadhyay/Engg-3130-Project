"""
Generalized behavior for random walking, one grid cell at a time.
"""

import mesa
from mesa import Agent


class RandomWalker(mesa.Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(
            self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def move_away_from(self, agent_class):
        """
            Move away from the nearest agent of class agent_class.
        """
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
        agents = [agent for agent in neighbors if isinstance(
            agent, Wolf)]
        if agents:
            # Move directly away from the nearest agent of class agent_class
            agent_distances = [self.model.grid.get_distance(
                agent.pos, self.pos) for agent in agents]
            agent_to_flee = agents[agent_distances.index(min(agent_distances))]
            x, y = self.pos
            dx = x - agent_to_flee.pos[0]
            dy = y - agent_to_flee.pos[1]
            new_x, new_y = x + dx, y + dy
            if self.model.grid.is_cell_empty((new_x, new_y)):
                self.model.grid.move_agent(self, (new_x, new_y))
            else:
                self.random_move()
        else:
            self.random_move()
