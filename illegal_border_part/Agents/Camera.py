import random

from mesa import Agent
from Agents.IllegalImmigrant import IllegalImmigrant

class Camera(Agent):
    def __init__(self, unique_id, model, x, y, camera_distance_view, percentage_of_chance_to_escape_after_being_noticed_by_the_camera):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.camera_distance_view = camera_distance_view
        self.percentage_of_chance_to_escape_after_being_noticed_by_the_camera = percentage_of_chance_to_escape_after_being_noticed_by_the_camera

    def step(self):
        self.check_environment()

    def check_environment(self):
        if 0 <= self.x < self.model.width and 0 <= self.y < self.model.height:

            min_x, max_x = max(0, self.x - self.camera_distance_view), min(self.model.width - 1, self.x + self.camera_distance_view)
            min_y, max_y = max(0, self.y - self.camera_distance_view), min(self.model.height - 1, self.y)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for agent in self.model.grid[x][y]:
                        if isinstance(agent, IllegalImmigrant) and agent.is_arrested is False:
                            if random.random() > self.percentage_of_chance_to_escape_after_being_noticed_by_the_camera / 100:
                                self.model.captured_ii_count += 1
                                agent.is_arrested = True
