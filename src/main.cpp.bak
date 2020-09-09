#include "search/IDAStarSearch.h"
#include "search/LsslrtastarSearch.h"
#include "search/WAStarSearch.h"
#include "utility/cxxopts/include/cxxopts.hpp"
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <typeindex>

using namespace std;

int main(int argc, char** argv)
{

    cxxopts::Options options(
      "./distributionPractice",
      "This is a suboptimal search to collect observed states");

    options.add_options()

      ("d,domain", "domain type: randomtree, tile, pancake, racetrack",
       cxxopts::value<std::string>()->default_value("pancake"))

        ("s,subdomain",
         "puzzle type: uniform, inverse, heavy, sqrt; "
         "pancake type: regular, heavy, sumheavy;"
         "racetrack map : barto-big, barto-bigger, hanse-bigger-double, "
         "uniform",
         cxxopts::value<std::string>()->default_value("heavy"))

          ("a,alg", "suboptimal algorithm: wastar, lsslrtastar",
           cxxopts::value<std::string>()->default_value("wastar"))

            ("p,par", "weight for weighted A*, lookahead for lsslrta*",
             cxxopts::value<double>()->default_value("2"))

              ("o,performenceOut", "performence Out file",
               cxxopts::value<std::string>())

                ("v,pathOut", "path Out file", cxxopts::value<std::string>())

                  ("h,help", "Print usage");

    auto args = options.parse(argc, argv);

    if (args.count("help")) {
        std::cout << options.help() << std::endl;
        exit(0);
    }

    auto d    = args["domain"].as<std::string>();
    auto sd   = args["subdomain"].as<std::string>();
    auto alg  = args["alg"].as<std::string>();
    auto para = args["par"].as<double>();

    Search* searchPtr;

    // create domain world and search algorithm
    if (d == "randomtree") {
        TreeWorld* world     = new TreeWorld(cin);
        auto       lookahead = (int)para;
        searchPtr = new LssLRTAStarSearch<TreeWorld>(*world, "a-star", "learn",
                                                     "minimin", lookahead);

    } else if (d == "tile") {
        SlidingTilePuzzle* world;

        if (sd == "uniform") {
            world = new SlidingTilePuzzle(cin);
        } else if (sd == "heavy") {
            world = new HeavyTilePuzzle(cin);
        } else if (sd == "inverse") {
            world = new InverseTilePuzzle(cin);
        } else {
            cout << "wrong tile type!\n";
            exit(1);
        }

        if (alg == "wastar") {
            auto weight = para;
            searchPtr   = new WAStarSearch<SlidingTilePuzzle>(*world, weight);
        } else if (alg == "lsslrtastar") {
            auto lookahead = (int)para;
            searchPtr      = new LssLRTAStarSearch<SlidingTilePuzzle>(
              *world, "a-star", "learn", "minimin", lookahead);
        }
    } else if (d == "pancake") {
        PancakePuzzle* world;

        world = new PancakePuzzle(cin);

        if (sd == "heavy") {
            world->setVariant(1);
        } else if (sd == "sumheavy") {
            world->setVariant(2);
        }

        if (alg == "wastar") {
            auto weight = para;
            searchPtr   = new WAStarSearch<PancakePuzzle>(*world, weight);
        } else if (alg == "lsslrtastar") {
            auto lookahead = (int)para;
            searchPtr      = new LssLRTAStarSearch<PancakePuzzle>(
              *world, "a-star", "learn", "minimin", lookahead);
        }

        else if (alg == "idastar") {
            searchPtr = new IDAStarSearch<PancakePuzzle>(*world);
        }
    } else if (d == "racetrack") {
        RaceTrack* world;

        string mapFile = "/home/aifs1/gu/phd/research/workingPaper/"
                         "realtime-nancy/worlds/racetrack/map/" +
                         sd + ".track";

        ifstream map(mapFile);

        if (!map.good()) {
            cout << "map file not exist: " << mapFile << endl;
            exit(1);
        }

        world = new RaceTrack(map, cin);

        if (alg == "wastar") {
            auto weight = para;
            searchPtr   = new WAStarSearch<RaceTrack>(*world, weight);
        } else if (alg == "lsslrtastar") {
            auto lookahead = (int)para;
            searchPtr      = new LssLRTAStarSearch<RaceTrack>(
              *world, "a-star", "learn", "minimin", lookahead);
        }

        else if (alg == "idastar") {
            searchPtr = new IDAStarSearch<RaceTrack>(*world);
        }
    } else {
        cout << "unknow domain!\n";
        std::cout << options.help() << std::endl;
        exit(0);
    }

    // perform search
    auto res = searchPtr->doSearch();

    // dumpout result and observed states
    if (args.count("performenceOut")) {
        ofstream out(args["performenceOut"].as<std::string>());

        out << res.nodesExpanded << " " << res.solutionFound << " "
            << res.solutionCost << endl;

        searchPtr->dumpClosedList(out);

        out.close();

    } else {
        cout << res.nodesExpanded << " " << res.solutionFound << " "
             << res.solutionCost << " " << res.initialH << endl;
    }

    // dumpout solution path
    if (args.count("pathOut")) {
        ofstream out(args["pathOut"].as<std::string>());
        out << res.soltuionPath << endl;
        out.close();
    }
}
