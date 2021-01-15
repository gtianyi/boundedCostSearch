#!/usr/bin/env python
'''
python3 script
plotting config code for generate bounded cost search related plots

Author: Tianyi Gu
Date: 01/12/2021
'''

from collections import OrderedDict

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
                "ptshhat": r"$\widehat{\mathrm{PTS}}$",
                # "ptsnancy": "expected work - 0 f",
                # "bees-EpsGlobal-withEPSLimitBug": "BEES-LBUG",
                "bees-EpsGlobal": "BEES",
                "ptsnancywithdhat": "XES",
                # "ptsnancywithdhat-withEPSLimitBug": "XES-LBUG",
                # "ptsnancywithdhat-cplus05": "XES-cp05",
                # "ptsnancywithdhat-sp100": "XES-sp100",
                # "ptsnancywithdhat-cp05withsp100": "XES-c05s100",
                # "ptsnancywithdhat-cp05withsp100": "XES-c05s100",
                # "bees": "BEES - EpsLocal",
                # "astar-with-bound": "A*",
                "bees95": "BEES95",
                # "bees95-cplus05": "BEES95-cp05",
                # "bees95-sp100": "BEES95-sp100",
                # "bees95-cp05withsp100": "BEES95-c05s100",
                # "bees95-withEPSLimitBug": "BEES95-LBUG",
                # "ptsnancywithdhatandbf": "XES-bf",
                # "ptsnancywithdhat-olv": "XES-OV-SI",
                # "ptsnancywithdhat-olv-withEPSLimitBug": "XES-OV-SI-LBUG",
                # "ptsnancyonlyprob-olv": "PTS-OV-SI",
                # "bees95-olv": "BEES95-OV-SI",
                # "bees95-olv-withEPSLimitBug": "BEES95-OV-SI-LBUG",
                # "ptsnancywithdhat-olv-no-soft-error": "XES-OV",
                # "ptsnancyonlyprob-olv-no-soft-error": "PTS-OV",
                # "bees-95-olv-no-soft-error": "BEES95-OV",
            }
        )

        self.algorithmPalette = {
            "PTS": "royalblue",
            r"$\widehat{\mathrm{PTS}}$": "orangered",
            # "ptsnancy": "expected work - 0 f",
            "BEES": "limegreen",
            # "BEES-LBUG": "maroon",
            # "BEES - EpsLocal": "deepskyblue",
            "XES": "magenta",
            # "XES-LBUG": "maroon",
            # "XES-cp05": "maroon",
            # "XES-sp100": "maroon",
            # "XES-c05s100": "maroon",
            "BEES95": "tan",
            # "BEES95-LBUG": "darkgreen",
            # "BEES95-cp05": "darkgreen",
            # "BEES95-sp100": "darkgreen",
            # "BEES95-c05s100": "darkgreen",
            # "XES-bf": "darkgreen",
            # "XES-OV": "maroon",
            # "PTS-OV": "deepskyblue",
            # "BEES95-OV": "gold",
            # "XES-OV-SI": "grey",
            # "XES-OV-SI-LBUG": "yellowgreen",
            # "PTS-OV-SI": "yellowgreen",
            # "BEES95-OV-SI": "mediumblue",
            # "BEES95-OV-SI-LBUG": "yellowgreen",
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
                                                "heavy": {"lower": 700, "upper": 6000},
                                                "sumheavy": {"lower": 700, "upper": 6000},
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
                                                "sumheavy": [],
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
                                         "sumheavy": {},
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
