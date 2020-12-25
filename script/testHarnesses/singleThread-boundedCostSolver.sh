#!/bin/bash
print_usage() {
    echo "./singleThread-boundedCostSolver.sh"
    echo "[-f instance]                    default: 1"
    echo "[-n # of instances to test]      default: 1"
    echo "[-d domain]                      "
    echo "support list,eg: -d tile -d pancake  available: tile, pancake, racetrack, vacuumworld"
    echo "[-st subdomain of tile]          default: uniform, heavy, inverse, heavy-easy, inverse-easy"
    echo "[-sp subdomain of pancake]       default: regular, heavy"
    echo "[-sv subdomain of vacuumworld]   default: uniform, heavy"
    echo "[-sr subdomain of racetrack]     default: barto-bigger, hansen-bigger"
    #echo "[-z domain size]                 default: 4"
    echo "[-u boundedCost solver]"
    echo " support list,eg: -u a1 -u a2    available: pts ptshhat ptsnancy bees astar wastar ptsnancywithdhat"
    echo "                                 default: pts ptshhat bees-EpsGlobal ptsnancywithdhat"
    #echo "[-bp bound percent wrt optimal]"
    #echo " support list,eg: -bp 10 -bp 300 default: 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500 520 540 560 580 600"
    echo "[-t time limit]                  default: 1800 (seconds)"
    echo "[-m memory limit]                default: 7.5(GB)"
    echo "[-w weight of wA*]               default: 2"
    echo "[-bt bound type]                 available: percentWrtOpt(default), absolute"
    echo "[-h help]"
    exit 1
}

if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "?" ]; then
    print_usage
fi

# Which instance to start testing on
first=1
# The number of instances to test on
n_of_i=1

domain=("tile" "pancake" "racetrack" "vacuumworld")
subdomain=()
subdomainTile=("uniform" "heavy" "inverse" "heavy-easy" "inverse-easy")
subdomainPancake=("regular" "heavy")
subdomainVacuumworld=("uniform" "heavy")
subdomainRacetrack=("barto-bigger" "hansen-bigger")

n_of_i_Tile=100
n_of_i_Pancake=100
n_of_i_Racetrack=25
n_of_i_Vacuumworld=60

size="4"
sizeOfRegularPancake="50"
sizeOfHeavyPancake="16"

#boundedCostSolvers=("pts" "ptshhat" "ptsnancy" "bees" "astar" "wastar")
boundedCostSolvers=("pts" "ptshhat" "bees-EpsGlobal" "ptsnancywithdhat")
boundPercents=()
boundPercentsA=(60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500 520 540 560 580 600 700 800 900 1000 1100 1200 1300 1400 1500  2000 3000)
boundPercentsB=(60 80 100 110 120 130 140 150 160 170 180 190 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500 520 540 560 580 600)
timeLimit=1800
memoryLimit=7
weight="2"
boundType="percentWrtOpt"

absoluteBounds=()
absoluteBoundsTileUniform=(40 60 80 100 120 140 160 180 200 220 240 260 280 300 600 900)
absoluteBoundsTileHeavy=(300 400 500 600 700 800 900 1000 2000 3000 4000 5000 6000)
absoluteBoundsTileReverse=(300 400 500 600 700 800 900 1000 2000 3000 4000 5000 6000)
#absoluteBoundsTileSqrt=(80 100 120 140 160 180 200 220 240 260)
absoluteBoundsTileSqrt=(280 300 350 400 450 500 600 700 800 900 1000)

solverCleared=false
boundCleared=false
domainCleared=false
subdomainTileCleared=false
subdomainRacetrackCleared=false
subdomainVacuumworldCleared=false
subdomainPancakeCleared=false
#parse arguments
for ((i = 1; i <= "$#"; i++)); do
    if [ ${!i} == "-f" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            first=${!var}
        fi
    fi

    if [ ${!i} == "-n" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            n_of_i=${!var}
        fi
    fi

    if [ ${!i} == "-d" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $domainCleared; then
                unset domain
                domainCleared=true
            fi
            var=$((i + 1))
            domain+=(${!var})
        fi
    fi

    if [ ${!i} == "-st" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $subdomainTileCleared; then
                unset subdomainTile
                subdomainTileCleared=true
            fi
            var=$((i + 1))
            subdomainTile+=(${!var})
        fi
    fi

    if [ ${!i} == "-sp" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $subdomainPancakeCleared; then
                unset subdomainPancake
                subdomainPancakeCleared=true
            fi
            var=$((i + 1))
            subdomainPancake+=(${!var})
        fi
    fi

    if [ ${!i} == "-sv" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $subdomainVacuumworldCleared; then
                unset subdomainVacuumworld
                subdomainVacuumworldCleared=true
            fi
            var=$((i + 1))
            subdomainVacuumworld+=(${!var})
        fi
    fi

    if [ ${!i} == "-sr" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $subdomainRacetrackCleared; then
                unset subdomainRacetrack
                subdomainRacetrackCleared=true
            fi
            var=$((i + 1))
            subdomainRacetrack+=(${!var})
        fi
    fi

    #if [ ${!i} == "-z" ]; then
        #if [ $((i + 1)) -le "$#" ]; then
            #var=$((i + 1))
            #size=${!var}
        #fi
    #fi

    if [ ${!i} == "-u" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $solverCleared; then
                unset boundedCostSolvers
                solverCleared=true
            fi
            var=$((i + 1))
            boundedCostSolvers+=(${!var})
        fi
    fi

    #if [ ${!i} == "-bp" ]; then
        #if [ $((i + 1)) -le "$#" ]; then
            #if ! $boundCleared; then
                #unset boundPercents
                #boundCleared=true
            #fi
            #var=$((i + 1))
            #boundPercents+=(${!var})
        #fi
    #fi

    if [ ${!i} == "-bt" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            boundType=${!var}
        fi
    fi

    if [ ${!i} == "-m" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            memoryLimit=${!var}
        fi
    fi

    if [ ${!i} == "-t" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            timeLimit=${!var}
        fi
    fi

    if [ ${!i} == "-w" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            weight=${!var}
        fi
    fi

    if [ ${!i} == "-h" ]; then
        print_usage
    fi

done

echo "first ${first}"
echo "domain ${domain[*]}"
echo "solvers ${boundedCostSolvers[*]}"
echo "time limit ${timeLimit}"
echo "memory limit ${memoryLimit}"
echo "bound type ${boundType}"

for curDomainId in "${!domain[@]}"; do
    curDomain=${domain[$curDomainId]}
    echo "running $curDomain"

    if [ "$curDomain" == "tile" ]; then
        subdomain=("${subdomainTile[@]}")
        boundPercents=("${boundPercentsA[@]}")
        n_of_i=$n_of_i_Tile
    fi

    if [ "$curDomain" == "pancake" ]; then
        subdomain=("${subdomainPancake[@]}")
        boundPercents=("${boundPercentsB[@]}")
        n_of_i=$n_of_i_Pancake
    fi

    if [ "${curDomain}" == "vacuumworld" ]; then
        subdomain=("${subdomainVacuumworld[@]}")
        boundPercents=("${boundPercentsB[@]}")
        n_of_i=$n_of_i_Vacuumworld
    fi

    if [ "${curDomain}" == "racetrack" ]; then
        subdomain=("${subdomainRacetrack[@]}")
        boundPercents=("${boundPercentsB[@]}")
        n_of_i=$n_of_i_Racetrack
    fi

    echo "subdomain ${subdomain[*]}"
    echo "n_of_i ${n_of_i}"

    if [ "$boundType" == "percentWrtOpt" ]; then 
        echo "boundPercents ${boundPercents[*]}"
    fi

    for curSubdomainId in "${!subdomain[@]}"; do
        curSubdomain=${subdomain[$curSubdomainId]}
        echo "running $curSubdomain"

        if [ "$boundType" == "absolute" ]; then 
            if [ "${curDomain}" == "tile"  ] && [ "${curSubdomain}" == "uniform"  ]; then
                absoluteBounds=("${absoluteBoundsTileUniform[@]}")  
            fi

            if [ "${curDomain}" == "tile"  ] && [ "${curSubdomain}" == "heavy"  ]; then
                absoluteBounds=("${absoluteBoundsTileHeavy[@]}")  
            fi

            if [ "${curDomain}" == "tile"  ] && [ "${curSubdomain}" == "reverse"  ]; then
                absoluteBounds=("${absoluteBoundsTileReverse[@]}")  
            fi

            if [ "${curDomain}" == "tile"  ] && [ "${curSubdomain}" == "sqrt"  ]; then
                absoluteBounds=("${absoluteBoundsTileSqrt[@]}")  
            fi

            echo "absolute bounds ${absoluteBounds[*]}"
        fi

        if [ "$curDomain" == "pancake" ];then
            if [ "$curSubdomain" == "regular" ]; then
                size=$sizeOfRegularPancake
            fi

            if [ "$curSubdomain" == "heavy" ]; then
                size=$sizeOfHeavyPancake
            fi

            echo "size ${size}"
        fi

        infile=""
        outfile=""

        research_home="/home/aifs1/gu/phd/research/workingPaper"
        infile_path="${research_home}/realtime-nancy/worlds/${curDomain}"

        outfile_path=""
        if [ "$boundType" == "percentWrtOpt" ]; then 
            outfile_path="${research_home}/boundedCostSearch/tianyi_results/${curDomain}/${curSubdomain}/solverDir"
        fi
        if [ "$boundType" == "absolute" ]; then 
            outfile_path="${research_home}/boundedCostSearch/tianyi_results_absolute_bound/${curDomain}/${curSubdomain}/solverDir"
        fi

        infile_name=""

        limitWrapper="${research_home}/boundedCostSearch/tianyicodebase/script/testHarnesses/limitWrapper.py"
        optimalSolRetriever="${research_home}/boundedCostSearch/tianyicodebase/script/optimalSolutionRetriever.py"

        if [ "${curDomain}" == "tile" ]; then

            if [ "${curSubdomain}" == "heavy-easy" ]; then
                infile_path="${research_home}/realtime-nancy/worlds/slidingTile_tianyi1000-easy-for-heavy"
            fi

            if [ "${curSubdomain}" == "inverse-easy" ]; then
                infile_path="${research_home}/realtime-nancy/worlds/slidingTile_tianyi1000-easy-for-inverse"
            fi

            infile_name="instance-${size}x${size}.st"
            outfile="${outfile_path}/${boundType}-BoundNumber-size-${size}-instance.json"
            infile="${infile_path}/${infile_name}"
        fi

        if [ "${curDomain}" == "pancake" ]; then
            infile_name="instance-${size}.pan"
            outfile="${outfile_path}/${boundType}-BoundNumber-size-${size}-instance.json"
            infile="${infile_path}/${size}/${infile_name}"
        fi

        if [ "${curDomain}" == "racetrack" ]; then
            infile_name="${curSubdomain}-instance.init"
            outfile="${outfile_path}/${boundType}-BoundNumber-instance.json"
            infile="${infile_path}/${infile_name}"
        fi

        if [ "${curDomain}" == "vacuumworld" ]; then

            infile_path="${research_home}/realtime-nancy/worlds/vacuumworld/200x200"

            if [ "${curSubdomain}" == "heavy-easy" ]; then
                infile_path="${research_home}/realtime-nancy/worlds/vacuumworld/200x200-6"
            fi

            infile_name="instance.vw"
            outfile="${outfile_path}/BoundPercent-BoundNumber-instance.json"
            infile="${infile_path}/${infile_name}"
        fi

        last=$(($first + $n_of_i))

        boundList=()

        if [ "$boundType" == "percentWrtOpt" ]; then 
            boundList=("${boundPercents[@]}")  
        fi

        if [ "$boundType" == "absolute" ]; then 
            boundList=("${absoluteBounds[@]}")  
        fi

        for solverId in "${!boundedCostSolvers[@]}"; do

            solverName=${boundedCostSolvers[$solverId]}
            echo $solverName

            outfile_path_alg="${outfile_path/solverDir/$solverName}"
            mkdir -p ${outfile_path_alg}
            outfile_alg="${outfile/solverDir/$solverName}"

            executable="${research_home}/boundedCostSearch/tianyicodebase_build_release/bin/bcs"

            for boundTypeValue in "${boundList[@]}"; do
                echo "${boundType} $boundTypeValue"

                instance=$first
                while ((instance < last)); do
                    infile_instance="${infile/instance/$instance}"
                    infile_instance="${infile_instance/tile/slidingTile}"
                    outfile_instance="${outfile_alg/instance/$instance}"
                    outfile_instance="${outfile_instance/BoundNumber/$boundTypeValue}"
                    tempfile="${outfile_instance}.temp"

                    curFileName=${infile_name/instance/$instance}

                    bound=$boundTypeValue

                    if [ "$boundType" == "percentWrtOpt" ]; then 
                        retrieverCommand="python ${optimalSolRetriever} -d ${curDomain} -s ${curSubdomain} -z ${size} -i ${curFileName}"
                        optimalSolution=$(${retrieverCommand})

                        percent=$(echo "${boundTypeValue} * ${optimalSolution}" | bc)
                        bound=$(echo "$percent / 100" | bc)
                    fi

                    echo "actural bound $bound"

                    if [ -f ${outfile_instance} ] || [ -f ${tempfile} ]; then

                        let instance++

                    else

                        realSubdomain="${curSubdomain}"
                        if [ "${curSubdomain}" == "heavy-easy" ]; then
                            realSubdomain="heavy"
                        fi

                        if [ "${curSubdomain}" == "inverse-easy" ]; then
                            realSubdomain="inverse"
                        fi

                        command="${executable} -d ${curDomain} -s ${realSubdomain} -a ${solverName} \
                            -b ${bound} -o ${outfile_instance} -i ${instance} "

                        if [ "${solverName}" == "wastar" ]; then
                            command+="-w ${weight} "
                        fi

                        command+="< ${infile_instance}"

                        echo "${command}" > ${tempfile}

                        executableOut=$(python $limitWrapper -c "${command}" -t $timeLimit -m $memoryLimit)

                        echo "${executableOut}" >> ${tempfile}

                        if [ -f ${outfile_instance} ]; then
                            rm ${tempfile}
                        fi

                        let instance++

                    fi

                done
            done
        done

        fixJson_running_flag="${research_home}/boundedCostSearch/tianyi_results/fixJson.${curDomain}.${curSubdomain}.run"
        fixJsonExecutable="${research_home}/boundedCostSearch/tianyicodebase/script/fixJson.py"

        sleep 1

        if [ ! -f ${fixJson_running_flag} ]; then
            echo "run" >> ${fixJson_running_flag}
            fixJsonOut=$(python ${fixJsonExecutable} -d ${curDomain} -s ${curSubdomain} -bt ${boundType} ) 
            echo "$fixJsonOut"  
        fi

    done
done
