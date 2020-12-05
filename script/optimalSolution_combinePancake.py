import json

new = {}

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/pancake.heavy.10.json") as f:
    data = json.load(f)
    for key in data:
        new[key] = data[key]

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/pancake.heavy.json") as f:
    data = json.load(f)
    for key in data:
        new[key] = data[key]

with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/pancake.heavy.new.json", 'w') as f:
    json.dump(new, f)
