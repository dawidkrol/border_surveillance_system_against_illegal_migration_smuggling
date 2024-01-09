import pygame
import random
from json import load
from math import sqrt

params = load(open("params.json", 'r'))
width, height = params["width"], params["height"]


def vector_with_max_len(max_length=params["max_x_y_guard_speed"]):
    x = random.randint(-max_length, max_length)
    max_y = round(sqrt(max_length ** 2 - x ** 2))
    y = random.randint(-max_y, max_y)
    return (x, y)

class Guard_patrol:

    def __init__(self,screen, x, y, range = 5):
        self.rect = pygame.Rect(x, 10, 10, 10)
        self.color = (0, 0, 255)
        # self.range = range
        self.screen = screen
        self.vector = vector_with_max_len()
    def drawing(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def go(self):
        if random.random()<=0.01 or self.rect.x + self.vector[0]>width or self.rect.x + self.vector[0]<0 or self.rect.y + self.vector[1]>height or self.rect.y + self.vector[1]<0:
            self.vector = vector_with_max_len()
        else:
            self.rect.x += self.vector[0]
            # self.rect.y += self.vector[1]
        self.drawing()

class Illegal_imigrant:
    def __init__(self, screen, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = (255, 0, 0)
        self.speed = random.randint(1,params["max_y_illegal_imigrant_speed"])
        self.screen = screen
        self.tool_efficency = random.randint(1, params["illegal_imigrants_tool_max_efficency_per_second"])
        self.barbed_wire_durability_left = params["barbed_wire_durability"]
    def drawing(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    def go(self):
        self.rect.y -= self.speed
        # if self.rect.y<0:
        #     print(self.rect.y)
        #     del self
        #
        #     return
        self.drawing()
    # def __del__(self):
    #     print("xD")

class Camera:
    def __init__(self,screen, x, y, range = 5):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = (0, 255, 255)
        # self.range = range
        self.screen = screen
    def drawing(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Barbed_wire:
    def __init__(self,screen, y = 0):
        self.rect = pygame.Rect(0, 0, 10000, 5)
        self.color = (255, 255, 0)
        self.screen = screen
    def drawing(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Border_line:
    def __init__(self,screen, y = 0):
        self.rect = pygame.Rect(0, 35, 10000, 5)
        self.color = (255, 0, 0)
        self.screen = screen
    def drawing(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Game:
    def __init__(self, screen, n_patrols : int, n_cameras : int, n_ii_per_second:float):
        self.screen = screen
        self.n_ii_per_second = n_ii_per_second
        self.barbed_wire = Barbed_wire(self.screen)
        self.border_line = Border_line(self.screen)
        self.patrols = []
        self.cameras = []
        self.illegal_imigrants = []
        # self.illegal_imigrants_on_barbed_wire = []
        self.counter_finished_imigrants = 0
        self.counter_spawn_illegal_imigrants = 0
        self.patrol_distance = 10
        for i in range (n_patrols):
            self.patrols.append(Guard_patrol(self.screen, width - self.patrol_distance * i, random.random()*height))
        for i in range (n_cameras):
            self.cameras.append(Camera(self.screen, random.random()*width, random.random()*height//10))

    def go(self):
        def is_collision(illegal_imigrant):
            for patrol in self.patrols:
                if sqrt( (illegal_imigrant.rect.x - patrol.rect.x)**2 + (illegal_imigrant.rect.y - patrol.rect.y)**2 ) < params["patrol_range"]:
                    return True
            for camera in self.cameras:
                if sqrt( (illegal_imigrant.rect.x - camera.rect.x)**2 + (illegal_imigrant.rect.y -camera.rect.y)**2 ) < params["camera_range"]:
                    return True
            return False

        def is_finished(illegal_imigrant):
            if illegal_imigrant.rect.y <=0:
                self.counter_finished_imigrants += 1
                return True
            return False

        if random.random()<1/30 * self.n_ii_per_second:
            self.illegal_imigrants.append(Illegal_imigrant(self.screen, random.random()*width, height))
            self.counter_spawn_illegal_imigrants +=1

        self.barbed_wire.drawing()
        self.border_line.drawing()

        for i in self.patrols:
            i.go()
        for i in self.cameras:

            i.drawing()

        self.illegal_imigrants = [ i for i in self.illegal_imigrants if not is_collision(i) and not is_finished(i) ]

        for i in self.illegal_imigrants:
            i.go()