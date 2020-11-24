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


class Configure:
    def __init__(self):

        self.algorithms = OrderedDict(
            {
                "pts": "PTS",
                "ptshhat": "PTS-h^",
                "ptsnancy": "expected work - 0 f",
                "bees": "BEES",
                # "wastar": "WA*",
                # "astar": "A*",
            }
        )

        self.baseline = {"tile":
                         {
                             # "uniform": {"wastar-with-bound": "WA*-with-bound"},
                             "uniform": {"bees": "BEES"},
                             "heavy": {"bees": "BEES"}
                         },
                         "pancake":
                         {
                             "regular": {"bees": "BEES"},
                             "heavy": {"bees": "BEES"}
                             # "heavy": {"wastar": "WA*"}
                         },
                         "racetrack":
                         {
                             "barto-big": {"bees": "BEES"},
                             "barto-bigger": {"bees": "BEES"},
                             "hansen-bigger": {"bees": "BEES"},
                             "uniform-small": {"bees": "BEES"},
                             "uniform": {"bees": "BEES"}
                         },
                         "vaccumworld":
                         {
                             # "uniform": {"wastar": "WA*"},
                             "uniform": {"bees": "BEES"},
                             "heavy": {"bees": "BEES"}
                             # "heavy": {"wastar": "WA*"}
                         }
                         }

        self.fixedbaseline = {"tile":
                              {
                                  "uniform": {"astar": "WA*"},
                                  "heavy": {"wastar": "WA*"}
                              },
                              "pancake":
                              {
                                  "regular": {"astar": "A*"}
                              },
                              "racetrack":
                              {
                                  "barto-big": {"astar": "A*"},
                                  "barto-bigger": {"astar": "A*"},
                                  "hansen-bigger": {"astar": "A*"},
                                  "uniform-small": {"astar": "A*"},
                                  "uniform": {"astar": "A*"}
                              }
                              }

        self.algorithm_order = ['PTS', 'PTS-h^', 'expected work']

        self.showname = {"nodeGen": "Total Nodes Generated",
                         "nodeExp": "Total Nodes expanded",
                         "nodeGenDiff": "Algorithm Node Generated /  baseline Node Generated",
                         "fixedbaseline": "Algorithm Node Generated /  baseline Node Generated",
                         "cpu": "Raw CPU Time"}

        self.totalInstance = {"tile": "100", "pancake": "100",
                              "racetrack": "25", "vaccumworld": "60"}

        self.additionalAlgorithms = {"tile":
                                     {
                                         "uniform": {"ptsnancywithdhat":"expected work - dhat"},
                                         # "uniform": {"wastar-with-bound": "WA*-with-bound",
                                         # "ptsnancy-if0thenverysmall": "expected work - no 0 op"},
                                         # "uniform": {"ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                                     # "ptsnancy-if001thenfhat": "expected work - 0 fhat",
                                                     # "ptsnancyonlyprob": "1/p(n)",
                                                     # "ptsnancyonlyeffort": "t(n)"},
                                         # "heavy": {}
                                         "heavy": {"ptsnancywithdhat":"expected work - dhat"}
                                        #  "ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                                   # "ptsnancy-if001thenfhat": "expected work - 0 fhat",
                                                   # "ptsnancyonlyprob": "1/p(n)",
                                                   # "ptsnancyonlyeffort": "t(n)"
                                     },
                                     "pancake":
                                     {
                                         "regular": {"ptsnancywithdhat":"expected work - dhat"},
                                         "heavy": {"ptsnancywithdhat":"expected work - dhat"},
                                         # "regular": {"astar-with-bound": "A*-with-bound"},
                                         # "regular": {"ptsnancy-if0thenverysmall": "expected work - no 0 op"},
                                         # "heavy": {"wastar": "WA*"}
                                         # "heavy": {"ptsnancy-if0thenverysmall": "expected work - no 0 op"}
                                         # "heavy": {"ptsnancyonlyprob": "1/p(n)",
                                                   # "ptsnancyonlyeffort": "t(n)"}


                                     },
                                     "vaccumworld":
                                     {
                                         # "uniform": {},
                                         "uniform": {"ptsnancywithdhat":"expected work - dhat"},
                                         # "uniform": {"wastar": "WA*"},
                                         # "heavy": {"wastar": "WA*"}
                                         "heavy": {"ptsnancy-if0thenverysmall": "expected work - no 0 op"}
                                     },
                                     "racetrack":
                                     {
                                         "barto-big": {
                                             "ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                             "ptsnancyonlyprob": "1/p(n)",
                                             "ptsnancyonlyeffort": "t(n)"
                                         },
                                         "barto-bigger": {},
                                         "hansen-bigger": {"ptsnancy-if0thenverysmall": "expected work - no 0 op"},
                                         "uniform-small": {"ptsnancy-if0thenverysmall": "expected work - no 0 op"},
                                         # "uniform": {}
                                         "uniform": {"ptsnancywithdhat":"expected work - dhat"},
                                     }
                                     }

    def getAlgorithms(self):
        return self.algorithms

    def getBaseline(self):
        return self.baseline

    def getFixedBaseline(self):
        return self.fixedbaseline

    def getShowname(self):
        return self.showname

    def getTotalInstance(self):
        return self.totalInstance

    def getAdditionalAlgorithms(self):
        return self.additionalAlgorithms


def parseArugments():

    parser = argparse.ArgumentParser(description='boundedCostPlot')

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
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double;\
        vaccumworld: uniform, heavy',
        default='uniform')

    parser.add_argument(
        '-b',
        action='store',
        dest='boundPercentStart',
        help='bound percent start: anything above 0.6,(default: 1.2)',
        default='1.2')

    parser.add_argument(
        '-e',
        action='store',
        dest='boundPercentEnd',
        help='bound percent end: anything below 6, (default: 6)',
        default='6')

    parser.add_argument('-z',
                        action='store',
                        dest='size',
                        help='domain size (default: 4)',
                        default='4')

    parser.add_argument(
        '-t',
        action='store',
        dest='plotType',
        help='plot type, nodeGen, cpu, coverage, nodeGenDiff(default), fixedbaseline',
        default='nodeGenDiff')

    return parser


def makeLinePlot(xAxis, yAxis, dataframe, hue,
                 xLabel, yLabel, totalInstance, outputName):
    sns.set(rc={
        'figure.figsize': (13, 10),
        'font.size': 27,
        'text.color': 'black'
    })

    ax = sns.lineplot(x=xAxis,
                      y=yAxis,
                      hue=hue,
                      style=hue,
                      palette="muted",
                      data=dataframe,
                      # data=dataframe,
                      # err_style="bars"
                      dashes=False
                      )

    ax.tick_params(colors='black', labelsize=12)
    ax.legend().set_title('Solved/Total: ' +
                          str(len(dataframe['instance'].unique()))+'/'+totalInstance)
    ax.set_yscale("log")
    plt.ylabel(yLabel, color='black', fontsize=18)
    plt.xlabel(xLabel, color='black', fontsize=18)

    plt.savefig(outputName, bbox_inches="tight", pad_inches=0)
   #  plt.savefig(outputName.replace(".jpg", ".eps"),
    # bbox_inches="tight", pad_inches=0)
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
        dfins = rawdf[rawdf["instance"] == instance]
        # keep instances solved by all algorithms across all bounds
        if len(dfins) == len(algorithms) * len(BaselineDf["Cost Bound w.r.t. Optimal"].unique()):
            df = df.append(dfins)

    # for instance in BaselineDf["instance"].unique():
        # for boundP in BaselineDf["Cost Bound w.r.t. Optimal"].unique():
            # # print(instance, boundP)
            # dfins = rawdf[(rawdf["instance"] == instance) &
            # (rawdf["Cost Bound w.r.t. Optimal"] == boundP)]
            # if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
            # df = df.append(dfins)

    boundPercents = BaselineDf["Cost Bound w.r.t. Optimal"].unique()
    boundPercents.sort()
    for boundP in boundPercents:
        print("bound percent ", boundP, "valid instances: ", len(
            df[df["Cost Bound w.r.t. Optimal"] == boundP]["instance"].unique()), "baseline avg:",
            df[(df["Cost Bound w.r.t. Optimal"] == boundP) &
               (df["Algorithm"] == baseline)]["nodeGen"].mean())

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


def makeFixedbaselineDf(rawdf, fixedbaseline, algorithms, args):
    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["Cost Bound w.r.t. Optimal"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    bounds = rawdf["Cost Bound w.r.t. Optimal"].unique()
    BaselineDf = readFixedBaselineData(args, fixedbaseline, bounds)
    baseline = next(iter(fixedbaseline.values()))

    # print("baseline data count, ", len(BaselineDf))

    for instance in BaselineDf["instance"].unique():
        dfins = rawdf[rawdf["instance"] == instance]
        # keep instances solved by all algorithms across all bounds
        if len(dfins) == len(algorithms) * len(BaselineDf["Cost Bound w.r.t. Optimal"].unique()):
            df = df.append(dfins)

    df = df.append(BaselineDf)
    # for instance in BaselineDf["instance"].unique():
    # for boundP in BaselineDf["Cost Bound w.r.t. Optimal"].unique():
    # # print(instance, boundP)
    # dfins = rawdf[(rawdf["instance"] == instance) &
    # (rawdf["Cost Bound w.r.t. Optimal"] == boundP)]
    # if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
    # df = df.append(dfins)

    bounds.sort()
    for boundP in bounds:
        print("bound percent ", boundP, "valid instances: ", len(
            df[df["Cost Bound w.r.t. Optimal"] == boundP]["instance"].unique()), "baseline avg:",
            df[(df["Cost Bound w.r.t. Optimal"] == boundP) &
               (df["Algorithm"] == baseline)]["nodeGen"].mean())

    differenceNodeGen = []

    for rowdata in df.iterrows():
        row = rowdata[1]
        relateastar = df[(df["instance"] == row['instance']) &
                         (df["Algorithm"] == baseline) &
                         (df["Cost Bound w.r.t. Optimal"] == row['Cost Bound w.r.t. Optimal'])]
        if relateastar.empty:
            print("error! fixed baseline not found")
            differenceNodeGen.append(np.nan)
        else:
            diffNodeGen = row['nodeGen'] / relateastar['nodeGen']
            # print("row",row)
            # print("relateastar",relateastar)
            diffNodeGen = diffNodeGen.values[0]
            differenceNodeGen.append(diffNodeGen)

    df["fixedbaseline"] = differenceNodeGen

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

            if domainType == "pancake" and sizeStr != domainSize:
                continue

            boundPercentStr = numbersInFileName[0]
            boundP = int(boundPercentStr)

            if(boundP/100 < float(args.boundPercentStart) or
               boundP/100 > float(args.boundPercentEnd)):
                continue

            with open(inPath_alg + "/" + jsonFile) as json_data:

                # print("reading ", alg, jsonFile)
                resultData = json.load(json_data)
                # if alg == "ptsnancy":
                # if alg == "ptsnancy" and resultData["node generated"] > 1000:
                # print("reading ", alg, jsonFile, "generated: ",
                # resultData["node generated"])

                # if alg == "ptsnancy" and resultData["node generated"] > 1000:
                # continue

                algorithm.append(algorithms[alg])
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


def readFixedBaselineData(args, fixedbaseline, bounds):

    baseline = next(iter(fixedbaseline.values()))
    baseline_key = next(iter(fixedbaseline.keys()))

    algorithm = []
    boundPercent = []
    cpu = []
    instance = []
    nodeExpanded = []
    nodeGenerated = []

    print("reading in fixed baseline data...", fixedbaseline)

    inPath = "../../../tianyi_results/" + args.domain + "/" + args.subdomain + '/alg'

    inPath_alg = inPath.replace('alg', baseline_key)
    for jsonFile in os.listdir(inPath_alg):
        if jsonFile[-5:] != ".json":
            continue

        numbersInFileName = re.findall(r'\d+', jsonFile)
        sizeStr = numbersInFileName[1]

        if args.domain == "pancake" and sizeStr != args.size:
            continue

        boundPercentStr = numbersInFileName[0]
        boundP = int(boundPercentStr)

        # since fixed baseline is not changing with bound, we only have data for b=100
        if(boundP/100 != 1):
            continue

        with open(inPath_alg + "/" + jsonFile) as json_data:

            # print("reading ", alg, jsonFile)
            resultData = json.load(json_data)

            for bp in bounds:

                algorithm.append(baseline)
                cpu.append(resultData["cpu time"])
                instance.append(resultData["instance"])
                nodeExpanded.append(resultData["node expanded"])
                nodeGenerated.append(resultData["node generated"])

                boundPercent.append(bp)

    rawdf = pd.DataFrame({
        "Algorithm": algorithm,
        "instance": instance,
        "Cost Bound w.r.t. Optimal": boundPercent,

        "nodeGen": nodeGenerated,
        "nodeExp": nodeExpanded,
        "cpu": cpu,
    })

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


def createOutFilePrefix(args):

    nowstr = datetime.now().strftime("%d%m%Y-%H%M")

    outDirectory = "../../../tianyi_plots/" + args.domain

    if not os.path.exists(outDirectory):
        os.mkdir(outDirectory)

    outFilePrefix = outDirectory + '/' + args.domain + "-" + \
        args.subdomain + "-" + args.size + '-' + nowstr

    return outFilePrefix


def plotting(args, config):
    print("building plots...")

    algorithms = config.getAlgorithms()
    algorithms.update(config.getAdditionalAlgorithms()
                      [args.domain][args.subdomain])

    showname = config.getShowname()
    totalInstance = config.getTotalInstance()

    if args.plotType == "coverage":
        makeCoverageTable(algorithms)
    elif args.plotType == "nodeGenDiff":

        cureBaseline = config.getBaseline()[args.domain][args.subdomain]
        baseline = next(iter(cureBaseline.values()))

        rawdf = readData(args, algorithms)
        df = makePairWiseDf(rawdf, baseline, algorithms)

        makeLinePlot("Cost Bound w.r.t. Optimal", args.plotType, df, "Algorithm",
                     "Cost Bound w.r.t. Optimal",
                     # "Cost Bound w.r.t. Suboptimal(w=3)",
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")

    elif args.plotType == "fixedbaseline":

        fixedbaseline = config.getFixedBaseline()[args.domain][args.subdomain]
        baseline = next(iter(fixedbaseline.values()))

        rawdf = readData(args, algorithms)
        df = makeFixedbaselineDf(rawdf, fixedbaseline, algorithms, args)

        makeLinePlot("Cost Bound w.r.t. Optimal", args.plotType, df, "Algorithm",
                     "Cost Bound w.r.t. Optimal",
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")

    else:
        df = readData(args, algorithms)
        makeLinePlot("Cost Bound w.r.t. Optimal", args.plotType, df, "Algorithm",
                     "Cost Bound w.r.t. Optimal", showname[args.plotType], totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    plotting(args, Configure())


if __name__ == '__main__':
    main()
