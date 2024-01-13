import random

from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa import Model

from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine
from Agents.Road import Road

from Agents.Migrant import Migrant


class LegalBorderModel(Model):
    def __init__(self, width, height, params):
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.not_captured_illegal_count = 0
        self.not_captured_legal_count = 0
        self.captured_legal_count = 0
        self.captured_illegal_count = 0

        self.datacollector = DataCollector(
            agent_reporters={"Position": "pos"},
            model_reporters={"Not_captured_Illegal_Immigrants": "not_captured_illegal_count", "Captured_Illegal_Immigrants": "captured_illegal_count"})


        self.schedule = RandomActivation(self)

        # Generating road line
        w_start = self.width // 2
        i = 0
        for h in range(self.height):
            for w in range(w_start, w_start + 5):
                self.road = Road(i, self)
                self.schedule.add(self.road)
                self.grid.place_agent(self.road, (w, h))
                i += 1

        # Generating border line
        for i in range(self.width):
            self.border_line = BorderLine(i, self)
            self.schedule.add(self.border_line)
            self.grid.place_agent(self.border_line, (i, height - 5))

        # Generating border fence
        for i in range(self.width):
            if i not in [j for j in range(w_start, w_start + 4)]:
                self.border_fence = BorderFence(i, self, 40)
                self.schedule.add(self.border_fence)
                self.grid.place_agent(self.border_fence, (i, height - 50))


        # Generating legal/illegal migrants
        h = 0
        for i in range(10):
            h += 3
            agent = Migrant(i, self, w_start + 2, h, random.choice([False, True]))
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
