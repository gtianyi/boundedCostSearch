# Bounded Cost Heuristic Search

## Welcome to bounded cost heuristic search project!
The purpose of the project is to implement several state-of-the-art BCS algorithms and run benchmark with classical search domains such as Sliding Tiles, Pancakes. 

## Prerequisites
We use `clang` ecosystem to compile and develop the codebase. You can install necessary components by running
```
sudo apt install clang-6.0 clang-tidy-6.0 clang-format-6.0
```

Install up-to-date CMake version. We also use `cmake-format` to keep our CMake files tidy.
```
sudo pip install cmake
sudo pip install cmake-format
```

## Compilation
```
git clone <repo>
mkdir build && cd build
cmake -GNinja ../<repo>
ninja <executable> 
```

## Run
```
bin/<executable>
```
