from mesa import Agent

from Agents.BorderLine import BorderLine


class Migrant(Agent):
    def __init__(self, unique_id, model, x, y, is_illegal):
        super().__init__(unique_id, model)
        self.is_illegal = is_illegal
        self.x = x
        self.y = y

    def step(self):
        for agent in self.model.grid[self.x][self.y + 2]:
            if not isinstance(agent, Migrant):
                self.y += 2
                self.model.grid.move_agent(self, (self.x, self.y))

                neighbors = self.model.grid.get_neighbors(self.pos, True, radius=5)
                border_fence_places = [agent for agent in neighbors if agent.pos[0] == self.pos[0] and
                                       agent.pos[1] < self.pos[1] and isinstance(agent, BorderLine)]

                if len(border_fence_places) > 0:
                    if self.is_illegal:
                        self.model.not_captured_illegal_count += 1
                    if not self.is_illegal:
                        self.model.not_captured_legal_count += 1
                    self.model.schedule.remove(self)
