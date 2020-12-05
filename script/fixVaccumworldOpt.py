import json

new = {}

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.uniform.json") as f:
    data = json.load(f)
    for key in data:
        if data[key] != '-1':
            new[key] = data[key]

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/vaccumworld.uniform-new.json", 'w') as f:
    json.dump(new, f)
