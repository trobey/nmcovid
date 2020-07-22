from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement

from .model import Covid
from .SimpleContinuousModule import SimpleCanvas

def virus_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": agent.color}

virus_canvas = SimpleCanvas(virus_draw, 1000, 1000)

#model_params = {
#    "population": 100,
#    "width": 787,
#    "height": 865,
#    "mobility": 6,
#    "social_distance": 2,
#    "asymptomatic_percentage": 40.0,
#}
model_params = {
                "width": 787,
                "height": 865,
                "population": UserSettableParameter('slider', 'Population', 1000, 0, 2000),
                "asymptomatic_percentage": UserSettableParameter('slider', 'Asymptomatic (%)', 40, 0, 100),
                "social_distance": UserSettableParameter('slider', 'Social Distance ', 4.0, 0.0, 6.0, 0.1),
                "mobility": UserSettableParameter('slider', 'Mobility', 6.0, 0.0, 10.0, 0.1)}

class CovidTextElement(TextElement):
    def render(self, model):
        infected = round(100 * model.count("Infected") / model.population, 1)
        susceptible = round(100 * model.count("Susceptible") / model.population ,1)
        return "location: " + model.state + " (infected " + str(infected) + "% susceptible " + str(susceptible) + "%)"

text_element = CovidTextElement()

chart_element = ChartModule([{"Label": "Susceptible", "Color": "#666666"},
                             {"Label": "Infected", "Color": "#AA0000"},
                             {"Label": "Recovered", "Color": "#00AA00"}])


server = ModularServer(Covid, [virus_canvas, text_element, chart_element], "Covid-19 Model", model_params)
