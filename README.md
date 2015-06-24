## The Smart Maintenance Demo

by Joe Hahn,
joe.hahn@infochimps.com,
20 May 2015

This is the Github repository for the master branch of the Smart Maintenance Demo for Hadoop,
this demo uses python's scikit-learn machine-learning algorithm to perform predictive
maintenance on 200 simulated motors. This non-parallelized code executes in 3.8 minutes on
a hadoop-foyer node, a followup effort will get this running in parallel on the hadoop
datanodes using Spark.

###To install:

First clone this github repo to your home directory on the hadoop foyer node:

    cd; git clone git@github.com:infochimps-sales/spark-airline-demo.git 
    
   
Then execute the installer, this will download and install some python libraries to all 
hadoop nodes, and is done in 5 minutes:

    cd spark-airline-demo
    ./install.sh


###To execute:

To submit this spark job to Yarn for execution:

    PYSPARK_PYTHON=/home/$USER/anaconda/bin/python spark-submit smart_maint_spark.py
    

Monitor this job's progress using the Spark UI by browsing:

    Cloudera Manager -> Home -> Yarn -> Resource Manager UI -> application_ID# -> Application Master


The output of this spark job is 3 png images that can be viewed by browsing

    http://cdh-foyer.platform.infochimps:12321/figs
    

###The Demo Storyline:



###Known Issues:


---If the png images are not browse-able, restart the webserver on the hadoop foyer node:

    /home/$USER/anaconda/bin/python -m SimpleHTTPServer 12321 > /dev/null 2>&1 &
    

---Spark's console output is *way* too verbose, I attempted to dial that down on foyer node via:

    sudo cp /opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/etc/spark/conf.dist/log4j.properties.template \
        /opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/etc/spark/conf.dist/log4j.properties


and in log4j.properties set

    log4j.rootCategory=WARN, console


but the above didn't help any...maybe to this on all datanodes?


###Debugging Tips:
        
    
One can execute this demo line-by-line at the python command line, useful for debugging:

    PYSPARK_PYTHON=/home/$USER/anaconda/bin/python pyspark


Then copy-n-past each line from smart_maint_spark.py into the python command line, 
EXCEPT for line 25: sc = SparkContext(conf=conf... 




###Still To do:

---browse the *.png output at http://cdh-foyer.platform.infochimps:12321

---restart the webserver when needed via

    /home/$USER/anaconda/bin/python -m SimpleHTTPServer 12321 > /dev/null 2>&1 &


---land the motor data in Impala, rather than keeping it all in memory.
  
---execute in parallel using these Spark settings:

    conf = SparkConf().setMaster("yarn-client").setAppName("sm-spark")
    sc = SparkContext(conf=conf)


---browse the spark UI:

    http://cdh-foyer.platform.infochimps:4040/jobs/


---why dont these spark jobs show up in cloudera's spark UI?

    http://cdh-rm.platform.infochimps:18088/


###Useful tips for when debugging:

To execute this demo line-by-line at the python command line (useful for debugging):

    PYSPARK_PYTHON=/home/$USER/anaconda/bin/python pyspark


Then copy-n-past each line from sm_spark.pro into the python command line, 
EXCEPT for line 27: sc = SparkContext(conf=conf... 

Alternatively, one can use spark-submit to submit this job to Spark

    PYSPARK_PYTHON=/home/$USER/anaconda/bin/python spark-submit smart_maint_spark.py


the above will run sm_spark.py as a Spark job that is executed locally on the foyer node.
Later the above will be adapted so that the job is run in parallel acrosss all of the
hadoop datanodes.


###ipython

sudo rm -f /usr/bin/python /usr/bin/ipython
sudo ln -s /home/$USER/anaconda/bin/python /usr/bin/python
sudo ln -s /home/$USER/anaconda/bin/ipython /usr/bin/ipython

and to undo the above: 
    sudo rm /usr/bin/python /usr/bin/ipython
    sudo ln -s /usr/bin/python2.6 /usr/bin/python

IPYTHON=1 pyspark
or: PYSPARK_DRIVER_PYTHON=ipython pyspark

