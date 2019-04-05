### Basic Mode
When running the soit in the basic mode (default) and you image passes the test, you should end-up with following output:

```console
[ ✓ ] ... File /launch.sh should be present on the image
[ ✓ ] ... File /launch.sh does contain SPARK_METRICS_ON
[ ✓ ] ... File /launch.sh does contain SPARK_MASTER_ADDRESS
[ ✓ ] ... File /entrypoint should be present on the image
[ ✓ ] ... Directory /opt/spark should be present on the image
[ ✓ ] ... Directory /opt/spark/conf/ is present on the image
[ ✓ ] ... Default config spark-defaults.conf is on the right place
[ ✓ ] ... File /opt/spark/bin/spark-class should be present on the image
[ ✓ ] ... File /opt/spark/RELEASE should be present on the image
[ ✓ ] ... The image should have the curl installed
[ ✓ ] ... The image should have the bash installed
```


### Full Mode

To run the `soit` in the full mode, add the `-f` or `--full` switch.
When running the soit in the full mode, you should be able to see the checks from the basic mode + following:

```console
...
[ ✓ ] ... It should be possible to start the master.
[ ✓ ] ... Master should start the web ui on port 8080
[ ✓ ] ... Master should be alive.
[ ✓ ] ... It should be possible to start the worker.
[ ✓ ] ... Worker should start the web ui on port 8081
[ ✓ ] ... Worker web ui should contain the master's ip
[ ✓ ] ... In the master's log file there should be worker registration message
[ ✓ ] ... In the worker's log file master registration should be mentioned
```
