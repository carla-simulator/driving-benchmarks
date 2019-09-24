import argparse
import os
import logging
import sys



import version09x.benchmarks.corl_2017 as corl2017
import version09x.benchmarks.no_crash as nocrash

from version09x.benchmark import benchmark

# TODO pip install atuomatically for the benchmark runner


# Run the predefined benchmarks
def predefined_benchmarks(args):

    if args.benchmark == 'CoRL2017':
        # This case is the full benchmark in all its glory
        if not corl2017.is_generated():
            corl2017.generate()
        corl2017.perform(args.docker, args.gpu, args.agent, args.config, args.port)

    elif args.benchmark == 'NoCrash':
        # This is generated directly and benchmark is started
        if not nocrash.is_generated():
            nocrash.generate()
        nocrash.perform(args.docker, args.gpu, args.agent, args.config, args.port)
    elif args.benchmark == 'CARLA_AD_2019_VALIDATION':
        print (" The other benchmarks related to carla challenge to be implemented")

    else:
        raise  ValueError(" Alias for benchmark not recognized")


# Use directly the json file based benchmarks.

def json_file_based(args):

    # We try to find the benchmark directly
    benchmark(args.benchmark, args.docker, args.gpu, args.agent, args.config, port=args.port)

# TODO make it able to rubn 084 benchmarks smoothly

if __name__ == '__main__':
    # Run like

    # python3 benchmark -b CoRL2017 -a agent -d
    # python3 benchmark -b NoCrash -a agent -d carlalatest:latest --port 4444

    description = ("Benchmark running")

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-d', '--docker', default=None, help='The dockername to be launched')

    parser.add_argument('-a', '--agent', default=None, help='The full path to the agent class used')

    parser.add_argument('-b', '--benchmark', default=None, help='The benchmark ALIAS or full'
                                                                'path to the json file')

    parser.add_argument('-c', '--config', default=None, help='The path to the configuration file')

    parser.add_argument('-g', '--gpu', default="0", help='The gpu number to be used')

    parser.add_argument('--port', default=None, help='Port for an already existent server')

    parser.add_argument('--debug', action='store_true', help='Set debug mode')

    args = parser.parse_args()

    # Set mode as debug mode
    if args.debug:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    # Test if the user is passing directly a json file or a complete alias for the benchmark.
    if '.json' in args.benchmark:
        json_file_based(args)
    else:
        predefined_benchmarks(args)




