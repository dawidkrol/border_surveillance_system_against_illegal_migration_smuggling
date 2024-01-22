from json import load

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from PIL import Image, ImageDraw, ImageTk

from Agents.Road import Road
from Models.LegalBorderModel import LegalBorderModel
from Agents.BorderFence import BorderFence
from Agents.BorderLine import BorderLine
from Agents.Migrant import Migrant
from Agents.Guard import Guard
from Agents.SuperCheckPlace import SuperCheckPlace
from Agents.GuardSuperCheck import GuardSuperCheck

params = load(open("params.json", 'r'))


def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 1, "h": 1}

    if isinstance(agent, Road):
        portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 1, "h": 1, "Color": "#6e6d6d"}

    if isinstance(agent, SuperCheckPlace):
        portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 1, "h": 1, "Color": "#363636"}

    elif isinstance(agent, BorderLine):
        portrayal["Color"] = "yellow"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 1

    elif isinstance(agent, BorderFence):
        portrayal["Color"] = "#5c2727"
        portrayal["h"] = 2
        portrayal["Layer"] = 1

    elif isinstance(agent, Migrant):
        portrayal["h"] = 1
        portrayal["w"] = 1
        portrayal["Layer"] = 3
        portrayal["Shape"] = "rect"

        if agent.is_illegal is True:
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "#02f5a4"

    elif isinstance(agent, Guard):
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 1

    elif isinstance(agent, GuardSuperCheck):
        portrayal["Color"] = "#02a4f5"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 1

    return portrayal


chart = ChartModule([
    {"Label": "Not_captured_Illegal_Immigrants", "Color": "red"},
    {"Label": "Captured_Illegal_Immigrants", "Color": "Green"}], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, params["width"], params["height"], params["width"] * 5, params["height"] * 5)

server = ModularServer(LegalBorderModel,
                       [grid, chart],
                       "Border Model",
                       {"width": params["width"], "height": params["height"], "params": params})

legend_data = {
    'red': 'illegal  migrant',
    '#02f5a4': 'legal migrant',
    'blue': 'guard',
    '#02a4f5': 'special guard',
    '#6e6d6d': 'road',
    '#363636': 'super check place',
    'yellow': 'border line',
    '#5c2727': 'border fence',
}


def generate_legend_image():
    image_width = 200
    image_height = 260

    legend_image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(legend_image)

    x_position = 10
    y_position = 10

    for color, value in legend_data.items():
        draw.rectangle([x_position, y_position, x_position + 20, y_position + 20], fill=color)
        draw.text((x_position + 30, y_position + 10), value, fill="black")
        y_position += 30

    legend_image
    legend_image.show()


generate_legend_image()

server.port = 5000
server.launch()
