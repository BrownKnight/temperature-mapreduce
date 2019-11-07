SECONDS=0

GoogleCredentialFilePath="./google-cloud-key.json"
if [ -f $GoogleCredentialFilePath ]; then
    echo "Found Google Application Credential File";
    export GOOGLE_APPLICATION_CREDENTIALS=$GoogleCredentialFilePath;
else
    echo "Could not find Google Application Credential File at $GoogleCredentialFilePath"
    echo "If you are NOT running this via Google Cloud Shell, please create a new credential file json to access Google Cloud Storage";
fi

if [ -z $CLUSTER_NAME ]; then
    echo "Environment Variable CLUSTER_NAME has not been set, using cluster-adhoot-cccw";
    CLUSTER_NAME=cluster-adhoot-cccw;
else
    echo "Using Environment Variable CLUSTER_NAME ($CLUSTER_NAME)";
fi

if [ -z $CLUSTER_REGION ]; then
    echo "Environment Variable CLUSTER_REGION has not been set, using us-central1";
    CLUSTER_REGION="us-central1";
else
    echo "Using Environment Variable CLUSTER_REGION ($CLUSTER_REGION)";
fi

if [ -z $GOOGLE_BUCKET_NAME ]; then
    echo "Environment Variable GOOGLE_BUCKET_NAME has not been set, using adhoot-cccw";
    GOOGLE_BUCKET_NAME="adhoot-cccw";
else
    echo "Using Environment Variable GOOGLE_BUCKET_NAME ($GOOGLE_BUCKET_NAME)";
fi

echo ""
echo "====================================="
echo " Hadoop Streaming Job "
echo "====================================="
echo ""

InputPath="gs://$GOOGLE_BUCKET_NAME/input"
IntermediatePath="gs://$GOOGLE_BUCKET_NAME/intermediate"
OutputPath="gs://$GOOGLE_BUCKET_NAME/output"

echo "Input Files: $InputPath"
echo "Intermediate Output Files: $IntermediatePath"
# time $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-$HADOOP_VERSION.jar -input $InputPath -output $IntermediatePath -mapper "python3 src/mapper.py" -reducer "python3 src/reducer.py"
time gcloud dataproc jobs submit hadoop --cluster $CLUSTER_NAME --region=$CLUSTER_REGION --jar file:///usr/lib/hadoop-mapreduce/hadoop-streaming.jar --files=src/mapper.py,src/reducer.py,src/weather.py -- -mapper mapper.py -reducer reducer.py -input $InputPath -output $IntermediatePath
echo "Hadoop Streaming complete"

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

time python3 src/plotter.py

echo "Total Time Elapsed: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"