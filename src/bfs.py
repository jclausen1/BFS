import numpy as np
from shapely.geometry import LineString, Point, Polygon

class Node: 
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent # coordinates of parent node or -1 if start, -2 if goal

def get_neighbours(node): 
    positions = [[-1,-1], [-1, 1], [1, -1], [1, 1]] # N E S W grid 
    
    x = node.x
    y = node.y 
    
    neighbours = []

    for pos in positions: 
        node = Node(x+pos[0], y+pos[1], [x,y])
        neighbours.append(node)

    return neighbours

def mark_points_in_Circle(grid, cx, cy, r):
    
    for i in range(cx - r, cx + r + 1):
        for j in range(cy - r, cy + r + 1):
            if (i**2 + j**2 <= r**2): 
                grid[i,j] = True

    return grid

def mark_points_in_Rectangle(grid, rx1, ry1, rx2, ry2):
    
    for i in range(rx1, rx2 + 1): 
        for j in range(ry1, ry2 + 1):
            grid[i,j] = True
    
    return grid

def get_path_from_goal(gx, gy, parent_grid): 
    path = []
    parent = parent_grid[gx, gy]

    while True:
        if parent == [-1]:
            return path 
        path.append(parent)
        parent = parent_grid[parent[0], parent[1]]
    ################################################### maybe implement a timeout function here? 

class BFS:
    def __init__(self, payload):
        width =  payload['width']
        height = payload['height']
        step_size = payload['step_size']
        grid_width = int(width/step_size)
        grid_height = int(height/step_size)

        start = np.array(payload['start'], dtype=int)
        goal = np.array(payload['goal'], dtype=int)
        goal_radius =  payload['goalRadius']
        
        obstacles = payload['obstacles']

        # Define Grid as np arrays 
        visited_grid = np.zeros((grid_width, grid_height), dtype=bool)
        blocked_grid = np.zeros((grid_width, grid_height), dtype=bool)
        goal_grid = np.zeros((grid_width, grid_height), dtype=bool)
        parent_grid = np.empty((grid_width, grid_height), dtype=object)

        # Mark start position
        parent_grid[start[0], start[1]] = [-1]

        # Mark goal points 
        goal_grid = mark_points_in_Circle(goal_grid, goal[0], goal[1], goal_radius)

        # Mark blocked points 
        for obstacle in obstacles: 
            if obstacle['shape'] == "rectangle":
                blocked_grid = mark_points_in_Rectangle(blocked_grid,
                                                        int(obstacle[0]), 
                                                        int(obstacle[1]),
                                                        int(obstacle[2]),
                                                        int(obstacle[3]))

            if obstacle['shape'] == "circle":
                cx,cy = obstacle['definition'][0],obstacle['definition'][1]
                r = obstacle['definition'][2]
                blocked_grid = mark_points_in_Circle(blocked_grid, int(cx), int(cy), int(r))
        

        start_node = Node(int(start[0]), int(start[1]), -1)

        nodes = []
        nodes.append(start_node)

        for node in nodes: 
            # Get neighbours    
            neighbours = get_neighbours(node)

            # For each neighbour 
            for neighbour in neighbours:
                
                nx = neighbour.x
                ny = neighbour.y

                # Check if visited or blocked
                if blocked_grid[nx, ny] or visited_grid[nx, ny]: 
                    continue

                # Mark parent 
                parent_grid[nx, ny] = neighbour.parent

                # Check if goal 
                if goal_grid[nx, ny]:
                    path = get_path_from_goal(goal[0], goal[1], parent_grid)
                    return path
                    
                # Add to queue 
                nodes.append(neighbour)

            # Mark visited
            visited_grid[node.x, node.y] = True





