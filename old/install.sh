#!/bin/bash 

#This bash script installs the smart-maintenance-demo on the hadoop foyer of the BDPaaS.
#
#To execute:    ./install

#install anaconda python on the /data drive on all hadoop nodes
hosts=( 'cdh-foyer' 'cdh-nn' 'cdh-rm' 'cdh-hh' )
for host in "${hosts[@]}"; do
    ssh -A $host 'echo; echo; echo installing python libraries on $(hostname)...;
        echo; echo;
        rm -rf Anaconda-2.1.0-Linux-x86_64.sh* anaconda;
        wget -nv http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.1.0-Linux-x86_64.sh;
        chmod +x Anaconda-2.1.0-Linux-x86_64.sh;
        ./Anaconda-2.1.0-Linux-x86_64.sh -b;
        rm -rf Anaconda-2.1.0-Linux-x86_64.sh'
done

#start webserver in background, to browse output
/home/$USER/anaconda/bin/python -m SimpleHTTPServer 12321 > /dev/null 2>&1 &