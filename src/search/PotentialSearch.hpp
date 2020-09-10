#pragma once
#include "../utility/PriorityQueue.h"
#include "../utility/SearchResultContainer.h"
#include <functional>
#include <unordered_map>

using namespace std;

template<class Domain, class Node>
class PotentialSearch
{
    typedef typename Domain::State     State;
    typedef typename Domain::Cost      Cost;
    typedef typename Domain::HashState Hash;

public:
    PotentialSearch(Domain& domain, string sorting)
        : domain(domain)
        , sortingFunction(sorting)
    {}

    double run(PriorityQueue<Node*>&              open,
               unordered_map<State, Node*, Hash>& closed,
               std::function<bool(Node*, unordered_map<State, Node*, Hash>&,
                                  PriorityQueue<Node*>&)>
                                      duplicateDetection,
               SearchResultContainer& res)
    {
        sortOpen(open);

        // Expand until find the goal
        while (!open.empty()) {
            // Pop lowest fhat-value off open
            Node* cur = open.top();

            // Check if current node is goal
            if (domain.isGoal(cur->getState())) {
                getSolutionPath(res, cur);
                return cur->getFValue();
            }

            res.nodesExpanded++;

            open.pop();
            cur->close();

            vector<State> children = domain.successors(cur->getState());
            res.nodesGenerated += children.size();

            for (State child : children) {
                Node* childNode =
                  new Node(cur->getGValue() + domain.getEdgeCost(child),
                           domain.heuristic_no_recording(child), child, cur);

                bool dup = duplicateDetection(childNode, closed);

                // Duplicate detection
                if (!dup) {
                    open.push(childNode);
                    closed[child] = childNode;
                } else
                    delete childNode;
            }
        }
    }

private:
    void sortOpen(PriorityQueue<Node*>& open)
    {
        open.swapComparator(Node::compareNodesF);
    }

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
    Domain& domain;
    string  sortingFunction;
};
