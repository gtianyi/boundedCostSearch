#pragma once
#include "BoundedCostBase.hpp"

using namespace std;

template<class Domain, class Node>
class PotentialSearch : public BoundedCostBase<Domain, Node>
{
    typedef typename Domain::State     State;
    typedef typename Domain::Cost      Cost;
    typedef typename Domain::HashState Hash;

public:
    PotentialSearch(Domain& domain_, const string& sorting_)
        : BoundedCostBase<Domain, Node>(domain_, sorting_)
    {}

    double run(PriorityQueue<Node*>&              open, PriorityQueue<Node*>&,
               unordered_map<State, Node*, Hash>& closed,
               unordered_map<State, Node*, Hash>&,
               std::function<bool(Node*, unordered_map<State, Node*, Hash>&)>
                                      duplicateDetection,
               SearchResultContainer& res)
    {
        sortOpen(open);

        // Expand until find the goal
        while (!open.empty()) {
            // Pop lowest fhat-value off open
            Node* cur = open.top();

            // Check if current node is goal
            if (this->domain.isGoal(cur->getState())) {
                this->getSolutionPath(res, cur);
                return cur->getGValue();
            }

            res.nodesExpanded++;

            open.pop();
            cur->close();

            /*   for (auto n : open) {*/
            // n->incDelayCntr();
            /*}*/

            vector<State> children = this->domain.successors(cur->getState());
            res.nodesGenerated += children.size();

            State bestChild;
            Cost  bestF = numeric_limits<double>::infinity();

            for (State child : children) {

                auto newG = cur->getGValue() + this->domain.getEdgeCost(child);
                auto newH = this->domain.heuristic(child);
                auto newD = this->domain.distance(child);

                // prune by bound
                if (this->sortingFunction != "astar" &&
                    this->sortingFunction != "wastar") {
                    // if (this->sortingFunction != "wastar") {
                    if (newG + newH > Node::bound) {
                        continue;
                    }
                }

                Node* childNode =
                  new Node(newG, newH, newD, this->domain.epsilonHGlobal(),
                           this->domain.epsilonDGlobal(), child, cur);

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

            if (this->sortingFunction != "pts" &&
                this->sortingFunction != "astar" &&
                this->sortingFunction != "wastar") {
                // Learn one-step error
                if (bestF != numeric_limits<double>::infinity()) {
                    Cost epsD =
                      (1 + this->domain.distance(bestChild)) - cur->getDValue();
                    Cost epsH = (this->domain.getEdgeCost(bestChild) +
                                 this->domain.heuristic(bestChild)) -
                                cur->getHValue();

                    this->domain.pushEpsilonHGlobal(epsH);
                    this->domain.pushEpsilonDGlobal(epsD);

                    this->domain.updateEpsilons();
                }
            }
        }

        return -1.0;
    }

private:
    void sortOpen(PriorityQueue<Node*>& open)
    {
        if (this->sortingFunction == "pts") {
            open.swapComparator(Node::compareNodesPTS);
        } else if (this->sortingFunction == "astar") {
            open.swapComparator(Node::compareNodesF);
        } else if (this->sortingFunction == "wastar") {
            open.swapComparator(Node::compareNodesWeightedF);
        } else if (this->sortingFunction == "ptshhat") {
            open.swapComparator(Node::compareNodesPTSHHat);
        } else if (this->sortingFunction == "ptsnancy") {
            open.swapComparator(Node::compareNodesPTSNancy);
        } else {
            cout << "Unknown algorithm!\n";
            exit(1);
        }
    }
};
