#pragma once
/*
  File: mst.h
  author: Tianyi Gu
  minimum spanning tree Class
*/
#ifndef MST_H
#define MST_H

#include <cmath>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

#include "DisjointSet.h"

using namespace std;

template<typename Location>
struct edge
{
    // default constructor
    edge(Location& l_, Location& r_, int w_)
        : left(l_)
        , right(r_)
        , weight(w_)
    {}

    bool operator!=(const edge& d) const
    {
        return left != d.left || right != d.right || weight != d.weight;
    }

    Location left;
    Location right;
    int      weight;
    bool     operator>(const edge& n) const { return weight < n.weight; }
    bool     operator<(const edge& n) const { return weight > n.weight; }
    bool     operator==(const edge& _node) const
    {
        if (left == _node.left && right == _node.right &&
            weight == _node.weight)
            return true;
        return false;
    }
    edge operator=(const edge& _node)
    {
        left   = _node.left;
        right  = _node.right;
        weight = _node.weight;
        return *this;
    }
};

template<typename Location>
int minimumSpanningTree(vector<Location>& nodeList)
{
    assert(nodeList.size() > 1);

    priority_queue<edge<Location>> edgeQueue;
    DisjointSet<Location>          djSet;
    // construct graph
    for (unsigned int i = 0; i < nodeList.size(); i++) {
        for (unsigned int j = 0; j < nodeList.size(); j++) {
            if (i <= j)
                continue;
            unsigned long d = max(nodeList[i].first, nodeList[j].first) -
                              min(nodeList[i].first, nodeList[j].first) +
                              max(nodeList[i].second, nodeList[j].second) -
                              min(nodeList[i].second, nodeList[j].second);
            edge<Location> e(nodeList[i], nodeList[j], static_cast<int>(d));
            edgeQueue.push(e);
            djSet.createSet(nodeList[i]);
            djSet.createSet(nodeList[j]);
        }
    }

    // Generate mst get hvalue
    int hvalue = 0;
    while (edgeQueue.size() > 0) {
        edge<Location> e = edgeQueue.top();
        edgeQueue.pop();
        if (djSet.findSet(e.left) != djSet.findSet(e.right)) {
            djSet.unionSets(e.left, e.right);
            hvalue += e.weight;
        }
    }
    return hvalue;
}

// last node is robot
template<typename Location>
int greedyTraversal(vector<Location>& nodeList)
{
    assert(nodeList.size() > 1);

    unsigned long cost = 0;

    auto cur = nodeList.back();
    nodeList.pop_back();

    while (!nodeList.empty()) {
        auto          bestIt   = nodeList.begin();
        unsigned long bestDist = std::numeric_limits<unsigned long>::max();

        for (auto it = nodeList.begin(); it != nodeList.end(); ++it) {
            unsigned long dist =
              max(it->first, cur.first) - min(it->first, cur.first) +
              max(it->second, cur.second) - min(it->second, cur.second);
            if (dist < bestDist) {
                bestDist = dist;
                bestIt   = it;
            }
        }

        cost += bestDist;
        cur = *bestIt;
        nodeList.erase(bestIt);
    }

    return static_cast<int>(cost);
}

template<typename Location>
int heavyMinimumSpanningTree(vector<Location>& nodeList,
                             unsigned int      currentWeight)
{
    assert(nodeList.size() > 1);

    priority_queue<edge<Location>> edgeQueue;
    DisjointSet<Location>          djSet;
    // construct graph
    for (unsigned int i = 0; i < nodeList.size(); i++) {
        for (unsigned int j = 0; j < nodeList.size(); j++) {
            if (i <= j)
                continue;
            unsigned long d = max(nodeList[i].first, nodeList[j].first) -
                              min(nodeList[i].first, nodeList[j].first) +
                              max(nodeList[i].second, nodeList[j].second) -
                              min(nodeList[i].second, nodeList[j].second);
            edge<Location> e(nodeList[i], nodeList[j], static_cast<int>(d));
            edgeQueue.push(e);
            djSet.createSet(nodeList[i]);
            djSet.createSet(nodeList[j]);
        }
    }
    auto cmp = [](edge<Location> left, edge<Location> right) {
        return left > right;
    };
    std::priority_queue<edge<Location>, std::vector<edge<Location>>,
                        decltype(cmp)>
      edgeQueueGreatestFirst(cmp);

    // Generate mst get hvalue
    while (edgeQueue.size() > 0) {
        edge<Location> e = edgeQueue.top();
        edgeQueue.pop();
        if (djSet.findSet(e.left) != djSet.findSet(e.right)) {
            djSet.unionSets(e.left, e.right);
            edgeQueueGreatestFirst.push(e);
        }
    }

    int hvalue      = 0;
    int weightAdded = 0;

    // get hvalue
    while (edgeQueueGreatestFirst.size() > 0) {
        edge<Location> e = edgeQueueGreatestFirst.top();
        edgeQueueGreatestFirst.pop();
        hvalue +=
          e.weight * max(1, (static_cast<int>(currentWeight) + weightAdded));
        weightAdded += 1;
    }

    return hvalue;
}

#endif
