mkdir output
rm output/result.csv

time cat ../2018.csv | python3 src/mapper.py | sort | python3 src/reducer.py > output/result.csv