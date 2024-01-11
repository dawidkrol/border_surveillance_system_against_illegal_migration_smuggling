import random
from mesa import Agent


class GuardPatrol(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y

    def step(self):
        self.move()

    def move(self):
        max_length = 5

        x = random.randint(0, max_length)

        self.x = self.x + x

        self.model.grid.move_agent(self, (self.x, self.y))