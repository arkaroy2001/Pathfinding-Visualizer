import math
from queue import PriorityQueue
import main
import time


class Graph():
    # create a nested map (adjacency list) of all grid squares
    def __init__(self, grid):
        self.numEdges = 0
        self.nodes = []
        self.neighbors_map = {}

        for column in grid:
            for square in column:
                if square.state == "wall":
                    continue

                self.neighbors_map[(square.x,square.y)]={}

                if grid[square.x][square.y - 1].state != "wall":
                    square.neighbors.append(grid[square.x][square.y - 1])
                    self.neighbors_map[(square.x,square.y)][(square.x,square.y-1)] = grid[square.x][square.y].weight + grid[square.x][square.y-1].weight
                if grid[square.x][square.y + 1].state != "wall":
                    square.neighbors.append(grid[square.x][square.y + 1])
                    self.neighbors_map[(square.x, square.y)][(square.x, square.y + 1)] = grid[square.x][square.y].weight + grid[square.x][square.y + 1].weight
                if grid[square.x - 1][square.y].state != "wall":
                    square.neighbors.append(grid[square.x - 1][square.y])
                    self.neighbors_map[(square.x, square.y)][(square.x-1, square.y)] = grid[square.x][square.y].weight + grid[square.x-1][square.y].weight
                if grid[square.x + 1][square.y].state != "wall":
                    square.neighbors.append(grid[square.x + 1][square.y])
                    self.neighbors_map[(square.x, square.y)][(square.x+1, square.y)] = grid[square.x][square.y].weight + grid[square.x+1][square.y].weight

                self.nodes.append((square.x, square.y))

        #print("HAHA")

        # for column in grid:
            #for square in column:
                #print("square:{},{}".format(square.x,square.y))
                #for neighbor in square.neighbors:
                   #print("neighbor:{},{}".format(neighbor.x,neighbor.y))

    def AllNodes(self):
        return self.nodes

    def edge_weight(self,outerTup,innerTup):
        if outerTup in self.neighbors_map:
            if innerTup in self.neighbors_map[outerTup]:
                return self.neighbors_map[outerTup][innerTup]

        return -1

    def findNeighbors(self,tup):
        neighbor_vect = []
        innerMap = self.neighbors_map[tup]

        for objects in innerMap:
            neighbor_vect.append(objects)

        return neighbor_vect

    def start_dijkstra(self, grid, SCREEN):
        counter = 0

        for i in grid:
            for j in i:
                if j.state == "wall" or j.border == True:
                    continue
                if j.state == "start_pos":
                    start_grid = j
                    counter = counter + 1
                elif j.state == "end_pos":
                    end_grid = j
                    counter = counter + 1

        if counter != 2:
            #print("What the heck")
            return

        pq = PriorityQueue()
        nodeMap = {}

        bt_helper = []

        start_coordinate = (start_grid.x,start_grid.y)
        end_coordinate = (end_grid.x,end_grid.y)
        for objects in self.AllNodes():
            Node = {"coordinate": objects,
                    "done": False, "distance": math.inf}
            nodeMap[objects] = Node


        nodeMap[start_coordinate]["distance"] = 0
        returnVect = []
        pq.put((0,(0,0),start_coordinate))
        #print("LOL")

        while not pq.empty():
            top = pq.get()

            if top[2] == end_coordinate:
                present = (self.edge_weight(top[2], nodeMap[top[2]]["prev"]), nodeMap[top[2]]["prev"], top[2])
                # grid[present[1][0]][present[1][1]].back_trace = True
                # grid[present[1][0]][present[1][1]].animate(SCREEN)
                # time.sleep(0.09)

                while present[1] != start_coordinate:
                    bt_helper.append(present)
                    present = (
                    self.edge_weight(nodeMap[present[1]]["prev"], present[1]), nodeMap[present[1]]["prev"],
                    present[1])
                    grid[present[2][0]][present[2][1]].back_trace = True
                    grid[present[2][0]][present[2][1]].animate(SCREEN)
                    time.sleep(0.04)
                    main.update_squares(SCREEN, grid)

                bt_helper.append(present)
                grid[present[2][0]][present[2][1]].back_trace = True
                grid[present[2][0]][present[2][1]].animate(SCREEN)
                # time.sleep(0.1)
                main.update_squares(SCREEN, grid)

                while not bt_helper:
                    returnVect.append(bt_helper.pop())

                # print("Fasho")
                return returnVect

            if nodeMap[top[2]]["done"] == False:
                nodeMap[top[2]]["done"] = True

                if top[2]!=start_coordinate and top[2]!=end_coordinate:
                    grid[top[2][0]][top[2][1]].is_visited=True
                    #print("HERE")
                    grid[top[2][0]][top[2][1]].animate(SCREEN)
                    #print("{},{}".format(top[2][0],top[2][1]))
                    time.sleep(0.02)

                main.update_squares(SCREEN, grid)
                grid_neighbors = self.findNeighbors(top[2])
                #grid_neighbors = self.neighbors_map[top[1]]
                edge = self.edge_weight(top[2],grid_neighbors[0])
                for neighbor in grid_neighbors:
                    if self.edge_weight(top[2],neighbor) + nodeMap[top[2]]["distance"] < nodeMap[neighbor]["distance"]:
                        nodeMap[neighbor]["distance"] = self.edge_weight(top[2],neighbor) + nodeMap[top[2]]["distance"]
                        pq.put((nodeMap[neighbor]["distance"], top[2],neighbor))
                        nodeMap[neighbor]["prev"] = top[2]
                        grid[neighbor[0]][neighbor[1]].is_visited = False
                        #grid[neighbor[0]][neighbor[1]].animate(main.SCREEN)



        return returnVect

    def start_astar(self, grid, SCREEN):
        counter = 0

        for i in grid:
            for j in i:
                if j.state == "wall" or j.border == True:
                    continue
                if j.state == "start_pos":
                    start_grid = j
                    counter = counter + 1
                elif j.state == "end_pos":
                    end_grid = j
                    counter = counter + 1

        if counter != 2:
            # print("What the heck")
            return

        pq = PriorityQueue()
        nodeMap = {}

        bt_helper = []

        start_coordinate = (start_grid.x, start_grid.y)
        end_coordinate = (end_grid.x, end_grid.y)
        for objects in self.AllNodes():
            Node = {"coordinate": objects, "done": False, "distance": math.inf,
                    "h-score":math.sqrt(abs(end_grid.x - objects[0])**2+abs(end_grid.y-objects[1])**2)}
            nodeMap[objects] = Node

        nodeMap[start_coordinate]["distance"] = 0
        returnVect = []
        pq.put((0+(math.sqrt(abs(end_grid.x - start_grid.x)**2+abs(end_grid.y-start_grid.y)**2)), (0, 0), start_coordinate))
        # print("LOL")

        while not pq.empty():
            top = pq.get()

            if top[2] == end_coordinate:
                present = (self.edge_weight(top[2], nodeMap[top[2]]["prev"]), nodeMap[top[2]]["prev"], top[2])
                # grid[present[1][0]][present[1][1]].back_trace = True
                # grid[present[1][0]][present[1][1]].animate(SCREEN)
                # time.sleep(0.09)

                while present[1] != start_coordinate:
                    bt_helper.append(present)
                    present = (
                        self.edge_weight(nodeMap[present[1]]["prev"], present[1]), nodeMap[present[1]]["prev"],
                        present[1])
                    grid[present[2][0]][present[2][1]].back_trace = True
                    grid[present[2][0]][present[2][1]].animate(SCREEN)
                    time.sleep(0.04)
                    main.update_squares(SCREEN, grid)

                bt_helper.append(present)
                grid[present[2][0]][present[2][1]].back_trace = True
                grid[present[2][0]][present[2][1]].animate(SCREEN)
                # time.sleep(0.1)
                main.update_squares(SCREEN, grid)

                while not bt_helper:
                    returnVect.append(bt_helper.pop())

                # print("Fasho")
                return returnVect

            if nodeMap[top[2]]["done"] == False:
                nodeMap[top[2]]["done"] = True

                if top[2] != start_coordinate and top[2] != end_coordinate:
                    grid[top[2][0]][top[2][1]].is_visited = True
                    # print("HERE")
                    grid[top[2][0]][top[2][1]].animate(SCREEN)
                    # print("{},{}".format(top[2][0],top[2][1]))
                    time.sleep(0.02)

                main.update_squares(SCREEN, grid)
                grid_neighbors = self.findNeighbors(top[2])
                # grid_neighbors = self.neighbors_map[top[1]]
                edge = self.edge_weight(top[2], grid_neighbors[0])
                for neighbor in grid_neighbors:
                    if self.edge_weight(top[2], neighbor) + nodeMap[top[2]]["distance"] < nodeMap[neighbor][
                        "distance"]:
                        nodeMap[neighbor]["distance"] = self.edge_weight(top[2], neighbor) + nodeMap[top[2]][
                            "distance"]
                        combined_score = nodeMap[neighbor]["distance"]+nodeMap[neighbor]["h-score"]
                        pq.put((combined_score, top[2], neighbor))
                        nodeMap[neighbor]["prev"] = top[2]
                        grid[neighbor[0]][
                            neighbor[1]].is_visited = False  # grid[neighbor[0]][neighbor[1]].animate(main.SCREEN)



        return returnVect

    def start_greedy(self, grid, SCREEN):
        counter = 0

        for i in grid:
            for j in i:
                if j.state == "wall" or j.border == True:
                    continue
                if j.state == "start_pos":
                    start_grid = j
                    counter = counter + 1
                elif j.state == "end_pos":
                    end_grid = j
                    counter = counter + 1

        if counter != 2:
            # print("What the heck")
            return

        pq = PriorityQueue()
        nodeMap = {}

        bt_helper = []

        start_coordinate = (start_grid.x, start_grid.y)
        end_coordinate = (end_grid.x, end_grid.y)
        for objects in self.AllNodes():
            Node = {"done": False,
                    "h-score":math.sqrt(abs(end_grid.x - objects[0])**2+abs(end_grid.y-objects[1])**2)}
            nodeMap[objects] = Node


        returnVect = []
        pq.put(((math.sqrt(abs(end_grid.x - start_grid.x)**2+abs(end_grid.y-start_grid.y)**2)), (0, 0), start_coordinate))
        # print("LOL")

        while not pq.empty():
            top = pq.get()

            if top[2] == end_coordinate:
                present = (self.edge_weight(top[2], nodeMap[top[2]]["prev"]), nodeMap[top[2]]["prev"], top[2])
                # grid[present[1][0]][present[1][1]].back_trace = True
                # grid[present[1][0]][present[1][1]].animate(SCREEN)
                # time.sleep(0.09)

                while present[1] != start_coordinate:
                    bt_helper.append(present)
                    present = (
                    self.edge_weight(nodeMap[present[1]]["prev"], present[1]), nodeMap[present[1]]["prev"],
                    present[1])
                    grid[present[2][0]][present[2][1]].back_trace = True
                    grid[present[2][0]][present[2][1]].animate(SCREEN)
                    time.sleep(0.04)
                    main.update_squares(SCREEN, grid)
                    print("HOLA")

                bt_helper.append(present)
                grid[present[2][0]][present[2][1]].back_trace = True
                grid[present[2][0]][present[2][1]].animate(SCREEN)
                # time.sleep(0.1)
                main.update_squares(SCREEN, grid)

                while not bt_helper:
                    returnVect.append(bt_helper.pop())

                # print("Fasho")
                return returnVect

            if nodeMap[top[2]]["done"] == False:
                nodeMap[top[2]]["done"] = True

                if top[2] != start_coordinate and top[2] != end_coordinate:
                    grid[top[2][0]][top[2][1]].is_visited = True
                    # print("HERE")
                    grid[top[2][0]][top[2][1]].animate(SCREEN)
                    # print("{},{}".format(top[2][0],top[2][1]))
                    time.sleep(0.02)

                main.update_squares(SCREEN, grid)
                grid_neighbors = self.findNeighbors(top[2])
                # grid_neighbors = self.neighbors_map[top[1]]
                edge = self.edge_weight(top[2], grid_neighbors[0])
                for neighbor in grid_neighbors:
                    if nodeMap[neighbor]["done"]==False:
                        h_score = nodeMap[neighbor]["h-score"]
                        pq.put((h_score, top[2], neighbor))
                        nodeMap[neighbor]["prev"] = top[2]
                        grid[neighbor[0]][
                            neighbor[1]].is_visited = False  # grid[neighbor[0]][neighbor[1]].animate(main.SCREEN)



        return returnVect
