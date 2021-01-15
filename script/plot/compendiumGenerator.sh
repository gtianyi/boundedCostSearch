#!/bin/bash
#author TianyiGu
#date 2020/12/20
#desc bounded cost plot compendimum auto generateor 

TIMESTAMP=`date +%Y%m%d-%H%M%S`
plotter="boundedCostPlot.py -ot ${TIMESTAMP}"

pythonOut=$(python ${plotter} -d tile -s uniform -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -t cpu -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -t cpu -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s uniform -t par10 -b 1 -e 20 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s heavy -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -t cpu -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -t cpu -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -t par10 -b 1 -e 20 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s heavy-easy -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -t cpu -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -t cpu -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -t par10 -b 1 -e 20 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s heavy-easy -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s inverse -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t par10 -b 1 -e 20 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s inverse -os below1 -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -b 1 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -b 3 -e 40 -os loose -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 1 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 3 -e 40 -os loose -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t par10 -b 1 -e 3 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse -t par10 -b 1 -e 20 -os loose -r pts)
echo "$pythonOut"

#pythonOut=$(python ${plotter} -d tile -s inverse-easy -os below1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 1 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 3 -e 40 -os loose)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 1 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 3 -e 40 -os loose)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t par10 -b 1 -e 3 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t par10 -b 1 -e 20 -os loose)
#echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s inverse-easy -os below1 -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 1 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 3 -e 40 -os loose -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 1 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 3 -e 40 -os loose -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -t coverageplt -b 1 -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -t par10 -b 1 -e 3 -os tight -r pts)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s inverse-easy -t par10 -b 1 -e 20 -os loose -r pts)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d tile -s reverse-easy -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -t cpu -b 1 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -t cpu -b 3 -e 40 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d tile -s reverse-easy -t par10 -b 1 -e 20 -os loose)
echo "$pythonOut"

##pythonOut=$(python ${plotter} -d tile -s reverse -bt absolute)
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s reverse -bt absolute -t cpu)
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s reverse -bt absolute -t coverageplt)
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s reverse -bt absolute -t par10)
##echo "$pythonOut"

##pythonOut=$(python ${plotter} -d tile -s sqrt -bt absolute) # lower = 80
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s sqrt -bt absolute) # lower = 140
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s sqrt -bt absolute -t cpu) # lower = 140
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s sqrt -bt absolute -t coverageplt)
##echo "$pythonOut"
##pythonOut=$(python ${plotter} -d tile -s sqrt -bt absolute -t par10) # lower = 140
##echo "$pythonOut"

pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -e 2.4 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t cpu -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t par10 -b 1 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -e 2.4 -os below1 -r ptshhat) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -b 1 -e 2.4 -os tight -r ptshhat) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t cpu -b 1 -e 2.4 -os tight -r ptshhat) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t par10 -b 1 -e 3 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t par10 -b 1 -os tight)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -e 2.4 -os below1) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -b 1 -e 2.4 -os tight) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -t cpu -b 1 -e 2.4 -os tight) #need to comment out ptshat
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -t par10 -b 1 -e 3 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d pancake -s sumheavy -z 10 -t par10 -b 1 -os tight)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d vacuumworld -s uniform -e 2 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -b 1 -e 2 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -b 1.8 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -t cpu -b 1 -e 2 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -t cpu -b 1.8 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s uniform -t par10 -b 1 -os loose)
echo "$pythonOut"

#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -e 2.4 -os below1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -b 1 -e 2.4 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -b 2 -os loose)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -t cpu -b 1 -e 2.4 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -t cpu -b 2 -os loose)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -t par10 -b 1 -e 3 -os tight)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vacuumworld -s heavy -t par10 -b 1 -os loose)
#echo "$pythonOut"

pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -e 3.5 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -b 1 -e 3.5 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -b 1.8 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -t cpu -b 1 -e 3.5 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -t cpu -b 1.8 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d vacuumworld -s heavy-easy -t par10 -b 1 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -e 2.4 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -t cpu -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht dijkstra -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t par10 -ht dijkstra -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t par10 -ht dijkstra -b 1 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -e 2.4 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -t cpu -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht dijkstra -t par10 -b 1 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -e 2.4 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -t cpu -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -ht euclidean -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t par10 -ht euclidean -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t par10 -ht euclidean -b 1 -os loose)
echo "$pythonOut"

pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -e 2.4 -os below1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -t cpu -b 1 -e 2.4 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -t cpu -b 2 -os loose)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -t coverageplt -b 1)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -t par10 -b 1 -e 3 -os tight)
echo "$pythonOut"
pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -ht euclidean -t par10 -b 1 -os loose)
echo "$pythonOut"

cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyicodebase/script/plot/BCS-tex/* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/

mv /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/main.tex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.tex

cd /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
bibtex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
dvips /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.dvi
ps2pdf /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.ps

mkdir -p /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/cpu
cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/tile/*tight*cpu* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/cpu/
cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/pancake/*tight*cpu* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/cpu/
cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/racetrack/*tight*cpu* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/cpu/
cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/vacuumworld/*tight*cpu* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/cpu/
