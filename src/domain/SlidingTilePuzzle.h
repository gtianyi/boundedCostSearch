#pragma once
#include "../utility/SlidingWindow.h"
#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <ostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include <bitset>

using namespace std;

class SlidingTilePuzzle
{
public:
    typedef double        Cost;
    static constexpr Cost COST_MAX = std::numeric_limits<Cost>::max();

    class State
    {
    public:
        State() {}

        State(std::vector<std::vector<int>> b, char l)
            : board(b)
            , label(l)
        {
            generateKey();
        }

        State(std::vector<std::vector<int>> b, char l, int f)
            : board(b)
            , label(l)
            , movedFace(f)
        {
            generateKey();
        }

        friend std::ostream& operator<<(std::ostream&                   stream,
                                        const SlidingTilePuzzle::State& state)
        {
            for (unsigned int r = 0; r < state.getBoard().size(); r++) {
                for (unsigned int c = 0; c < state.getBoard()[r].size(); c++) {
                    stream << std::setw(3) << state.getBoard()[r][c] << " ";
                }
                stream << endl;
            }
            return stream;
        }

        bool operator==(const State& state) const
        {
            return board == state.getBoard();
        }

        bool operator!=(const State& state) const
        {
            return board != state.getBoard();
        }

        void generateKey()
        {
            // This will provide a unique hash for every state in the 15 puzzle,
            // Other puzzle variants may/will see collisions...
            unsigned long long val = 0;
            for (unsigned int r = 0; r < board.size(); r++) {
                for (unsigned int c = 0; c < board[r].size(); c++) {
                    val = val << 4;
                    val = val | static_cast<unsigned long long>(board[r][c]);
                }
            }
            theKey = val;
        }

        unsigned long long key() const { return theKey; }

        std::string toString() const
        {
            std::string s = "";
            for (unsigned int r = 0; r < board.size(); r++) {
                for (unsigned int c = 0; c < board[r].size(); c++) {
                    s += std::to_string(board[r][c]) + " ";
                }
                s += "\n";
            }
            return s;
        }

        void dumpToProblemFile(ofstream& f)
        {
            f << "4 4\n";
            f << "starting positions for each tile:\n";

            for (unsigned int r = 0; r < board.size(); r++) {
                for (unsigned int c = 0; c < board[r].size(); c++) {
                    // assert(board[r][c] >= 0);
                    // assert(board[r][c] < 16);
                    f << board[r][c] << "\n";
                }
            }

            f << "goal positions:\n";

            for (int i = 0; i < 16; i++) {
                f << i << "\n";
            }
        }

        std::vector<std::vector<int>> getBoard() const { return board; }

        char getLabel() const { return label; }

        int getFace() const { return movedFace; }

        void markStart() { label = 's'; }

    private:
        std::vector<std::vector<int>> board;
        char                          label;
        int                           movedFace;
        unsigned long long            theKey =
          std::numeric_limits<unsigned long long>::max();
    };

    struct HashState
    {
        std::size_t operator()(const State& s) const
        {
            return s.key();

            /*This tabulation hashing causes mad bugs and non-deterministic
            behavior. Fix later, use shitty hash now and get results...
            unsigned int hash = 0;

            unsigned long long key = s.key();

            // For each byte in the key...
            for (int i = 7; i >= 0; i--)
            {
                    unsigned int byte = key >> (i * 8) & 0x000000FF;
                    hash = leftRotate(hash, 1);
                    hash = hash ^ SlidingTilePuzzle::table[byte];
            }
            cout << key << " " << hash << endl;
            return hash;
            */
        }

        std::size_t leftRotate(std::size_t n, unsigned int d) const
        {
            return (n << d) | (n >> (32 - d));
        }
    };

    SlidingTilePuzzle()
        : size(4)
    {}

    SlidingTilePuzzle(std::istream& input)
    {
        // Get the dimensions of the puzzle
        string line;
        getline(input, line);
        stringstream ss(line);
        // Get the first dimension...
        ss >> size;
        // We don't give a shit about the second dimension,
        // because every puzzle should be square.

        // Skip the next line
        getline(input, line);

        // Initialize the nxn puzzle board
        std::vector<int>              rows(static_cast<size_t>(size), 0);
        std::vector<std::vector<int>> board(static_cast<size_t>(size), rows);
        startBoard = board;
        endBoard   = board;

        // Following lines are the input puzzle...
        size_t r = 0;
        size_t c = 0;

        for (size_t i = 0; i < size * size; i++) {
            c = i % size;

            getline(input, line);
            int          tile;
            stringstream ss2(line);
            ss2 >> tile;

            startBoard[r][c] = tile;

            if (c >= size - 1) {
                r++;
            }
        }

        // Skip the next line
        getline(input, line);

        // Following lines are the goal puzzle...
        r = 0;
        c = 0;

        for (size_t i = 0; i < size * size; i++) {
            c = i % size;

            getline(input, line);
            int          tile;
            stringstream ss2(line);
            ss2 >> tile;

            endBoard[r][c] = tile;

            if (c >= size - 1) {
                r++;
            }
        }

        // If the table of random numbers for the hash function hasn't been
        // filled
        // then it should be filled now...
        if (SlidingTilePuzzle::table.empty()) {
            srand(static_cast<unsigned int>(time(NULL)));
            for (int i = 0; i < 256; i++) {
                table.push_back(rand());
            }
        }

        startState = State(startBoard, 's');
    }

    virtual ~SlidingTilePuzzle() {}

    bool isGoal(const State& s) const
    {
        if (s.getBoard() == endBoard) {
            return true;
        }

        return false;
    }

    Cost distance(const State& state)
    {
        // Check if the distance of this state has been updated
        if (correctedD.find(state) != correctedD.end()) {
            return correctedD[state];
        }

        Cost d = manhattanDistance(state);

        updateDistance(state, d);

        return correctedD[state];
    }

    Cost distanceErr(const State& state)
    {
        // Check if the distance error of this state has been updated
        if (correctedDerr.find(state) != correctedDerr.end()) {
            return correctedDerr[state];
        }

        Cost derr = manhattanDistance(state);

        updateDistanceErr(state, derr);

        return correctedDerr[state];
    }

    virtual Cost heuristic(const State& state)
    {
        // Check if the heuristic of this state has been updated
        if (correctedH.find(state) != correctedH.end()) {
            return correctedH[state];
        }

        Cost h = manhattanDistance(state);

        updateHeuristic(state, h);

        return correctedH[state];
    }

    virtual Cost heuristic_no_recording(const State& state)
    {
        return manhattanDistance(state);
    }

    Cost epsilonHGlobal() { return curEpsilonH; }

    Cost epsilonDGlobal() { return curEpsilonD; }

    void updateEpsilons()
    {
        if (expansionCounter == 0) {
            curEpsilonD = 0;
            curEpsilonH = 0;

            return;
        }

        curEpsilonD = epsilonDSum / expansionCounter;

        curEpsilonH = epsilonHSum / expansionCounter;
    }

    void pushEpsilonHGlobal(double eps)
    {
        if (eps < 0)
            eps = 0;
        else if (eps > 1)
            eps = 1;

        epsilonHSum += eps;
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

    Cost manhattanDistance(const State& state) const
    {
        Cost manhattanSum = 0;

        for (size_t r = 0; r < size; r++) {
            for (size_t c = 0; c < size; c++) {
                size_t value = static_cast<size_t>(state.getBoard()[r][c]);
                if (value == 0) {
                    continue;
                }

                manhattanSum += fabs(value / size - r) + fabs(value % size - c);
                // cout << value << " sum " << manhattanSum << endl;
            }
        }

        return manhattanSum;
    }

    double getBranchingFactor() const { return 2.13; }

    void moveUp(std::vector<State>&           succs,
                std::vector<std::vector<int>> board) const
    {
        size_t r = 0;
        size_t c = 0;
        // Find the location of the blank space
        bool found = false;
        for (r = 0; r < size; r++) {
            for (c = 0; c < size; c++) {
                if (board[r][c] == 0) {
                    found = true;
                    break;
                }
            }

            if (found)
                break;
        }

        // Now try to move the blank tile up one row...
        if (r > 0) {
            std::swap(board[r][c], board[r - 1][c]);
            succs.push_back(State(board, 'U', board[r][c]));
        }
    }

    void moveDown(std::vector<State>&           succs,
                  std::vector<std::vector<int>> board) const
    {
        size_t r = 0;
        size_t c = 0;
        // Find the location of the blank space
        bool found = false;
        for (r = 0; r < size; r++) {
            for (c = 0; c < size; c++) {
                if (board[r][c] == 0) {
                    found = true;
                    break;
                }
            }

            if (found)
                break;
        }

        // Now try to move the blank tile down one row...
        if (r + 1 < size) {
            std::swap(board[r][c], board[r + 1][c]);
            succs.push_back(State(board, 'D', board[r][c]));
        }
    }

    void moveLeft(std::vector<State>&           succs,
                  std::vector<std::vector<int>> board) const
    {
        size_t r = 0;
        size_t c = 0;
        // Find the location of the blank space
        bool found = false;
        for (r = 0; r < size; r++) {
            for (c = 0; c < size; c++) {
                if (board[r][c] == 0) {
                    found = true;
                    break;
                }
            }

            if (found)
                break;
        }

        // Now try to move the blank tile left one column...
        if (c > 0) {
            std::swap(board[r][c], board[r][c - 1]);
            succs.push_back(State(board, 'L', board[r][c]));
        }
    }

    void moveRight(std::vector<State>&           succs,
                   std::vector<std::vector<int>> board) const
    {
        size_t r = 0;
        size_t c = 0;
        // Find the location of the blank space
        bool found = false;
        for (r = 0; r < size; r++) {
            for (c = 0; c < size; c++) {
                if (board[r][c] == 0) {
                    found = true;
                    break;
                }
            }

            if (found)
                break;
        }

        // Now try to move the blank tile left one column...
        if (c + 1 < size) {
            std::swap(board[r][c], board[r][c + 1]);
            succs.push_back(State(board, 'R', board[r][c]));
        }
    }

    std::vector<State> successors(const State& state) const
    {
        std::vector<State> successors;

        // Don't allow inverse actions, to cut down on branching factor

        if (state.getLabel() != 'D')
            moveUp(successors, state.getBoard());
        if (state.getLabel() != 'U')
            moveDown(successors, state.getBoard());
        if (state.getLabel() != 'R')
            moveLeft(successors, state.getBoard());
        if (state.getLabel() != 'L')
            moveRight(successors, state.getBoard());

        return successors;
    }

    std::vector<State> predecessors(const State& state) const
    {
        std::vector<State> predecessors;

        moveUp(predecessors, state.getBoard());
        moveDown(predecessors, state.getBoard());
        moveLeft(predecessors, state.getBoard());
        moveRight(predecessors, state.getBoard());

        return predecessors;
    }

    const State getStartState() const { return startState; }

    // heavy, inverse, make a extansion class, and overwrite this method
    virtual Cost getEdgeCost(State) { return 1; }

    string getDomainInformation()
    {
        string info =
          "{ \"Domain\": \"Sliding Tile Puzzle\", \"Dimensions\": " +
          std::to_string(size) + "x" + std::to_string(size) + " }";
        return info;
    }

    string getDomainName() { return "SlidingTilePuzzle"; }

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

    std::vector<std::vector<int>>         startBoard;
    std::vector<std::vector<int>>         endBoard;
    size_t                                size;
    State                                 startState;
    SlidingWindow<int>                    expansionDelayWindow;
    unordered_map<State, Cost, HashState> correctedH;
    unordered_map<State, Cost, HashState> correctedD;
    unordered_map<State, Cost, HashState> correctedDerr;

    double epsilonHSum;
    double epsilonDSum;
    double curEpsilonH;
    double curEpsilonD;
    double expansionCounter;

    string expansionPolicy;
    int    lookahead;

    static vector<int> table;
};

vector<int> SlidingTilePuzzle::table;
