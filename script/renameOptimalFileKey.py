import json

new = {}
newName_oldName = {}

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.heavy-easy.json") as f:
    data = json.load(f)
    for i, key in enumerate(data):
        # new[str(i+1)+'-4x4.st'] = data[key]
        new[str(i+1)+'.vw'] = data[key]
        # newName_oldName[str(i+1)+'-4x4.st'] = key
        newName_oldName[str(i+1)+'.vw'] = key

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.heavy-easy-new.json", 'w') as f:
    json.dump(new, f)

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.heavy-easy-new-old-namemap.json", 'w') as f:
    json.dump(newName_oldName, f)
