import random

from mesa import Agent
from Agents.IllegalImmigrant import IllegalImmigrant

class Radar(Agent):
    def __init__(self, unique_id, model, x, y, radar_distance_view, percentage_of_chance_to_escape_after_being_noticed_by_the_radar):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.radar_distance_view = radar_distance_view
        self.percentage_of_chance_to_escape_after_being_noticed_by_the_radar = percentage_of_chance_to_escape_after_being_noticed_by_the_radar

    def step(self):
        self.check_environment()

    def check_environment(self):
        if 0 <= self.x < self.model.width and 0 <= self.y < self.model.height:

            min_x, max_x = max(0, self.x - self.radar_distance_view), min(self.model.width - 1, self.x + self.radar_distance_view)
            min_y, max_y = max(0, self.y - self.radar_distance_view), min(self.model.height - 1, self.y + self.radar_distance_view)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for agent in self.model.grid[x][y]:
                        if isinstance(agent, IllegalImmigrant) and agent.is_arrested is False:
                            if random.random() > self.percentage_of_chance_to_escape_after_being_noticed_by_the_radar / 100:
                                self.model.captured_ii_count += 1
                                agent.is_arrested = True
