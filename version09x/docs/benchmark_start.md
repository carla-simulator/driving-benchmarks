
## Benchmarking


This repository replaces the benchmarking repo of the CARLA repository
It receives an experience description file (json file) 

There are also alias that automatically generate the benchmarks
for some of the main benchmarks showed on papers.

### Getting Started 
 

First step: have the CARLA environment generator up and running.



### Benchmark some published benchmarks

#### CORL 2017 from ()

python3 benchmark_runner.py -b CoRL2017 -d <docker_image_name> -a cexp/agents/DummyAgent.py

#### No Crash from ()

python3 benchmark_runner.py -b NoCrash -d <docker_image_name> -a cexp/agents/DummyAgent.py

#### CARLA Challenge 2019 test prep 

TO BE ADDED



### Benchmark 
This command benchmarks a dummy agent (goes forward) on a sample
three episodes benchmark: 

    python3 benchmark_runner.py -b database/sample_benchmark.json -d <docker_image_name> -a cexp/agents/DummyAgent.py

The  CARLA docker images can be obtained by using [this tutorial](https://carla.readthedocs.io/en/latest/carla_docker/)