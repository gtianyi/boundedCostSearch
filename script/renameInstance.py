import json
import os
import shutil

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/tile.heavy-easy-new-old-namemap.json") as f:
    data = json.load(f)
    for i, key in enumerate(data):
        if os.path.exists(data[key]):
            shutil.copy2(data[key], '/home/aifs1/gu/phd/research/workingPaper/realtime-nancy/worlds/slidingTile_tianyi1000-easy-for-heavy/'+key)
