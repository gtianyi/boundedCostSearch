#pragma once
#include <bitset>
using namespace std;

struct pair_hash
{
    template<class T1, class T2>
    std::size_t operator()(std::pair<T1, T2> const& pair) const
    {
        std::size_t h1 = std::hash<T1>()(pair.first);
        std::size_t h2 = std::hash<T2>()(pair.second);

        return h1 ^ h2;
    }
};

template<class T>
inline void hash_combine(unsigned long long& seed, const T& v)
{
    std::hash<T> hasher;
    seed ^= hasher(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}
