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

### Conan Setup

The [Conan](https://conan.io) package manager is used to manage project's external
dependencies. This section describes the process of setting it up.  Installation is as simple as running

```
sudo pip3 install conan
```

#### Creating Profiles
We need to setup a Conan profile — a list of properties that characterize the
environment.  The following commands will create a new profile called `default` and set it up
for Ubuntu 16.04 environment.  If you are using several profiles, you may want to choose a
more descriptive name for it.
```
# create new profile called 'default'
conan profile new default --detect
# modify settings of the 'default' profile
conan profile update settings.compiler.version=5.4 default
conan profile update settings.compiler.libcxx=libstdc++11 default
```
At the moment, there exist precompiled versions of the packages needed by
the project for this particular profile:

```
os=Linux
arch=x86_64
compiler=gcc
compiler.version=5.4
compiler.libcxx=libstdc++11
build_type=Release
```

Note that you can have multiple profiles and also modify existing ones when needed.
For more details see the Conan [Getting Started](https://docs.conan.io/en/latest/getting_started.html) guide.


## Compilation
```
git clone git@github.com:gtianyi/boundedCostSearch.git
mkdir build && cd build
conan install ../boundedCostSearch
cmake -GNinja ../boundedCostSearch
ninja bcs 
```

## Run
```
bin/bcs -h
This is a bounded cost search benchmark
Usage:
  ./bcs [OPTION...]

  -d, --domain arg          domain type: randomtree, tile, pancake, racetrack
                            (default: tile)
  -s, --subdomain arg       puzzle type: uniform, inverse, heavy, sqrt;
                            pancake type: regular, heavy, sumheavy;racetrack map :
                            barto-big, barto-bigger, hanse-bigger-double,
                            uniform (default: uniform)
  -a, --alg arg             suboptimal algorithm: pts, ptshhat, ptsnancy
                            (default: ptsnancy)
  -b, --bound arg           cost bound (default: 10)
  -i, --instance arg        instance file name (default: 2-4x4.st)
  -o, --performenceOut arg  performence Out file
  -v, --pathOut arg         path Out file
  -h, --help                Print usage
```
