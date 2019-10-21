CARLA Driving Benchmarks Repository
===================================


This repository was made in order to store different driving benchmarks
that run on the [CARLA simulator](https://github.com/carla-simulator/carla)

Right now we have available the following benchmarks:

Version 0.8.4:

* CoRL2017 - [Docs](Docs/benchmark_start.md/#corl-2017) / [Paper](http://proceedings.mlr.press/v78/dosovitskiy17a/dosovitskiy17a.pdf).

* NoCrash - [Docs](Docs/benchmark_start.md/#carla-100) /[Paper] 

[Version 0.9.6](Docs/benchmark_start.md)


We are working on having a 0.9.X version of the CoRL2017 Benchmark.
We happily accept new benchmarks as pull requests.


License
-------

CARLA Benchmarks specific code is distributed under MIT License.





## Benchmarking


This repository replaces the benchmarking repo of the CARLA repository
It receives an experience description file (json file) 

There are also alias that automatically generate the benchmarks
for some of the main benchmarks showed on papers.



### Benchmark 
This command benchmarks a dummy agent (goes forward) on a sample
three episodes benchmark: 

    python3 benchmark_runner.py -b database/sample_benchmark.json -d <docker_image_name> -a cexp/agents/DummyAgent.py

The  CARLA docker images can be obtained by using [this tutorial](https://carla.readthedocs.io/en/latest/carla_docker/)

### Benchmark some published benchmarks

#### CORL 2017 from ()

python3 benchmark_runner.py -b CoRL2017 -d <docker_image_name> -a cexp/agents/DummyAgent.py

#### No Crash from ()

python3 benchmark_runner.py -b NoCrash -d <docker_image_name> -a cexp/agents/DummyAgent.py

#### CARLA Challenge 2019 test prep 

TO BE ADDED
