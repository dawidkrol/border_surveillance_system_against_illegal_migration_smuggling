import random
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from Agents.BarbedWire import BarbedWire
from Agents.Camera import Camera
from Agents.GuardPatrol import GuardPatrol
from Agents.IllegalImmigrant import IllegalImmigrant
from mesa import Model


class BorderModel(Model):
    def __init__(self, width, height, n_patrols, n_cameras, n_ii_per_second, params):
        self.height = height
        self.width = width
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.agent_count = n_patrols
        self.not_captured_ii_count = 0
        self.captured_ii_count = 0

        self.datacollector = DataCollector(
            agent_reporters={"Position": "pos"},
            model_reporters={"Not_captured_Illegal_Immigrants": "not_captured_ii_count", "Captured_Illegal_Immigrants": "captured_ii_count"})


        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(n_patrols):
            agent = GuardPatrol(i, self, width - 1 - (20 * i), height - 5)
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        for i in range(n_cameras):
            agent = Camera(i, self, random.randint(0, width - 1), height - 5)
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        for i in range(30):
            agent = IllegalImmigrant(i, self, random.randint(0, width - 1), 1)
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        self.barbed_wire = BarbedWire(0, self)
        self.schedule.add(self.barbed_wire)
        self.grid.place_agent(self.barbed_wire, (width - 1, height - 3))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()