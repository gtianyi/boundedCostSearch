import json

new = {}
newName_oldName = {}

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/tile.heavy-easy.json") as f:
    data = json.load(f)
    for i, key in enumerate(data):
        new[str(i+1)+'-4x4.st'] = data[key]
        newName_oldName[str(i+1)+'-4x4.st'] = key

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/tile.heavy-easy-new.json", 'w') as f:
    json.dump(new, f)

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/tile.heavy-easy-new-old-namemap.json", 'w') as f:
    json.dump(newName_oldName, f)
