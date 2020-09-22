#!/bin/bash
print_usage() {
    echo "./singleThread-boundedCostSolver.sh"
    echo "[-f instance]                    default: 1"
    echo "[-n # of instances to test]      default: 1"
    echo "[-d domain]                      default: pancake"
    echo "[-s subdomain]                   default: regular"
    echo "[-z domain size]                 default: 32"
    echo "[-u boundedCost solver]"
    echo " support list,eg: -u a1 -u a2    default: pts ptshhat ptsnancy bees beepsnancy"
    echo "[-b bound]"
    echo " support list,eg: -b 10 -b 30    default: 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100"
    echo "[-t time limit]                  default: 600 (seconds)"
    echo "[-m memory limit]                default: 7.5 (GB)"
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
domain="pancake"
subdomain="regular"
size="32"
boundedCostSolvers=("pts" "ptshhat" "ptsnancy" "bees" "beepsnancy")
bounds=(5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100)
timeLimit=600
memoryLimit=7.5

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

    if [ ${!i} == "-b" ]; then
        if [ $((i + 1)) -le "$#" ]; then
            if ! $boundCleared; then
                unset bounds
                boundCleared=true
            fi
            var=$((i + 1))
            bounds+=(${!var})
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
echo "bounds ${bounds[*]}"
echo "time limit ${timeLimit}"
echo "memory limit ${memoryLimit}"

infile=""
outfile=""

research_home="/home/aifs1/gu/phd/research/workingPaper"
infile_path="${research_home}/realtime-nancy/worlds/${domain}"
outfile_path="${research_home}/boundedCostSearch/tianyi_results/${domain}/${subdomain}/solverDir"
infile_name=""

limitWrapper="${research_home}/boundedCostSearch/tianyicodebase/script/testHarnesses/limitWrapper.py"
optimalSolParser="${research_home}/boundedCostSearch/tianyicodebase/script/optimalSolutionParser.py"

if [ "$domain" == "tile" ]; then
    infile_name="$instance-${size}x${size}.st"
    outfile="${outfile_path}/Bound-BoundNumber-size-${size}-instance.json"
fi

if [ "$domain" == "pancake" ]; then
    infile_name="$instance-${size}.pan"
    outfile="${outfile_path}/Bound-BoundNumber-size-${size}-instance.json"
fi

if [ "$domain" == "racetrack" ]; then
    infile_name="${subdomain}-instance.init"
    outfile="${outfile_path}/Bound-BoundNumber-instance.json"
fi

infile="${infile_path}/${infile_name}"

last=$(($first + $n_of_i))

for solverId in "${!boundedCostSolvers[@]}"; do

    solverName=${boundedCostSolvers[$solverId]}
    echo $solverName

    outfile_path_alg="${outfile_path/solverDir/$solverName}"
    mkdir -p ${outfile_path_alg}
    outfile_alg="${outfile/solverDir/$solverName}"

    executable="${research_home}/boundedCostSearch/tianyicodebase_build_release/bin/bcs"

    for bound in "${bounds[@]}"; do
        echo "bound $bound"

        instance=$first
        while ((instance < last)); do
            infile_instance="${infile/instance/$instance}"
            infile_instance="${infile_instance/tile/slidingTile}"
            outfile_instance="${outfile_alg/instance/$instance}"
            outfile_instance="${outfile_instance/BoundNumber/$bound}"
            tempfile="${outfile_instance}.temp"

            optimalSolution=${python optimalSolutionParser.py -i ${infile_name/instance/$instance}}

            if [ -f ${outfile_instance} ] || [ -f ${tempfile} ]; then

                let instance++

            else

                command="${executable} -d ${domain} -s ${subdomain} -a ${solverName} \
                    -b ${bound} -o ${outfile_instance} -i ${instance} < ${infile_instance}"

                echo "$command" > ${tempfile}

                python $limitWrapper -c "${command}" -t $timeLimit -m $memoryLimit

                if [ -f ${outfile_instance} ]; then
                    rm ${tempfile}
                fi

                let instance++

            fi

        done
    done
done
