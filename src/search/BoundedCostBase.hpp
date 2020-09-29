#pragma once
#include "../utility/PriorityQueue.h"
#include "../utility/SearchResultContainer.h"
#include <functional>
#include <unordered_map>

using namespace std;

template<class Domain, class Node>
class BoundedCostBase
{
    typedef typename Domain::State     State;
    typedef typename Domain::Cost      Cost;
    typedef typename Domain::HashState Hash;

public:
    BoundedCostBase(Domain& domain_, const string& sorting_)
        : domain(domain_)
        , sortingFunction(sorting_)
    {}

    virtual ~BoundedCostBase(){};

    virtual double run(
      PriorityQueue<Node*>& open, PriorityQueue<Node*>& openhat,
      unordered_map<State, Node*, Hash>& closed,
      unordered_map<State, Node*, Hash>& expanded,
      std::function<bool(Node*, unordered_map<State, Node*, Hash>&)>
                             duplicateDetection,
      SearchResultContainer& res) = 0;

protected:
    virtual void sortOpen(PriorityQueue<Node*>& open) = 0;

    void getSolutionPath(SearchResultContainer& res, Node* goal)
    {
        auto cur = goal;

        string p = "";
        while (cur) {
            p   = cur->getState().toString() + p;
            cur = cur->getParent();
        }

        res.soltuionPath = p;
    }

protected:
    Domain&      domain;
    const string sortingFunction;
};
