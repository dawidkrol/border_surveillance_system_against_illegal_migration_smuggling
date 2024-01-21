import os
import random
import numpy as np
from tabulate import tabulate

from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa import Model

from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine
from Agents.Road import Road
from Agents.Migrant import Migrant
from Agents.Guard import Guard
from Agents.SuperCheckPlace import SuperCheckPlace
from Agents.GuardSuperCheck import GuardSuperCheck


class LegalBorderModel(Model):
    def __init__(self, width, height, params):
        self.width = width
        self.height = height
        self.params = params
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.not_captured_illegal_count = 0
        self.not_captured_legal_count = 0
        self.captured_legal_count = 0
        self.captured_illegal_count = 0
        self.illegal_migrant_last_id = 0

        self.step_count = 0
        self.steps_by_my_migrant_step_definition = params['steps_by_my_migrant_step_definition']
        self.number_of_migrants = 0

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

        i = 0
        for h in range(20):
            for w in range(w_start + 5, w_start + 10):
                self.road = SuperCheckPlace(i, self)
                self.schedule.add(self.road)
                self.grid.place_agent(self.road, (w, height - 50 - h))
                i += 1

        i = 0
        self.guard = Guard(i, self, params)
        self.schedule.add(self.guard)
        self.grid.place_agent(self.guard, (width // 2, height - 55))

        self.guard = GuardSuperCheck(i, self, params)
        self.schedule.add(self.guard)
        self.grid.place_agent(self.guard, ((width // 2) + 9, height - 55))


        # Generating legal/illegal migrants
        h = 0
        for i in range(params['n_migrants_start']):
            h += 3
            self.illegal_migrant_last_id += 1
            agent = Migrant(self.illegal_migrant_last_id, self, w_start + 2, h, random.choice([True, False]), random.random(), random.random(),
                            random.random())
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

            self.number_of_migrants += 1

            is_illegal = agent.is_illegal
            suspicion = agent.suspicion
            illegal_items = agent.illegal_items
            legal_documents = agent.legal_documents

            print('\n\nMigrant:\nis illegal:', is_illegal, '\nsuspicion:', suspicion, '\nillegal items:', illegal_items,
                  '\nlegal_documents:', legal_documents)


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.display_confusion_matrix()
        if self.step_count % self.steps_by_my_migrant_step_definition == 0:
            for i in range(self.params['new_migrants_per_step']):
                self.add_migrant()
        self.step_count += 1

    def add_migrant(self):
        w_start = self.width // 2
        self.illegal_migrant_last_id += 1
        if self.number_of_migrants > self.params['max_migrants_count']:
            print("Stop generating migrants")
            return
        agent = Migrant(self.illegal_migrant_last_id, self, w_start + 2, 0, random.choice([True, False]), random.random(), random.random(),
                        random.random())
        self.grid.place_agent(agent, (agent.x, agent.y))
        self.schedule.add(agent)
        self.number_of_migrants += 1

    def display_confusion_matrix(self):
        data = np.array([
            [self.not_captured_legal_count, self.not_captured_illegal_count],
            [self.captured_legal_count, self.captured_illegal_count]
        ])
        labels = ['legal migrant', 'illegal migrant']
        col_labels = ['not captured', 'captured']
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Confusion Matrix:")
        print(tabulate(data, headers=labels, showindex=col_labels, tablefmt="fancy_grid"))