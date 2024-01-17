from mesa import Agent
import numpy as np

from Agents.Migrant import Migrant


class Guard(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.migrant_to_check = None
        self.suspiciousness = 0.5
        self.accuracy = 1

    def step(self):
        neighbors_2 = self.model.grid.get_neighbors(self.pos, True, radius=2)

        agents = [agent for agent in neighbors_2 if isinstance(agent, Migrant)]
        if len(agents) > 0:
            if self.migrant_to_check is None:
                agents.sort(key=lambda x: x.pos[1], reverse=True)
                self.migrant_to_check = agents[0]
                self.migrant_to_check.stopped = True
                return

            if not self.check_documents():
                self.arest_migrant()
                return

            # if bardzo podejrzany
            if self.check_suspicion():
                self.go_to_super_check()
                return

            self.migrant_to_check.stopped = False
            self.migrant_to_check = None

    def check_documents(self) -> bool:
        print(self.migrant_to_check.legal_documents, self.accuracy, np.abs(self.migrant_to_check.legal_documents - 1) * self.accuracy)
        return np.abs(self.migrant_to_check.legal_documents - 1) * self.accuracy <= 0.5

    def check_suspicion(self) -> bool:
        return self.suspiciousness * self.migrant_to_check.suspicion >= 0.3

    def go_to_super_check(self):
        w = self.model.width // 2 + 7
        h = self.model.height - 68
        if len(self.model.grid[w][h]) == 1:
            self.migrant_to_check.go_to(w, h, False)
            self.migrant_to_check = None

    def arest_migrant(self):
        if self.migrant_to_check.is_illegal:
            self.model.captured_illegal_count += 1
        else:
            self.model.captured_legal_count += 1

        self.migrant_to_check.is_arrested = True
        self.migrant_to_check = None
