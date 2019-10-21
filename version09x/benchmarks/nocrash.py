
import json
import os


from version09x.benchmark import benchmark

def produce_csv():  # Maybe leave just like the empty task here.
    pass


def perform(docker, gpu, agent, config, port, agent_name, non_rendering_mode):

    # Perform the benchmark

    # empty
    conditions = ['training', 'newtown', 'newweathertown', 'newweather']

    tasks = ['empty', 'regular', 'dense']

    towns = {'training': 'Town01',
             'newweather': 'Town01',
             'newtown': 'Town02',
             'newweathertown': 'Town02'}



    for c in conditions:
        for t in tasks:
            benchmark_file = os.path.join('version09x','descriptions', 'nocrash',
                                          'nocrash_' + c + '_' + t + '_' + towns[c] + '.json')
            print (" STARTING BENCHMARK ", benchmark_file)
            benchmark(benchmark_file, docker, gpu, agent, config, port=port,
                      agent_checkpoint_name=agent_name, non_rendering_mode=non_rendering_mode)



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
                                    "SoftRainSunset"]
                    }

    tasks = {'empty': { 'Town01': {},
                        'Town02': {}
                        },
             'regular': { 'Town01': {'background_activity': {"vehicle.*": 20,
                                                            "walker.*": 50}} ,
                          'Town02': {'background_activity': {"vehicle.*": 15,
                                                              "walker.*": 50}}

             },
             'dense': {'Town01': {'background_activity': {"vehicle.*": 100,
                                                             "walker.*": 250}},
                         'Town02': {'background_activity': {"vehicle.*": 70,
                                                             "walker.*": 150}}

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


if __name__ == '__main__':
    generate_nocrash_config_file()