#!/bin/bash
print_usage() {
    echo "./singleThread-boundedCostSolver.sh"
    echo "[-f instance]                    default: 1"
    echo "[-n # of instances to test]      default: 1"
    echo "[-d domain]                      default: tile"
    echo "[-s subdomain]                   default: uniform"
    echo "[-z domain size]                 default: 4"
    echo "[-u boundedCost solver]"
    echo " support list,eg: -u a1 -u a2    available: pts ptshhat ptsnancy bees astar wastar ptsnancywithdhat"
    echo "                                 default: pts ptshhat bees-EpsGlobal ptsnancywithdhat"
    echo "[-bp bound percent wrt optimal]"
    echo " support list,eg: -bp 10 -bp 300 default: 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500 520 540 560 580 600"
    echo "[-t time limit]                  default: 1800 (seconds)"
    echo "[-m memory limit]                default: 7(GB)"
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
domain="tile"
subdomain="uniform"
size="4"
#boundedCostSolvers=("pts" "ptshhat" "ptsnancy" "bees" "astar" "wastar")
boundedCostSolvers=("pts" "ptshhat" "bees-EpsGlobal" "ptsnancywithdhat")
boundPercents=(100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500 520 540 560 580 600)
timeLimit=1800
memoryLimit=7
weight="2"
boundType="percentWrtOpt"

absoluteBounds=()
absoluteBoundsTileUniform=(40 60 80 100 120 140 160 180 200 220 240 260 280 300 600 900)
absoluteBoundsTileHeavy=(300 400 500 600 700 800 900 1000 2000 3000 4000 5000 6000)

solverCleared=false
boundCleared=false
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
            var=$((i + 1))
            domain=${!var}
        fi
    fi

    if [ ${!i} == "-s" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            subdomain=${!var}
        fi
    fi

    if [ ${!i} == "-z" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            var=$((i + 1))
            size=${!var}
        fi
    fi

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

    if [ ${!i} == "-bp" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $boundCleared; then
                unset boundPercents
                boundCleared=true
            fi
            var=$((i + 1))
            boundPercents+=(${!var})
        fi
    fi

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
echo "n_of_i ${n_of_i}"
echo "domain ${domain}"
echo "subdomain ${subdomain}"
echo "size ${size}"
echo "solvers ${boundedCostSolvers[*]}"
echo "time limit ${timeLimit}"
echo "memory limit ${memoryLimit}"
echo "bound type ${boundType}"

if [ "$boundType" == "percentWrtOpt" ]; then 
    echo "boundPercents ${boundPercents[*]}"
fi

if [ "$boundType" == "absolute" ]; then 
    if [ "$domain" == "tile"  ] && [ "$subdomain" == "uniform"  ]; then
        absoluteBounds=("${absoluteBoundsTileUniform[@]}")  
    fi

    if [ "$domain" == "tile"  ] && [ "$subdomain" == "heavy"  ]; then
        absoluteBounds=("${absoluteBoundsTileHeavy[@]}")  
    fi

    echo "absolute bounds ${absoluteBounds[*]}"
fi

infile=""
outfile=""

research_home="/home/aifs1/gu/phd/research/workingPaper"
infile_path="${research_home}/realtime-nancy/worlds/${domain}"

outfile_path=""
if [ "$boundType" == "percentWrtOpt" ]; then 
    outfile_path="${research_home}/boundedCostSearch/tianyi_results/${domain}/${subdomain}/solverDir"
fi
if [ "$boundType" == "absolute" ]; then 
    outfile_path="${research_home}/boundedCostSearch/tianyi_results_absolute_bound/${domain}/${subdomain}/solverDir"
fi

infile_name=""

limitWrapper="${research_home}/boundedCostSearch/tianyicodebase/script/testHarnesses/limitWrapper.py"
optimalSolRetriever="${research_home}/boundedCostSearch/tianyicodebase/script/optimalSolutionRetriever.py"

if [ "$domain" == "tile" ]; then
    infile_name="instance-${size}x${size}.st"
    outfile="${outfile_path}/${boundType}-BoundNumber-size-${size}-instance.json"
    infile="${infile_path}/${infile_name}"
fi

if [ "$domain" == "pancake" ]; then
    infile_name="instance-${size}.pan"
    outfile="${outfile_path}/${boundType}-BoundNumber-size-${size}-instance.json"
    infile="${infile_path}/${size}/${infile_name}"
fi

if [ "$domain" == "racetrack" ]; then
    infile_name="${subdomain}-instance.init"
    outfile="${outfile_path}/${boundType}-BoundNumber-instance.json"
    infile="${infile_path}/${infile_name}"
fi

if [ "$domain" == "vaccumworld" ]; then
    infile_name="instance.vw"
    outfile="${outfile_path}/BoundPercent-BoundNumber-instance.json"
    infile="${infile_path}/200x200/${infile_name}"
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
                retrieverCommand="python ${optimalSolRetriever} -d ${domain} -s ${subdomain} -z ${size} -i ${curFileName}"
                optimalSolution=$(${retrieverCommand})

                percent=$((${boundTypeValue} * ${optimalSolution}))
                bound=$(echo "$percent / 100" | bc)
            fi

            echo "actural bound $bound"

            if [ -f ${outfile_instance} ] || [ -f ${tempfile} ]; then

                let instance++

            else

                command="${executable} -d ${domain} -s ${subdomain} -a ${solverName} \
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
