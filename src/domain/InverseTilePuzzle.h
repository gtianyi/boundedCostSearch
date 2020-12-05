#pragma once
#include "SlidingTilePuzzle.h"

class InverseTilePuzzle : public SlidingTilePuzzle
{
public:
    using SlidingTilePuzzle::SlidingTilePuzzle;

    Cost getEdgeCost(State state)
    {
        return 1.0 / static_cast<double>(state.getFace());
    }

    Cost heuristic(const State& state)
    {
        return manhattanDistanceWithInverseFaceCost(state);
    }

    Cost manhattanDistanceWithInverseFaceCost(const State& state) const
    {
        Cost manhattanSum = 0;

        for (size_t r = 0; r < size; r++) {
            for (size_t c = 0; c < size; c++) {
                auto value = state.getBoard()[r][c];
                if (value == 0) {
                    continue;
                }

                manhattanSum +=
                  (1.0 / static_cast<double>(value)) *
                  (fabs(value / static_cast<int>(size) - static_cast<int>(r)) +
                   fabs(value % static_cast<int>(size) - static_cast<int>(c)));
                // cout << "value " << value << " sum " << manhattanSum << endl;
            }
        }

        return manhattanSum;
    }
};
