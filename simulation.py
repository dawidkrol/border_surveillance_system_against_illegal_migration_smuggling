from json import load

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine
from Agents.GuardPatrol import GuardPatrol
from Agents.IllegalImmigrant import IllegalImmigrant
from Agents.Camera import Camera
from Agents.Radar import Radar
from Models.BorderModel import BorderModel

params = load(open("params.json", 'r'))


def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}

    if isinstance(agent, GuardPatrol):
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, IllegalImmigrant):
        if not agent.is_arrested:
            portrayal["Color"] = "red"
            portrayal["w"] = 1
            portrayal["h"] = 1
        else:
            portrayal["Color"] = "black"
            portrayal["w"] = 1
            portrayal["h"] = 1
    elif isinstance(agent, Camera):
        portrayal["Color"] = "cyan"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, Radar):
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, BorderLine):
        portrayal["Color"] = "yellow"
        portrayal["w"] = 10000
        portrayal["h"] = 1
        portrayal["Layer"] = 1
    elif isinstance(agent, BorderFence):
        if agent.is_destroyed is False:
            portrayal["Color"] = "black"
            portrayal["w"] = 1
            portrayal["h"] = 2
            portrayal["Layer"] = 1
        else:
            portrayal["Color"] = "white"
            portrayal["w"] = 1
            portrayal["h"] = 2
            portrayal["Layer"] = 1

    return portrayal

chart = ChartModule([
    {"Label": "Not_captured_Illegal_Immigrants", "Color": "red"},
    {"Label": "Captured_Illegal_Immigrants", "Color": "Green"}], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, params["width"], params["height"], params["width"] * 3, params["height"] * 3)


server = ModularServer(BorderModel,
                       [grid, chart],
                       "Border Model",
                       {"width": params["width"], "height": params["height"], "n_patrols": params["n_patrols"], "n_migrants": params["n_migrants"],
                        "n_cameras": params["n_cameras"], "n_radars": params["n_radars"], "params": params})

server.port = 8521
server.launch()

