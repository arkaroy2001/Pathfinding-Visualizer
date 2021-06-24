import main
import colors
import pygame
import math

class GridSquare:
    def __init__(self, row, col, width, PAD):
        self.x = col
        self.y = row
        self.PAD = PAD
        self.color = colors.WHITE
        self.neighbors = []
        self.width = width
        self.state = "free"

    border = False
    distance = math.inf
    done = False
    weight = 1
    is_visited = False
    back_trace = False



    def clicked(self, target_state):
        if target_state == self.state:
            if not self.border:
                self.turn_to_free()
            return

        elif target_state == "wall":
            self.turn_to_wall()
            return

        elif target_state == "start_pos":
            if (not self.border):
                self.turn_to_start_pos()
            return

        elif target_state == "end_pos":
            if (not self.border):
                self.turn_to_end_pos()
            return

    def turn_to_start_pos(self):
        self.state = "start_pos"
        #print("YOU")
        self.distance = 0
        self.color = colors.BLUE

    def turn_to_end_pos(self):
        self.state = "end_pos"
        self.color = colors.RED

    def turn_to_wall(self):
        self.state = "wall"
        self.color = colors.DARK_GRAY

    def turn_to_free(self):
        self.state = "free"
        self.distance = math.inf
        self.color = colors.WHITE

    def print_values(self):
        print("Node Coords: ", self.x, self.y)

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.color,
            (((self.width + self.PAD) * self.x + self.PAD),((self.width+self.PAD) * self.y+self.PAD),self.width,self.width))

    def animate(self, SCREEN):
        if self.is_visited==True:
            self.color = colors.PURPLE
        if self.back_trace == True:
            self.color = colors.LIME_GREEN
        self.draw(SCREEN)
        #print("THERE")

