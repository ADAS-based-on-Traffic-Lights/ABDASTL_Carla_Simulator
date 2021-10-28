# Carla_Simulator_Traffic_Lights

## Built with 
This project was built with:
* Python 3.7.11
* Carla Simulator 0.9.5
* pygame 2.0.1
* numpy 1.21.1
* conda 4.9.2

## Installation Dependencies
First Download the Carla simulator.

After that, clone the repo as follows:
```
https://github.com/AndresGarciaEscalante/Carla_Simulator_Traffic_Lights.git
```

Create a conda environment with:
```
conda create --name TL python=3.7
```

Once you are inside the environment, then install the following dependencies:
```
pip install --user pygame numpy
pip install opencv-python
pip install -U numpy
```

## About the Project
This project uses the Carla simulator to emulate the behaviour of the Emergency Brake Driver Assistant System from Traffic Lights using Deep Learning and Fuzzy Logic, which is my master thesis at Tecnologico de Monterrey. 

## Run the Simulator with:
```
./CarlaUE4.exe Town03 -windowed -ResX=160 -ResY=120 -quality-level=Low
```