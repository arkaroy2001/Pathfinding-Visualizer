from tkinter import font

import pygame
from pygame.locals import *
import math
import tkinter as tk
from tkinter import *
import os
import sys
import button
import colors
import grid_square
import grid_utils
# root = tk.Tk()
# # root.mainloop()
import dijkstra

WIN_WIDTH = 800
WIN_HEIGHT = 700

WIDTH = int(WIN_WIDTH*0.7)
HEIGHT = int(WIN_HEIGHT*0.8)
PAD = 1
FPS = 60

width = 40

#define colors



#define global variable
current_mode = "wall"


def current_walls():
    global current_mode
    current_mode = "wall"

def current_start_pos():
    global current_mode
    current_mode = "start_pos"

def current_end_pos():
    global current_mode
    current_mode = "end_pos"


def main():
    # print("You entered: ", sys.argv[1], sys.argv[2], sys.argv[3])
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(colors.BLACK)
    pygame.display.set_caption("PathFinding Visualizer")
    grid = grid_utils.load_grid(14, 14, width, 1)

    # button = pygame.Rect(5,HEIGHT+10,100,50)
    while True:

        wall_button,start_button,end_button,pathfind_button,clear_button = drawButtons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = event.pos
                mouse_pos = pygame.mouse.get_pos()

                if wall_button.button_rect.collidepoint(mouse_pos):
                    #print("Wall Button was pressed")
                    current_walls()
                elif start_button.button_rect.collidepoint(mouse_pos):
                    #print("Start Button was pressed")
                    current_start_pos()
                elif end_button.button_rect.collidepoint(mouse_pos):
                    #print("End Button was pressed")
                    current_end_pos()
                elif clear_button.button_rect.collidepoint(mouse_pos):
                    #print("Clear Button was pressed")
                    grid = grid_utils.clear_grid(grid,14,14)
                elif pathfind_button.button_rect.collidepoint(mouse_pos):
                    #print("Pathfind Button was pressed")
                    grid = grid_utils.clean_grid(grid, 14, 14)
                    graph = dijkstra.Graph(grid)
                    graph.start_search(grid, SCREEN)
                else:
                    column = mouse_pos[0] // (width + PAD)
                    row = mouse_pos[1] // (width + PAD)
                    try:
                        if current_mode == "start_pos":
                            for i in grid:
                                for j in i:
                                    #print("OK")
                                    if j.state == "start_pos":
                                        j.turn_to_free()
                            #print("HERE")
                            # grid[column][row].clicked(current_mode)

                        elif current_mode == "end_pos":
                            for i in grid:
                                for j in i:
                                    if j.state == "end_pos":
                                        j.turn_to_free()
                            # grid[column][row].clicked(current_mode)

                        grid[column][row].clicked(current_mode)
                        #grid[column][row].print_values()
                    except:
                        pass

            elif pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                column = position[0] // (width + PAD)
                row = position[1] // (width + PAD)

                if current_mode == "end_pos":
                    pass
                elif current_mode == "start_pos":
                    pass


                else:
                    try:
                        if grid[column][row].state == current_mode:
                            pass
                        else:
                            grid[column][row].clicked(current_mode)

                    except:
                        pass


        # pygame.draw.rect(SCREEN,[255,0,0], button)


        #update all the squares
        update_squares(SCREEN, grid)

def update_squares(SCREEN, grid):
    for row in grid:
        for square in row:
            square.draw(SCREEN)

    pygame.display.update()

def drawButtons():
    wall_button = button.Button(SCREEN, colors.GRAY, 5, HEIGHT + 15, 150, 50, "Wall")
    wall_button.draw()
    start_button = button.Button(SCREEN, colors.BLUE, 5 + 155, HEIGHT + 15, 150, 50, "Start Position")
    start_button.draw()
    end_button = button.Button(SCREEN, colors.RED, 5 + (2 * 155), HEIGHT + 15, 150, 50, "End Position")
    end_button.draw()
    pathfind_button = button.Button(SCREEN, colors.LIME_GREEN, 5 + (3 * 155), HEIGHT + 15, 150, 50, "Path Find")
    pathfind_button.draw()
    clear_button = button.Button(SCREEN, colors.ORANGE, 5 + (4 * 155), HEIGHT + 15, 150, 50, "Clear Grid")
    clear_button.draw()

    return wall_button,start_button,end_button,pathfind_button,clear_button





if __name__ == "__main__":
    main()







