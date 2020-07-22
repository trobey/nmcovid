'''
Covid-19
=============================================================
A Mesa implementation of a coronavirus SIR model on a continuous space.
'''

import numpy as np
import math
import csv
import random

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from PIL import Image

from .agents import Susceptible, Infected, Recovered


class Covid(Model):
    '''
    Covid model class. Handles agent creation, placement and scheduling.
    '''

    def __init__(self,
                 population=100,
                 width=100,
                 height=100,
                 mobility=6,
                 social_distance=2,
                 asymptomatic_percentage=50.0):
        '''
        Create a new Covid model.

        Args:
            population: Number of people (density) with one asymptomatic infected person.
            asymptomatic_percentage: Percentage of infected people that are asymptomatic.  Asymptomatic people transmit the virus for 42 time steps versus 15 time steps for those that are symptomatic.
            social_distance: Distance at which neighboring susceptible agents can b ecome infected.
            mobility: The maximum distance that an agent can travel.
        '''

        self.current_id = 0;
        self.population = population
        self.mobility = mobility
        self.social_distance = social_distance
        self.asymptomatic_percentage = asymptomatic_percentage
        self.state = "home"
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, False)
        self.image = Image.open(r"nmcounties.jpg")
        self.num = {
            'San Juan': 0,
            'Rio Arriba': 0,
            'Taos': 0,
            'Colfax': 0,
            'Union': 0,
            'Los Alamos': 0,
            'Mora': 0,
            'Harding': 0,
            'McKinley': 0,
            'Sandoval': 0,
            'Santa Fe': 0,
            'San Miguel': 0,
            'Quay': 0,
            'Cibola': 0,
            'Valencia': 0,
            'Bernalillo': 0,
            'Torrance': 0,
            'Guadalupe': 0,
            'Curry': 0,
            'Catron': 0,
            'Socorro': 0,
            'Lincoln': 0,
            'De Baca': 0,
            'Roosevelt': 0,
            'Sierra': 0,
            'Chaves': 0,
            'Hidalgo': 0,
            'Grant': 0,
            'Luna': 0,
            'Doña Ana': 0,
            'Otero': 0,
            'Eddy': 0,
            'Lea': 0,
        }
        self.pop = {
            'San Juan': 0,
            'Rio Arriba': 0,
            'Taos': 0,
            'Colfax': 0,
            'Union': 0,
            'Los Alamos': 0,
            'Mora': 0,
            'Harding': 0,
            'McKinley': 0,
            'Sandoval': 0,
            'Santa Fe': 0,
            'San Miguel': 0,
            'Quay': 0,
            'Cibola': 0,
            'Valencia': 0,
            'Bernalillo': 0,
            'Torrance': 0,
            'Guadalupe': 0,
            'Curry': 0,
            'Catron': 0,
            'Socorro': 0,
            'Lincoln': 0,
            'De Baca': 0,
            'Roosevelt': 0,
            'Sierra': 0,
            'Chaves': 0,
            'Hidalgo': 0,
            'Grant': 0,
            'Luna': 0,
            'Doña Ana': 0,
            'Otero': 0,
            'Eddy': 0,
            'Lea': 0,
        }
        with open('counties.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                county = row[2].replace(' County', '')
                if (county != '' and county != 'County'):
                    population = row[3].replace(',', '')
                    self.pop[county] = population
        total = 0
        for value in self.pop.values():
            total += int(value)
        for county, value in self.pop.items():
            self.pop[county] = round(int(self.population) * int(value) / int(total))
        total = 0
        for value in self.pop.values():
            total += int(value)
        if (self.population != total):
            self.pop['Bernalillo'] += self.population - total

        self.make_agents()
        self.running = True

        self.datacollector = DataCollector(
            {"Susceptible": lambda m: self.count("Susceptible"),
             "Infected": lambda m: self.count("Infected"),
             "Recovered": lambda m: self.count("Recovered")})

    def counties(self, pixel):
        if (pixel == (87, 127, 77)):
            return 'San Juan'
        elif (pixel == (168, 144, 178)):
            return 'Rio Arriba'
        elif (pixel == (131, 141, 91)):
            return 'Taos'
        elif (pixel == (189, 204, 119)):
            return 'Colfax'
        elif (pixel == (197, 112, 58)):
            return 'Union'
        elif (pixel == (211, 165, 80)):
            return 'Los Alamos'
        elif (pixel == (186, 81, 52)):
            return 'Mora'
        elif (pixel == (106, 97, 126)):
            return 'Harding'
        elif (pixel == (91, 124, 143)):
            return 'McKinley'
        elif (pixel == (92, 59, 40)):
            return 'Sandoval'
        elif (pixel == (75, 113, 116)):
            return 'Santa Fe'
        elif (pixel == (109, 103, 53)):
            return 'San Miguel'
        elif (pixel == (49, 73, 73)):
            return 'Quay'
        elif (pixel == (178, 62, 49)):
            return 'Cibola'
        elif (pixel == (138, 99, 84)):
            return 'Valencia'
        elif (pixel == (137, 184, 214)):
            return 'Bernalillo'
        elif (pixel == (106, 106, 104)):
            return 'Torrance'
        elif (pixel == (146, 117, 87)):
            return 'Guadalupe'
        elif (pixel == (156, 150, 88)):
            return 'Curry'
        elif (pixel == (67, 94, 149)):
            return 'Catron'
        elif (pixel == (55, 80, 50)):
            return 'Socorro'
        elif (pixel == (145, 186, 178)):
            return 'Lincoln'
        elif (pixel == (82, 33, 37)):
            return 'De Baca'
        elif (pixel == (195, 189, 189)):
            return 'Roosevelt'
        elif (pixel == (238, 219, 99)):
            return 'Sierra'
        elif (pixel == (243, 234, 129)):
            return 'Chaves'
        elif (pixel == (41, 30, 60)):
            return 'Hidalgo'
        elif (pixel == (116, 140, 106)):
            return 'Grant'
        elif (pixel == (11, 10, 8)):
            return 'Luna'
        elif (pixel == (157, 56, 74)):
            return 'Doña Ana'
        elif (pixel == (52, 53, 48)):
            return 'Otero'
        elif (pixel == (207, 144, 135)):
            return 'Eddy'
        elif (pixel == (138, 171, 80)):
            return 'Lea'
        else:
            return ''

    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''

        for i in range(self.population):
            pos = self.inside()
            person = Susceptible(self.next_id(), self, pos)
            self.space.place_agent(person, pos)
            self.schedule.add(person)
        agent_key = random.randint(0, self.population - 1)
        agent = self.schedule._agents[agent_key]
        asymptomatic = True
        person = Infected(self.next_id(), self, agent.pos, True)
        person.set_imperial(agent.home, agent.work, agent.travel)
        self.space.remove_agent(agent)
        self.schedule.remove(agent)
        self.space.place_agent(person, person.pos)
        self.schedule.add(person)

    def inside(self):
        while (1):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            if (y > 10.0 and y < self.space.y_max - 10.0 and x > 10.0 and x < self.space.x_max - 10.0):
                coordinate = x, y
                pixel = self.image.getpixel(coordinate)
                if (pixel != (255, 255, 255)):
                    county = self.counties(pixel)
                    if (county != ''):
                        if (self.num[county] < self.pop[county]):
                          self.num[county] += 1
                          return np.array((x, y))

    def step(self):
        self.infect()

        if self.state == "home":
            self.state = "work"
        elif self.state == "work":
            self.state = "community"
        elif self.state == "community":
            self.state = "home"

        self.schedule.step()

        # collect data
        self.datacollector.collect(self)
        if self.count("Infected") == 0:
          self.running = False

    def infect(self):
        agent_keys = list(self.schedule._agents.keys())
        susceptible = [];
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == "Susceptible":
                susceptible.append(agent_key)
        for agent_key in susceptible:
            agent = self.schedule._agents[agent_key]
            neighbors = self.space.get_neighbors(agent.pos, self.social_distance)
            for neighbor in neighbors:
                if neighbor.name == "Infected":
                    asymptomatic = False
                    if (100.0 * self.random.random() < self.asymptomatic_percentage):
                        asymptomatic = True
                    person = Infected(self.next_id(), self, agent.pos, asymptomatic)
                    person.set_imperial(agent.home, agent.work, agent.travel)
                    self.space.remove_agent(agent)
                    self.schedule.remove(agent)
                    self.space.place_agent(person, person.pos)
                    self.schedule.add(person)
                    break

    def count(self, type):
        agent_keys = list(self.schedule._agents.keys())
        num = 0
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == type:
                num += 1
        return num

