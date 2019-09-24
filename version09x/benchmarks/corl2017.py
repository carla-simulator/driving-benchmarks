
import json
import os

from cexp.benchmark import benchmark


def produce_csv():
    pass

def perform(docker, gpu, agent, config, port):

    # empty
    conditions = ['training', 'newtown', 'newweathertown', 'newweather']

    towns = {'training': 'Town01',
             'newweather': 'Town01',
             'newtown': 'Town02',
             'newweathertown': 'Town02'}

    for c in conditions:
        t = 'empty'
        benchmark_file = os.path.join('database', 'nocrash', 'nocrash_' + c + '_' + t + '_' + towns[c] + '.json')
        print (" STARTING BENCHMARK ", benchmark_file)
        benchmark(benchmark_file, docker, gpu, agent, config, port=port)
        print (" FINISHED ")



def generate():

    root_route_file_position = 'database/corl2017'
    #filename_town01 = os.path.join(root_route_file_position, 'Town01_navigation.json')

    # The sensor information should be on get data
    sensors = [{'type': 'sensor.camera.rgb',
                'x': 2.0, 'y': 0.0,
                'z': 1.40, 'roll': 0.0,
                'pitch': -15.0, 'yaw': 0.0,
                'width': 800, 'height': 600,
                'fov': 100,
                'id': 'rgb'}
               ]

    # For each of the routes to be evaluated.

    # Tows to be generated
    town_sets = {'Town01': {'empty': 'Town01_straight.xml',
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

    tasks = {'empty': {'Town01': {"file": "None"},
                       'Town02': {"file": "None"}
                        },
             'one_curve': {'Town01': {"file": "None"},
                            'Town02': {"file": "None"}
                           },
             'navigation': {'Town01': {"file": "None"},
                            'Town02': {"file": "None"}
                            },

             'navigation_dynamic': {'Town01': {'background_activity': {"vehicle.*": 20,
                                                                        "walker.*": 50}} ,
                                    'Town02': {'background_activity': {"vehicle.*": 15,
                                                                       "walker.*": 50}}
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
                            "additional_sensors": sensors,
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



if __name__ == '__main__':

    generate_corl2017_config_file()