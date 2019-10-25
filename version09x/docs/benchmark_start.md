
## Benchmarking


This repository replaces the benchmarking repo of the CARLA repository
It receives an experience description file (json file) 

There are also alias that automatically generate the benchmarks
for some of the main benchmarks showed on papers.

### Getting Started 
 

You just need to have [the CARLA environment generator up and running](https://github.com/felipecode/cexp/blob/master/docs/getting_started.md)
and add it to your PYTHONPATH

    export PYTHONPATH=<path_to_carla_experience>:$PYTHONPATH

### Benchmark some published benchmarks

WARNING: the docker image should be the one tested on the CARLA CEXP

#### CORL 2017 from ()

python3 benchmark_runner.py -b CoRL2017 -d <docker_image_name> -a version09x/agents/NPCAgent.py

#### No Crash from ()

python3 benchmark_runner.py -b NoCrash -d <docker_image_name> -a version09x/agents/NPCAgent.py

#### CARLA Challenge 2019 test prep 

TO BE ADDED


[Detailed explanation of the benchmark and its results]()


### Benchmark some custom benchmark

This command benchmarks a dummy agent (goes forward) on a sample cust
three episodes benchmark: 

    python3 benchmark_runner.py -b database/sample_benchmark.json -d <docker_image_name> -a cexp/agents/DummyAgent.py

The CARLA docker images can be obtained by using [this tutorial](https://carla.readthedocs.io/en/latest/carla_docker/)


### Defining the Agent Class to be Benchmarked