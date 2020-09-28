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

import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import table
import numpy as np


def configure():

    algorithms = OrderedDict(
        {
            "pts": "PTS",
            "ptshhat": "PTS-h^",
            "ptsnancy": "expected work",
            "bees": "BEES",
            "beepsnancy": "BEEPS-expected work",
        }
    )

    baseline = {"tile":
                {
                    "uniform": {"astar": "A*"},
                    "heavy": {"ptshhat": "PTS-h^"}
                },
                "pancake":
                {
                    "16": {"astar": "A*"}
                }
                }

    algorithm_order = ['PTS', 'PTS-h^', 'expected work']

    showname = {"nodeGen": "Total Nodes Generated",
                "nodeExp": "Total Nodes expanded",
                "nodeGenDiff": "Algorithm Node Generated /  baseline Node Generated",
                "cpu": "Raw CPU Time"}

    return algorithms, algorithm_order, showname, baseline


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
        help='plot type, nodeGen(default), cpu, coverage, nodeGenDiff',
        default='nodeGen')

    return parser


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
                      data=dataframe
                      # data=dataframe,
                      # err_style="bars"
                      )

    ax.tick_params(colors='black', labelsize=12)
    ax.set_yscale("log")
    plt.ylabel(yLabel, color='black', fontsize=18)
    plt.xlabel(xLabel, color='black', fontsize=18)

    plt.savefig(outputName, bbox_inches="tight", pad_inches=0)
    plt.savefig(outputName.replace(".jpg", ".eps"),
                bbox_inches="tight", pad_inches=0)
    plt.close()
    plt.clf()
    plt.cla()


def makePairWiseDf(rawdf, baseline, algorithms):
    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["Cost Bound w.r.t. Optimal"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    BaselineDf = rawdf[rawdf["Algorithm"] == baseline]

    # print("baseline data count, ", len(BaselineDf))
    for instance in BaselineDf["instance"].unique():
        for boundP in BaselineDf["Cost Bound w.r.t. Optimal"].unique():
            # print(instance, boundP)
            dfins = rawdf[(rawdf["instance"] == instance) &
                          (rawdf["Cost Bound w.r.t. Optimal"] == boundP)]
            if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
                df = df.append(dfins)

    differenceNodeGen = []

    for rowdata in df.iterrows():
        row = rowdata[1]
        relateastar = df[(df["instance"] == row['instance']) &
                         (df["Algorithm"] == baseline) &
                         (df["Cost Bound w.r.t. Optimal"] == row['Cost Bound w.r.t. Optimal'])]
        if relateastar.empty:
            print("error! baseline not found")
            differenceNodeGen.append(np.nan)
        else:
            diffNodeGen = row['nodeGen'] / relateastar['nodeGen']
            # print("row",row)
            # print("relateastar",relateastar)
            diffNodeGen = diffNodeGen.values[0]
            differenceNodeGen.append(diffNodeGen)

    df["nodeGenDiff"] = differenceNodeGen

    return df


def readData(args, algorithms):
    domainSize = args.size
    domainType = args.domain
    subdomainType = args.subdomain

    algorithm = []
    boundPercent = []
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

            numbersInFileName = re.findall(r'\d+', jsonFile)
            sizeStr = numbersInFileName[1]

            if sizeStr != domainSize:
                continue

            boundPercentStr = numbersInFileName[0]
            boundP = int(boundPercentStr)

            with open(inPath_alg + "/" + jsonFile) as json_data:

                print("reading ", alg, jsonFile)
                resultData = json.load(json_data)

                algorithm.append(algorithms[resultData["algorithm"]])
                boundPercent.append(boundP/100)
                cpu.append(resultData["cpu time"])
                instance.append(resultData["instance"])
                nodeExpanded.append(resultData["node expanded"])
                nodeGenerated.append(resultData["node generated"])

    rawdf = pd.DataFrame({
        "Algorithm": algorithm,
        "instance": instance,
        "Cost Bound w.r.t. Optimal": boundPercent,

        "nodeGen": nodeGenerated,
        "nodeExp": nodeExpanded,
        "cpu": cpu,
    })

    # print rawdf
    return rawdf


def makeCoverageTable(algorithms):

    inPath = "../../../tianyi_results/"
    out_file = "../../../tianyi_plots/coverageSummary-" + \
        datetime.now().strftime("%d%m%Y-%H%M")+".jpg"

    domains = []
    subdomains = []
    algs = []
    # size=[]
    memOut = []
    total = []

    for domain in os.listdir(inPath):
        for subdomain in os.listdir(inPath+domain+"/"):
            for alg in os.listdir(inPath+domain+"/"+subdomain+"/"):
                if alg not in algorithms:
                    continue
                domains.append(domain)
                subdomains.append(subdomain)
                algs.append(algorithms[alg])

                allFiles = os.listdir(inPath+domain+"/"+subdomain+"/"+alg)

                outOfMem = [f for f in allFiles if f[-5:] != ".json"]

                total.append(len(allFiles))
                memOut.append(len(outOfMem))

                # index = jsonFile.find('size') + 5
                # sizeStr = jsonFile[index:]
                # indexEnd = sizeStr.find('-')
                # sizeStr = sizeStr[:indexEnd]

                # size.append(sizeStr)

    df = pd.DataFrame({
        "Domain": domains,
        "Subdomain": subdomains,
        "Algorithm": algs,
        # "Size": size,
        "Out of Memory": memOut,
        "Total": total
    })

    ax = plt.subplot(frame_on=False)  # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df, loc='upper right')  # where df is your data frame

    plt.savefig(out_file, dpi=200)


def plotting(args, algorithms, showname, baseline):
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

    if args.plotType == "coverage":
        makeCoverageTable(algorithms)
    elif args.plotType == "nodeGenDiff":
        rawdf = readData(args, algorithms)
        df = makePairWiseDf(rawdf, baseline, algorithms)
        makeLinePlot(width, height, "Cost Bound w.r.t. Optimal", args.plotType, df, "Algorithm",
                     "Cost Bound w.r.t. Optimal",
                     showname[args.plotType].replace("baseline", baseline),
                     out_file + args.plotType+".jpg")
    else:
        df = readData(args, algorithms)
        makeLinePlot(width, height, "Cost Bound w.r.t. Optimal", args.plotType, df, "Algorithm",
                     "Cost Bound w.r.t. Optimal", showname[args.plotType],
                     out_file + args.plotType+".jpg")


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    algorithms, _, showname, baseline = configure()

    curBaseline = baseline[args.domain][args.subdomain]

    algorithms.update(curBaseline)

    plotting(args, algorithms, showname, next(iter(curBaseline.values())))


if __name__ == '__main__':
    main()
