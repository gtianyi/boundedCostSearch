#pragma once
/*
  File: mst.h
  author: Tianyi Gu
  minimum spanning tree Class
*/
#ifndef MST_H
#define MST_H

#include <cmath>
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
int mst(vector<Location>& nodeList)
{
    assert(nodeList.size() > 1);

    priority_queue<edge<Location>> edgeQueue;
    DisjointSet<Location>          djSet;
    // construct graph
    for (int i = 0; i < nodeList.size(); i++) {
        for (int j = 0; j < nodeList.size(); j++) {
            if (i <= j)
                continue;
            int d = std::abs(nodeList[i].first - nodeList[j].first) +
                    std::abs(nodeList[i].second - nodeList[j].second);
            edge<Location> e(nodeList[i], nodeList[j], d);
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
};

// last node is robot
template<typename Location>
int greedyTraversal(vector<Location>& nodeList)
{
    assert(nodeList.size() > 1);

    int cost = 0;

    auto cur = nodeList.back();
    nodeList.pop_back();

    while (!nodeList.empty()) {
        auto bestIt   = nodeList.begin();
        int  bestDist = std::numeric_limits<int>::max();

        for (auto it = nodeList.begin(); it != nodeList.end(); ++it) {
            int dist = std::abs(*it.first - cur.first) +
                       std::abs(*it.second - cur.second);
            if (dist < bestDist) {
                bestDist = dist;
                bestIt   = it;
            }
        }

        cost += bestDist;
        cur = *bestIt;
        nodeList.erase(bestIt);
    }

    return cost;
};

#endif
