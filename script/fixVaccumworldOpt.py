import json

new = {}

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.heavy-easy.json") as f:
    data = json.load(f)
    for key in data:
        if len(new) == 60:
            break
        if data[key] != '-1':
            new[key] = data[key]

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.heavy-easy-new.json", 'w') as f:
    json.dump(new, f)
