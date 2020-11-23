#!/usr/bin/env python
'''
python3 script
python script code for decoding optimal solution json file

Author: Tianyi Gu
Date: 09/22/2020
'''

__author__ = 'TianyiGu'

import argparse
import json

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

    parser.add_argument('-i',
                        action='store',
                        dest='instance',
                        help='instance file name (default: 1-4x4.st)',
                        default='1-4x4.st')

    return parser


def main():
    parser = parseArugments()
    args = parser.parse_args()
    # print(args)

    solutionFile = researchHome+"/boundedCostSearch/optimalSolution/" +\
        args.domain+"."+args.subdomain

    if args.domain == "pancake":
        solutionFile += "."+args.size

    solutionFile += ".json"

    with open(solutionFile) as json_file:
        data = json.load(json_file)
        print(data[args.instance])

if __name__ == '__main__':
    main()
