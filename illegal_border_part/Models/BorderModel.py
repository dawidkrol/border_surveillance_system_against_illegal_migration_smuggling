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
    def __init__(self, width, height, n_patrols, cameras, radars, n_migrants, params):
        self.width = width
        self.height = height
        self.params = params
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.agent_count = n_patrols
        self.not_captured_ii_count = 0
        self.captured_ii_count = 0
        self.illegal_migrant_last_id = 0
        self.guard_last_id = 0
        self.is_alarm_state = False
        self.step_count = 0
        self.my_generate_step_definition = params['steps_by_my_generate_step_definition']
        self.number_of_patrols = 0
        self.number_of_migrants = 0
        self.steps_by_my_migrant_step_definition = params['steps_by_my_migrant_step_definition']

        self.datacollector = DataCollector(
            agent_reporters={"Position": "pos"},
            model_reporters={"Not_captured_Illegal_Immigrants": "not_captured_ii_count",
                             "Captured_Illegal_Immigrants": "captured_ii_count"})

        self.schedule = RandomActivation(self)

        # Generating patrols
        if n_patrols > 0:
            patrol_distance = (self.width - 2) // n_patrols
        else:
            patrol_distance = 1

        for i in range(n_patrols):
            self.guard_last_id = i
            self.number_of_patrols += 1
            agent = GuardPatrol(self.guard_last_id, self, width - (patrol_distance * (1 + i)), height - 12,
                                params['max_patrol_speed'], params['patrol_distance_view'],
                                params['how_many_suspects_it_can_capture_at_the_same_time_per_my_capture_step'],
                                params['steps_by_my_capture_step_definition'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating cameras
        for i in cameras:
            agent = Camera(i, self, i['x'], i['y'],
                           i['distance_view'],
                           params['percentage_of_chance_to_escape_after_being_noticed_by_the_camera'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating cameras
        for i in radars:
            agent = Radar(i, self, i['x'], i['y'],
                          i['distance_view'],
                          params['percentage_of_chance_to_escape_after_being_noticed_by_radar'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating migrants
        for i in range(n_migrants):
            self.ill_agent_last_id = i
            self.number_of_migrants += 1
            agent = IllegalImmigrant(self.ill_agent_last_id, self, random.randint(0, width - 1), 1,
                                     params['max_y_illegal_imigrant_speed'],
                                     params['illegal_imigrants_tool_efficency'],
                                     params[
                                         'percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed'])
            self.grid.place_agent(agent, (agent.x, agent.y))
            self.schedule.add(agent)

        # Generating border line
        for i in range(self.width):
            self.border_line = BorderLine(i, self)
            self.schedule.add(self.border_line)
            self.grid.place_agent(self.border_line, (i, height - 3))

        if params['is_fence']:
            # Generating border fence
            for i in range(self.width):
                self.border_fence = BorderFence(i, self, params['fence_resilience'])
                self.schedule.add(self.border_fence)
                self.grid.place_agent(self.border_fence, (i, height - 15))

    def step(self):
        self.step_count += 1
        if self.step_count % self.my_generate_step_definition == 0:
            if self.is_alarm_state:
                for i in range(self.params['new_patrols_per_my_step_definition_after_alarm_state']):
                    self.add_guard()
        if self.captured_ii_count >= self.params['alarm_state_after_seeing_more_than_agents']:
            self.is_alarm_state = True
            print("!!!!!!!!!! ALARM !!!!!!!!!!!!!")
        if self.step_count % self.steps_by_my_migrant_step_definition == 0:
            for i in range(self.params['new_migrants_per_step']):
                self.add_illegal_migrant()
        self.datacollector.collect(self)
        self.schedule.step()

    def add_illegal_migrant(self):
        self.illegal_migrant_last_id += 1
        self.number_of_migrants += 1
        if self.number_of_migrants > self.params['max_migrants_count']:
            print("Stop generating migrants")
            return
        agent = IllegalImmigrant(self.illegal_migrant_last_id, self, random.randint(0, self.width - 1), 1,
                                 self.params['max_y_illegal_imigrant_speed'],
                                 self.params['illegal_imigrants_tool_efficency'],
                                 self.params[
                                     'percent_of_chance_to_choose_to_destroy_the_obstacle_if_there_is_already_a_destroyed'])
        self.grid.place_agent(agent, (agent.x, agent.y))
        self.schedule.add(agent)

    def add_guard(self):
        self.guard_last_id += 1
        self.number_of_patrols += 1
        if self.number_of_patrols > self.params['max_patrol_count']:
            print("!!!!! This is max number of patrols !!!!!")
            return
        agent = GuardPatrol(self.guard_last_id, self, 0, self.height - 12,
                            self.params['max_patrol_speed'], self.params['patrol_distance_view'],
                            self.params['how_many_suspects_it_can_capture_at_the_same_time_per_my_capture_step'],
                            self.params['steps_by_my_capture_step_definition'])
        self.grid.place_agent(agent, (agent.x, agent.y))
        self.schedule.add(agent)
