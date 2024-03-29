from json import load

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from PIL import Image, ImageDraw, ImageTk

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
            portrayal = {"Shape": "circle", "Color": "#fa0000", "Filled": "true", "Layer": 0, "r": 1, "w": 1, "h": 1}
        else:
            # portrayal = {"Shape": "rect", "Color": "#915353", "Filled": "false", "Layer": 0, "r": 1, "w": 1, "h": 1}
            portrayal = {"Shape": "rect", "Color": "white", "Filled": "false", "Layer": 0, "r": 1, "w": 1, "h": 1}
    elif isinstance(agent, Camera):
        portrayal["Color"] = "cyan"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, Radar):
        portrayal["Color"] = "#027320"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, BorderLine):
        portrayal["Color"] = "yellow"
        portrayal["w"] = 1
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
                        "cameras": params["cameras"], "radars": params["radars"], "params": params})


legend_data = {
    '#fa0000': 'illegal  migrant',
    'blue': 'guard',
    'cyan': 'camera',
    '#027320': 'radar',
    'yellow': 'border line',
    'black': 'border fence',
}


def generate_legend_image():
    image_width = 200
    image_height = 200

    legend_image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(legend_image)

    x_position = 10
    y_position = 10

    for color, value in legend_data.items():
        draw.rectangle([x_position, y_position, x_position + 20, y_position + 20], fill=color)
        draw.text((x_position + 30, y_position + 10), value, fill="black")
        y_position += 30

    legend_image.show()


generate_legend_image()

server.port = 5001
server.launch()
