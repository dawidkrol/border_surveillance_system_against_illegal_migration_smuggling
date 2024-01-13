import random
from mesa import Agent

from Agents.BorderFence import BorderFence
from Agents.IllegalImmigrant import IllegalImmigrant

class GuardPatrol(Agent):
    def __init__(self, unique_id, model, x, y, speed, patrol_distance_view, how_many_suspects_it_can_capture_at_the_same_time):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.speed = speed
        self.patrol_distance_view = patrol_distance_view
        self.how_many_suspects_it_can_capture_at_the_same_time = how_many_suspects_it_can_capture_at_the_same_time
        self.watch_destroyed_fence = False

    def step(self):
        self.move()
        self.check_enviroment()

    def move(self):
        neighbors = self.model.grid.get_neighbors(self.pos, True, radius=self.patrol_distance_view)

        destroyed_border_fence_places = [agent for agent in neighbors if isinstance(agent, BorderFence)
                                         and agent.is_destroyed is True]

        guards_near = [agent for agent in neighbors if isinstance(agent, GuardPatrol) and agent.watch_destroyed_fence == True]

        if (len(destroyed_border_fence_places) > 0 and len(guards_near) == 0) or self.watch_destroyed_fence == True:
            place = random.choice(destroyed_border_fence_places)
            self.watch_destroyed_fence = True
            self.go_to_place(place.pos)
            return

        else:
            x = random.randint(0, self.speed)
            self.x = self.x + x
            self.model.grid.move_agent(self, (self.x, self.y))

    def go_to_place(self, chosen_position):
        new_x, new_y = chosen_position
        new_y = new_y + 4
        if 0 < new_x < self.model.width and 0 < new_y < self.model.height:
            self.x = new_x
            self.y = new_y
            self.model.grid.move_agent(self, (self.x, self.y))

    def check_enviroment(self):
        if 0 <= self.x < self.model.width and 0 <= self.y < self.model.height:
            min_x, max_x = max(0, self.x - 5), min(self.model.width - 1, self.x + 5)
            min_y, max_y = max(0, self.y - 5), min(self.model.height - 1, self.y + 5)

            captured_migrant = 0

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for agent in self.model.grid[x][y]:
                        if isinstance(agent, IllegalImmigrant) and agent.is_arrested is False and captured_migrant < self.how_many_suspects_it_can_capture_at_the_same_time:
                            self.model.captured_ii_count += 1
                            agent.is_arrested = True
                            captured_migrant += 1
            if captured_migrant > 0:
                print(captured_migrant)
            return
