import math
import random
from mesa import Agent

from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine


class IllegalImmigrant(Agent):
    def __init__(self, unique_id, model, x, y, speed, tool_efficiency,
                 percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.x = x
        self.y = y
        self.speed = speed
        self.tool_efficiency = tool_efficiency
        self.percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed = percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed
        self.is_arrested = False
        self.destroying_fence = None

    def step(self):
        if self.is_arrested:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            neighbors = self.model.grid.get_neighbors(self.pos, True, radius=self.speed)

            border_fence_places = [agent for agent in neighbors if
                                   agent.pos[1] > self.pos[1] and isinstance(agent, BorderFence)]
            if len(border_fence_places) > 0 and self.destroying_fence is None:
                self.fence_managing(border_fence_places)

            else:
                self.move(neighbors)

    def fence_managing(self, border_fence_places):
        destroyed_border_fence_places = [agent for agent in border_fence_places if agent.is_destroyed is True]
        if len(destroyed_border_fence_places) == 0 or \
                random.random() < self.percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed / 100:
            self.choose_fence_place_to_destroy(border_fence_places)
        else:
            self.choose_destroyed_place_in_fance(destroyed_border_fence_places)

    def choose_destroyed_place_in_fance(self, destroyed_border_fence_places):
        place = random.choice(destroyed_border_fence_places)
        self.go_to_place(place.pos)
        self.destroying_fence = place

    def choose_fence_place_to_destroy(self, border_fence_places):
        chosen_fence = min(border_fence_places, key=lambda x: x.resilience)
        self.go_to_place(chosen_fence.pos)
        self.destroying_fence = chosen_fence

    def go_to_place(self, chosen_position):
        new_x, new_y = chosen_position
        new_y = new_y - 2
        if 0 < new_x < self.model.width and 0 < new_y < self.model.height:
            self.x = new_x
            self.y = new_y
            self.model.grid.move_agent(self, (self.x, self.y))

    def move(self, neighbors):
        if self.destroying_fence is not None and self.destroying_fence.is_destroyed is False:
            self.try_to_destroy_border_fence(self.destroying_fence)
            return

        y = random.randint(0, self.speed)
        max_x = round(math.sqrt(self.speed // 2 - y // 2))
        x = random.randint(-max_x, max_x)

        new_x = self.x + x
        new_y = self.y + y
        self.go_to_place((new_x, new_y))

        border_fence_places = [agent for agent in neighbors if agent.pos[0] == self.pos[0] and
                               agent.pos[1] < self.pos[1] and isinstance(agent, BorderLine)]

        if len(border_fence_places) > 0:
            self.model.not_captured_ii_count += 1
            self.model.schedule.remove(self)

    def try_to_destroy_border_fence(self, border_fence_place: BorderFence):
        border_fence_place.resilience -= self.tool_efficiency
        if border_fence_place.resilience <= 0:
            border_fence_place.is_destroyed = True