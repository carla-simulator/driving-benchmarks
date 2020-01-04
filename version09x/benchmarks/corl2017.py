
import json
import os
import sys
import importlib


# TODO perform could be the same function for everyone.

def perform(docker, gpu, agent, config, port, agent_name,
            non_rendering_mode, save_trajectories, small=False):

    # empty
    if small:
        conditions = ['training', 'newtown']
    else:
        conditions = ['training', 'newtown', 'newweathertown', 'newweather']

    tasks = ['empty', 'one_curve', 'navigation', 'navigation_dynamic']

    towns = {'training': 'Town01',
             'newweather': 'Town01',
             'newtown': 'Town02',
             'newweathertown': 'Town02'}


    module_name = os.path.basename(agent).split('.')[0]
    #sys.path.insert(0, os.path.dirname(agent))
    print (" importing the agent ! ! ", module_name, " ", agent)
    agent_module = importlib.import_module(module_name)

    print ( " Trying yo import !")

    from version09x.benchmark import execute_benchmark

    if agent_name is None:
        agent_name = agent_module.__name__
    print ( " Trying yo import !")
    for c in conditions:
        for t in tasks:
            file_name = os.path.join('corl2017', 'corl2017_' + c + '_' + t + '_' + towns[c] + '.json')
            execute_benchmark(file_name,
                              docker, gpu, agent_module, config, port=port,
                              agent_name=agent_name,
                              non_rendering_mode=non_rendering_mode,
                              save_trajectories=save_trajectories,
                              make_videos=make_videos)
            #benchmark_file = os.path.join('version09x/descriptions', 'corl2017',
            #                              'corl2017_' + c + '_' + t + '_' + towns[c] + '.json')
            #print (" STARTING BENCHMARK ", benchmark_file)
            #benchmark(benchmark_file, docker, gpu, agent_module, config, port=port,
            #          agent_checkpoint_name=agent_name, non_rendering_mode=non_rendering_mode,
            #          save_trajectories=save_trajectories)
            # Create the results folder here if it does not exists
            #if not os.path.exists('_results'):
            #    os.mkdir('_results')


            #file_base_out = os.path.join('_results', agent_name + '_corl2017_' + c + '_' + t +
            #                             '.csv')
            #summary_data = check_benchmarked_episodes_metric(benchmark_file,
            #                                                 agent_name)

            #if check_benchmark_finished(benchmark_file, agent_name):
            #    write_summary_csv(file_base_out, agent_name, summary_data)




def is_generated():

    if os.path.exists('version09x/descriptions/corl2017/corl2017_newweather_empty_Town01.json'):
        return True

    else:
        return False

def generate():

    root_route_file_position = 'version09x/descriptions/corl2017'

    # For each of the routes to be evaluated.

    # Tows to be generated
    town_sets = {'Town01': {'straight': 'Town01_straight.xml',
                            'one_curve': 'Town01_one_curve.xml',
                            'navigation': 'Town01_navigation.xml',
                            'navigation_dynamic': 'Town01_navigation.xml'
                            },

                 'Town02': {'empty': 'Town02_straight.xml',
                            'one_curve': 'Town02_one_curve.xml',
                            'navigation': 'Town02_navigation.xml',
                            'navigation_dynamic': 'Town02_navigation.xml'
                            }
                 }

    # Weathers to be generated later
    weather_sets = {'training': ["ClearNoon",
                                 "WetNoon",
                                 "HardRainNoon",
                                 "ClearSunset"],
                    'new_weather':  ["WetSunset",
                                    "SoftRainSunset"]
                    }

    tasks = {'empty': {'Town01': {},
                       'Town02': {}
                        },
             'one_curve': {'Town01': {},
                            'Town02': {}
                           },
             'navigation': {'Town01': {},
                            'Town02': {}
                            },

             'navigation_dynamic': {'Town01': {'background_activity': {"vehicle.*": 20,
                                                                        "walker.*": 50,
                                                                       "cross_factor": 0.1},
                                                                        } ,
                                    'Town02': {'background_activity': {"vehicle.*": 15,
                                                                       "walker.*": 50,
                                                                       "cross_factor": 0.1}
                                               }
             }

    }

    name_dict = {'training':{'Town01': 'training',
                             'Town02': 'newtown'
                             },
                 'new_weather': {'Town01': 'newweather',
                                 'Town02': 'newweathertown'

                 }
    }

    for task_name in tasks.keys():

        for town_name in town_sets.keys():

            for w_set_name in weather_sets.keys():
                # get the actual set  from th name
                w_set = weather_sets[w_set_name]
                new_json = {"envs": {},
                            "package_name": 'corl2017_' + name_dict[w_set_name][town_name] + '_'
                                            + task_name + '_' + town_name}

                for weather in w_set:

                    for env_number in range(25):  # IT is always

                        env_dict = {
                            "route": {
                                "file": town_sets[town_name][task_name],
                                "id": env_number
                            },
                            "scenarios": tasks[task_name][town_name],
                            "town_name": town_name,
                            "vehicle_model": "vehicle.lincoln.mkz2017",
                            "weather_profile": weather,
                            "repetitions": 1

                        }

                        new_json["envs"].update({weather + '_route' + str(env_number).zfill(5): env_dict})

                filename = os.path.join(root_route_file_position, 'corl2017_' + name_dict[w_set_name][town_name] + '_'
                                                                   + task_name + '_' + town_name + '.json')

                with open(filename, 'w') as fo:
                    fo.write(json.dumps(new_json, sort_keys=True, indent=4))


