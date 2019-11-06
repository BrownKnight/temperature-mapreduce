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
    echo "Environment Variable CLUSTER_NAME has not been set, using adhoot-cccw-cluster";
    $CLUSTER_NAME="cluster-adhoot-cccw";
else
    echo "Using Environment Variable CLUSTER_NAME ($CLUSTER_NAME)";
fi

if [ -z $CLISTER_REGION ]; then
    echo "Environment Variable CLISTER_REGION has not been set, using us-central1";
    $CLISTER_REGION="us-central1";
else
    echo "Using Environment Variable CLISTER_REGION ($CLUSTER_NAME)";
fi

InputPath="gs://adhoot-cccw/input"
IntermediatePath="gs://adhoot-cccw/intermediate"
OutputPath="gs://adhoot-cccw/output"

echo "Running via Hadoop Streaming"
echo "Input Files: $InputPath"
echo "Intermediate Output Files: $IntermediatePath"
# time $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-$HADOOP_VERSION.jar -input $InputPath -output $IntermediatePath -mapper "python3 src/mapper.py" -reducer "python3 src/reducer.py"
time gcloud dataproc jobs submit hadoop --cluster $CLUSTER_NAME --region=$CLUSTER_REGION --jar file:///usr/lib/hadoop-mapreduce/hadoop-streaming.jar --files=src/mapper.py,src/reducer.py -- -mapper src/mapper.py -reducer src/reducer.py -input $InputPath -output $IntermediatePath
echo "Hadoop Streaming complete"


echo "Now processing results"
echo "Intermediate Output Files: $IntermediatePath"
echo "Output Files: $OutputPath"
time python3 src/process_results.py $IntermediatePath $OutputPath

echo "Total Time Elapsed: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"