#include "BoundedCostSearch.hpp"

#include <cxxopts.hpp>
#include <nlohmann/json.hpp>

#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <typeindex>

using namespace std;

int main(int argc, char** argv)
{

    cxxopts::Options options("./bcs",
                             "This is a bounded cost search benchmark");

    auto optionAdder = options.add_options();

    optionAdder(
      "d,domain",
      "domain type: randomtree, tile, pancake, racetrack, vaccumworld",
      cxxopts::value<std::string>()->default_value("vaccumworld"));

    optionAdder("s,subdomain",
                "puzzle type: uniform, inverse, heavy, sqrt; "
                "pancake type: regular, heavy, sumheavy;"
                "racetrack map : barto-big, barto-bigger, hanse-bigger-double, "
                "vaccumworld: uniform, heavy ",
                cxxopts::value<std::string>()->default_value("uniform"));

    optionAdder("a,alg", "suboptimal algorithm: pts, ptshhat, ptsnancy",
                cxxopts::value<std::string>()->default_value("ptsnancy"));

    optionAdder("b,bound", "cost bound",
                cxxopts::value<double>()->default_value("10"));

    optionAdder("i,instance", "instance file name",
                cxxopts::value<std::string>()->default_value("2-4x4.st"));

    optionAdder("w,weight", "weight for wA* baseline",
                cxxopts::value<double>()->default_value("2"));

    optionAdder("o,performenceOut", "performence Out file",
                cxxopts::value<std::string>());

    optionAdder("v,pathOut", "path Out file", cxxopts::value<std::string>());

    optionAdder("h,help", "Print usage");

    auto args = options.parse(argc, argv);

    if (args.count("help")) {
        std::cout << options.help() << std::endl;
        exit(0);
    }

    auto d      = args["domain"].as<std::string>();
    auto sd     = args["subdomain"].as<std::string>();
    auto alg    = args["alg"].as<std::string>();
    auto bound  = args["bound"].as<double>();
    auto weight = args["weight"].as<double>();

    Search* searchPtr;

    // create domain world and search algorithm
    if (d == "tile") {
        SlidingTilePuzzle* world;

        if (sd == "uniform") {
            world = new SlidingTilePuzzle(cin);
        } else if (sd == "heavy") {
            world = new HeavyTilePuzzle(cin);
        } else if (sd == "inverse") {
            world = new InverseTilePuzzle(cin);
        } else {
            cout << "unknown tile type!\n";
            exit(1);
        }

        searchPtr =
          new BoundedCostSearch<SlidingTilePuzzle>(*world, bound, alg, weight);
    } else if (d == "pancake") {
        PancakePuzzle* world;

        world = new PancakePuzzle(cin);

        if (sd == "heavy") {
            world->setVariant(1);
        } else if (sd == "sumheavy") {
            world->setVariant(2);
        }

        searchPtr =
          new BoundedCostSearch<PancakePuzzle>(*world, bound, alg, weight);

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

        searchPtr =
          new BoundedCostSearch<RaceTrack>(*world, bound, alg, weight);

    } else if (d == "vaccumworld") {
        VaccumWorld* world;

        world = new VaccumWorld(cin);

        if (sd == "heavy") {
            world->setVariant(1);
        }

        searchPtr =
          new BoundedCostSearch<VaccumWorld>(*world, bound, alg, weight);

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

        nlohmann::json record;

        record["node expanded"]  = res.nodesExpanded;
        record["node generated"] = res.nodesGenerated;
        record["solution found"] = res.solutionFound;
        record["solution cost"]  = res.solutionCost;
        record["bound"]          = bound;
        record["cpu time"]       = res.totalCpuTime;
        record["instance"]       = args["instance"].as<std::string>();
        record["algorithm"]      = args["alg"].as<std::string>();

        out << record;

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
