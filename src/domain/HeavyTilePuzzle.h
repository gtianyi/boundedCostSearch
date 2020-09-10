#pragma once
#include "SlidingTilePuzzle.h"

class HeavyTilePuzzle : public SlidingTilePuzzle
{
public:
    using SlidingTilePuzzle::SlidingTilePuzzle;

    Cost getEdgeCost(State state) { return state.getFace(); }

    Cost heuristic(const State& state)
    {
        // Check if the heuristic of this state has been updated
        if (correctedH.find(state) != correctedH.end()) {
            return correctedH[state];
        }

        Cost h = manhattanDistanceWithFaceCost(state);

        updateHeuristic(state, h);

        return correctedH[state];
    }

    Cost heuristic_no_recording(const State& state)
    {
        return manhattanDistanceWithFaceCost(state);
    }

    Cost manhattanDistanceWithFaceCost(const State& state) const
    {
        Cost manhattanSum = 0;

        for (size_t r = 0; r < size; r++) {
            for (size_t c = 0; c < size; c++) {
                auto value = static_cast<size_t>(state.getBoard()[r][c]);
                if (value == 0) {
                    continue;
                }

                manhattanSum +=
                  static_cast<double>(value) * fabs(value / size - r) +
                  fabs(value % size - c);
                // cout << "value " << value << " sum " << manhattanSum << endl;
            }
        }

        return manhattanSum;
    }
};
