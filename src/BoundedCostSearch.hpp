#pragma once

#include "SearchBase.hpp"

#include <boost/math/special_functions/erf.hpp>
#include <cmath>
#include <ctime>
#include <functional>
#include <iostream>
#include <set>
#include <unordered_map>
#include <vector>

using namespace std;

template<class Domain>
class BoundedCostSearch : public Search
{
public:
    typedef typename Domain::State     State;
    typedef typename Domain::Cost      Cost;
    typedef typename Domain::HashState Hash;

    struct Node
    {
        Cost  g;
        Cost  h;
        Cost  d;
        Cost  epsH;
        Cost  epsD;
        Cost  epsHVar;
        int   delayCntr;
        State stateRep;
        Node* parent;
        bool  open;

        static Cost   bound;
        static double weight;

        Cost   ptsnancywithdhat;
        double nancyPotential;

    public:
        Cost getGValue() const { return g; }
        Cost getHValue() const { return h; }
        Cost getFValue() const { return g + h; }
        Cost getDValue() const { return d; }
        Cost getEpsilonH() const { return epsH; }
        Cost getEpsilonHVar() const { return epsHVar; }
        Cost getEpsilonD() const { return epsD; }
        Cost getDHatValue() const { return (d / (1.0 - epsD)); }
        Cost getHHatValue() const { return h + getDHatValue() * epsH; }
        Cost getFHatValue() const { return g + getHHatValue(); }

        State getState() const { return stateRep; }
        Node* getParent() const { return parent; }

        // for bounded cost search
        // petrick pts
        // Cost getPTSValue() const { return 1 / (1 - h / (bound + 1 - g)); }
        // original pts
        // Cost getPTSValue() const { return h / (bound - g); }
        // BEES pts
        Cost getPTSValue() const { return h / (1 - (g / bound)); }
        Cost getPTSHHatValue() const
        {
            // return 1 / (1 - getHHatValue() / (bound + 1 - g));
            // return getHHatValue() / (bound - g);
            return getHHatValue() / (1 - (g / bound));
        }

        Cost getPotentialNancyValue() const { return nancyPotential; }

        void computePotentialNancyValue()
        {
            if (getHValue() == getHHatValue() || getHValue() == 0) {
                nancyPotential = getFValue() <= bound ? 1. : 0.;
                return;
            }

            auto mean               = getFHatValue();
            auto standard_deviation = std::abs(mean - getFValue()) / 2;
            auto cdf_xi    = cumulative_distribution((bound + 0.5 - mean) /
                                                  standard_deviation);
            auto cdf_alpha = cumulative_distribution((getFValue() - mean) /
                                                     standard_deviation);

            assert(cdf_xi >= 0 && cdf_xi <= 1);
            assert(cdf_alpha >= 0 && cdf_alpha <= 1);

            /*    cout << "g " << g << " h " << h << " h hat" <<
             * getHHatValue()*/
            //<< " f hat" << getFHatValue() << "std " <<
            // standard_deviation
            //<< "\n";
            // cout << "cdf_xi " << cdf_xi << " cdf_alpha " << cdf_alpha
            // <<
            // "\n"; cout << "epsH " << epsH << " epsD " << epsD << "\n";
            /*cout << "p " << (cdf_xi - cdf_alpha) / (1 - cdf_alpha) <<
             * "\n";*/

            nancyPotential = (cdf_xi - cdf_alpha) / (1 - cdf_alpha);
        }

        void computePotentialNancyValueWithOnlineVar()
        {
            if (getEpsilonHVar() == 0 || getHValue() == 0) {
                nancyPotential = getFValue() <= bound ? 1. : 0.;
                return;
            }

            auto mean = getFHatValue();
            auto standard_deviation =
              std::sqrt(getDHatValue() * getEpsilonHVar());
            auto cdf_xi =
              cumulative_distribution((bound - mean) / standard_deviation);
            auto cdf_alpha = cumulative_distribution((getFValue() - mean) /
                                                     standard_deviation);

            assert(cdf_xi >= 0 && cdf_xi <= 1);
            assert(cdf_alpha >= 0 && cdf_alpha <= 1);

            nancyPotential = (cdf_xi - cdf_alpha) / (1 - cdf_alpha);
        }

        Cost getPTSNancyValue() const
        {
            auto nancypts = getPotentialNancyValue();

            return d / nancypts;
        }

        void computePTSNancyValueWithDHat(const string& algName)
        {
            if (algName == "ptsnancywithdhat") {
                computePotentialNancyValue();
            } else if (algName == "ptsnancywithdhat-olv" ||
                       algName == "ptsnancyonlyprob-olv") {
                computePotentialNancyValueWithOnlineVar();
            } else {
                cout << "unknow ptsnancy variation";
                exit(1);
            }

            auto nancypts = getPotentialNancyValue();

            ptsnancywithdhat = getDHatValue() / nancypts;
        }

        void computePTSNancyValueWithDHatAndBranchingFactor(
          const double branchingFactor)
        {
            computePotentialNancyValue();
            auto nancypts = getPotentialNancyValue();

            ptsnancywithdhat = pow(getDHatValue(), branchingFactor) / nancypts;
        }

        Cost getPTSNancyValueWithDHat() const { return ptsnancywithdhat; }

        void setHValue(Cost val) { h = val; }
        void setGValue(Cost val) { g = val; }
        void setDValue(Cost val) { d = val; }
        void setEpsilonH(Cost val) { epsH = val; }
        void setEpsilonHVar(Cost val) { epsHVar = val; }
        void setEpsilonD(Cost val) { epsD = val; }
        void setState(State s) { stateRep = s; }
        void setParent(Node* p) { parent = p; }

        void incDelayCntr() { delayCntr++; }
        int  getDelayCntr() { return delayCntr; }

        Node(Cost g_, Cost h_, Cost d_, Cost epsH_, Cost epsD_, Cost epsHVar_,
             State state_, Node* parent_)
            : g(g_)
            , h(h_)
            , d(d_)
            , epsH(epsH_)
            , epsD(epsD_)
            , epsHVar(epsHVar_)
            , delayCntr(0)
            , stateRep(state_)
            , parent(parent_)
            , open(true)
        {}

        friend std::ostream& operator<<(std::ostream& stream, const Node& node)
        {
            stream << node.getState() << "\n";
            stream << "f: " << node.getFValue() << "\n";
            stream << "g: " << node.getGValue() << "\n";
            stream << "h: " << node.getHValue() << "\n";
            stream << "pts : " << node.getPTSValue() << "\n";
            stream << "action generated by: " << node.getState().getLabel()
                   << "\n";
            stream << "-----------------------------------------------"
                   << "\n";
            stream << "\n";
            return stream;
        }

        bool onOpen() { return open; }
        void close() { open = false; }
        void reopen() { open = true; }

        static bool compareNodesF(const Node* n1, const Node* n2)
        {
            // Tie break on g-value
            if (n1->getFValue() == n2->getFValue()) {
                return n1->getGValue() > n2->getGValue();
            }
            return n1->getFValue() < n2->getFValue();
        }

        static bool compareNodesWeightedF(const Node* n1, const Node* n2)
        {
            // Tie break on g-value
            auto n1WeightedF = n1->getGValue() + weight * n1->getHValue();
            auto n2WeightedF = n2->getGValue() + weight * n2->getHValue();
            if (n1WeightedF == n2WeightedF) {
                return n1->getGValue() > n2->getGValue();
            }
            return n1WeightedF < n2WeightedF;
        }

        static bool compareNodesDHat(const Node* n1, const Node* n2)
        {
            // Tie break on g-value
            if (n1->getDHatValue() == n2->getDHatValue()) {
                return n1->getGValue() > n2->getGValue();
            }
            return n1->getDHatValue() < n2->getDHatValue();
        }

        static bool compareNodesPTS(const Node* n1, const Node* n2)
        {
            // Tie break on low f, high g-value, low d
            if (n1->getPTSValue() == n2->getPTSValue()) {
                if (n1->getFValue() == n2->getFValue()) {
                    if (n1->getGValue() == n1->getGValue()) {
                        return n1->getDValue() < n2->getDValue();
                    }
                    return n1->getGValue() > n2->getGValue();
                }
                return n1->getFValue() < n2->getFValue();
            }
            return n1->getPTSValue() < n2->getPTSValue();
        }

        static bool compareNodesPTSHHat(const Node* n1, const Node* n2)
        {
            // Tie break on low fhat, high g-value, low d
            if (n1->getPTSHHatValue() == n2->getPTSHHatValue()) {
                if (n1->getFHatValue() == n2->getFHatValue()) {
                    if (n1->getGValue() == n1->getGValue()) {
                        return n1->getDValue() < n2->getDValue();
                    }
                    return n1->getGValue() > n2->getGValue();
                }
                return n1->getFHatValue() < n2->getFHatValue();
            }
            return n1->getPTSHHatValue() < n2->getPTSHHatValue();
        }

        static bool compareNodesPTSNancy(const Node* n1, const Node* n2)
        {
            if (n1->getPotentialNancyValue() < 0.01 &&
                n2->getPotentialNancyValue() >= 0.01) {
                return false;
            } else if (n1->getPotentialNancyValue() >= 0.01 &&
                       n2->getPotentialNancyValue() < 0.01) {
                return true;
            } else if (n1->getPotentialNancyValue() < 0.01 &&
                       n2->getPotentialNancyValue() < 0.01) {
                return n1->getFValue() < n2->getFValue();
            } else if (n1->getPTSNancyValue() == n2->getPTSNancyValue()) {
                // Tie break on g-value
                return n1->getGValue() > n2->getGValue();
            }
            return n1->getPTSNancyValue() < n2->getPTSNancyValue();
        }

        static bool compareNodesPTSNancyOnlyProb(const Node* n1, const Node* n2)
        {
            if (n1->getPotentialNancyValue() == n2->getPotentialNancyValue()) {
                // Tie break on g-value
                return n1->getGValue() > n2->getGValue();
            }
            return n1->getPotentialNancyValue() > n2->getPotentialNancyValue();
        }

        static bool compareNodesD(const Node* n1, const Node* n2)
        {
            if (n1->getDValue() == n2->getDValue()) {
                // Tie break on g-value
                return n1->getGValue() > n2->getGValue();
            }
            return n1->getDValue() < n2->getDValue();
        }

        static bool compareNodesPTSNancyWithDhat(const Node* n1, const Node* n2)
        {
            /*if (n1->getPotentialNancyValue() < 0.01 &&*/
            // n2->getPotentialNancyValue() >= 0.01) {
            // return false;
            //} else if (n1->getPotentialNancyValue() >= 0.01 &&
            // n2->getPotentialNancyValue() < 0.01) {
            // return true;
            //} else if (n1->getPotentialNancyValue() < 0.01 &&
            // n2->getPotentialNancyValue() < 0.01) {
            // return n1->getFValue() < n2->getFValue();
            //} else if (n1->getPTSNancyValueWithDHat() ==
            // n2->getPTSNancyValueWithDHat()) {
            //// Tie break on g-value
            // return n1->getGValue() > n2->getGValue();
            //}
            // return n1->getPTSNancyValueWithDHat() <
            /*n2->getPTSNancyValueWithDHat();*/

            // Tie break on low f, high g-value, low d
            auto n1ESEValue = n1->getPTSNancyValueWithDHat();
            auto n2ESEValue = n2->getPTSNancyValueWithDHat();
            if (n1ESEValue == n2ESEValue) {
                if (n1->getFValue() == n2->getFValue()) {
                    if (n1->getGValue() == n1->getGValue()) {
                        return n1->getDValue() < n2->getDValue();
                    }
                    return n1->getGValue() > n2->getGValue();
                }
                return n1->getFValue() < n2->getFValue();
            }
            return n1ESEValue < n2ESEValue;
        }

    private:
        double cumulative_distribution(double x) const
        {
            /*int t = 0;*/
            // for (int i = 0; i < 10000; i++) {
            // t += 1;
            /*}*/
            return (1 + boost::math::erf(
                          x / std::sqrt(2.),
                          boost::math::policies::make_policy(
                            boost::math::policies::promote_double<false>()))) /
                   2.;
        }
    };

    BoundedCostSearch(Domain& domain_, Cost bound_, const string& algStr,
                      double weight_)
        : domain(domain_)
    {
        Node::bound  = bound_;
        Node::weight = weight_;

        // olv = online varance
        if (algStr == "wastar" || algStr == "astar" || algStr == "pts" ||
            algStr == "ptshhat" || algStr == "ptsnancy" ||
            algStr == "ptsnancyonlyprob" || algStr == "ptsnancyonlyeffort" ||
            algStr == "ptsnancyonlyeffort-dhat" ||
            algStr == "ptsnancywithdhat" || algStr == "ptsnancywithdhatandbf" ||
            algStr == "ptsnancywithdhat-olv" ||
            algStr == "ptsnancyonlyprob-olv") {
            algorithm = new PotentialSearch<Domain, Node>(domain, algStr);
        } else if (algStr == "bees" || algStr == "beeps" ||
                   algStr == "beepsnancy" || algStr == "bees-EpsGlobal" ||
                   algStr == "bees95" || algStr == "bees95-olv") {
            algorithm = new BEES<Domain, Node>(domain, algStr);
        } else {
            cout << "unknown algorithm name!";
            exit(1);
        }
    }

    ~BoundedCostSearch() { clean(); }

    SearchResultContainer doSearch()
    {
        SearchResultContainer res;

        auto inith = domain.heuristic(domain.getStartState());
        auto initD = domain.distance(domain.getStartState());

        // Get the start node
        Node* cur = new Node(
          0, inith, initD, domain.epsilonHGlobal(), domain.epsilonDGlobal(),
          domain.epsilonHVarGlobal(), domain.getStartState(), NULL);

        open.push(cur);
        res.initialH = inith;

        clock_t startTime = clock();

        // Expand some nodes
        double solutionCost = algorithm->run(open, openhat, closed, expanded,
                                             duplicateDetection, res);

        res.solutionFound = solutionCost != -1.0;
        res.solutionCost  = solutionCost;

        res.totalCpuTime =
          static_cast<double>(clock() - startTime) / CLOCKS_PER_SEC;

        return res;
    }

private:
    static bool duplicateDetection(Node*                              node,
                                   unordered_map<State, Node*, Hash>& closed,
                                   PriorityQueue<Node*>&)
    {
        // Check if this state exists
        typename unordered_map<State, Node*, Hash>::iterator it =
          closed.find(node->getState());

        if (it != closed.end()) {
            /*cout << "dup found \n";*/
            // cout << "new " << node->getState();
            // cout << "old " << it->second->getState();

            // if the new node is better, update it on close
            if (node->getGValue() < it->second->getGValue()) {
                it->second->setGValue(node->getGValue());
                it->second->setParent(node->getParent());
                it->second->setHValue(node->getHValue());
                it->second->setDValue(node->getDValue());
                it->second->setEpsilonH(node->getEpsilonH());
                it->second->setEpsilonHVar(node->getEpsilonHVar());
                it->second->setEpsilonD(node->getEpsilonD());
                it->second->setState(node->getState());

                // This state has been generated before, check if its node is on
                // OPEN
                /*if (it->second->onOpen()) {*/
                //// This node is on OPEN, keep the better g-value
                // open.remove(it->second);
                // open.push(it->second);
                ////} else {
                //////cout << "reopen\n";
                //// it->second->reopen();
                /*}*/

                //// reopen the node
                /*open.push(it->second);*/
            }

            return true;
        }

        return false;
    }

    void clean()
    {
        // Empty OPEN and CLOSED
        open.clear();

        // delete all of the nodes from the last expansion phase
        for (typename unordered_map<State, Node*, Hash>::iterator it =
               closed.begin();
             it != closed.end(); it++)
            delete it->second;

        closed.clear();

        delete algorithm;
    }

protected:
    Domain&                           domain;
    BoundedCostBase<Domain, Node>*    algorithm;
    PriorityQueue<Node*>              open;
    PriorityQueue<Node*>              openhat;
    unordered_map<State, Node*, Hash> closed;
    unordered_map<State, Node*, Hash> expanded;
};

template<class Domain>
double BoundedCostSearch<Domain>::Node::weight;

template<class Domain>
typename Domain::Cost BoundedCostSearch<Domain>::Node::bound;
