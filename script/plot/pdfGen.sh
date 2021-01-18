TIMESTAMP="20210117-144106"

cp /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyicodebase/script/plot/BCS-tex/* /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/

mv /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/main.tex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.tex

cd /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
bibtex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
latex /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}
dvips /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.dvi
ps2pdf /home/aifs1/gu/phd/research/workingPaper/boundedCostSearch/tianyi_plots/${TIMESTAMP}/bcs-compendium-${TIMESTAMP}.ps

