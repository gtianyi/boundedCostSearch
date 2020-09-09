#pragma once
#include <iostream>

using namespace std;

struct ResultContainer
{
    bool   solutionFound;
    double solutionCost;
    int    nodesGenerated;
    int    nodesExpanded;
    double totalCpuTime;

    ResultContainer()
    {
        solutionFound  = false;
        solutionCost   = -1;
        nodesGenerated = 0;
        nodesExpanded  = 0;
        totalCpuTime   = 0;
    }

    ResultContainer(const ResultContainer& res)
    {
        solutionFound  = res.solutionFound;
        solutionCost   = res.solutionCost;
        nodesGenerated = res.nodesGenerated;
        nodesExpanded  = res.nodesExpanded;
        totalCpuTime   = res.totalCpuTime;
    }

    ResultContainer& operator=(const ResultContainer& rhs)
    {
        if (&rhs == this)
            return *this;
        else {
            solutionFound  = rhs.solutionFound;
            solutionCost   = rhs.solutionCost;
            nodesGenerated = rhs.nodesGenerated;
            nodesExpanded  = rhs.nodesExpanded;
            totalCpuTime   = rhs.totalCpuTime;
            return *this;
        }
    }
};
