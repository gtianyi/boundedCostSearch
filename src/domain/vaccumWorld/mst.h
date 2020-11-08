#pragma once
/*
  File: mst.h
  author: Tianyi Gu
  minimum spanning tree Class
*/
#ifndef MST_H
#define MST_H

#include <cmath>
#include <queue>
#include <vector>

#include "DisjointSet.h"

using namespace std;

template<typename Location>
struct edge
{
    // default constructor
    edge(Location& l_, Location& r_, double w_)
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
    double   weight;
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
    priority_queue<edge<Location>> edgeQueue;
    DisjointSet<Location>          djSet;
    // construct graph
    for (int i = 0; i < nodeList.size(); i++) {
        for (int j = 0; j < nodeList.size(); j++) {
            if (i <= j)
                continue;
            double d = std::fabs(nodeList[i].first - nodeList[j].first) +
                       std::fabs(nodeList[i].second - nodeList[j].second);
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

#endif
