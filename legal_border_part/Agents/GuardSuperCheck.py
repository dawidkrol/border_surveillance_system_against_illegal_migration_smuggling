import numpy as np
from mesa import Agent

from Agents.Migrant import Migrant


class GuardSuperCheck(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.suspiciousness = 0.5
        self.accuracy = 1.0

        self.migrant_to_check = None
        self.go_to_arest = False

        self.steps_to_arest = 4
        self.actual_steps = 0
        self.aresting = False


    def step(self):
        if self.aresting:
            if self.actual_steps >= self.steps_to_arest:
                self.arest_migrant()
                return
            else:
                self.actual_steps += 1
                return

        neighbors_2 = self.model.grid.get_neighbors(self.pos, True, radius=2)

        agents = [agent for agent in neighbors_2 if isinstance(agent, Migrant)]
        if len(agents) > 0:
            if self.migrant_to_check is None:
                agents.sort(key=lambda x: x.pos[1], reverse=True)
                self.migrant_to_check = agents[0]
                self.migrant_to_check.stopped = True
                return

            if not self.check_documents():
                self.aresting = True
                return

            if not self.check_items():
                self.aresting = True
                return

            self.return_agent_to_the_road()


    def check_documents(self) -> bool:
        return np.abs(self.migrant_to_check.legal_documents - 1) * self.accuracy <= 0.2

    def check_items(self) -> bool:
        return self.suspiciousness * (self.migrant_to_check.illegal_items - 1) <= 0.3

    def arest_migrant(self):
        if self.migrant_to_check.is_illegal:
            self.model.captured_illegal_count += 1
        else:
            self.model.captured_legal_count += 1

        self.migrant_to_check.is_arrested = True
        self.migrant_to_check = None
        self.aresting = False
        self.actual_steps = 0

    def return_agent_to_the_road(self):
        w = self.model.width // 2 + 2
        h = self.pos[1] + 2
        if len(self.model.grid[w][h]) == 1 and len(self.model.grid[w][h + 1]) == 1 and \
            len(self.model.grid[w][h - 1]) == 1 and len(self.model.grid[w][h + 2]) == 1 and \
             len(self.model.grid[w][h - 2]) == 1:
            self.migrant_to_check.go_to(w, h, False)
            self.migrant_to_check = None
