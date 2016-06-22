## The Smart Maintenance Demo

by Joe Hahn,<br />
joe.hahn@infochimps.com,<br />
22 June 2016<br />
git branch=vanilla<br />

This is the Github repository for the _vanilla_ branch of the Smart Maintenance Demo
that was adapted to run on the vanilla-cdh Hadoop cluster.
This demo uses the Support Vector Machines (SVM) algorithm to perform predictive
maintenance on 200 simulated motors, with most of the computations being done in
parallell across the Hadoop cluster's datanodes using Spark.


###Assumptions:

This repo is installed and executed on a vanilla-cdh Hadoop cluster that was created
per https://github.com/infochimps-sales/vanilla-cdh-launch/tree/ubuntu14.04


###Installation:

First clone this github repo to your home directory on the hadoop foyer node:

    cd; git clone git@github.com:infochimps-sales/smart-maintenance-demo.git
    cd smart-maintenance-demo
    git fetch --all
    git checkout vanilla
    git branch -a


###To execute:

To submit this spark job to Yarn for execution:

    PYSPARK_PYTHON=apython spark-submit --master yarn --num-executors 13 --executor-cores 5 \
        --executor-memory 1G --driver-memory 1G smart_maint.py


Monitor this job's progress using the Spark UI by browsing:

    Cloudera Manager -> Home -> Yarn -> Resource Manager UI -> application_ID# -> Application Master


The output of this spark job is three png images that can be viewed by browsing

    http://cdh-foyer.platform.infochimps:12321/figs
    

###The demo's storyline:

This demo calculates the operational history of 200 simulated motors over time. Initially these
motors are evolved using a _run-to-fail_ maintenance strategy. Each motor has two knobs,
Pressure (P) and Temperature (T), and the size of the dots in the following scatterplot
shows that the longest-lived motors have (P,T) settings in these intervals: 40 < P < 60 and T < 100,
with motors being progressively shorter-lived the further their P,T setting are from the
sweet spot at P~50 and T<100: 

![](https://github.com/infochimps-sales/smart-maintenance-demo/blob/master/figs/fail_factor.png)

The demo evolves these motors in run-to-fail mode until time t=200, and then (just for kicks)
it switches to a _scheduled-maintenance_ strategy during times 200 < t < 400.
During scheduled-maintenance operation, every engine is sent to maintenance every 5 days,
this simply removes some cruft and temporarily reduces the likelihood of motor failure.
Meanwhile the SVM algorithm is trained on the run-to-fail data, which is simply the observed
engine lifetimes versus their (P,T) settings. Once trained, the SVM algorithm is now 
able to use an engine's (P,T) settings to predict that engine's lifetime ie its 
estimated time-to-fail. Thereafter (at times t > 400) the engines are evolved using
_predictive-maintenance_, which simply sends an engine into maintenance
when its predicted time-to-fail is one day hence. The following diagram shows the SVM's
so-called _prediction surface_, which map's the engines' predicted time-to-fail across the
(P,T) parameter space. Note that SVM's predicted time-to-fail does indeed recover
the engines' sweet-spot at 40 < P < 60 and T < 100, though the edges of the predicted stable
zone is somewhat ragged.

![](https://github.com/infochimps-sales/smart-maintenance-demo/blob/master/figs/predicted_time_to_fail.png)

Each operating engine also generate earnings at a rate of $1000/day, while engines that are
being maintained instead generate modest expenses (-$200/day), with failed engines generating
larger expenses (-$2000/day) while in the shop for repairs. The following shows
that operating these engines in _run-to-fail_ mode is very expensive, resulting in
cumulative losses of -$13M by time t=200. This plot also shows that operating these
engines using a _scheduled-maintenance_ strategy is a wash, with earnings nearly balancing expenses.
But switching to a _predictive-maintenance_ strategy at t=400 then results in earnings that
exceeds expenses, so much so that the operators of these engines recover all lost earnings
by time t=870, and have earned $6M at the end of this simulation.

![](https://github.com/infochimps-sales/smart-maintenance-demo/blob/master/figs/revenue.png)

So this demo's main punchline is: _get Smart Maintenance on the BDPaas to optimize
equipment maintenance schedules and to  dramatically reduce expenses and grow earnings._

###Known issues:


If the png images are not browse-able, restart the webserver on the hadoop foyer node:

    /home/$USER/anaconda/bin/python -m SimpleHTTPServer 12321 > /dev/null 2>&1 &


###Debugging notes:
        

To benchmark spark's commandline settings:

    START=$(date +%s); \
    PYSPARK_PYTHON=apython spark-submit --master yarn --num-executors 13 --executor-cores 5 \
        --executor-memory 1G --driver-memory 1G smart_maint.py; \
    echo "execution time (seconds) = "$(( $(date +%s) - $START ))


One can also execute this demo line-by-line at the python command line using pyspark,
this is useful when debugging code:

    PYSPARK_PYTHON=ipython pyspark


Then copy-n-past each line from smart_maint_spark.py into the python command line, 
EXCEPT for line 25: sc = SparkContext(conf=conf... 

To get pyspark to use ipython (rather than python):

    sudo rm -f /usr/bin/python /usr/bin/ipython
    sudo ln -s /home/$USER/anaconda/bin/python /usr/bin/python
    sudo ln -s /home/$USER/anaconda/bin/ipython /usr/bin/ipython
    IPYTHON=1 pyspark


And to undo the above changes:
 
    sudo rm /usr/bin/python /usr/bin/ipython
    sudo ln -s /usr/bin/python2.6 /usr/bin/python
