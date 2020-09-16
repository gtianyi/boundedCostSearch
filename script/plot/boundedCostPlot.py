#!/usr/bin/env python
'''
python3 script
plotting code for generate bounded cost search related plots

Author: Tianyi Gu
Date: 09/15/2020
'''

__author__ = 'TianyiGu'

import argparse
import json
import os
from collections import OrderedDict
# import sys
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def configure():

    algorithms = OrderedDict({"pts": "PTS", "ptshhat": "PTS-h^"})

    algorithm_order = ['PTS', 'PTS-h^']

    showname = {"nodeGen": "Total Nodes Generated",
                "nodeExp": "Total Nodes expanded",
                "cpu": "Raw CPU Time"}

    return algorithms, algorithm_order, showname


def makeLinePlot(width, height, xAxis, yAxis, dataframe, hue,
                 xLabel, yLabel, outputName):
    sns.set(rc={
        'figure.figsize': (width, height),
        'font.size': 27,
        'text.color': 'black'
    })

    ax = sns.lineplot(x=xAxis,
                      y=yAxis,
                      hue=hue,
                      style=hue,
                      palette="muted",
                      data=dataframe,
                      err_style="bars")

    ax.tick_params(colors='black', labelsize=12)
    ax.set_yscale("log")
    plt.ylabel(yLabel, color='black', fontsize=18)
    plt.xlabel(xLabel, color='black', fontsize=18)

    plt.savefig(outputName, bbox_inches="tight", pad_inches=0)
    # plt.savefig(outputName.replace(".eps", ".png"),
    # bbox_inches="tight",
    # pad_inches=0)
    plt.close()
    plt.clf()
    plt.cla()


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

    parser.add_argument(
        '-t',
        action='store',
        dest='plotType',
        help='plot type, nodeGen(default), cpu',
        default='nodeGen')

    return parser


def readData(args, algorithms):
    # domainSize = args.size
    domainType = args.domain
    subdomainType = args.subdomain

    algorithm = []
    bound = []
    cpu = []
    instance = []
    nodeExpanded = []
    nodeGenerated = []

    print("reading in data...")

    domainDir = domainType

    inPath = "../../../tianyi_results/" + domainDir + "/" + subdomainType + '/alg'

    for alg in algorithms:
        print("reading ", alg)
        inPath_alg = inPath.replace('alg', alg)
        for jsonFile in os.listdir(inPath_alg):
            if jsonFile[-5:] != ".json":
                continue

            with open(inPath_alg + "/" + jsonFile) as json_data:

                # print("reading ", jsonFile)
                resultData = json.load(json_data)

                algorithm.append(algorithms[resultData["algorithm"]])
                bound.append(resultData["bound"])
                cpu.append(resultData["cpu time"])
                instance.append(resultData["instance"])
                nodeExpanded.append(resultData["node expanded"])
                nodeGenerated.append(resultData["node generated"])

    df = pd.DataFrame({
        "Algorithm": algorithm,
        "instance": instance,
        "Cost Bound": bound,

        "nodeGen": nodeGenerated,
        "nodeExp": nodeExpanded,
        "cpu": cpu,
    })

    # print df
    return df


def plotting(args, df, showname):
    print("building plots...")

    domainSize = args.size
    domainType = args.domain
    subdomainType = args.subdomain

    nowstr = datetime.now().strftime("%d%m%Y-%H%M")

    out_dir = "../../../tianyi_plots/" + domainType

    width = 13
    height = 10

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_file = out_dir + '/' + domainType + "-" + \
        subdomainType + "-" + domainSize + '-' + nowstr

    makeLinePlot(width, height, "Cost Bound", args.plotType, df, "Algorithm",
                 "Cost Bound", showname[args.plotType], out_file + args.plotType+".jpg")


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    algorithms, _, showname = configure()

    df = readData(args, algorithms)

    plotting(args, df, showname)


if __name__ == '__main__':
    main()
