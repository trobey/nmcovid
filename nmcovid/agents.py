import numpy as np
import math

from mesa import Agent

class Person(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)

    def move(self, start, mobility):
        while (1):
            angle = 360.0 * self.random.random()
            dist = mobility * self.random.random()
            x = math.sin(angle) * dist + start[0]
            y = math.cos(angle) * dist + start[1]
            if (y > 10.0 and y < self.model.space.y_max - 10.0 and x > 10.0 and x < self.model.space.x_max - 10.0):
                coordinate = x, y
                pixel = self.model.image.getpixel(coordinate)
                if (pixel != (255, 255, 255)):
                    return np.array((x, y))

class Susceptible(Person):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.name = "Susceptible"
        self.color = "Black"
        self.home = np.array(pos)
        self.work = self.move(self.home, 25.0)
        # 10% travel for work.
        self.travel = False
        if (100.0 * self.random.random() < 10.0):
            self.travel = True
        else:
            self.travel = False

    def step(self):
        if self.model.state == "community" or (self.model.state == "work" and self.travel):
            new_pos = self.move(self.home, 30.0)
        elif self.model.state == "work":
            new_pos = self.move(self.work, self.model.mobility)
        else:
            new_pos = self.move(self.home, self.model.mobility)
        self.model.space.move_agent(self, new_pos)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Infected(Person):
    def __init__(self, unique_id, model, pos, asymptomatic):
        super().__init__(unique_id, model, pos)
        self.name = "Infected"
        self.color = "Red"
        self.asymptomatic = asymptomatic
        if self.asymptomatic:
            self.energy = 42
        else:
            self.energy = 15
        self.home = np.array(pos)
        self.work = self.move(self.home, 25.0)
        # 10% travel for work.
        if (100.0 * self.random.random() < 10.0):
            self.travel = True
        else:
            self.travel = False

    def step(self):
        '''
        Get the Infected person's neighbors, compute the new vector, and move accordingly.
        '''
        if self.model.state == "community" or (self.model.state == "work" and self.travel):
            new_pos = self.move(self.home, 30.0)
        elif self.model.state == "work":
            new_pos = self.move(self.work, self.model.mobility)
        else:
            new_pos = self.move(self.home, self.model.mobility)

        self.model.space.move_agent(self, new_pos)

        self.energy -= 1
        if self.energy == 0:
          person = Recovered(self.model.next_id(), self.model, self.pos)
          person.set_imperial(self.home, self.work, self.travel)
          self.model.space.remove_agent(self)
          self.model.schedule.remove(self)
          self.model.space.place_agent(person, person.pos)
          self.model.schedule.add(person)

    def set_imperial(self, home, work, travel):
          self.home = np.array(home)
          self.work = np.array(work)
          self.travel = travel

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Recovered(Person):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.name = "Recovered"
        self.color = "Green"

    def step(self):
        '''
        Get the Infected person's neighbors, compute the new vector, and move accordingly.
        '''
        if self.model.state == "community":
            new_pos = self.move(self.home, 30.0)
        elif self.model.state == "work":
            new_pos = self.move(self.work, self.model.mobility)
        else:
            new_pos = self.move(self.home, self.model.mobility)
            
        self.model.space.move_agent(self, new_pos)

    def set_imperial(self, home, work, travel):
          self.home = np.array(home)
          self.work = np.array(work)
          self.travel = travel

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
