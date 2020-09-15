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
    PotentialSearch(Domain& domain_, string sorting_)
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

            // std::cout << "generated: " << res.nodesGenerated << std::endl;

            for (State child : children) {

                auto newG = cur->getGValue() + domain.getEdgeCost(child);
                auto newH = domain.heuristic_no_recording(child);

                // prune by bound
                if (newG + newH > bound) {
                    continue;
                }

                Node* childNode = new Node(newG, newH, child, cur, bound);

                bool dup = duplicateDetection(childNode, closed);

                // Duplicate detection
                if (!dup) {
                    open.push(childNode);
                    closed[child] = childNode;
                } else
                    delete childNode;
            }
        }

        return -1.0;
    }

private:
    void sortOpen(PriorityQueue<Node*>& open)
    {
        open.swapComparator(Node::compareNodesPTS);
        // open.swapComparator(Node::compareNodesF);
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
