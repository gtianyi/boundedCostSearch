#!/usr/bin/ python
'''
python3 script
python script code for
1. solve problems give problem folder and solver command, with time bound
2. sort solved problems by number of node generated
3. copy selected problems to target folder
4. rename problem from instance id 1, and record the mapping, dump out the recording JSON
5. dump out the solution

Author: Tianyi Gu
Date: 12/10/2020
'''

__author__ = 'TianyiGu'

import argparse
import os
import json
from subprocess import Popen, PIPE, TimeoutExpired
# import re
from shutil import copy2
from operator import getitem

researchHome = "/home/aifs1/gu/phd/research/workingPaper"


def parseArugments():

    parser = argparse.ArgumentParser(description='optimalSolver')

    parser.add_argument(
        '-d',
        action='store',
        dest='domain',
        help='domain: tile(default),future support: pancake, racetrack, vaccumworld',
        default='tile')

    parser.add_argument(
        '-s',
        action='store',
        dest='subdomain',
        help='subdomain: tile: uniform, heavy(default), inverse, reverse future support: sqrt; \
        pancake: regular, heavy; \
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double\
        vaccumworld: uniform, heavy;',
        default='heavy')

    parser.add_argument('-z',
                        action='store',
                        dest='size',
                        help='domain size (default: 4)',
                        default='4')

    return parser


def solverConfig():

    solver = {"tile": {"uniform": researchHome +
                              "/realtime-nancy/build_release/tile-uniform idastar uniform",
                              "heavy": researchHome +
                              "/realtime-nancy/build_release/distributionPractice"
                              " -d tile -s heavy -a wastar -p 1",
                              "inverse": researchHome +
                              # "/realtime-nancy/build_release/tile-pdb-heavy-inverse"
                              # " idastar inverse",
                              "/realtime-nancy/build_release/distributionPractice"
                              " -d tile -s inverse -a wastar -p 1",
                              "reverse": researchHome +
                              "/realtime-nancy/build_release/distributionPractice"
                              " -d tile -s reverse -a wastar -p 1",
                       },
                     }

    problemFolder = {
        "tile": "slidingTile_tianyi1000",
        "pancake": "pancake",
        "racetrack": "racetrack",
        "vaccumworld": "vaccumworld/200x200"
    }

    return solver, problemFolder


def solverOutPutParser(args, outStr):
    if args.domain == "tile":

        # if args.subdomain == "uniform":
            # for line in outStr:
                # lineContent = line.split()
                # if lineContent[1] == b'"solution':
                    # sol = re.findall(r'\d+', lineContent[3].decode("utf-8"))[0]
                    # return sol

        # elif args.subdomain == "heavy":
        if args.subdomain in ["heavy", "inverse", "reverse"]:
            sol = outStr[0].split()[2].decode("utf-8")
            nodeGen = outStr[0].split()[0].decode("utf-8")
            return nodeGen, sol

        # if args.subdomain == "inverse":
            # sol=""
            # nodeGen=""

            # for line in outStr:
                # lineContent = line.split()
                # if lineContent[2] == b'generated':
                    # nodeGen = lineContent[3].decode("utf-8")
                # elif lineContent[0] == b'solution':
                    # sol = lineContent[2].decode("utf-8")
                    # break

            # return nodeGen, sol

    # elif args.domain in ["pancake", "racetrack", "vaccumworld"]:
        # return outStr[0].split()[2].decode("utf-8")

    return "error: parsing solver output"


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    solvers, problemFolder = solverConfig()

    solver = solvers[args.domain][args.subdomain]

    problemDir = researchHome+"/realtime-nancy/worlds/" + \
        problemFolder[args.domain]+"/"

    # if args.domain == "racetrack":
        # problemDir = researchHome+"/realtime-nancy/worlds/" + \
            # problemFolder[args.domain]+"-"+args.subdomain+"/"
    # elif args.domain == "pancake":
        # problemDir = researchHome+"/realtime-nancy/worlds/" + \
            # problemFolder[args.domain]+"/"+args.size+"/"

    nodeGenJson = {}

    counter = 0
    solvedCounter=0
    total = len(os.listdir(problemDir))
    print("solving problems, total", total)
    for problemFile in os.listdir(problemDir):
    #     if(len(nodeGenJson) == 100):
            # break

        counter += 1
        command = solver + " < " + problemDir+problemFile

        # print("command ",command)

        process = Popen("exec " + command, stdin=PIPE,
                        stdout=PIPE, stderr=PIPE, shell=True)

        try:
            outlines = process.communicate(timeout=300)[0].splitlines()
            nodeGen, sol = solverOutPutParser(args, outlines)
            nodeGenJson[problemFile] = {"nodeGen":int(nodeGen), "solution": sol }
            solvedCounter += 1
            print(problemFile, nodeGen, str(counter/total*100)+"%", "solved: ", solvedCounter)
        except TimeoutExpired:
            process.kill()
            print(problemFile, "cutoff", str(counter/total*100)+"%", "solved: ", solvedCounter)

    outDir = researchHome+"/realtime-nancy/worlds/" +\
        problemFolder[args.domain] + "-easy-for-"+args.subdomain+"/"

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    sortedByNodeGen = dict(sorted(nodeGenJson.items(), key=lambda x: getitem(x[1], 'nodeGen')))

    print(sortedByNodeGen)

    print("copying files...")
    counter=0
    newName_oldName = {}
    solutionJson={}
    for fileName in sortedByNodeGen:
        counter += 1
        if counter > 100:
            break

        copy2(problemDir+fileName, outDir+str(counter)+"-4x4.st")
        newName_oldName[str(counter)+'-4x4.st'] = fileName
        solutionJson[str(counter)+"-4x4.st"] = sortedByNodeGen[fileName]["solution"]

    print("dump rename mapping")
    with open("/home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/optimalSolution/tile."+\
              args.subdomain+"-easy-new-old-namemap.json", 'w') as f:
        json.dump(newName_oldName, f)


    print("dump solution file")
    solutionOutFile = researchHome+"/boundedCostSearch/optimalSolution/" +\
        args.domain+"."+args.subdomain+"-easy.json"

    with open(solutionOutFile, 'w') as json_file:
        json.dump(solutionJson, json_file)


if __name__ == '__main__':
    main()
