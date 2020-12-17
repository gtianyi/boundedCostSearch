#pragma once
#include "SlidingTilePuzzle.h"

class SqrtTilePuzzle : public SlidingTilePuzzle
{
public:
    using SlidingTilePuzzle::SlidingTilePuzzle;

    Cost getEdgeCost(State state)
    {
        return sqrt(static_cast<double>(state.getFace()));
    }

    Cost heuristic(const State& state)
    {
        return manhattanDistanceWithSqrtFaceCost(state);
    }

    Cost manhattanDistanceWithSqrtFaceCost(const State& state) const
    {
        Cost manhattanSum = 0;

        for (size_t r = 0; r < size; r++) {
            for (size_t c = 0; c < size; c++) {
                auto value = state.getBoard()[r][c];
                if (value == 0) {
                    continue;
                }

                manhattanSum +=
                  sqrt(static_cast<double>(value)) *
                  (fabs(value / static_cast<int>(size) - static_cast<int>(r)) +
                   fabs(value % static_cast<int>(size) - static_cast<int>(c)));
                // cout << "value " << value << " sum " << manhattanSum << endl;
            }
        }

        return manhattanSum;
    }
};
