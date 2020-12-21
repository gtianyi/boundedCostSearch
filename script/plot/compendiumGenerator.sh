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

#pythonOut=$(python ${plotter} -d tile -s heavy)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -t cpu -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -t cpu -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy -t par10 -b 1 -e 20)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d tile -s heavy-easy)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -t cpu -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -t cpu -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s heavy-easy -t par10 -b 1 -e 20)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d tile -s inverse)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -t cpu -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse -t par10 -b 1 -e 20)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d tile -s inverse-easy)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t cpu -b 3 -e 40)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d tile -s inverse-easy -t par10 -b 1 -e 20)
#echo "$pythonOut"

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

#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t cpu -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t cpu -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s regular -z 50 -t par10 -b 1)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -e 2.4) #need to comment out ptshat
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -b 1 -e 2.4) #need to comment out ptshat
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t cpu -b 1 -e 2.4) #need to comment out ptshat
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t cpu -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d pancake -s heavy -z 16 -t par10 -b 1)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -e 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -b 1 -e 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -b 1.8)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -t cpu -b 1 -e 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -t cpu -b 1.8)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s uniform -t par10 -b 1)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -t cpu -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -t cpu -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy -t par10 -b 1)
#echo "$pythonOut"


#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -e 3.5)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -b 1 -e 3.5)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -b 1.8)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -t cpu -b 1 -e 3.5)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -t cpu -b 1.8)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d vaccumworld -s heavy-easy -t par10 -b 1)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t cpu -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t cpu -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s barto-bigger -t par10 -b 1)
#echo "$pythonOut"

#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -t cpu -b 1 -e 2.4)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -t cpu -b 2)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -t coverageplt -b 1)
#echo "$pythonOut"
#pythonOut=$(python ${plotter} -d racetrack -s hansen-bigger -t par10 -b 1)
#echo "$pythonOut"

cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/BCS-tex/* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/

cd /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium
bibtex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium
dvips /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium.dvi
ps2pdf /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium.ps
