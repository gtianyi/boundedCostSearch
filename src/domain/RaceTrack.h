#pragma once
#include "../utility/PairHash.h"
#include "../utility/SlidingWindow.h"
#include "../utility/debug.h"
#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <ostream>
#include <queue>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <bitset>

class RaceTrack
{
    using Location = pair<size_t, size_t>;

public:
    typedef double        Cost;
    static constexpr Cost COST_MAX = std::numeric_limits<Cost>::max();
    static constexpr int  INT_MAX  = std::numeric_limits<int>::max();

    class State
    {
    public:
        State() {}

        State(int x_, int y_, int dx_, int dy_)
            : x(x_)
            , y(y_)
            , dx(dx_)
            , dy(dy_)
        {
            generateKey();
        }

        friend std::ostream& operator<<(std::ostream&           stream,
                                        const RaceTrack::State& state)
        {
            stream << "x: " << state.x << " ";
            stream << "y: " << state.y << " ";
            stream << "dx: " << state.dx << " ";
            stream << "dy: " << state.dy << "\n";
            return stream;
        }

        bool operator==(const State& state) const
        {
            return theKey == state.key();
        }

        bool operator!=(const State& state) const
        {
            return theKey != state.key();
        }

        void generateKey()
        {
            // This will provide a unique hash for every state in the racetrack,
            unsigned long long val        = 0xCBF29CE484222325;
            unsigned int       x_unsigned = static_cast<unsigned int>(x);

            val = val ^ x_unsigned ^ (static_cast<size_t>(dx) << 8) ^
                  (static_cast<size_t>(y) << 16) ^
                  (static_cast<size_t>(dy) << 24);
            theKey = val;
        }

        unsigned long long key() const { return theKey; }

        int getX() const { return x; }

        int getY() const { return y; }

        int getDX() const { return dx; }

        int getDY() const { return dy; }

        std::string toString() const
        {
            std::string s = to_string(x) + " " + to_string(y) + " " +
                            to_string(dx) + " " + to_string(dy) + "\n";
            return s;
        }

        void dumpToProblemFile(ofstream& f)
        {
            f << "x y dx dy for racetrack:\n";
            f << x << " " << y << " " << dx << " " << dy << "\n";
            f << "goal positions are in the map";
        }

        void markStart() { label = 's'; }

    private:
        int                x, y, dx, dy;
        char               label;
        unsigned long long theKey =
          std::numeric_limits<unsigned long long>::max();
    };

    struct HashState
    {
        std::size_t operator()(const State& s) const { return s.key(); }

        // not sure if this necessary
        /*std::size_t leftRotate(std::size_t n, unsigned int d) const {*/
        // return (n << d) | (n >> (32 - d));
        /*}*/
    };

    RaceTrack(std::ifstream& raceMap, std::istream& initialState)
    {
        parseMap(raceMap);
        resetInitialState(initialState);
        initilaizeActions();
        computeDijkstraMap();
    }

    bool isGoal(const State& s) const
    {
        Location loc = Location(s.getX(), s.getY());
        return finishline.find(loc) != finishline.end();
    }

    Cost distance(const State& state)
    {
        // Check if the distance of this state has been updated
        if (correctedD.find(state) != correctedD.end()) {
            return correctedD[state];
        }

        Cost d = dijkstraMaxH(state);

        updateDistance(state, d);

        return correctedD[state];
    }

    Cost distanceErr(const State& state)
    {
        // Check if the distance error of this state has been updated
        if (correctedDerr.find(state) != correctedDerr.end()) {
            return correctedDerr[state];
        }

        Cost derr = dijkstraMaxH(state);

        updateDistanceErr(state, derr);

        return correctedDerr[state];
    }

    Cost heuristic(const State& state) { return dijkstraMaxH(state); }

    Cost epsilonHGlobal() { return curEpsilonH; }

    Cost epsilonDGlobal() { return curEpsilonD; }

    Cost epsilonHVarGlobal() { return curEpsilonHVar; }

    void updateEpsilons()
    {
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
        if (eps < 0)
            eps = 0;
        else if (eps > 1)
            eps = 1;

        epsilonHSum += eps;
        epsilonHSumSq += eps * eps;
        expansionCounter++;
    }

    void pushEpsilonDGlobal(double eps)
    {
        if (eps < 0)
            eps = 0;
        else if (eps > 1)
            eps = 1;

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

    /*Cost maxT(const State& startState, const Location& endLoc) const {*/
    // return max(abs(startState.getX() - endLoc.first) / maxXSpeed,
    // abs(startState.getY() - endLoc.second) / maxYSpeed);
    //}

    // Cost maxH(const State& state) const {
    // Cost c = COST_MAX;

    // for (const auto goalLoc : finishline) {
    // auto newC = maxT(state, goalLoc);
    // if (c > newC)
    // c = newC;
    //}

    // return c;
    /*}*/

    Cost dijkstraMaxH(const State& state) const
    {
        // cout << state;
        return static_cast<double>(dijkstraMap[static_cast<size_t>(
                 state.getX())][static_cast<size_t>(state.getY())]) /
               maxSpeed;
    }

    double getBranchingFactor() const { return 9; }

    bool isLegalLocation(int x, int y) const
    {
        return x >= 0 && y >= 0 && static_cast<size_t>(x) < mapWidth &&
               static_cast<size_t>(y) < mapHeight &&
               blockedCells.find(
                 Location(static_cast<size_t>(x), static_cast<size_t>(y))) ==
                 blockedCells.end();
    }

    bool isCollisionFree(int x, int y, int dx, int dy,
                         Location& lastLegalLocation) const
    {
        double distance = round(sqrt(pow(static_cast<double>(dx), 2.0) +
                                     pow(static_cast<double>(dy), 2.0)));

        double xRunning = double(x);
        double yRunning = double(y);

        double dt    = 1.0 / distance;
        bool   valid = true;

        double stepX = static_cast<double>(dx) * dt;
        double stepY = static_cast<double>(dy) * dt;

        for (int i = 1; i <= static_cast<int>(distance); i++) {
            xRunning += stepX;
            yRunning += stepY;

            if (!isLegalLocation(static_cast<int>(round(xRunning)),
                                 static_cast<int>(round(yRunning)))) {
                valid = false;
                break;
            }

            lastLegalLocation = Location(static_cast<size_t>(round(xRunning)),
                                         static_cast<size_t>(round(yRunning)));
        }

        return valid;
    }

    std::vector<State> successors(const State& state)
    {
        std::vector<State> successors;

        for (auto action : actions) {
            int newDX = state.getDX() + action.first;
            int newDY = state.getDY() + action.second;

            // check if dx, dy already 0?
            // otherwise will alway stay?
            // would it prefer to move so that be closer to goal
            if (newDX == 0 && newDY == 0) {
                if (state.getDX() == 0 && state.getDY() == 0)
                    continue;
                State succ(state.getX(), state.getY(), newDX, newDY);
                successors.push_back(succ);
                continue;
            }

            auto lastLegalLocation = Location(state.getX(), state.getY());
            if (isCollisionFree(state.getX(), state.getY(), newDX, newDY,
                                lastLegalLocation)) {
                State succ(state.getX() + newDX, state.getY() + newDY, newDX,
                           newDY);

                successors.push_back(succ);
            } else if (lastLegalLocation !=
                       Location(state.getX(), state.getY())) {
                // air bag
                State succ(static_cast<int>(lastLegalLocation.first),
                           static_cast<int>(lastLegalLocation.second), 0, 0);

                successors.push_back(succ);
            }
        }

        // air bag
        if (successors.size() == 0) {
            State succ(state.getX(), state.getY(), 0, 0);
            successors.push_back(succ);
        }

        // recording predecessor
        for (const auto& succ : successors) {
            predecessorsTable[succ].push_back(state);
        }

        return successors;
    }

    const std::vector<State> predecessors(const State& state) const
    {
        // DEBUG_MSG("preds table size: "<<predecessorsTable.size());
        if (predecessorsTable.find(state) != predecessorsTable.end())
            return predecessorsTable.at(state);
        return vector<State>();
    }

    const State getStartState() const { return startState; }

    Cost getEdgeCost(State) { return 1; }

    string getDomainInformation()
    {
        string info = "{ \"Domain\": \"race track\", \"widthxheight\": " +
                      std::to_string(mapHeight) + "x" +
                      std::to_string(mapHeight) + " }";
        return info;
    }

    string getDomainName() { return "RaceTrack"; }

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
        correctedH.clear();
        correctedDerr.clear();
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

    string getSubDomainName() const { return ""; }

private:
    void parseMap(std::ifstream& raceMap)
    {
        string line;
        getline(raceMap, line);
        stringstream ss(line);
        ss >> mapWidth;

        getline(raceMap, line);

        stringstream ss2(line);
        ss2 >> mapHeight;

        for (size_t y = 0; y < mapHeight; y++) {

            getline(raceMap, line);
            stringstream ss3(line);

            for (size_t x = 0; x < mapWidth; x++) {
                char cell;
                ss3 >> cell;

                switch (cell) {
                    case '#':
                        blockedCells.insert(Location(x, y));
                        break;
                    case '*':
                        finishline.insert(Location(x, y));
                        break;
                    case '@':
                        startLocation = Location(x, y);
                        break;
                }
            }
        }

        maxXSpeed = static_cast<double>(mapWidth) / 2;
        maxYSpeed = static_cast<double>(mapHeight) / 2;
        maxSpeed  = max(maxXSpeed, maxYSpeed);

        startState = State(static_cast<int>(startLocation.first),
                           static_cast<int>(startLocation.second), 0, 0);
        // cout << "size: " << mapWidth << "x" << mapHeight << "\n";
        // cout << "blocked: " << blockedCells.size() << "\n";
        // cout << "finish: " << finishline.size() << "\n";
    }

    void initilaizeActions()
    {
        actions = {make_pair(-1, 1),  make_pair(0, 1),  make_pair(1, 1),
                   make_pair(-1, 0),  make_pair(0, 0),  make_pair(1, 0),
                   make_pair(-1, -1), make_pair(0, -1), make_pair(1, -1)};
    }

    void resetInitialState(std::istream& input)
    {
        string line;
        // skip the first line
        getline(input, line);
        getline(input, line);
        stringstream ss(line);
        int          x, y, dx, dy;
        ss >> x;
        ss >> y;
        ss >> dx;
        ss >> dy;

        startState = State(x, y, dx, dy);
        // cout << "start" << startState << "\n";
    }

    void computeDijkstraMap()
    {
        vector<size_t> col(mapHeight, std::numeric_limits<size_t>::max());
        dijkstraMap = vector<vector<size_t>>(mapWidth, col);

        for (const auto& g : finishline) {
            dijkstraOneGoal(g, dijkstraMap);
        }

        // visualize the dijkstra map (for debug usage)
        /*vector<size_t>         rotateCol(mapWidth, INT_MAX);*/
        // vector<vector<size_t>> rotatedMap(mapHeight, rotateCol);
        // for (size_t i = 0; i < rotatedMap.size(); i++) {
        // for (size_t j = 0; j < rotateCol.size(); j++) {
        // rotatedMap[i][j] = dijkstraMap[j][i];
        //}
        //}

        // for (auto r : rotatedMap) {
        // for (auto c : r) {
        // if (c > 100000)
        // cout << std::setw(5) << "x";
        // else
        // cout << std::setw(5) << c;
        //}
        // cout << "\n";
        /*}*/
    }

    void dijkstraOneGoal(const Location          goal,
                         vector<vector<size_t>>& dijkstraMap_)
    {
        DijkstraNode start(goal, 0);

        priority_queue<DijkstraNode, vector<DijkstraNode>, CompareCost> open;
        // priority_queue<DijkstraNode> open;
        unordered_set<Location, pair_hash> closed;

        open.push(start);
        closed.insert(start.loc);

        while (!open.empty()) {
            auto n = open.top();
            open.pop();

            if (dijkstraMap_[n.loc.first][n.loc.second] > n.cost) {
                dijkstraMap_[n.loc.first][n.loc.second] = n.cost;
            }

            auto kids = getLegalKids(n);

            for (auto kid : kids) {
                if (closed.find(kid.loc) == closed.end()) {
                    open.push(kid);
                    closed.insert(kid.loc);
                }
            }
        }
    }

    struct DijkstraNode
    {
        Location loc;
        size_t   cost;

        DijkstraNode(Location l, size_t c)
            : loc(l)
            , cost(c)
        {}
    };

    struct CompareCost
    {
        bool operator()(DijkstraNode const& n1, DijkstraNode const& n2)
        {
            // return "true" if "n1" is ordered
            // before "n2" in a max heap, for example:
            // be careful, min heap should be return false, for example:
            // here is min heap for cost
            return n1.cost > n2.cost;
        }
    };

    vector<DijkstraNode> getLegalKids(DijkstraNode n)
    {

        vector<DijkstraNode> ret;
        auto                 x_ = static_cast<int>(n.loc.first);
        auto                 y_ = static_cast<int>(n.loc.second);

        if (isLegalLocation(x_ + 1, y_)) {
            Location loc(n.loc.first + 1, y_);
            ret.push_back(DijkstraNode(loc, n.cost + 1));
        }

        if (isLegalLocation(x_, y_ + 1)) {
            Location loc(x_, y_ + 1);
            ret.push_back(DijkstraNode(loc, n.cost + 1));
        }

        if (isLegalLocation(x_ - 1, y_)) {
            Location loc(x_ - 1, y_);
            ret.push_back(DijkstraNode(loc, n.cost + 1));
        }

        if (isLegalLocation(x_, y_ - 1)) {
            Location loc(x_, y_ - 1);
            ret.push_back(DijkstraNode(loc, n.cost + 1));
        }

        return ret;
    }

    std::unordered_set<Location, pair_hash> blockedCells;
    std::unordered_set<Location, pair_hash> finishline;
    vector<pair<int, int>>                  actions;
    vector<vector<size_t>>                  dijkstraMap;
    size_t                                  mapWidth;
    size_t                                  mapHeight;
    double                                  maxXSpeed;
    double                                  maxYSpeed;
    double                                  maxSpeed;
    Location                                startLocation;
    State                                   startState;

    SlidingWindow<int>                             expansionDelayWindow;
    unordered_map<State, Cost, HashState>          correctedH;
    unordered_map<State, Cost, HashState>          correctedD;
    unordered_map<State, Cost, HashState>          correctedDerr;
    unordered_map<State, vector<State>, HashState> predecessorsTable;

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
