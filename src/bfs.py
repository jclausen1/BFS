import numpy as np
from shapely.geometry import LineString, Point, Polygon

class Node: 
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent # coordinates of parent node or -1 if start, -2 if goal

def in_window(x, y, window_width, window_height):
    if x < 0 or y < 0 or x >= window_width or y >= window_height:
        return False
    return True

def get_neighbours(node, parents): 
    positions = [[-1,0], [1, 0], [0, -1], [0, 1]] # N E S W grid 
    
    x = node.x
    y = node.y 
    
    neighbours = []

    for pos in positions: 
        # Check in bounds 
        if not in_window(x+pos[0], y+pos[1], parents.shape[0], parents.shape[1]):
            continue

        if parents[x+pos[0], y+pos[1]] != None: 
            continue

        node = Node(x+pos[0], y+pos[1], [x,y])
        neighbours.append(node)

    return neighbours

def mark_points_in_Circle(grid, cx, cy, r):
    
    for i in range(cx - r, cx + r + 1):
        for j in range(cy - r, cy + r + 1):

            # Check in bounds 
            if not in_window(i, j, grid.shape[0], grid.shape[1]):
                continue

            if (((i-cx)**2 + (j-cy)**2) <= r**2):
                grid[i,j] = True

    return grid

def mark_points_in_Rectangle(grid, rx1, ry1, rx2, ry2):
    
    for i in range(rx1, rx2 + 1): 
        for j in range(ry1, ry2 + 1):

            # Check in bounds 
            if not in_window(i, j, grid.shape[0], grid.shape[1]):
                continue
            
            grid[i,j] = True
    
    return grid

def get_path_from_goal(gx, gy, parent_grid): 
    path = []
    parent = parent_grid[gx, gy]

    path.append([gx,gy])

    while True:
        if parent == [-1]:
            return path 
        path.append(parent)

        parent = parent_grid[parent[0], parent[1]]

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
        goal_grid = mark_points_in_Circle(  goal_grid, 
                                            int(goal[0]/step_size),    
                                            int(goal[1]/step_size), 
                                            int(goal_radius/step_size))

        # Mark blocked points 
        for obstacle in obstacles: 
            if obstacle['shape'] == "rectangle":
                obs = np.array(obstacle['definition']) / step_size
                blocked_grid = mark_points_in_Rectangle(blocked_grid,
                                                        int(obs[0]), 
                                                        int(obs[1]),
                                                        int(obs[2]),
                                                        int(obs[3]))

            if obstacle['shape'] == "circle":
                cx,cy = obstacle['definition'][0] / step_size ,obstacle['definition'][1] / step_size
                r = obstacle['definition'][2] / step_size
                blocked_grid = mark_points_in_Circle(blocked_grid, int(cx), int(cy), int(r))
        

        start_node = Node(int(start[0]), int(start[1]), -1)

        nodes = []
        nodes.append(start_node)

        self.blocked_grid = blocked_grid
        self.goal_grid = goal_grid

        path_found = False
        
        while len(nodes) != 0 and not path_found: 

            node = nodes.pop(0)

            # Get neighbours    
            neighbours = get_neighbours(node, parent_grid)

            # Mark visited
            visited_grid[node.x, node.y] = True

            # Check if goal 
            if goal_grid[node.x, node.y]:
                path = get_path_from_goal(node.x, node.y, parent_grid)
                self.path = path
                path_found = True

            # For each neighbour 
            for neighbour in neighbours:
                
                nx = neighbour.x
                ny = neighbour.y

                # Check if visited or blocked
                if blocked_grid[nx, ny] or visited_grid[nx, ny]: 
                    continue

                # Mark parent 
                parent_grid[nx, ny] = neighbour.parent
                    
                # Add to queue 
                nodes.append(neighbour)



