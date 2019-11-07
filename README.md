# temperature-mapreduce

## Introduction
temperature-mapreduce is a program designed to take weather datasets created by NCEI 
<small>(See https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/ and 
https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
for more)</small>
and run them through a Hadoop MapReduce program to filter out extraneous data and output only the temperature 
difference for a given location on every day of the year (dependent on the dataset).

By default, the program will output the difference between the maximum and minimum temperature for every day in the 
dataset for the Oxford and Waddington locations.
To add/edit locations, simply edit the `WeatherObservationLocation` enum in `src/weather.py` file to include the name
and the code (from the dataset) of the location

Results from the MapReduce program will be processed by the `process_results.py` script the combine the results from
the reducers and create one-column separate csv files for each location

## How to run the program
#### via Google Cloud Shell (Recommended)
1. If you don't have one already, create a new Google Dataproc cluster in Google Cloud
2. If you don't have already, create a Google Storage Bucket to store the input/outputs of this program in
<br> NOTE: There should be no folders in the bucket called `intermediate` or `output`
3. Upload your dataset to your Google Storage Bucket. The script will look for the input at `gs://<bucket_name>/input`
4. Open Cloud Shell and clone this git repository. You can either replicate the repository in 
'Google Source Repositories', or clone straight from GitHub.
5. Navigate to inside this repository.
6. Set the following environment variables <small>(If you want to change from defaults)</small>:
    ```
    CLUSTER_NAME (defaults to cluster-adhoot-cccw)
    CLUSTER_REGION (defaults to us-central1)
    GOOGLE_BUCKET_NAME (defaults to adhoot-cccw)
   ```
7. Run the `run.sh` script
    <br>
    This script will run the Hadoop MapReduce program via `gcloud dataproc jobs submit`, then will run a couple of 
    python scripts to process the resultant files into one-column csv's, then create plots using those files.
    
You should find the resulting csv files and data plots at `gs://<bucket_name>/output`

#### Locally (For Testing)
To run locally for testing purposes, you can use the `run-with-pipe.sh` script, which will process the dataset using a 
single mapper and reducer on your local machine. Output will be saved to `output/result.csv`.

If you have hadoop installed locally, you can use the `run-with-hadoop-streaming.sh` script to process your dataset 
with multiple mappers/reducers in the same way that running it on Google's Cloud infrastructure would.
Output will be saved to the `./output/` directory. You may need to set the `HADOOP_HOME` environment variable to the
location of your hadoop installation before running this script.

#### Prerequisites
- To use data from Google Cloud Storage (i.e. `gs://` links) you will need to ensure your python environment 
has the `google-cloud-storage` python package installed
- To create plots using the `src/plotter.py` script, you need to ensure the python environment has the `matplotlib` 
python package installed