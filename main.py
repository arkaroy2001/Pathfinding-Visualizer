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
import Algo


num_rows = 20
num_cols = 20

square_width = 40
PAD = 1

WIN_WIDTH = (num_rows * (square_width+PAD))+250
WIN_HEIGHT = (num_cols * (square_width+PAD))+100

WIDTH = (num_cols * (square_width+PAD))
HEIGHT = (num_cols * (square_width+PAD))

FPS = 60




#define colors

# WIN_WIDTH = 800
# WIN_HEIGHT = 700



#define global variable
current_mode = "wall"
current_algo = "dijkstra"

astar_clicked = False
greedy_clicked = False
dijk_clicked = True

def current_walls():
    global current_mode
    current_mode = "wall"

def current_start_pos():
    global current_mode
    current_mode = "start_pos"

def current_end_pos():
    global current_mode
    current_mode = "end_pos"

def current_dijk():
    global current_algo,dijk_clicked,astar_clicked,greedy_clicked
    current_algo = "dijkstra"
    dijk_clicked = True
    astar_clicked = False
    greedy_clicked = False

def current_astar():
    global current_algo,dijk_clicked,astar_clicked,greedy_clicked
    current_algo = "astar"
    dijk_clicked = False
    astar_clicked = True
    greedy_clicked = False

def current_greedy():
    global current_algo,dijk_clicked,astar_clicked,greedy_clicked
    current_algo = "greedy"
    dijk_clicked = False
    astar_clicked = False
    greedy_clicked = True


def main():
    # print("You entered: ", sys.argv[1], sys.argv[2], sys.argv[3])
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT),pygame.RESIZABLE|pygame.SCALED)
    CLOCK = pygame.time.Clock()
    SCREEN.fill(colors.BLACK)
    pygame.display.set_caption("PathFinding Visualizer")
    grid = grid_utils.load_grid(num_cols, num_rows, square_width, 1)

    # button = pygame.Rect(5,HEIGHT+10,100,50)
    while True:

        wall_button,start_button,end_button,pathfind_button,\
        clear_button,dijk_button,astar_button,greedy_button = drawButtons()

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
                    grid = grid_utils.clear_grid(grid,num_cols,num_rows)
                elif dijk_button.button_rect.collidepoint(mouse_pos):
                    current_dijk()
                elif astar_button.button_rect.collidepoint(mouse_pos):
                    current_astar()
                elif greedy_button.button_rect.collidepoint(mouse_pos):
                    current_greedy()
                elif pathfind_button.button_rect.collidepoint(mouse_pos):
                    #print("Pathfind Button was pressed")
                    grid = grid_utils.clean_grid(grid, num_cols, num_rows)
                    graph = Algo.Graph(grid)
                    if current_algo == "dijkstra":
                        graph.start_dijkstra(grid, SCREEN)
                    elif current_algo == "astar":
                        graph.start_astar(grid, SCREEN)
                    elif current_algo == "greedy":
                        graph.start_greedy(grid, SCREEN)
                else:
                    column = mouse_pos[0] // (square_width + PAD)
                    row = mouse_pos[1] // (square_width + PAD)
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
                column = position[0] // (square_width + PAD)
                row = position[1] // (square_width + PAD)

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
    wall_button = button.Button(SCREEN, colors.GRAY, 5, HEIGHT + 5, 160, 75, "Wall")
    wall_button.draw()
    start_button = button.Button(SCREEN, colors.BLUE, 5 + 165, HEIGHT + 5, 160, 75, "Start Position")
    start_button.draw()
    end_button = button.Button(SCREEN, colors.RED, 5 + (2 * 165), HEIGHT + 5, 160, 75, "End Position")
    end_button.draw()
    pathfind_button = button.Button(SCREEN, colors.LIME_GREEN, 5 + (3 * 165), HEIGHT + 5, 160, 75, "Path Find")
    pathfind_button.draw()
    clear_button = button.Button(SCREEN, colors.ORANGE, 5 + (4 * 165), HEIGHT + 5, 160, 75 , "Clear Grid")
    clear_button.draw()
    dijk_button = button.Button(SCREEN, colors.LIME_GREEN if dijk_clicked is True else colors.WHITE ,WIDTH+2,10,WIN_WIDTH-(WIDTH+2),50, "Dijkstra")
    dijk_button.draw()
    astar_button = button.Button(SCREEN, colors.LIME_GREEN if astar_clicked is True else colors.WHITE,WIDTH+2,10+55,WIN_WIDTH-(WIDTH+2),50, "A*")
    astar_button.draw()
    greedy_button = button.Button(SCREEN, colors.LIME_GREEN if greedy_clicked is True else colors.WHITE, WIDTH + 2, 10 + 110, WIN_WIDTH - (WIDTH + 2), 50, "Greedy First")
    greedy_button.draw()
    return wall_button,start_button,end_button,pathfind_button,clear_button,dijk_button,astar_button,greedy_button





if __name__ == "__main__":
    main()







