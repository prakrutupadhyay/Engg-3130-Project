import mesa

from wolf_sheep.agents import Wolf, Sheep, GrassPatch, Cheetah
from wolf_sheep.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal["Shape"] = "wolf_sheep/resources/sheep.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["Animal"] = "Sheep"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Wolf:
        portrayal["Shape"] = "wolf_sheep/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["Animal"] = "Wolf"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Cheetah:
        portrayal["Shape"] = "wolf_sheep/resources/cheetah.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["Animal"] = "Cheetah"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": mesa.visualization.Slider(
        "Initial Sheep Population", 100, 10, 300
    ),
    "sheep_reproduce": mesa.visualization.Slider(
        "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 50, 10, 300),
    "wolf_reproduce": mesa.visualization.Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": mesa.visualization.Slider(
        "Wolf Gain From Food Rate", 20, 1, 50
    ),

    "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
    "sheep_clustering": mesa.visualization.Slider("Sheep Clustering Radius", 2, 1, 10),
    "near_sheep": mesa.visualization.Slider("Wolf vision radius", 1, 1, 10),
    "near_sheep2": mesa.visualization.Slider("Cheetah vision radius", 1, 1, 10),
    "height": mesa.visualization.Slider("Grid height", 60, 5, 60),
    "width": mesa.visualization.Slider("Grid width", 60, 5, 60),
}
canvas_element = mesa.visualization.CanvasGrid(
    wolf_sheep_portrayal, model_params["width"].value, model_params["height"].value, model_params["height"].value*15, model_params["width"].value*15)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Sheep", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00AA00"},
        {"Label": "Cheetah", "Color": "#AA0000"},
    ]
)
server = mesa.visualization.ModularServer(
    WolfSheep, [canvas_element,
                chart_element], "Wolf Sheep Predation", model_params
)
server.port = 8521
