#pragma once
#include "../utility/SlidingWindow.h"
#include <algorithm>
#include <bitset>
#include <cassert>
#include <fstream>
#include <iomanip>
#include <limits>
#include <ostream>
#include <queue>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include <bitset>

using namespace std;

class PancakePuzzle
{
public:
    typedef double          Cost;
    static constexpr double COST_MAX = std::numeric_limits<double>::max();

    class State
    {
    public:
        State() {}

        State(std::vector<unsigned int> b, size_t l)
            : ordering(b)
            , label(l)
        {
            generateKey();
        }

        std::vector<unsigned int> getOrdering() const { return ordering; }

        friend std::ostream& operator<<(std::ostream&               stream,
                                        const PancakePuzzle::State& state)
        {
            for (size_t r = 0; r < state.getOrdering().size(); r++) {
                stream << std::setw(3)
                       << static_cast<int>(state.getOrdering()[r]) << " ";
            }
            return stream;
        }

        bool operator==(const State& state) const
        {
            return ordering == state.getOrdering();
        }

        bool operator!=(const State& state) const
        {
            return ordering != state.getOrdering();
        }

        void generateKey()
        {
            /*
                    FNV-1a
            */
            unsigned long long offset_basis = 0xCBF29CE484222325;
            unsigned long long fnv_prime    = 0x100000001B3;
            size_t             i;
            for (i = 0; i < ordering.size(); ++i) {
                unsigned int value = ordering[i];
                offset_basis       = offset_basis ^ value;
                offset_basis *= fnv_prime;
            }
            theKey = offset_basis;
        }

        unsigned long long key() const { return theKey; }

        std::string toString() const
        {
            std::string s = "";
            for (size_t r = 0; r < ordering.size(); r++) {
                s += std::to_string(static_cast<int>(ordering[r])) + " ";
            }
            return s + "\n";
        }

        size_t getLabel() const { return label; }

        void markStart() { label = 0; }

        void dumpToProblemFile(ofstream& f)
        {
            f << ordering.size() << "\n";

            f << "starting positions for pancake :\n";

            for (size_t r = 0; r < ordering.size(); r++) {
                f << ordering[r] << "\n";
            }

            f << "end positions pancake:\n";

            for (size_t i = 1; i <= ordering.size(); i++) {
                f << i << "\n";
            }
        }

    private:
        std::vector<unsigned int> ordering;
        size_t                    label;
        unsigned long long        theKey =
          std::numeric_limits<unsigned long long>::max();
    };

    struct HashState
    {
        std::size_t operator()(const State& s) const { return s.key(); }
    };

    PancakePuzzle(std::istream& input)
    {
        // Get the size of pancake
        string line;
        getline(input, line);
        stringstream ss(line);
        ss >> size;

        // Skip the next line
        getline(input, line);
        std::vector<unsigned int> rows(size, 0);

        startOrdering = rows;
        endOrdering   = rows;

        for (size_t i = 0; i < size; ++i) {
            getline(input, line);
            startOrdering[i] = static_cast<unsigned int>(stoi(line));
        }
        // Skip the next line
        getline(input, line);

        for (size_t i = 0; i < size; ++i) {
            getline(input, line);
            endOrdering[i] = static_cast<unsigned int>(stoi(line));
        }

        puzzleVariant = 0; // Default
        startState    = State(startOrdering, 0);
    }

    /*
    // For making pancakes with out cin files
    PancakePuzzle(int len, int variant, int seed ) {
        // Variants:
        // 0: Regular pancake puzzle, where each flip cost 1.
        // 1: Cost is max of two elements of each end of the set being flipped.
        // 2: Each pancake has a weight, equal to its index.
        //    The cost is the sum of the indexes of pancakes being flipped.

        if (len > 255){
            fprintf (stderr, "Max pancake size is 255\n");
            exit(1);
        }

        srand(seed);

        std::unordered_map<int, char> numbers;

        // Generating random unique numbers
        while (startOrdering.size() < len){
            int tmp = numbers.size();
            int rr = rand() % len + 1;
            numbers[rr] = 0;
            if (tmp != numbers.size()){
                startOrdering.push_back(rr);
            }
        }

        endOrdering = startOrdering;
        sort(endOrdering.begin(), endOrdering.end());

        puzzleVariant = variant;
        size = len;

        startState = State(startOrdering, 0);
    }
    */

    void setVariant(int variant) { puzzleVariant = variant; }

    bool isGoal(const State& s) const
    {
        if (s.getOrdering() == endOrdering) {
            return true;
        }

        return false;
    }

    Cost gapHeuristic(const State& state) const
    {
        // Using gap heuristic from - Landmark Heuristics for the Pancake
        // Problem Where add 1 to heuristic if the adjacent sizes of the
        // pancakes differs more than 1 For heavy pancake problems. For each gap
        // b/w x and y, add min(x,y) to heuristic instead of just 1
        size_t size_ = state.getOrdering().size();
        size_t plate = size_ + 1;
        size_t sum   = 0;

        for (size_t i = 1; i < size; ++i) {
            size_t x   = state.getOrdering()[i - 1];
            size_t y   = state.getOrdering()[i];
            int    dif = static_cast<int>(x) - static_cast<int>(y);
            if (dif > 1 || dif < -1) {
                if (puzzleVariant == 0) {
                    ++sum;
                } else {
                    sum += min(x, y);
                }
            }
        }

        size_t x   = state.getOrdering()[size - 1];
        int    dif = static_cast<int>(x) - static_cast<int>(plate);
        if (dif > 1 || dif < -1) {
            if (puzzleVariant == 0) {
                ++sum;
            } else {
                sum += x;
            }
        }
        return static_cast<double>(sum);
    }

    Cost distance(const State& state)
    {
        // Check if the distance of this state has been updated
        if (correctedD.find(state) != correctedD.end()) {
            return correctedD[state];
        }

        Cost d = gapHeuristic(state);
        updateDistance(state, d);

        return correctedD[state];
    }

    Cost distanceErr(const State& state)
    {
        // Check if the distance error of this state has been updated
        if (correctedDerr.find(state) != correctedDerr.end()) {
            return correctedDerr[state];
        }

        Cost derr = gapHeuristic(state);
        updateDistanceErr(state, derr);

        return correctedDerr[state];
    }

    Cost heuristic(const State& state)
    {
        // Check if the heuristic of this state has been updated
        if (correctedH.find(state) != correctedH.end()) {
            return correctedH[state];
        }

        Cost h = gapHeuristic(state);
        updateHeuristic(state, h);

        return correctedH[state];
    }

    Cost heuristic_no_recording(const State& state)
    {
        return gapHeuristic(state);
    }

    Cost epsilonHGlobal() { return curEpsilonH; }

    Cost epsilonDGlobal() { return curEpsilonD; }

    Cost epsilonHVarGlobal() { return curEpsilonHVar; }

    void updateEpsilons()
    {
        // TODO

        if (expansionCounter == 0) {
            curEpsilonD    = 0;
            curEpsilonH    = 0;
            curEpsilonHVar = 0;

            return;
        }

        curEpsilonD = epsilonDSum / expansionCounter;

        curEpsilonH = epsilonHSum / expansionCounter;

        curEpsilonHVar =
          (epsilonHSumSq - (epsilonHSum * epsilonHSum) / expansionCounter) /
          (expansionCounter - 1);

        assert(curEpsilonHVar > 0);
    }

    void pushEpsilonHGlobal(double eps)
    {
        // TODO

        if (eps < 0)
            eps = 0;
        /* No idea why set the limit to 1
        else if (eps > 1){
            eps = 1;
        }
        */
        epsilonHSum += eps;
        epsilonHSumSq += eps * eps;
        expansionCounter++;
    }

    void pushEpsilonDGlobal(double eps)
    {
        // TODO

        if (eps < 0)
            eps = 0;
        /*
        else if (eps > 1)
            eps = 1;
        */
        epsilonDSum += eps;
        expansionCounter++;
    }

    void updateDistance(const State& state, Cost value)
    {
        correctedD[state] = value;
    }

    void updateDistanceErr(const State& state, Cost value)
    {
        correctedDerr[state] = value;
    }

    void updateHeuristic(const State& state, Cost value)
    {
        correctedH[state] = value;
    }

    double getBranchingFactor() const
    {
        return static_cast<double>(size) - 1; //  I think this is right
    }

    void flipOrdering(std::vector<State>&       succs,
                      std::vector<unsigned int> ordering, int loc) const
    {
        int start = 0;
        int end   = loc;
        while (start < end) {
            std::swap(ordering[static_cast<size_t>(start++)],
                      ordering[static_cast<size_t>(end--)]);
        }

        succs.push_back(State(ordering, static_cast<size_t>(loc)));
    }

    std::vector<State> successors(const State& state) const
    {
        std::vector<State> successors;
        for (int i = static_cast<int>(size) - 1; i > 0; --i) {
            // Don't allow inverse actions, to cut down on branching factor
            if (state.getLabel() == static_cast<size_t>(i))
                continue;

            flipOrdering(successors, state.getOrdering(), i);
        }
        return successors;
    }

    std::vector<State> predecessors(const State& state) const
    {
        std::vector<State> predecessors;
        for (int i = static_cast<int>(size) - 1; i > 0; --i) {
            flipOrdering(predecessors, state.getOrdering(), i);
        }
        return predecessors;
    }

    const State getStartState() const { return startState; }

    Cost getEdgeCost(State state)
    {
        // Looking at Andew's code, it looks like this is called
        // mostly on successors being generated. So the label
        // will tell which index the parent chose to flip at.

        // Variants:
        // 0: Regular pancake puzzle, where each flip cost 1.
        // 1: Cost is max of two elements of each end of the set being flipped.
        // 2: Each pancake has a weight, equal to its index.
        //    The cost is the sum of the indexes of pancakes being flipped.

        size_t l = state.getLabel();

        if (puzzleVariant == 1) {
            size_t i = state.getOrdering()[0];
            size_t j = state.getOrdering()[l];
            if (i > j)
                return static_cast<double>(i);
            return static_cast<double>(j);
        }

        if (puzzleVariant == 2) {
            size_t sum = 0;
            for (size_t i = 1; i <= l; ++i) {
                sum += i;
            }
            return static_cast<double>(sum);
        }

        // Variant 1
        return 1;
    }

    string getDomainInformation()
    {
        string variant;
        if (puzzleVariant == 0) {
            variant = "\"Pancake Puzzle\"";
        } else if (puzzleVariant == 1) {
            variant = "\"Heavy Pancake DPS\"";
        } else if (puzzleVariant == 2) {
            variant = "\"Heavy Pancake Sum\"";
        }
        string info = "{ \"Domain\": " + variant +
                      ", \"Dimensions\": " + std::to_string(size) + " }";
        return info;
    }

    string getDomainName()
    {
        if (puzzleVariant == 0)
            return "PancakePuzzle";

        // Cost is max of two elements of each end of the set being flipped
        if (puzzleVariant == 1)
            return "PancakePuzzleDPS";

        // Cost of starting index
        if (puzzleVariant == 2)
            return "PancakePuzzleSum";

        return "Unknow variant";
    }

    void initialize(string policy, int la)
    {
        epsilonDSum      = 0;
        epsilonHSum      = 0;
        expansionCounter = 0;
        curEpsilonD      = 0;
        curEpsilonH      = 0;

        expansionPolicy = policy;
        lookahead       = la;
        correctedD.clear();
        correctedDerr.clear();
        correctedH.clear();
        expansionDelayWindow.clear();
    }

    void pushDelayWindow(int val) { expansionDelayWindow.push(val); }

    double averageDelayWindow()
    {
        if (expansionDelayWindow.size() == 0)
            return 1;

        double avg = 0;

        for (auto i : expansionDelayWindow) {
            avg += i;
        }

        avg /= static_cast<double>(expansionDelayWindow.size());

        return avg;
    }

    bool validatePath(queue<int> path)
    {
        std::vector<unsigned int> board = startOrdering;

        std::vector<State> successors;

        while (!path.empty()) {
            size_t start = 0;
            size_t end   = static_cast<size_t>(path.front());
            while (start < end) {
                std::swap(board[start++], board[end--]);
            }
            path.pop();
        }

        if (board == endOrdering)
            return true;
        return false;
    }

    std::vector<unsigned int> startOrdering;
    std::vector<unsigned int> endOrdering;

    State                                 startState;
    SlidingWindow<int>                    expansionDelayWindow;
    unordered_map<State, Cost, HashState> correctedH;
    unordered_map<State, Cost, HashState> correctedD;
    unordered_map<State, Cost, HashState> correctedDerr;
    int                                   puzzleVariant;
    size_t                                size;

    double epsilonHSum;
    double epsilonHSumSq;
    double epsilonDSum;
    double curEpsilonH;
    double curEpsilonD;
    double curEpsilonHVar;
    double expansionCounter;

    string expansionPolicy;
    int    lookahead;
};
