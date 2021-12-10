import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from pprint import pprint

from src.bfs import BFS

payload = {}

payload['obstacles'] = [{"shape":"rectangle", "definition":[20,10,40,20]},{"shape":"circle", "definition":[10,10,3]}, {"shape":"circle", "definition":[50,50,20]}]
payload['start'] = [0,0]
payload['goal'] = [350,250]
payload['goalRadius'] = 10
payload['width'] = 400
payload['height'] = 400

payload['obstacles'] = [{"shape":"rectangle", "definition":[0,0,2,2]},
                        {"shape":"rectangle", "definition":[6,6,10,10]},
                        {"shape":"rectangle", "definition":[6,4,6,6]},
                        {"shape":"rectangle", "definition":[10,10,14,14]},
                        {"shape":"circle", "definition":[4,2,1]}]
payload['start'] = [12,8]
payload['goal'] = [0,8]
payload['goalRadius'] = 1
payload['width'] = 14
payload['height'] = 14
payload['step_size'] = 1

if __name__ == '__main__':
    bfs = BFS(payload)
    print(bfs.__dict__)
    
    cmap1 = matplotlib.colors.ListedColormap(['none', 'green'])
    cmap2 = matplotlib.colors.ListedColormap(['none', 'red'])
    cmap3 = matplotlib.colors.ListedColormap(['none', 'blue'])

    path_grid = np.zeros(bfs.blocked_grid.shape, dtype=bool)

    for pt in bfs.path: 
        path_grid[pt[0], pt[1]] = True

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(bfs.blocked_grid, cmap=cmap2, interpolation='nearest')
    ax.imshow(bfs.goal_grid, cmap=cmap1, interpolation='nearest')
    ax.imshow(path_grid, cmap=cmap3, interpolation='nearest')
    plt.show()