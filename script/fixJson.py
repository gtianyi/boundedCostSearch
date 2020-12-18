#!/usr/bin/ python
'''
python3 script
python script code for fixing json result format.

Author: Tianyi Gu
Date: 09/29/2020
'''

__author__ = 'TianyiGu'

import argparse
import os
import re
import in_place

researchHome = "/home/aifs1/gu/phd/research/workingPaper"
# researchHome = "/home/aifs1/gu/Downloads"


def parseArugments():

    parser = argparse.ArgumentParser(description='fixJson')

    parser.add_argument(
        '-d',
        action='store',
        dest='domain',
        help='domain: tile(default), pancake, racetrack, vaccumworld',
        default='tile')

    parser.add_argument(
        '-s',
        action='store',
        dest='subdomain',
        help='subdomain: tile: uniform(default), heavy, inverse; \
        pancake: regular, heavy; \
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double',
        default='uniform')

    parser.add_argument(
        '-a',
        action='append',
        dest='algorithms',
        help='algorithms: wastar, astar, pts, ptshhat, ptsnancy, bees default(all)',
        default=[])

    parser.add_argument(
        '-bt',
        action='store',
        dest='boundType',
        help='boundType: absolute, percentWrtOpt(default);',
        default='percentWrtOpt')

#     parser.add_argument('-z',
    # action='store',
    # dest='size',
    # help='domain size (default: 4)',
    # default='4')

    return parser


def main():

    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    # algorithms = ['astar', 'pts', 'ptshhat', 'ptsnancy', 'bees', 'wastar']
    algorithms = ['pts', 'ptshhat', 'ptsnancywithdhat', 'bees-EpsGlobal']

    if len(args.algorithms) != 0:
        algorithms = args.algorithms

    resultDir = "tianyi_results"

    if args.boundType == "absolute":
        resultDir = "tianyi_results_absolute_bound"

    for algorithm in algorithms:

        fileDir = researchHome + "/boundedCostSearch/" + resultDir + "/" + \
            args.domain+"/"+args.subdomain+"/"+algorithm+"/"

        if not os.path.exists(fileDir):
            print("not found, skip ", algorithm)
            continue

        print("processing ", algorithm)
        for fileName in os.listdir(fileDir):

            # print("processing ", fileName)
            if fileName[-5:] != ".json":
                continue

            with in_place.InPlace(fileDir+fileName) as file:
                for line in file:
                    match = [m.start() for m in re.finditer(r'}', line)]
                    if len(match) > 1 or line[-1]!='}':
                        file.write(line[:(match[0]+1)])
                    else:
                        file.write(line)


if __name__ == '__main__':
    main()
