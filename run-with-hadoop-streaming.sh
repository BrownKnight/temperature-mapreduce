rm -r output/hadoop
time /Users/aman/hadoop/bin/hadoop jar /Users/aman/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -input ../2018.csv -output output/hadoop -mapper "python3 src/mapper.py" -reducer "python3 src/reducer.py"