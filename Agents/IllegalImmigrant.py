import math
import random
from mesa import Agent

from Agents.GuardPatrol import GuardPatrol
from Agents.Camera import Camera


class IllegalImmigrant(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.speed = 10
        self.tool_efficiency = random.randint(1, 20)

    def step(self):
        self.move()

    def move(self):
        y = random.randint(0, self.speed)
        max_x = round(math.sqrt(self.speed // 2 - y // 2))
        x = random.randint(-max_x, max_x)

        new_x = self.x + x
        new_y = self.y + y

        if 0 < new_x < self.model.width and 0 < new_y < self.model.height:
            self.x = new_x
            self.y = new_y
            self.model.grid.move_agent(self, (self.x, self.y))

        if 0 <= new_x < self.model.width and 0 <= new_y < self.model.height:
            # Check if the new position is within the valid range for neighboring cells
            min_x, max_x = max(0, new_x - 5), min(self.model.width - 1, new_x + 5)
            min_y, max_y = max(0, new_y - 5), min(self.model.height - 1, new_y + 5)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for agent in self.model.grid[x][y]:
                        if isinstance(agent, GuardPatrol) or isinstance(agent, Camera):
                            self.model.captured_ii_count += 1
                            self.model.schedule.remove(self)
                            return

        if self.y >= self.model.height - 3:
            self.model.not_captured_ii_count += 1
            self.model.schedule.remove(self)