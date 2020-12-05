#!/usr/bin/ python
'''
python3 script
python script code for gather optmial solution and dump as json

Author: Tianyi Gu
Date: 09/22/2020
'''

__author__ = 'TianyiGu'

import argparse
import os
from subprocess import Popen, PIPE, TimeoutExpired
# import re
from shutil import copy2

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
        help='subdomain: tile: uniform, heavy(default), future support: inverse; \
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
                              " -d tile -s heavy -a wastar -p 1"},
                     # "pancake": {"regular": researchHome +
                                 # "/realtime-nancy/build_release/distributionPractice"
                                 # " -d pancake -s regular -a wastar -p 1",
                                 # "heavy": researchHome +
                                 # "/realtime-nancy/build_release/distributionPractice"
                                 # " -d pancake -s heavy -a wastar -p 3"},
                     # "racetrack": {"barto-big": researchHome +
                                   # "/realtime-nancy/build_release/distributionPractice"
                                   # " -d racetrack -s barto-big -a wastar -p 1",
                                   # "barto-bigger": researchHome +
                                   # "/realtime-nancy/build_release/distributionPractice"
                                   # " -d racetrack -s barto-bigger -a wastar -p 1",
                                   # "hansen-bigger": researchHome +
                                   # "/realtime-nancy/build_release/distributionPractice"
                                   # " -d racetrack -s hansen-bigger -a wastar -p 1",
                                   # "uniform": researchHome +
                                   # "/realtime-nancy/build_release/distributionPractice"
                                   # " -d racetrack -s uniform -a wastar -p 1",
                                   # "uniform-small": researchHome +
                                   # "/realtime-nancy/build_release/distributionPractice"
                                   # " -d racetrack -s uniform-small -a wastar -p 1"},
                     # "vaccumworld": {"uniform": researchHome +
                                     # "/boundedCostSearch/tianyicodebase_build_release/bin/bcs"
                                     # " -d vaccumworld -a astar",
                                     # "heavy": researchHome +
                                     # "/boundedCostSearch/tianyicodebase_build_release/bin/bcs"
                                     # " -d vaccumworld -a astar -s heavy"}
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
        if args.subdomain == "heavy":
            return outStr[0].split()[0].decode("utf-8")

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
        if(len(nodeGenJson) == 100):
            break

        counter += 1
        command = solver + " < " + problemDir+problemFile

        # print("command ",command)

        process = Popen("exec " + command, stdin=PIPE,
                        stdout=PIPE, stderr=PIPE, shell=True)

        try:
            outlines = process.communicate(timeout=300)[0].splitlines()
            nodeGen = solverOutPutParser(args, outlines)
            nodeGenJson[problemFile] = int(nodeGen)
            solvedCounter += 1
            print(problemFile, nodeGen, str(counter/total*100)+"%", "solved: ", solvedCounter)
        except TimeoutExpired:
            process.kill()
            print(problemFile, "cutoff", str(counter/total*100)+"%", "solved: ", solvedCounter)

    outDir = researchHome+"/realtime-nancy/worlds/" +\
        problemFolder[args.domain] + "-easy-for-"+args.subdomain+"/"

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    sortedByNodeGen = dict(sorted(nodeGenJson.items(), key=lambda item: item[1]))

    print(sortedByNodeGen)

    print("copying files...")
    counter=0
    for fileName in sortedByNodeGen:
        counter += 1
        if counter > 100:
            break

        copy2(problemDir+fileName, outDir+fileName)


if __name__ == '__main__':
    main()
