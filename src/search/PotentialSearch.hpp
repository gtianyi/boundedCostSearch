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
    PotentialSearch(Domain& domain_, const string& sorting_)
        : domain(domain_)
        , sortingFunction(sorting_)
    {}

    double run(PriorityQueue<Node*>&              open,
               unordered_map<State, Node*, Hash>& closed,
               std::function<bool(Node*, unordered_map<State, Node*, Hash>&)>
                                      duplicateDetection,
               SearchResultContainer& res, Cost bound)
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

            State bestChild;
            Cost  bestF = numeric_limits<double>::infinity();

            for (State child : children) {

                auto newG = cur->getGValue() + domain.getEdgeCost(child);
                auto newH = domain.heuristic(child);
                auto newD = domain.distance(child);

                // prune by bound
                if (newG + newH > bound) {
                    continue;
                }

                Node* childNode =
                  new Node(newG, newH, newD, domain.epsilonHGlobal(),
                           domain.epsilonDGlobal(), child, cur, bound);

                bool dup = duplicateDetection(childNode, closed);

                if (!dup && childNode->getFValue() < bestF) {
                    bestF     = childNode->getFValue();
                    bestChild = child;
                }

                // Duplicate detection
                if (!dup) {
                    open.push(childNode);
                    closed[child] = childNode;
                } else
                    delete childNode;
            }

            // Learn one-step error
            if (bestF != numeric_limits<double>::infinity()) {
                Cost epsD = (1 + domain.distance(bestChild)) - cur->getDValue();
                Cost epsH = (domain.getEdgeCost(bestChild) +
                             domain.heuristic(bestChild)) -
                            cur->getHValue();

                domain.pushEpsilonHGlobal(epsH);
                domain.pushEpsilonDGlobal(epsD);
            }
        }

        return -1.0;
    }

private:
    void sortOpen(PriorityQueue<Node*>& open)
    {
        if (sortingFunction == "pts") {
            open.swapComparator(Node::compareNodesPTS);
        } else if (sortingFunction == "ptshhat") {
            open.swapComparator(Node::compareNodesPTSHHat);
        } else if (sortingFunction == "ptsnancy") {
            open.swapComparator(Node::compareNodesPTSHHat);
        } else {
            cout << "Unknown algorithm!\n";
            exit(1);
        }
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
    Domain&      domain;
    const string sortingFunction;
};
