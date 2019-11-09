SECONDS=0

echo ""
echo "====================================="
echo " MapReduce Program "
echo "====================================="
echo ""

InputPath="./input"
IntermediatePath="./intermediate"
OutputPath="./output"

rm -r $IntermediatePath $OutputPath
mkdir $IntermediatePath $OutputPath

echo "Input Files: $InputPath"
echo "Intermediate Output Files: $IntermediatePath"
# time $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-$HADOOP_VERSION.jar -input $InputPath -output $IntermediatePath -mapper "python3 src/mapper.py" -reducer "python3 src/reducer.py"
time cat ../2018.csv | python3 src/mapper.py | sort | python3 src/reducer.py > output/result.csv
echo "MapReduce complete"

echo ""
echo "====================================="
echo " Processing Results "
echo "====================================="
echo ""

echo "Intermediate Output Files: $IntermediatePath"
echo "Output Files: $OutputPath"
time python3 src/process_results.py $IntermediatePath $OutputPath

echo ""
echo "====================================="
echo " Plotting Data "
echo "====================================="
echo ""

Plots="$OutputPath/plot_result.png"
echo "Output Files: $OutputPath"
echo "Plots: $Plots"
time python3 src/plotter.py $OutputFiles $Plots

echo "Total Time Elapsed: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"