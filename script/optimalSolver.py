#!/usr/bin/ python
'''
python3 script
python script code for gather optmial solution and dump as json

Author: Tianyi Gu
Date: 09/22/2020
'''

__author__ = 'TianyiGu'

import argparse
import json
import os
from subprocess import Popen, PIPE
import re

researchHome = "/home/aifs1/gu/phd/research/workingPaper"


def parseArugments():

    parser = argparse.ArgumentParser(description='optimalSolver')

    parser.add_argument(
        '-d',
        action='store',
        dest='domain',
        help='domain: tile(default), pancake, racetrack, vacuumworld',
        default='tile')

    parser.add_argument(
        '-s',
        action='store',
        dest='subdomain',
        help='subdomain: tile: uniform(default), heavy, inverse, reverse, sqrt; \
        pancake: regular, heavy; \
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double\
        vacuumworld: uniform, heavy;',
        default='uniform')

    parser.add_argument('-z',
                        action='store',
                        dest='size',
                        help='domain size (default: 4)',
                        default='4')

    return parser


def solverConfig():

    optimalSolver = {"tile": {"uniform": researchHome +
                              "/realtime-nancy/build_release/tile-uniform idastar uniform",
                              "heavy": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar heavy",
                              "heavy-easy": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar heavy",
                              "inverse": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar inverse",
                              "reverse": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar reverse",
                              },
                     "pancake": {"regular": researchHome +
                                 "/realtime-nancy/build_release/distributionPractice"
                                 " -d pancake -s regular -a wastar -p 1",
                                 "heavy": researchHome +
                                 "/realtime-nancy/build_release/distributionPractice"
                                 " -d pancake -s heavy -a wastar -p 3"},
                     "racetrack": {"barto-big": researchHome +
                                   "/realtime-nancy/build_release/distributionPractice"
                                   " -d racetrack -s barto-big -a wastar -p 1",
                                   "barto-bigger": researchHome +
                                   "/realtime-nancy/build_release/distributionPractice"
                                   " -d racetrack -s barto-bigger -a wastar -p 1",
                                   "hansen-bigger": researchHome +
                                   "/realtime-nancy/build_release/distributionPractice"
                                   " -d racetrack -s hansen-bigger -a wastar -p 1",
                                   "uniform": researchHome +
                                   "/realtime-nancy/build_release/distributionPractice"
                                   " -d racetrack -s uniform -a wastar -p 1",
                                   "uniform-small": researchHome +
                                   "/realtime-nancy/build_release/distributionPractice"
                                   " -d racetrack -s uniform-small -a wastar -p 1"},
                     "vacuumworld": {"uniform": researchHome +
                                     "/boundedCostSearch/tianyicodebase_build_release/bin/bcs"
                                     " -d vacuumworld -a astar",
                                     "heavy": researchHome +
                                     "/boundedCostSearch/tianyicodebase_build_release/bin/bcs"
                                     " -d vacuumworld -a astar -s heavy",
                                     "heavy-easy": researchHome +
                                     "/boundedCostSearch/tianyicodebase_build_release/bin/bcs"
                                     " -d vacuumworld -a astar -s heavy"}
                     }

    problemFolder = {
        "tile": "slidingTile",
        "tile-heavy-easy": "slidingTile_tianyi1000-easy-for-heavy",
        "pancake": "pancake",
        "racetrack": "racetrack",
        "vacuumworld": "vacuumworld/200x200",
        "vacuumworld-heavy-easy": "vacuumworld/200x200-6"
    }

    return optimalSolver, problemFolder


def solverOutPutParser(args, outStr):
    if args.domain == "tile":

        if args.subdomain == "uniform":
            for line in outStr:
                lineContent = line.split()
                if lineContent[1] == b'"solution':
                    sol = re.findall(r'\d+', lineContent[3].decode("utf-8"))[0]
                    return sol

        elif args.subdomain in ["heavy", "heavy-easy", "inverse", "inverse-easy", "reverse"] :
            for line in outStr:
                lineContent = line.split()
                if lineContent[0] == b'solution':
                    sol = lineContent[2].decode("utf-8")
                    return sol

    elif args.domain in ["pancake", "racetrack", "vacuumworld"]:
        return outStr[0].split()[2].decode("utf-8")

    return "error: parsing solver output"


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    solvers, problemFolder = solverConfig()

    solver = solvers[args.domain][args.subdomain]

    problemDir = researchHome+"/realtime-nancy/worlds/"
    if args.domain == "tile":
        if args.subdomain in ["uniform", "heavy", "inverse", "reverse"]:
            problemDir += problemFolder[args.domain]+"/"
        elif args.subdomain == "heavy-easy":
            problemDir += problemFolder[args.domain+"-"+args.subdomain]+"/"
    if args.domain == "racetrack":
        problemDir += problemFolder[args.domain]+"-"+args.subdomain+"/"
    elif args.domain == "pancake":
        problemDir += problemFolder[args.domain]+"/"+args.size+"/"

    if args.domain == "vacuumworld":
        if args.subdomain in ["uniform", "heavy"]:
            problemDir += problemFolder[args.domain]+"/"
        elif args.subdomain == "heavy-easy":
            problemDir += problemFolder[args.domain+"-"+args.subdomain]+"/"

    solutionJson = {}

    counter = 0
    total = len(os.listdir(problemDir))
    for problemFile in os.listdir(problemDir):
        counter += 1
        command = solver + " < " + problemDir+problemFile

        # print("command ",command)

        process = Popen("exec " + command, stdin=PIPE,
                        stdout=PIPE, stderr=PIPE, shell=True)

        outlines = process.communicate()[0].splitlines()

        sol = solverOutPutParser(args, outlines)
        solutionJson[problemFile] = sol
        print(problemFile, sol, str(counter/total*100)+"%")

    outFile = researchHome+"/boundedCostSearch/optimalSolution/" +\
        args.domain+"."+args.subdomain

    if args.domain == "pancake":
        outFile += "."+args.size

    outFile += ".json"

    with open(outFile, 'w') as json_file:
        json.dump(solutionJson, json_file)

if __name__ == '__main__':
    main()
