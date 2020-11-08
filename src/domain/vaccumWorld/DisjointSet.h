#pragma once
/*
  File: DisjointSet.h
  author: Tianyi Gu
  DisjointSet Class
*/

#include <map>
using namespace std;

template<typename T>
class DisjointSet
{
private:
    std::map<T, T>   parents; // access to set representitives
    std::map<T, int> depths;  // used for path compression
public:
    DisjointSet(){};

    // Creates a singleton set from the parameter.
    void createSet(T p)
    {
        parents[p] = p;
        depths[p]  = 1;
    }

    // Finds and returns the representative of the set
    // which contains the parameter. Implements path compression.
    T findSet(T p)
    {
        if (parents[p] == p)
            return p;
        else {
            parents[p] = findSet(parents[p]);
            depths[p]  = 2;
            return parents[p];
        }
    }

    // Combines the sets which contain the parameters.
    // Return false if two  parameters are already in the same set;
    // otherwise, union the two sets by rank and return true
    bool unionSets(T p, T q)
    {
        if (findSet(p) == findSet(q))
            return false;
        if (depths[p] < depths[q]) {
            depths[q] += depths[findSet(p)];
            parents[findSet(p)] = q;
        } else {
            depths[p] += depths[findSet(q)];
            parents[findSet(q)] = p;
        }
        return true;
    }
};
