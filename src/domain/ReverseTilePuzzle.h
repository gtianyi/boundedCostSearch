#pragma once
#include "SlidingTilePuzzle.h"

class ReverseTilePuzzle : public SlidingTilePuzzle
{
public:
    using SlidingTilePuzzle::SlidingTilePuzzle;

    Cost getEdgeCost(State state) { return 16 - state.getFace(); }

    Cost heuristic(const State& state)
    {
        return manhattanDistanceWithReverseFaceCost(state);
    }

    Cost manhattanDistanceWithReverseFaceCost(const State& state) const
    {
        Cost manhattanSum = 0;

        for (size_t r = 0; r < size; r++) {
            for (size_t c = 0; c < size; c++) {
                int value = state.getBoard()[r][c];
                if (value == 0) {
                    continue;
                }

                manhattanSum +=
                  (16 - static_cast<double>(value)) *
                  (fabs(value / static_cast<int>(size) - static_cast<int>(r)) +
                   fabs(value % static_cast<int>(size) - static_cast<int>(c)));
                // cout << "value " << value << " sum " << manhattanSum << endl;
            }
        }

        return manhattanSum;
    }
};
