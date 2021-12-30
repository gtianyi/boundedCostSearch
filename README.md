# Bounded Cost Heuristic Search

## Welcome to bounded cost heuristic search project!
The purpose of the project is to implement several state-of-the-art BCS algorithms and run benchmark with classical search domains such as Sliding Tiles, Pancakes. 

# Paper
[1] Maximilian Fickert, Tianyi Gu, and Wheeler Ruml, Bounded-Cost Search Using Estimates of Uncertainty. Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence (IJCAI-21), 2021.

[[pdf]](http://gtianyi.github.io/publication/xes-IJCAI-21.pdf)  [[slides]](http://gtianyi.github.io/slides/ijcai_21_xes_slides.pdf) [[poster]](http://gtianyi.github.io/slides/xes-poster-ijcai21.pdf)
[[talk]](https://ijcai-21.org/videos-slides/?video=994)
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
conan install ../boundedCostSearch --build missing
cmake -GNinja ../boundedCostSearch
ninja bcs 
```

## Run
```
cd <repo>
cd ../build
bin/bcs -h
This is a bounded cost search benchmark
Usage:
  ./bcs [OPTION...]

  -d, --domain arg          domain type: randomtree, tile, pancake,
                            racetrack, vaccumworld (default: vaccumworld)
  -s, --subdomain arg       puzzle type: uniform, inverse, heavy, sqrt;
                            pancake type: regular, heavy, sumheavy; racetrack map :
                            barto-big, barto-bigger, hanse-bigger-double,
                            vaccumworld: uniform, heavy;  (default: uniform)
  -a, --alg arg             baseline algorithm: pts, bees, beeps; new
                            algorithm: ptshhat, ptsnancy, beepsnancy; other
                            algorithm: astar, wastar;  (default: ptsnancy)
  -b, --bound arg           cost bound (default: 10)
  -i, --instance arg        instance file name (default: 2-4x4.st)
  -w, --weight arg          weight for wA* baseline (default: 2)
  -o, --performenceOut arg  performence Out file
  -v, --pathOut arg         path Out file
  -h, --help                Print usage

```

## Experiments Pipeline
1. check if the bounded cost algorithm can solve single instance
```
cd 
cd <repo>
cd ../build
bin/bcs -h
```

2. Compute optimal solution for all instances
```
cd <repo>/script
python optimalSolver.py -h
optional arguments:
  -h, --help    show this help message and exit
  -d DOMAIN     domain: tile(default), pancake, racetrack
  -s SUBDOMAIN  subdomain: tile: uniform(default), heavy, inverse; 
                           pancake: regular, heavy; 
                           racetrack : barto-big,uniform-small, 
                                       barto-bigger, hanse-bigger-double
  -z SIZE       domain size (default: 4)
```

check if the optimal solution json is generated correctly
```
cd <repo>
cd ../optimalSolution/
ls -l
total 52
drwxrwxr-x  2 gu gu 4096 Oct  1 15:55 .
drwxrwxr-x 12 gu gu 4096 Sep 30 09:26 ..
-rw-rw-r--  1 gu gu 5676 Sep 29 12:03 pancake.regular.json
-rw-rw-r--  1 gu gu  741 Oct  1 15:17 racetrack.barto-bigger.json
-rw-rw-r--  1 gu gu  666 Oct  1 07:02 racetrack.barto-big.json
-rw-rw-r--  1 gu gu  766 Oct  1 15:55 racetrack.hansen-bigger.json
-rw-rw-r--  1 gu gu  616 Oct  1 15:43 racetrack.uniform.json
-rw-rw-r--  1 gu gu  766 Oct  1 07:03 racetrack.uniform-small.json
-rw-rw-r--  1 gu gu 1992 Sep 25 14:35 tile.heavy.json
-rw-rw-r--  1 gu gu 1892 Sep 22 12:51 tile.uniform.json
```

3. run experiment script   
(better check if it can run correctly for a single instance befor batch run)
```
cd <repo>/script/testHarnesses
./singleThread-boundedCostSolver.sh -h

[-f instance]                    default: 1
[-n # of instances to test]      default: 1
[-d domain]                      default: tile
[-s subdomain]                   default: uniform
[-z domain size]                 default: 4
[-u boundedCost solver]
 support list,eg: -u a1 -u a2    default: pts ptshhat ptsnancy bees astar wastar
[-b bound percent wrt optimal]
 support list,eg: -b 10 -b 300   default: 60 80 100 120 140 160 180 200 220 240 
                                          260 280 300 320 340 360 380 400 420 
                                          440 460 480 500 520 540 560 580 600
[-t time limit]                  default: 1800 (seconds)
[-m memory limit]                default: 7(GB)
[-h help]
```

4. fix json format error caused by batch run on ai cluster 
```
cd <repo>/script
python fixJson.py -h

usage: fixJson.py [-h] [-d DOMAIN] [-s SUBDOMAIN] [-a ALGORITHMS]
optional arguments:
  -h, --help     show this help message and exit
  -d DOMAIN      domain: tile(default), pancake, racetrack
  -s SUBDOMAIN   subdomain: tile: uniform(default), heavy, inverse; 
                            pancake: regular, heavy; 
                            racetrack : barto-big,uniform-small, 
                                        barto-bigger, hanse-bigger-double
  -a ALGORITHMS  algorithms: wastar, astar, pts, ptshhat, ptsnancy, bees default(all)
```

5. plot results
```
cd <repo>/script/plot
boundedCostPlot.py -h
usage: boundedCostPlot.py [-h] [-d DOMAIN] [-s SUBDOMAIN] [-b BOUNDPERCENTSTART] [-z SIZE] [-t PLOTTYPE]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN             domain: tile(default), pancake, racetrack
  -s SUBDOMAIN          subdomain: tile: uniform(default), heavy, inverse; 
                                   pancake: regular, heavy; 
                                   racetrack : barto-big,uniform-small, 
                                               barto-bigger, hanse-bigger-double
  -b BOUNDPERCENTSTART  bound percent start: anything above 1.2
  -z SIZE               domain size (default: 4)
  -t PLOTTYPE           plot type, nodeGen, cpu, coverage, nodeGenDiff(default)
```

# Problem Instances
All the instances can be found [here](https://github.com/gtianyi/searchDomainInstanceFiles)
