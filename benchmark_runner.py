import argparse
import os
import logging
import sys
import importlib


import version09x.benchmarks.corl2017 as corl2017
import version09x.benchmarks.nocrash as nocrash


# TODO pip install atuomatically for the benchmark runner


# Run the predefined benchmarks
# We have a list of them to be runned.
def predefined_benchmarks(args):

    if args.benchmark == 'CoRL2017':
        # This case is the full benchmark in all its glory
        if not corl2017.is_generated():
            corl2017.generate()
        print ( " It is performed !")
        corl2017.perform(args.docker, args.gpu, args.agent, args.config,
                         args.port, args.agent_name, args.non_rendering_mode,
                         args.draw_trajectories, make_videos=args.make_videos)

    elif args.benchmark == 'NoCrash':
        # This is generated directly and benchmark is started
        if not nocrash.is_generated():
            nocrash.generate()
        nocrash.perform(args.docker, args.gpu, args.agent, args.config,
                        args.port, args.agent_name, args.non_rendering_mode,
                        args.draw_trajectories, make_videos=args.make_videos,)
    elif args.benchmark == 'NoCrashS' or args.benchmark == 'NoCrashSmall':
        # This is generated directly and benchmark is started
        if not nocrash.is_generated():
            nocrash.generate()
        nocrash.perform(args.docker, args.gpu, args.agent, args.config,
                        args.port, args.agent_name, args.non_rendering_mode,
                        args.draw_trajectories, make_videos=args.make_videos, small=True)
    elif args.benchmark == 'NoCrashSW':
        # This is generated directly and benchmark is started
        if not nocrash.is_generated():
            nocrash.generate()
        nocrash.perform(args.docker, args.gpu, args.agent, args.config,
                        args.port, args.agent_name, args.non_rendering_mode,
                        args.draw_trajectories, make_videos=args.make_videos, single_weather=True)

    elif args.benchmark == 'CARLA_AD_2019_VALIDATION':
        print (" The other benchmarks related to carla challenge to be implemented")

    else:
        raise ValueError(" Alias for benchmark not recognized")


# Use directly the json file based benchmarks.

def json_file_based(args):
    from version09x.benchmark import execute_benchmark
    module_name = os.path.basename(args.agent).split('.')[0]
    print (" module name ", module_name)
    sys.path.insert(0, os.path.dirname(args.agent))
    agent_module = importlib.import_module(module_name)
    if args.agent_name is None:
        agent_name = agent_module.__name__
    else:
        agent_name = args.agent_name
    # The json file should be the  path to the json file from the descriptions folder.
    execute_benchmark(args.benchmark, args.docker,
                      args.gpu, agent_module, args.config, args.port, agent_name,
                      args.non_rendering_mode,
                      args.draw_trajectories, args.make_videos)

# TODO make it able to rubn 084 benchmarks smoothly

if __name__ == '__main__':
    # Run like

    # python3 benchmark -b CoRL2017 -a agent -d
    # python3 benchmark -b NoCrash -a agent -d carlalatest:latest --port 4444

    description = ("Benchmark running tool")

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-d', '--docker', default=None, required=True,
                        help='The dockername to be launched')

    parser.add_argument('-a', '--agent', default=None, help='The full path to the agent class used')

    parser.add_argument('-b', '--benchmark', default=None, help='The benchmark ALIAS or full'
                                                                'path to the json file')

    parser.add_argument('-c', '--config', default=None, help='The path to the configuration '
                                                             'file for the agent.')

    parser.add_argument('-mk', '--make_videos', action='store_true', help='If videos '
                                                                         'are goin to be saved')

    parser.add_argument('-g', '--gpu', default="0", help='The gpu number to be used')

    parser.add_argument('-an', '--agent-name', help='if you want to change agent name')

    parser.add_argument('--port', default=None, help='Port for an already existent server')

    parser.add_argument('--non-rendering-mode', action='store_true', help='Set debug mode')

    parser.add_argument('--draw-trajectories', action='store_true',
                        help='Set to draw the trajectories went by the vehicle after the episode')

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




