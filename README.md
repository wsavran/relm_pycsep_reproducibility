# Reproducing RELM results using pyCSEP

This repository contains the reproducibility package for the Savran et al. (2021) SCEC Annual Meeting poster. Specifically, it contains the software and digital artifacts necessary to reproduce Fig. 3. Figs. 1 and 2 can be reproduced directly from the pyCSEP pacakage, because they are tutorials that are self contained within the pyCSEP software distribution. This experiment takes around 6 hours on a modern desktop computer if simulation 1e6 trials per forecast per evaluation (ignoring the Number test).

## Code description

The code to execute the main experiment can be found in the ```scripts``` directory of this repository. There are three ```*.py``` files 
1. ```main_experiment.py```
2. ```experiment_utilites.py```
3. ```experiment_config.py```

Running ```main_experiment.py``` is a self-contained program that will create Fig. 3 from the poster. ```experiment_utilites.py``` contains utility methods used in the experiment, for example, plotting utilites and utilites to load data files. ```experiment_config.py``` contains the configuration for the experiment, and can be modified if users would like to adjust parameters, such as the seed for the PRNG or the number of simulations used in the evaluations. 

In the top-level directory, the script ```./run_all.sh``` is a light-weight shell script that does the following
1. Runs ```download_data.py``` -- Downloads and verifies using md5 checksums the forecast data used in this verification exercise.
2. Creates a Docker image including ```pyCSEP```
3. Runs the experiment using the Docker run time environment. 

## Software dependencies

In order to run this reproducibility package, the user must have access to a Unix shell that has python3 installed with the requests libary. You can install the requests library using

    pip install requests
    
Additionally, you will need to have the Docker runtime environment installed and running on your machine. 
   

## Instructions for running

These instructions assume that your environment is configured correctly with Docker, and python3 with the requests library installed. Running this package is as simple as:

    git clone https://github.com/wsavran/relm_pycsep_reproducibility.git
    cd relm_pycsep_reproducibility
    ./run_all.sh
    
