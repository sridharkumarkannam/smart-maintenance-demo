## The Smart Maintenance Demo

by Joe Hahn,
joe.hahn@infochimps.com,
20 May 2015

This is the Github repository for the master branch of the Smart Maintenance Demo for Hadoop.

###To install:

1 ssh into the platform's hadoop foyer node:

     ssh -A joehahn@52.8.44.194
     ssh -A cdh-foyer
     

2 install Anaconda python, which provides a painless way to install nearly all of the python
  libraries to be used here

    wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.1.0-Linux-x86_64.sh 
    bash Anaconda-2.1.0-Linux-x86_64.sh (and accept all defaults)


3 clone the smart maintenance demo

    git clone git@github.com:infochimps-sales/smart-maintenance-demo.git
    cd smart-maintenance-demo/source


4 execute the demo

    ~/anaconda/bin/python smart_maint.py


5 install screen & restart webserver

    sudo yum install screen
    screen -S webserver -X quit
    screen -S webserver -d -m sh -c "cd ~/smart-maintenance-demo/source/data;
        ~/anaconda/bin/python -m SimpleHTTPServer 12321"


6 browse the *.png images stored in http://cdh-foyer.platform.infochimps:12321
    


###Notes (in-progress) on parallelizing this using spark

1 spark/ipython:

	PYSPARK_DRIVER_PYTHON=~/anaconda/bin/ipython /usr/bin/pyspark
	

