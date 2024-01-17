from mesa import Agent


class Migrant(Agent):
    def __init__(self, unique_id, model, x, y, is_illegal, suspicion, illegal_items, legal_documents):
        super().__init__(unique_id, model)
        self.is_illegal = is_illegal
        self.x = x
        self.y = y
        self.suspicion = suspicion
        self.illegal_items = illegal_items
        self.legal_documents = legal_documents

        self.stopped = False
        self.is_arrested = False

        if self.is_illegal:
            self.legal_documents = 1
            self.illegal_items = 0

    def go_to(self, x, y, stopped=True):
        self.model.grid.move_agent(self, (x, y))
        self.x = x
        self.y = y
        self.stopped = stopped

    def step(self):
        if self.is_arrested:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            neighbors_4 = self.model.grid.get_neighbors(self.pos, True, radius=4)
            agent_in_front_of = [agent for agent in neighbors_4 if agent.pos[0] == self.pos[0] and
                                 agent.pos[1] > self.pos[1] and isinstance(agent, Migrant) and
                                 agent.pos[1] < self.pos[1] + 4]

            if self.stopped:
                return

            if len(agent_in_front_of) <= 0:
                self.y += 2
                self.model.grid.move_agent(self, (self.x, self.y))

            if self.y > self.model.height - 10:
                if self.is_illegal:
                    self.model.not_captured_illegal_count += 1
                if not self.is_illegal:
                    self.model.not_captured_legal_count += 1
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
