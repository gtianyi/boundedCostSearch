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
# from scipy.stats import gmean
import math

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
                # "ptsnancy": "expected work - 0 f",
                "bees-EpsGlobal": "BEES",
                "ptsnancywithdhat": "expected work - dhat",
                # "bees": "BEES - EpsLocal",
                # "astar-with-bound": "A*",
            }
        )

        self.baseline = {"tile":
                         {
                             "uniform": {"astar": "A*"},
                             # "uniform": { "wastar-with-bound": "WA*" },
                             # "uniform": { "bees-EpsGlobal": "BEES" },
                             # "uniform": { "wastar": "WA*"},
                             "heavy": {"wastar-with-bound": "WA*"}
                         },
                         "pancake":
                         {
                             # "regular": {"ptsnancywithdhat": "expected work - dhat"},
                             "regular": {"wastar": "WA*"},
                             "heavy": {"bees-EpsGlobal": "BEES"}
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
                                  # "uniform": {"astar": "A*"},
                                  "uniform": {"wastar": "WA*"},
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

        self.showname = {"nodeGen": "Total Nodes Generated",
                         "nodeExp": "Total Nodes expanded",
                         "nodeGenDiff": "Algorithm Node Generated /  baseline Node Generated",
                         "fixedbaseline":
                         "log10 (Algorithm Node Generated /  baseline Node Generated)",
                         "cpu": "Raw CPU Time",
                         "solved": "Number of Solved Instances (Total=totalInstance)",
                         "boundValues":{"absolute":"Cost Bound",
                                        "wrtOpt":"Cost Bound w.r.t Optimal"}
                         }

        self.totalInstance = {"tile": "100", "pancake": "100",
                              "racetrack": "25", "vaccumworld": "60"}

        self.absoluteBoundsLimit = {"tile":{"uniform": {"lower":40, "upper":300},
                                            "heavy": {"lower":700, "upper":6000},
                                            "heavy-easy": {"lower":300, "upper":6000}
                                            }
                                   }

        self.additionalAlgorithms = {"tile":
                                     {
                                         # "uniform": { "wastar-with-bound": "WA*"},
                                         # "uniform": {"wastar": "WA*"},
                                         "uniform": {},
                                         # "uniform": {"ptsnancywithdhat": "expected work - dhat",
                                         # "bees": "BEES - EpsLocal",
                                         # },
                                         # "uniform": {"ptsnancywithdhat": "expected work - dhat",
                                         # "ptsnancyonlyeffort": "t(n)",
                                         # "ptsnancyonlyeffort-dhat": "t(n)-dhat"},
                                         # "uniform": {"wastar-with-bound": "WA*-with-bound",
                                         # "ptsnancy-if0thenverysmall": "expected work - no 0 op"},
                                         # "uniform": {"ptsnancy-if0thenverysmall": \
                                         # "expected work - no 0 op",
                                         # "ptsnancy-if001thenfhat": "expected work - 0 fhat",
                                         # "ptsnancyonlyprob": "1/p(n)",
                                         # "ptsnancyonlyeffort": "t(n)"},
                                         "heavy": {},
                                         # "heavy": {"ptsnancywithdhat": "expected work - dhat"}
                                         # "heavy": {"wastar-with-bound": "WA*"}
                                         #  "ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                         # "ptsnancy-if001thenfhat": "expected work - 0 fhat",
                                         # "ptsnancyonlyprob": "1/p(n)",
                                         # "ptsnancyonlyeffort": "t(n)"
                                         "heavy-easy": {}
                                     },
                                     "pancake":
                                     {
                                         "regular": {"wastar": "WA*"},
                                         # "regular": {},
                                         # "heavy": {"wastar": "WA*"},
                                         "heavy": {},
                                         # "regular": {"astar-with-bound": "A*-with-bound"},
                                         # "regular": {"ptsnancy-if0thenverysmall": \
                                         # "expected work - no 0 op"},
                                         # "heavy": {"wastar": "WA*"}
                                         # "heavy": {"ptsnancy-if0thenverysmall": \
                                         # "expected work - no 0 op"}
                                         # "heavy": {"ptsnancyonlyprob": "1/p(n)",
                                         # "ptsnancyonlyeffort": "t(n)"}


                                     },
                                     "vaccumworld":
                                     {
                                         # "uniform": {},
                                         "uniform": {"ptsnancywithdhat": "expected work - dhat"},
                                         # "uniform": {"wastar": "WA*"},
                                         # "heavy": {"wastar": "WA*"}
                                         "heavy": {"ptsnancy-if0thenverysmall": \
                                                   "expected work - no 0 op"}
                                     },
                                     "racetrack":
                                     {
                                         "barto-big": {
                                             "ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                             "ptsnancyonlyprob": "1/p(n)",
                                             "ptsnancyonlyeffort": "t(n)"
                                         },
                                         "barto-bigger": {},
                                         "hansen-bigger": {"ptsnancy-if0thenverysmall": \
                                                           "expected work - no 0 op"},
                                         "uniform-small": {"ptsnancy-if0thenverysmall": \
                                                           "expected work - no 0 op"},
                                         # "uniform": {}
                                         "uniform": {"ptsnancywithdhat": "expected work - dhat"},
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

    def getAbsoluteBoundLimits(self):
        return self.absoluteBoundsLimit

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
        help='bound percent start: anything above 0.6,(default: 1)',
        default='1')

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
        help='plot type, nodeGen(default), cpu, coveragetb, coverageplt, \
                         nodeGenDiff, fixedbaseline',
        default='nodeGen')

    parser.add_argument(
        '-bt',
        action='store',
        dest='boundType',
        help='bound type: absolute, wrtOpt(default)',
        default='wrtOpt')

    return parser

# _ = totalInstance


def makeLinePlot(xAxis, yAxis, dataframe, hue,
                 xLabel, yLabel, _, outputName):
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
                      err_style="bars",
                      # estimator=gmean,
                      # ci=None,
                      dashes=False
                      )

    ax.tick_params(colors='black', labelsize=12)
    # ax.legend().set_title('Solved/Total: ' +
    # str(len(dataframe['instance'].unique()))+'/'+totalInstance)
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
    df["boundValues"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    BaselineDf = rawdf[rawdf["Algorithm"] == baseline]

    # print("baseline data count, ", len(BaselineDf))

    for instance in BaselineDf["instance"].unique():
        dfins = rawdf[rawdf["instance"] == instance]
        # keep instances solved by all algorithms across all bounds
        if len(dfins) == len(algorithms) * len(BaselineDf["boundValues"].unique()):
            df = df.append(dfins)

    # for instance in BaselineDf["instance"].unique():
        # for boundP in BaselineDf["boundValues"].unique():
            # # print(instance, boundP)
            # dfins = rawdf[(rawdf["instance"] == instance) &
            # (rawdf["boundValues"] == boundP)]
            # if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
            # df = df.append(dfins)

    boundPercents = BaselineDf["boundValues"].unique()
    boundPercents.sort()
    for boundP in boundPercents:
        print("bound percent ", boundP, "valid instances: ", len(
            df[df["boundValues"] == boundP]["instance"].unique()), "baseline avg:",
            df[(df["boundValues"] == boundP) &
               (df["Algorithm"] == baseline)]["nodeGen"].mean())

    differenceNodeGen = []

    for rowdata in df.iterrows():
        row = rowdata[1]
        relateastar = df[(df["instance"] == row['instance']) &
                         (df["Algorithm"] == baseline) &
                         (df["boundValues"] == row['boundValues'])]
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


def allSolvedDf(rawdf, algorithms):
    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["boundValues"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    for instance in rawdf["instance"].unique():
        dfins = rawdf[rawdf["instance"] == instance]
        # keep instances solved by all algorithms across all bounds
        if len(dfins) == len(algorithms) * len(rawdf["boundValues"].unique()):
            df = df.append(dfins)

    # for instance in rawdf["instance"].unique():
        # for boundP in rawdf["boundValues"].unique():
            # # print(instance, boundP)
            # dfins = rawdf[(rawdf["instance"] == instance) &
                          # (rawdf["boundValues"] == boundP)]

            # if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
                # df = df.append(dfins)

    boundPercents = rawdf["boundValues"].unique()
    boundPercents.sort()
    for boundP in boundPercents:
        print("bound percent ", boundP, "valid instances: ", len(
            df[df["boundValues"] == boundP]["instance"].unique()))

    return df


def makeFixedbaselineDf(rawdf, fixedbaseline, algorithms, args):
    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["boundValues"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    bounds = rawdf["boundValues"].unique()
    BaselineDf = readFixedBaselineData(args, fixedbaseline)

    # print("baseline data count, ", len(BaselineDf))

    # for instance in BaselineDf["instance"].unique():
    # dfins = rawdf[rawdf["instance"] == instance]
    # # keep instances solved by all algorithms across all bounds
    # if len(dfins) == len(algorithms) * len(bounds):
    # df = df.append(dfins)

    for instance in rawdf["instance"].unique():
        for boundP in rawdf["boundValues"].unique():
            # print(instance, boundP)
            dfins = rawdf[(rawdf["instance"] == instance) &
                          (rawdf["boundValues"] == boundP)]
            if len(dfins) == len(algorithms):  # keep instances solved by all algorithms
                df = df.append(dfins)

    bounds.sort()
    for boundP in bounds:
        print("bound percent ", boundP, "valid instances: ", len(
            df[df["boundValues"] == boundP]["instance"].unique()),
            "valid baseline instance: ", len(BaselineDf["instance"]))

    differenceNodeGen = []

    for rowdata in df.iterrows():
        row = rowdata[1]
        relateastar = BaselineDf[BaselineDf["instance"] == row['instance']]
        if relateastar.empty:
            print("error! fixed baseline not found")
            differenceNodeGen.append(np.nan)
        else:
            diffNodeGen = row['nodeGen'] / relateastar['nodeGen']
            # print("row",row)
            # print("relateastar",relateastar)
            # compute geometric mean in plots
            diffNodeGen = math.log(diffNodeGen.values[0], 10)
            differenceNodeGen.append(diffNodeGen)

    df["fixedbaseline"] = differenceNodeGen

    return df


def readData(args, algorithms, absoluteBoundsLimit):
    domainSize = args.size
    domainType = args.domain
    subdomainType = args.subdomain

    algorithm = []
    boundValue = []
    cpu = []
    instance = []
    nodeExpanded = []
    nodeGenerated = []

    print("reading in data...")

    resultDir = "tianyi_results"
    if args.boundType == "absolute":
        resultDir = "tianyi_results_absolute_bound"

    domainDir = domainType

    inPath = "../../../" + resultDir + "/" + domainDir + "/" + subdomainType + '/alg'

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

            boundValueStr = numbersInFileName[0]
            boundV = int(boundValueStr)

            lowerBound = absoluteBoundsLimit[args.domain][args.subdomain]["lower"]
            upperBound = absoluteBoundsLimit[args.domain][args.subdomain]["upper"]

            if args.boundType == "wrtOpt":
                boundV = boundV / 100
                lowerBound = float(args.boundPercentStart)
                upperBound = float(args.boundPercentEnd)

            if(boundV < lowerBound or boundV > upperBound):
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
                boundValue.append(boundV)
                cpu.append(resultData["cpu time"])
                instance.append(resultData["instance"])
                nodeExpanded.append(resultData["node expanded"])
                nodeGenerated.append(resultData["node generated"])

    rawdf = pd.DataFrame({
        "Algorithm": algorithm,
        "instance": instance,
        "boundValues": boundValue,

        "nodeGen": nodeGenerated,
        "nodeExp": nodeExpanded,
        "cpu": cpu,
    })

    # print rawdf
    return rawdf


def readFixedBaselineData(args, fixedbaseline):

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

            algorithm.append(baseline)
            cpu.append(resultData["cpu time"])
            instance.append(resultData["instance"])
            nodeExpanded.append(resultData["node expanded"])
            nodeGenerated.append(resultData["node generated"])

            boundPercent.append(boundP/100)

    rawdf = pd.DataFrame({
        "Algorithm": algorithm,
        "instance": instance,
        "boundValues": boundPercent,

        "nodeGen": nodeGenerated,
        "nodeExp": nodeExpanded,
        "cpu": cpu,
    })

    return rawdf


def makeCoverageTable(df, args, totalInstance):
    out_file = createOutFilePrefix(args) + args.plotType+".jpg"

    algs = []

    boundSolved = {}

    boundStr = df["boundValues"].unique()
    bounds = [float(i) for i in boundStr]
    bounds.sort()

    for cbound in bounds:
        boundSolved[str(cbound)] = []

    for alg in df["Algorithm"].unique():

        algs.append(alg)

        for cbound in df["boundValues"].unique():
            dfins = df[(df["Algorithm"] == alg) & (
                df["boundValues"] == cbound)]
            boundSolved[str(float(cbound))].append(str(len(dfins))+"/"+totalInstance)

    data = {"Algorihtm": algs}
    data.update(boundSolved)

    nrows, ncols = len(algs)+1, len(bounds)
    hcell, wcell = 0.3, 1
    hpad, wpad = 0, 0
    fig = plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
    ax = fig.add_subplot(111)
    ax.axis('off')

    tabledf = pd.DataFrame(data)

    # ax = plt.subplot(frame_on=False)  # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, tabledf, loc='center')  # where tabledf is your data frame

    plt.savefig(out_file, dpi=200)


def makeCoveragePlot(df, args, totalInstance, showname):
    algs = []
    bound = []
    solved = []

    for alg in df["Algorithm"].unique():
        for cbound in df["boundValues"].unique():
            algs.append(alg)
            bound.append(cbound)
            dfins = df[(df["Algorithm"] == alg) & (
                df["boundValues"] == cbound)]
            solved.append(len(dfins))

    rawdf = pd.DataFrame({
        "Algorithm": algs,
        "boundValues": bound,
        "solved": solved
    })

    makeLinePlot("boundValues", "solved", rawdf, "Algorithm",
                 showname["boundValues"][args.boundType],
                 showname["solved"].replace(
                     "totalInstance", totalInstance), totalInstance,
                 createOutFilePrefix(args) + args.plotType+".jpg")


def createOutFilePrefix(args):

    nowstr = datetime.now().strftime("%d%m%Y-%H%M")

    outDirectory = "../../../tianyi_plots/" + args.domain

    if not os.path.exists(outDirectory):
        os.mkdir(outDirectory)

    outFilePrefix = outDirectory + '/' + args.domain + "-" + \
        args.subdomain + "-" + args.boundType + "-" +\
        args.size + '-' + nowstr

    return outFilePrefix


def plotting(args, config):
    print("building plots...")

    algorithms = config.getAlgorithms()
    algorithms.update(config.getAdditionalAlgorithms()
                      [args.domain][args.subdomain])

    showname = config.getShowname()
    totalInstance = config.getTotalInstance()

    rawdf = readData(args, algorithms, config.getAbsoluteBoundLimits())

    if args.plotType == "coveragetb":
        makeCoverageTable(rawdf, args, totalInstance[args.domain])
    elif args.plotType == "coverageplt":
        makeCoveragePlot(rawdf, args, totalInstance[args.domain], showname)
    elif args.plotType == "nodeGenDiff":

        cureBaseline = config.getBaseline()[args.domain][args.subdomain]
        baseline = next(iter(cureBaseline.values()))

        df = makePairWiseDf(rawdf, baseline, algorithms)

        makeLinePlot("boundValues", args.plotType, df, "Algorithm",
                     showname["boundValues"][args.boundType],
                     # "Cost Bound w.r.t. Suboptimal(w=3)",
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")

    elif args.plotType == "fixedbaseline":

        fixedbaseline = config.getFixedBaseline()[args.domain][args.subdomain]
        baseline = next(iter(fixedbaseline.values()))

        df = makeFixedbaselineDf(rawdf, fixedbaseline, algorithms, args)

        makeLinePlot("boundValues", args.plotType, df, "Algorithm",
                     showname["boundValues"][args.boundType],
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")

    else:
        df = allSolvedDf(rawdf, algorithms)
        makeLinePlot("boundValues", args.plotType, rawdf, "Algorithm",
                     showname["boundValues"][args.boundType], showname[args.plotType],
                     totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg")


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    plotting(args, Configure())


if __name__ == '__main__':
    main()
