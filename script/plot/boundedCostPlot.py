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


class BaselineConfigure:
    def __init__(self):
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
                             # "regular": {"ptsnancywithdhat": "XES"},
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
                         "vacuumworld":
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

    def getBaseline(self):
        return self.baseline

    def getFixedBaseline(self):
        return self.fixedbaseline


class Configure:
    def __init__(self):

        self.algorithms = OrderedDict(
            {
                "pts": "PTS",
                # "ptshhat": "PTS-h^",
                # "ptsnancy": "expected work - 0 f",
                # "bees-EpsGlobal": "BEES",
                "ptsnancywithdhat": "XES",
                "ptsnancywithdhat-withEPSLimitBug": "XES-LBUG",
                # "bees": "BEES - EpsLocal",
                # "astar-with-bound": "A*",
                # "bees95": "BEES95",
                # "bees95-withEPSLimitBug": "BEES95-LBUG",
                # "ptsnancywithdhatandbf": "XES-bf",
                "ptsnancywithdhat-olv": "XES-OV-SI",
                # "ptsnancywithdhat-olv-withEPSLimitBug": "XES-OV-SI-LBUG",
                # "ptsnancyonlyprob-olv": "PTS-OV-SI",
                # "bees95-olv": "BEES95-OV-SI",
                "bees95-olv-withEPSLimitBug": "BEES95-OV-SI-LBUG",
                # "ptsnancywithdhat-olv-no-soft-error": "XES-OV",
                # "ptsnancyonlyprob-olv-no-soft-error": "PTS-OV",
                # "bees-95-olv-no-soft-error": "BEES95-OV",
            }
        )

        self.algorithmPalette = {
            "PTS": "royalblue",
            # "PTS-h^": "orangered",
            # "ptsnancy": "expected work - 0 f",
            # "BEES": "limegreen",
            "XES": "magenta",
            "XES-LBUG": "maroon",
            # "BEES95": "tan",
            # "BEES95-LBUG": "darkgreen",
            # "XES-bf": "darkgreen",
            # "XES-OV": "maroon",
            # "PTS-OV": "deepskyblue",
            # "BEES95-OV": "gold",
            "XES-OV-SI": "grey",
            # "XES-OV-SI-LBUG": "yellowgreen",
            # "PTS-OV-SI": "yellowgreen",
            # "BEES95-OV-SI": "mediumblue",
            "BEES95-OV-SI-LBUG": "yellowgreen",
        }

        self.showname = {"nodeGen": "Total Nodes Generated",
                         "nodeExp": "Total Nodes expanded",
                         "nodeGenDiff": "Algorithm Node Generated /  baseline Node Generated",
                         "fixedbaseline":
                         "log10 (Algorithm Node Generated /  baseline Node Generated)",
                         "cpu": "Raw CPU Time",
                         "solved": "Number of Solved Instances (Total=totalInstance)",
                         "boundValues": {"absolute": "Cost Bound",
                                         "wrtOpt": "Cost Bound w.r.t Optimal"}
                         }

        self.totalInstance = {"tile": "100", "pancake": "100",
                              "racetrack": "25", "vacuumworld": "60"}

        self.domainBoundsConfig = {"absoluteBoundsLimit":
                                   {"tile": {"uniform": {"lower": 40, "upper": 300},
                                             "heavy": {"lower": 700, "upper": 6000},
                                             "heavy-easy": {"lower": 300, "upper": 6000},
                                             "inverse": {"lower": 20, "upper": 600},
                                             "inverse-easy": {"lower": 20, "upper": 600},
                                             "reverse": {"lower": 300, "upper": 6000},
                                             "reverse-easy": {"lower": 300, "upper": 6000},
                                             "sqrt": {"lower": 140, "upper": 1000},
                                             },
                                    "vacuumworld": {"uniform": {"lower": 40, "upper": 300},
                                                    "heavy": {"lower": 700, "upper": 6000},
                                                    "heavy-easy": {"lower": 700, "upper": 6000},
                                                    },
                                    "pancake": {"regular": {"lower": 40, "upper": 300},
                                                "heavy": {"lower": 700, "upper": 6000}
                                                },
                                    "racetrack": {"barto-bigger": {"lower": 40, "upper": 300},
                                                  "hansen-bigger": {"lower": 700, "upper": 6000}
                                                  },
                                    },
                                   "avaiableBoundPercent":
                                   {"tile": [60, 80, 100, 120, 140, 160, 180,
                                             200, 220, 240, 260, 280,
                                             300, 400, 500, 600, 800, 1000, 1300, 2000, 3000],
                                    "vacuumworld": [60, 80, 100, 110, 120, 130, 140, 150,
                                                    160, 170, 180, 190,
                                                    200, 240, 280, 300, 340, 380, 400, 500, 600],
                                    "pancake": [60, 80, 100, 110, 120, 130, 140, 150,
                                                160, 170, 180, 190,
                                                200, 240, 280, 300, 340, 380, 400, 500, 600],
                                    "racetrack": [60, 80, 100, 110, 120, 130, 140, 150,
                                                  160, 170, 180, 190,
                                                  200, 240, 280, 300, 340, 380, 400, 500, 600],
                                    },
                                   "avaiableAbsoluteBounds":
                                   {"tile": {"uniform": [40, 60, 80, 100, 120, 140, 160, 180,
                                                         200, 220, 240, 260, 280, 300, 600, 900],
                                             "heavy": [300, 400, 500, 600, 700, 800, 900,
                                                       1000, 2000, 3000, 4000, 5000, 6000],
                                             "reverse": [300, 400, 500, 600, 700, 800, 900,
                                                         1000, 2000, 3000, 4000, 5000, 6000],
                                             "sqrt": [280, 300, 350, 400, 450, 500, 600,
                                                      700, 800, 900, 1000],

                                             },
                                    "vacuumworld": {"uniform": [],
                                                    "heavy": [],
                                                    "heavy-easy": [],
                                                    },
                                    "pancake": {"regular": [],
                                                "heavy": [],
                                                },
                                    "racetrack": {"barto-bigger": [],
                                                  "hansen-bigger": [],
                                                  },

                                    }
                                   }

        self.additionalAlgorithms = {"tile":
                                     {
                                         # "uniform": { "wastar-with-bound": "WA*"},
                                         # "uniform": {"wastar": "WA*"},
                                         "uniform": {},
                                         # "uniform": {"ptsnancywithdhat": "XES",
                                         # "bees": "BEES - EpsLocal",
                                         # },
                                         # "uniform": {"ptsnancywithdhat": "XES",
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
                                         # "heavy": {"ptsnancywithdhat": "XES"}
                                         # "heavy": {"wastar-with-bound": "WA*"}
                                         #  "ptsnancy-if0thenverysmall": "expected work - no 0 op",
                                         # "ptsnancy-if001thenfhat": "expected work - 0 fhat",
                                         # "ptsnancyonlyprob": "1/p(n)",
                                         # "ptsnancyonlyeffort": "t(n)"
                                         "heavy-easy": {},
                                         "inverse": {},
                                         "inverse-easy": {},
                                         "reverse": {},
                                         "reverse-easy": {},
                                         "sqrt": {},
                                     },
                                     "pancake":
                                     {
                                         # "regular": {"wastar": "WA*"},
                                         "regular": {},
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
                                     "vacuumworld":
                                     {
                                         "uniform": {},
                                         # "uniform": {"ptsnancywithdhat": "XES"},
                                         # "uniform": {"wastar": "WA*"},
                                         # "heavy": {"wastar": "WA*"}
                                         "heavy": {},
                                         # "heavy": {"ptsnancy-if0thenverysmall": \
                                         # "expected work - no 0 op"}
                                         "heavy-easy": {},
                                     },
                                     "racetrack":
                                     {
                                         "barto-big": {
                                             # "ptsnancy-if0thenverysmall":
                                             # "expected work - no 0 op",
                                             # "ptsnancyonlyprob": "1/p(n)",
                                             # "ptsnancyonlyeffort": "t(n)"
                                         },
                                         "barto-bigger": {},
                                         "hansen-bigger": {
                                             # "ptsnancy-if0thenverysmall": \
                                             # "expected work - no 0 op"
                                         },
                                         "uniform-small": {
                                             # "ptsnancy-if0thenverysmall": \
                                             # "expected work - no 0 op"
                                         },
                                         # "uniform": {}
                                         "uniform": {
                                             # "ptsnancywithdhat": "XES"
                                         },
                                     }
                                     }

    def getAlgorithms(self, removeAlgorithm):
        if removeAlgorithm != "NA" and (removeAlgorithm in self.algorithms):
            self.algorithms.pop(removeAlgorithm)
        return self.algorithms

    def getShowname(self):
        return self.showname

    def getTotalInstance(self):
        return self.totalInstance

    def getDomainBoundsConfig(self):
        return self.domainBoundsConfig

    def getAdditionalAlgorithms(self):
        return self.additionalAlgorithms

    def getAlgorithmColor(self):
        return self.algorithmPalette


def parseArugments():

    parser = argparse.ArgumentParser(description='boundedCostPlot')

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
        help='subdomain: tile: uniform(default), heavy, inverse; \
        pancake: regular, heavy; \
        racetrack : barto-big,uniform-small, barto-bigger, hanse-bigger-double;\
        vacuumworld: uniform, heavy',
        default='uniform')

    parser.add_argument(
        '-b',
        action='store',
        dest='boundPercentStart',
        help='bound percent start: anything above 0.6,(default: 0.6)',
        default='0.6')

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
                         nodeGenDiff, fixedbaseline, part10',
        default='nodeGen')

    parser.add_argument(
        '-bt',
        action='store',
        dest='boundType',
        help='bound type: absolute, wrtOpt(default)',
        default='wrtOpt')

    parser.add_argument(
        '-ot',
        action='store',
        dest='outTime',
        help='time in outfile name (default NA, use now())',
        default='NA')

    parser.add_argument(
        '-os',
        action='store',
        dest='outSuffix',
        help='suffix in outfile name (default NA)',
        default='NA')

    parser.add_argument(
        '-r',
        action='store',
        dest='removeAlgorithm',
        help='remove (omit) algorithm (default NA)',
        default='NA')

    return parser

#_ = totalInstance


def makeLinePlot(xAxis, yAxis, dataframe, hue,
                 xLabel, yLabel, _, outputName, colorDict,
                 showSolvedInstance=True, useLogScale=True):
    sns.set(rc={
        'figure.figsize': (13, 10),
        'font.size': 27,
        'text.color': 'black'
    })

    mean_df = dataframe.groupby(hue).mean().reset_index()
    mean_df=mean_df.sort_values(by=[yAxis], ascending=False)
    hue_order_list=mean_df[hue]

    ax = sns.lineplot(x=xAxis,
                      y=yAxis,
                      hue=hue,
                      hue_order=hue_order_list,
                      style=hue,
                      palette=colorDict,
                      data=dataframe,
                      err_style="bars",
                      # estimator=gmean,
                      # ci=None,
                      dashes=False
                      )

    ax.tick_params(colors='black', labelsize=24)

    if showSolvedInstance:
        ax.legend().texts[0].set_text(
            'Solved:' + str(len(dataframe['instance'].unique())))
    if useLogScale:
        ax.set_yscale("log")

    plt.ylabel(yLabel, color='black', fontsize=26)
    plt.xlabel(xLabel, color='black', fontsize=26)
    plt.setp(ax.get_legend().get_texts(), fontsize='26')  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='26')  # for legend title

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


def allSolvedDf(rawdf):
    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["boundValues"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    algorithms = rawdf["Algorithm"].unique()

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

    boundValues = rawdf["boundValues"].unique()
    boundValues.sort()
    for boundV in boundValues:
        print("bound percent ", boundV, "valid instances: ", len(
            df[df["boundValues"] == boundV]["instance"].unique()))

    return df


def makePar10Df(rawdf, totalInstance):

    par10Algorithm = []
    par10BoundValue = []
    par10Cpu = []
    par10Instance = []
    par10NodeExpanded = []
    par10NodeGenerated = []

    boundValues = rawdf["boundValues"].unique()
    boundValues.sort()
    algorithms = rawdf["Algorithm"].unique()

    maxCPU = rawdf["cpu"].max()
    maxNodeGen = rawdf["nodeGen"].max()
    maxNodeExp = rawdf["nodeExp"].max()
    for alg in algorithms:
        for boundV in boundValues:
            dfins = rawdf[(rawdf["Algorithm"] == alg) &
                          (rawdf["boundValues"] == boundV)]
            numberUnsolved = int(totalInstance) - len(dfins)
            if numberUnsolved > 0:
                for i in range(numberUnsolved):
                    par10Instance.append("par10-"+str(i))
                    par10Algorithm.append(alg)
                    par10BoundValue.append(boundV)
                    par10Cpu.append(maxCPU*10)
                    par10NodeGenerated.append(maxNodeGen*10)
                    par10NodeExpanded.append(maxNodeExp*10)

    par10df = pd.DataFrame({
        "Algorithm": par10Algorithm,
        "instance": par10Instance,
        "boundValues": par10BoundValue,
        "nodeGen": par10NodeGenerated,
        "nodeExp": par10NodeExpanded,
        "cpu": par10Cpu,
    })

    df = pd.DataFrame()
    df["Algorithm"] = np.nan
    df["instance"] = np.nan
    df["boundValues"] = np.nan
    df["nodeGen"] = np.nan
    df["nodeExp"] = np.nan
    df["cpu"] = np.nan

    df = df.append(rawdf)
    df = df.append(par10df)

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


def readData(args, algorithms, domainBoundsConfig):
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

    inPath = "../../../" + resultDir + "/" + \
        domainDir + "/" + subdomainType + '/alg'

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

            lowerBound = \
                domainBoundsConfig["absoluteBoundsLimit"][args.domain][args.subdomain]["lower"]
            upperBound = \
                domainBoundsConfig["absoluteBoundsLimit"][args.domain][args.subdomain]["upper"]
            allAvailableBoundValue = []
            # allAvailableBoundValue = \
                # domainBoundsConfig["avaiableAbsoluteBounds"][args.domain][args.subdomain]

            if args.boundType == "wrtOpt":
                boundV = boundV / 100
                lowerBound = float(args.boundPercentStart)
                upperBound = float(args.boundPercentEnd)
                allAvailableBoundValue = domainBoundsConfig["avaiableBoundPercent"][args.domain]

            if(boundV < lowerBound or
               boundV > upperBound or
               (boundV*100 not in allAvailableBoundValue)):
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
            boundSolved[str(float(cbound))].append(
                str(len(dfins))+"/"+totalInstance)

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


def makeCoveragePlot(df, args, totalInstance, showname, colorDict):
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
                 createOutFilePrefix(args) + args.plotType+".jpg", colorDict,
                 showSolvedInstance=False, useLogScale=False)


def createOutFilePrefix(args):

    nowstr = datetime.now().strftime("%d%m%Y-%H%M%S")

    outDirectory = "../../../tianyi_plots/" + args.domain

    if args.outTime != 'NA':
        outDirectory = "../../../tianyi_plots/" + args.outTime + "/" + args.domain

    if not os.path.exists(outDirectory):
        os.makedirs(outDirectory, exist_ok=True)

    outFilePrefix = outDirectory + '/' + args.domain + "-" + \
        args.subdomain + "-" + args.boundType + "-"

    if args.domain == 'pancake':
        outFilePrefix += args.size + "-"

    if args.outTime == 'NA':
        outFilePrefix += nowstr + "-"

    if args.outSuffix != 'NA':
        outFilePrefix += args.outSuffix + "-"

    if args.removeAlgorithm != 'NA':
        outFilePrefix += "no-"+args.removeAlgorithm + "-"

    return outFilePrefix


def plotting(args, config, baselineConfig):
    print("building plots...")

    algorithms = config.getAlgorithms(args.removeAlgorithm)
    algorithms.update(config.getAdditionalAlgorithms()
                      [args.domain][args.subdomain])

    showname = config.getShowname()
    totalInstance = config.getTotalInstance()

    rawdf = readData(args, algorithms, config.getDomainBoundsConfig())

    if args.plotType == "coveragetb":
        makeCoverageTable(rawdf, args, totalInstance[args.domain])
    elif args.plotType == "coverageplt":
        makeCoveragePlot(rawdf, args, totalInstance[args.domain],
                         showname, config.getAlgorithmColor())
    elif args.plotType == "nodeGenDiff":

        cureBaseline = baselineConfig.getBaseline()[
            args.domain][args.subdomain]
        baseline = next(iter(cureBaseline.values()))

        df = makePairWiseDf(rawdf, baseline, algorithms)

        makeLinePlot("boundValues", args.plotType, df, "Algorithm",
                     showname["boundValues"][args.boundType],
                     # "Cost Bound w.r.t. Suboptimal(w=3)",
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg",
                     config.getAlgorithmColor())

    elif args.plotType == "fixedbaseline":

        fixedbaseline = baselineConfig.getFixedBaseline()[
            args.domain][args.subdomain]
        baseline = next(iter(fixedbaseline.values()))

        df = makeFixedbaselineDf(rawdf, fixedbaseline, algorithms, args)

        makeLinePlot("boundValues", args.plotType, df, "Algorithm",
                     showname["boundValues"][args.boundType],
                     showname[args.plotType].replace(
                         "baseline", baseline), totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg",
                     config.getAlgorithmColor())

    elif args.plotType == "par10":

        df = makePar10Df(rawdf, totalInstance[args.domain])

        makeLinePlot("boundValues", "cpu", df, "Algorithm",
                     showname["boundValues"][args.boundType],
                     "Par10 CPU Time", totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg",
                     config.getAlgorithmColor(), showSolvedInstance=False)

    else:
        df = allSolvedDf(rawdf)
        makeLinePlot("boundValues", args.plotType, df, "Algorithm",
                     showname["boundValues"][args.boundType], showname[args.plotType],
                     totalInstance[args.domain],
                     createOutFilePrefix(args) + args.plotType+".jpg",
                     config.getAlgorithmColor())


def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    plotting(args, Configure(), BaselineConfigure())


if __name__ == '__main__':
    main()
