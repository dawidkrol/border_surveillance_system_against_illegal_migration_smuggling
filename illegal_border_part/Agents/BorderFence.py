from mesa import Agent


class BorderFence(Agent):
    def __init__(self, unique_id, model, resilience):
        super().__init__(unique_id, model)
        self.is_destroyed = False
        self.resilience = resilience

    def step(self):
        pass
        # print(self.destroyed_places)
