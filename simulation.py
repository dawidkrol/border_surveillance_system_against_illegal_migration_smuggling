from json import load

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from Agents.BarbedWire import BarbedWire
from Agents.BorderLine import BorderLine
from Agents.GuardPatrol import GuardPatrol
from Agents.IllegalImmigrant import IllegalImmigrant
from Agents.Camera import Camera
from Models.BorderModel import BorderModel

params = load(open("params.json", 'r'))


def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}

    if isinstance(agent, GuardPatrol):
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, IllegalImmigrant):
        portrayal["Color"] = "red"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, Camera):
        portrayal["Color"] = "cyan"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, BarbedWire):
        portrayal["Color"] = "yellow"
        portrayal["w"] = 10000
        portrayal["h"] = 1
        portrayal["Layer"] = 1
    elif isinstance(agent, BorderLine):
        portrayal["Color"] = "red"
        portrayal["w"] = 10000
        portrayal["h"] = 5
        portrayal["Layer"] = 1

    return portrayal

chart = ChartModule([
    {"Label": "Not_captured_Illegal_Immigrants", "Color": "red"},
    {"Label": "Captured_Illegal_Immigrants", "Color": "Green"}], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)


server = ModularServer(BorderModel,
                       [grid, chart],
                       "Border Model",
                       {"width": params["width"], "height": params["height"], "n_patrols": params["n_patrols"], "n_cameras": params["n_cameras"],
                        "n_ii_per_second": params["mean_illegal_imigrants_respawn_per_second"], "params": params})

server.port = 8521
server.launch()

