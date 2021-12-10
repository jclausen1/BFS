import numpy as np
#from pprint import pprint

from src.bfs import BFS

payload = {}

payload['obstacles'] = [{"shape":"rectangle", "definition":[20,10,40,20]},{"shape":"circle", "definition":[10,10,3]}, {"shape":"circle", "definition":[50,50,20]}]
payload['start'] = [0,0]
payload['goal'] = [350,250]
payload['goalRadius'] = 10
payload['width'] = 400
payload['height'] = 400

payload['obstacles'] = [{"shape":"rectangle", "definition":[0,0,2,2]},{"shape":"circle", "definition":[4,2,1]}]
payload['start'] = [8,0]
payload['goal'] = [0,7]
payload['goalRadius'] = 1
payload['width'] = 14
payload['height'] = 14
payload['step_size'] = 1

if __name__ == '__main__':
    bfs = BFS(payload)
    print(bfs.__dict__)
    
    