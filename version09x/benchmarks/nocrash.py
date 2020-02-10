
import json
import os
import sys
import importlib



def perform(docker, gpu, agent, config, port, agent_name, non_rendering_mode,
            save_trajectories, small=False, make_videos=False, single_weather=False):

    """

    :param docker:
    :param gpu:
    :param agent:
    :param config:
    :param port:
    :param agent_name:
    :param non_rendering_mode:
    :param save_trajectories:
    :param small: If small is set to true it means that the only new town conditions will be
                  used
    :return:
    """
    # Perform the benchmark
    if single_weather:
        conditions = ['trainingsw', 'newtownsw']
    elif small:
        conditions = ['training', 'newtown']
    else:
        conditions = ['training', 'newtown', 'newweathertown', 'newweather']

    tasks = ['empty', 'regular', 'dense']

    towns = {'training': 'Town01',
             'newweather': 'Town01',
             'newtown': 'Town02',
             'newweathertown': 'Town02',
             'trainingsw': 'Town01',
             'newtownsw': 'Town02'}

    module_name = os.path.basename(agent).split('.')[0]
    sys.path.insert(0, os.path.dirname(agent))
    print ( "HANG ON IMPORT")
    agent_module = importlib.import_module(module_name)
    if agent_name is None:
        agent_name = agent_module.__name__


    from version09x.benchmark import execute_benchmark

    for c in conditions:
        for t in tasks:
            file_name = os.path.join('nocrash', 'nocrash_' + c + '_' + t + '_' + towns[c] + '.json')
            execute_benchmark(file_name,
                              docker, gpu, agent_module, config, port=port,
                              agent_name=agent_name,
                              non_rendering_mode=non_rendering_mode,
                              save_trajectories=save_trajectories,
                              make_videos=make_videos)

            #benchmark_file = os.path.join('version09x','descriptions', 'nocrash',
            #                              'nocrash_' + c + '_' + t + '_' + towns[c] + '.json')
            #benchmark(benchmark_file, docker, gpu, agent_module, config, port=port,
            #          agent_checkpoint_name=agent_name,
            #          non_rendering_mode=non_rendering_mode,
            #          save_trajectories=save_trajectories)
            # Create the results folder here if it does not exists
            #if not os.path.exists('_results'):
            #    os.mkdir('_results')

            #file_base_out = os.path.join('_results', agent_name + '_nocrash_' + c + '_' + t +
            #                             '.csv')
            #summary_data = check_benchmarked_episodes_metric(benchmark_file,
            #                                                 agent_name)

            #if check_benchmark_finished(benchmark_file, agent_name):
            #    write_summary_csv(file_base_out, agent_name, summary_data)




def is_generated():

    if os.path.exists('version09x/nocrash/nocrash_newtown_dense_Town02.json'):
        return True

    else:
        return False

def generate():

    """
    This function generates the json file with the full benchmark description.
    This is ingested by the CEXP to produce the benchmark.

    It should generate the json description files inside the description folder.
    :return: None
    """


    # TODO this is hardcoded
    root_route_file_position = 'version09x/descriptions/nocrash'

    # For each of the routes to be evaluated.
    # Tows to be generated
    town_sets = {'Town01': 'Town01_navigation.xml',
                 'Town02': 'Town02_navigation.xml'}

    # Weathers to be generated later
    weather_sets = {'training': ["ClearNoon",
                                  "WetNoon",
                                  "HardRainNoon",
                                   "ClearSunset"],
                    'new_weather':  ["WetSunset",
                                    "SoftRainSunset"],
                    'single_weather': ["ClearNoon"]
                    }

    tasks = {'empty': { 'Town01': {},
                        'Town02': {}
                        },
             'regular': { 'Town01': {'background_activity': {"vehicle.*": 20,
                                                            "walker.*": 125,
                                                             "cross_factor": 0.5}} ,
                          'Town02': {'background_activity': {"vehicle.*": 15,
                                                              "walker.*": 100,
                                                             "cross_factor": 0.5}}

             },
             'dense': {'Town01': {'background_activity': {"vehicle.*": 100,
                                                             "walker.*": 400,
                                                          "cross_factor": 0.5}},
                         'Town02': {'background_activity': {"vehicle.*": 70,
                                                             "walker.*": 300,
                                                            "cross_factor": 0.5}}

                         }

    }


    name_dict = {'training':{'Town01': 'training',
                             'Town02': 'newtown'
                             },
                 'new_weather': {'Town01': 'newweather',
                                 'Town02': 'newweathertown'

                 },
                 'single_weather': {'Town01': 'trainingsw',
                              'Town02': 'newtownsw'
                              },
    }

    time_out_dict = {'dense': 1.2,
                     'regular': 1.0,
                     'empty': 0.8 }

    for task_name in tasks.keys():

        for town_name in town_sets.keys():

            for w_set_name in weather_sets.keys():
                # get the actual set  from th name
                w_set = weather_sets[w_set_name]
                new_json = { "default_seconds_per_meter": time_out_dict[task_name],
                            "envs": {},
                            "package_name": 'nocrash_' + name_dict[w_set_name][town_name] + '_'
                                            + task_name + '_' + town_name}

                for weather in w_set:

                    for env_number in range(25):

                        env_dict = {
                            "route": {
                                "file":  town_sets[town_name],
                                "id": env_number
                            },
                            "scenarios": tasks[task_name][town_name],
                            "town_name": town_name,
                            "vehicle_model": "vehicle.lincoln.mkz2017",
                            "weather_profile": weather,
                            "repetitions": 1
                        }

                        new_json["envs"].update({weather + '_route' + str(env_number).zfill(5): env_dict})

                filename = os.path.join(root_route_file_position, 'nocrash_' + name_dict[w_set_name][town_name] + '_'
                                                                   + task_name + '_' + town_name + '.json')

                with open(filename, 'w') as fo:
                    # with open(os.path.join(root_route_file_position, 'all_towns_traffic_scenarios3_4.json'), 'w') as fo:
                    fo.write(json.dumps(new_json, sort_keys=True, indent=4))

