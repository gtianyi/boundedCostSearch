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
import in_place

researchHome = "/home/aifs1/gu/phd/research/workingPaper"


def parseArugments():

    parser = argparse.ArgumentParser(description='fixJson')

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

    parser.add_argument(
        '-a',
        action='append',
        dest='algorithms',
        help='algorithms: wastar, astar, pts, ptshhat, ptsnancy, bees default(all)',
        default=[])

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

    algorithms = ['astar', 'pts', 'ptshhat', 'ptsnancy', 'bees', 'wastar']

    if len(args.algorithms) != 0:
        algorithms = args.algorithms

    for algorithm in algorithms:

        fileDir = researchHome + "/boundedCostSearch/tianyi_results/" + \
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
                    if line[-2] == '}':
                        file.write(line[:-1])
                    elif line[-3] == '}':
                        file.write(line[:-2])
                    elif line[-4] == '}':
                        file.write(line[:-3])
                    elif line[-5] == '}':
                        file.write(line[:-4])
                    else:
                        file.write(line)


if __name__ == '__main__':
    main()
