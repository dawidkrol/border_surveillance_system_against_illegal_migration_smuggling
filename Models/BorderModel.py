import random
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine
from Agents.Camera import Camera
from Agents.GuardPatrol import GuardPatrol
from Agents.IllegalImmigrant import IllegalImmigrant
from mesa import Model

from Agents.Radar import Radar


class BorderModel(Model):
    def __init__(self, width, height, n_patrols, n_cameras, n_radars, n_migrants, params):
        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.agent_count = n_patrols
        self.not_captured_ii_count = 0
        self.captured_ii_count = 0

        self.datacollector = DataCollector(
            agent_reporters={"Position": "pos"},
            model_reporters={"Not_captured_Illegal_Immigrants": "not_captured_ii_count", "Captured_Illegal_Immigrants": "captured_ii_count"})


        self.schedule = RandomActivation(self)

        # Generating patrols
        for i in range(n_patrols):
            agent = GuardPatrol(i, self, width - (30 * (1+i)), height - 10, params['max_patrol_speed'], params['patrol_distance_view'], params['how_many_suspects_it_can_capture_at_the_same_time'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating cameras
        for i in range(n_cameras):
            agent = Camera(i, self, random.randint(0, width - 1), random.randint(height - 20, height - 1),
                           params['camera_distance_view'], params['percentage_of_chance_to_escape_after_being_noticed_by_the_camera'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating cameras
        for i in range(n_radars):
            agent = Radar(i, self, random.randint(0, width - 1), random.randint(height - 20, height - 1),
                          params['radar_distance_view'], params['percentage_of_chance_to_escape_after_being_noticed_by_the_camera'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating migrants
        for i in range(n_migrants):
            agent = IllegalImmigrant(i, self, random.randint(0, width - 1), 1, params['max_y_illegal_imigrant_speed'],
                                     params['illegal_imigrants_tool_efficency'],
                                     params['percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating border line
        self.border_line = BorderLine(0, self)
        self.schedule.add(self.border_line)
        self.grid.place_agent(self.border_line, (width - 1, height - 3))

        # Generating border fence
        for i in range(self.width):
            self.border_fence = BorderFence(i, self, 40)
            self.schedule.add(self.border_fence)
            self.grid.place_agent(self.border_fence, (i, height - 15))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
