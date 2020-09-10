#pragma once
#include <cmath>
#include <limits>

using namespace std;

class RandomGenerator
{
    long          lo;
    long          hi;
    unsigned long seed;
    long          test;
    const long    a = 48271.0;
    const long    m = 2147483647.0;
    const long    q = m / a;
    const long    r = m % a;

public:
    RandomGenerator()
        : seed(0)
    {}
    RandomGenerator(unsigned long seed_)
        : seed(seed_){};
    unsigned long getSeed() { return seed; }
    void          setSeed(unsigned long s) { seed = s; }
    double        random()
    {
        hi   = static_cast<long>(seed) / q;
        lo   = static_cast<long>(seed) % q;
        test = a * lo - r * hi;
        if (test > 0.0)
            seed = static_cast<unsigned long>(test);
        else
            seed = static_cast<unsigned long>(test + m);
        return (static_cast<double>(seed) / static_cast<double>(m));
    }
};
