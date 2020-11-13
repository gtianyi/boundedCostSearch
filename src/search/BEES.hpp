#pragma once
#include "BoundedCostBase.hpp"

using namespace std;

template<class Domain, class Node>
class BEES : public BoundedCostBase<Domain, Node>
{
    typedef typename Domain::State     State;
    typedef typename Domain::Cost      Cost;
    typedef typename Domain::HashState Hash;

public:
    BEES(Domain& domain_, const string& sorting_)
        : BoundedCostBase<Domain, Node>(domain_, sorting_)
    {}

    double run(PriorityQueue<Node*>& open, PriorityQueue<Node*>& openhat,
               unordered_map<State, Node*, Hash>& closed,
               unordered_map<State, Node*, Hash>& expanded,
               std::function<bool(Node*, unordered_map<State, Node*, Hash>&,
                                  PriorityQueue<Node*>&)>
                                      duplicateDetection,
               SearchResultContainer& res)
    {
        sortOpen(open);
        sortOpenHat(openhat);

        // Expand until find the goal
        while (!open.empty() || !openhat.empty()) {

            Node* cur;

            if (!openhat.empty()) {
                cur = openhat.top();
                openhat.pop();
            } else {
                cur = open.top();
                while (expanded.find(cur->getState()) != expanded.end()) {
                    open.pop();
                    cur = open.top();
                }
                open.pop();
            }

            expanded[cur->getState()] = cur;

            // Check if current node is goal
            if (this->domain.isGoal(cur->getState())) {
                this->getSolutionPath(res, cur);
                return cur->getFValue();
            }

            res.nodesExpanded++;

            cur->close();

            vector<State> children = this->domain.successors(cur->getState());
            res.nodesGenerated += children.size();

            State bestChild;
            Cost  bestF = numeric_limits<double>::infinity();

            for (State child : children) {

                auto newG = cur->getGValue() + this->domain.getEdgeCost(child);
                auto newH = this->domain.heuristic(child);
                auto newD = this->domain.distance(child);

                // prune by bound
                if (newG + newH > Node::bound) {
                    continue;
                }

                Node* childNode =
                  new Node(newG, newH, newD, this->domain.epsilonHGlobal(),
                           this->domain.epsilonDGlobal(), child, cur);

                bool dup = duplicateDetection(childNode, closed, open);

                if (!dup && childNode->getFValue() < bestF) {
                    bestF     = childNode->getFValue();
                    bestChild = child;
                }

                // Duplicate detection
                if (!dup) {
                    open.push(childNode);

                    if (childNode->getFHatValue() <= Node::bound) {
                        openhat.push(childNode);
                    }

                    closed[child] = childNode;
                } else
                    delete childNode;
            }

            if (this->sortingFunction != "pts") {
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
        if (this->sortingFunction == "bees") {
            open.swapComparator(Node::compareNodesF);
        } else if (this->sortingFunction == "beeps") {
            open.swapComparator(Node::compareNodesPTSHHat);
        } else if (this->sortingFunction == "beepsnancy") {
            open.swapComparator(Node::compareNodesPTSNancy);
        } else {
            cout << "Unknown algorithm!\n";
            exit(1);
        }
    }

    void sortOpenHat(PriorityQueue<Node*>& openhat)
    {
        openhat.swapComparator(Node::compareNodesDHat);
    }
};
