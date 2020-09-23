#!/usr/bin/env python
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

    parser = argparse.ArgumentParser(description='boundedCostPlot')

    parser.add_argument(
        '-d',
        action='store',
        dest='domain',
        help='domain: tile(default), pancake, racetrack',
        default='tile')

    parser.add_argument(
        '-s',
        action='store',
        dest='subdomain',
        help='subdomain: tile: uniform(default), heavy, inverse; \
        pancake: regular, heavy; \
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double',
        default='uniform')

    parser.add_argument('-z',
                        action='store',
                        dest='size',
                        help='domain size (default: 4)',
                        default='4')

    return parser


def solverConfig():

    optimalSolver = {"tile": {"uniform": researchHome +
                              "/realtime-nancy/build_release/tile-uniform idastar uniform"}}

    problemFolder = {
        "tile": "slidingTile"
    }

    return optimalSolver, problemFolder


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    solvers, problemFolder = solverConfig()

    solver = solvers[args.domain][args.subdomain]

    problemDir = researchHome+"/realtime-nancy/worlds/" + \
        problemFolder[args.domain]+"/"

    solutionJson = {}

    counter = 0
    total = len(os.listdir(problemDir))
    for problemFile in os.listdir(problemDir):
        counter += 1
        command = solver + " < " + problemDir+problemFile

        process = Popen("exec " + command, stdin=PIPE,
                        stdout=PIPE, stderr=PIPE, shell=True)

        outlines = process.communicate()[0].splitlines()

        for line in outlines:
            lineContent = line.split()
            if lineContent[1] == b'"solution':
                sol = re.findall(r'\d+', lineContent[3].decode("utf-8"))[0]
                solutionJson[problemFile] = sol
                print(problemFile, sol, str(counter/total*100)+"%")
                break

    outFile = researchHome+"/boundedCostSearch/optimalSolution/" +\
        args.domain+"."+args.subdomain+".json"

    with open(outFile, 'w') as json_file:
        json.dump(solutionJson, json_file)


if __name__ == '__main__':
    main()