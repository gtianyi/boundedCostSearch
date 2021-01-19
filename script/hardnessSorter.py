#!/usr/bin/ python
'''
python3 script
python script code for compare hardness of tile variants

Author: Tianyi Gu
Date: 01/18/2021
'''

__author__ = 'TianyiGu'

from subprocess import Popen, PIPE

researchHome = "/home/aifs1/gu/phd/research/workingPaper"


def solverConfig():

    optimalSolver = {"uniform": researchHome +
                              "/realtime-nancy/build_release/tile-uniform idastar uniform",
                              "heavy": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar heavy",
                              "heavy-easy": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar heavy",
                              "inverse": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar inverse",
                              "reverse": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar reverse",
                              "sqrt": researchHome +
                              "/realtime-nancy/build_release/tile-pdb idastar sqrt",
                              }

    return optimalSolver


def solverOutPutParser(outStr):
    for line in outStr:
        lineContent = line.split()
        if lineContent[2] == b'generated':
            nodeGen = lineContent[3].decode("utf-8")
            return nodeGen

    return -1

def main():
    solvers = solverConfig()

    subdomains=["heavy","inverse","sqrt"]

    problemDir = researchHome+"/realtime-nancy/worlds/slidingTile/"

    nodeGenSum = {}
    for subdomain in subdomains:
        solver = solvers[subdomain]
        nodeGenSum[subdomain] = 0

        for sid in range(1,11):
            command = solver + " < " + problemDir+str(sid)+"-4x4.st"

            print("command ",command)

            process = Popen("exec " + command, stdin=PIPE,
                            stdout=PIPE, stderr=PIPE, shell=True)

            outlines = process.communicate()[0].splitlines()

            nodeGen = solverOutPutParser(outlines)
            print(subdomain, sid, nodeGen)

            nodeGenSum[subdomain] += int(nodeGen)

    sortedByNodeGen = dict(sorted(nodeGenSum.items(),key=lambda x:x[1]))

    print(sortedByNodeGen)

if __name__ == '__main__':
    main()
