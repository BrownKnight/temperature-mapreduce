SECONDS=0
echo ""
echo "====================================="
echo " Environment Variable Setup "
echo "====================================="
echo ""


if [ -z $HADOOP_HOME ]; then
    echo "Environment Variable HADOOP_HOME has not been set, using ~/hadoop";
    HADOOP_HOME=~/hadoop;
else
    echo "Using Environment Variable HADOOP_HOME ($HADOOP_HOME)";
fi

if [ -z $HADOOP_VERSION ]; then
    echo "Environment Variable HADOOP_VERSION has not been set, using 3.2.1";
    HADOOP_VERSION="3.2.1";
else
    echo "Using Environment Variable HADOOP_VERSION ($HADOOP_VERSION)";
fi


echo ""
echo "====================================="
echo " MapReduce Program "
echo "====================================="
echo ""

InputPath="output/input"
IntermediatePath="output/intermediate"
OutputPath="output/output"

rm -r $IntermediatePath $OutputPath
# mkdir $IntermediatePath $OutputPath

echo "Input Files: $InputPath"
echo "Intermediate Output Files: $IntermediatePath"
time $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-$HADOOP_VERSION.jar -input $InputPath -output $IntermediatePath -mapper src/mapper.py -reducer src/reducer.py
# time cat ../2018.csv | python3 src/mapper.py | sort | python3 src/reducer.py > output/result.csv
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

Plots="$OutputPath"
echo "Output Files: $OutputPath"
echo "Plots: $Plots"
time python3 src/plotter.py $OutputPath/*.csv $Plots

echo "Total Time Elapsed: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"