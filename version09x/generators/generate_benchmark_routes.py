

"""
This script generates and prints the maps for all the routes used on the benchmarks
that are available
"""

import argparse
import random
import numpy as np
import os
import logging
import sys
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import xml.etree.ElementTree as ET

from cexp.env.server_manager import start_test_server, check_test_server
from cexp.env.datatools.map_drawer import draw_line, draw_map, draw_text, get_map_max_min_positions
from cexp.env.utils.route_configuration_parser import clean_route, parse_routes_file

import carla
from PIL import Image
from tools.converter import Converter

from srunner.challenge.utils.route_manipulation import interpolate_trajectory

from agents.navigation.local_planner import RoadOption

""""
This script generates routes based on the compitation of the start and end scenarios.
"""


# We have a global world object initialized on the beginning to be used by any function
world = None

def estimate_route_distance(route):
    route_length = 0.0  # in meters
    prev_point = route[0][0]
    for current_point, _ in route[1:]:
        dist = current_point.location.distance(prev_point.location)
        route_length += dist
        prev_point = current_point


    return route_length


def is_distance_ahead(point_a, point_b, distance):
    """
    Check if the ROUTE distance between two points is bigger than "distance"
    :param point_a:
    :param point_b:
    :param distance:
    :return:
    """
    global world

    _, route = interpolate_trajectory(world, [point_a.location, point_b.location])

    return distance < estimate_route_distance(route)


def is_straight_ahead(point_a, point_b, distance):
    """
    Check if the ROUTE distance between two points is bigger than "distance"
    :param point_a:
    :param point_b:
    :param distance:
    :return:
    """

    _, route_initial = interpolate_trajectory(world, [point_a.location, point_b.location])
    if estimate_route_distance(route_initial) < distance or \
        estimate_route_distance(route_initial) > 3*distance:
        print ("Rejected because it is too small")
        return False
    route = clean_route(route_initial)

    print (" Straight test ")

    # TODO analize the size of the straight
    if len(route) > 3:
        print ("Rejected because of size")
        return False

    for point in route:

        # Check if there are any curve
        if point[2] == RoadOption.LEFT or point[2] == RoadOption.RIGHT:
            print ("Rejected because of curve")
            return False


    yaw_difference = point_a.rotation.yaw - point_b.rotation.yaw
    print (" yaw difference is ", yaw_difference)
    if math.fabs(yaw_difference) > 10 and math.fabs(yaw_difference) < 340:
        print ("Rejected because of curve")
        return False


    return True


def is_one_turn_ahead(point_a, point_b, distance):
    """
    Check if the ROUTE distance between two points is bigger than "distance"
    :param point_a:
    :param point_b:
    :param distance:
    :return:
    """
    _, route_initial = interpolate_trajectory(world, [point_a.location, point_b.location])
    if estimate_route_distance(route_initial) < distance or \
        estimate_route_distance(route_initial) > 3*distance:
        print ("Rejected because it is too small")
        return False
    route = clean_route(route_initial)

    print ( " One curve test ")
    if len(route) != 1:
        print (" reject because of size")
        return False
    for point in route:
        # Check if there are any curve
        if point[2] == RoadOption.STRAIGHT:
            print (" reject due to straight")
            return False


    return True




def write_routes(ofilename, output_routes, town_name):

    with open(ofilename, 'w+') as fd:
        fd.write("<?xml version=\"1.0\"?>\n")
        fd.write("<routes>\n")
        for idx, route in enumerate(output_routes):
            fd.write("\t<route id=\"{}\" map=\"{}\"> \n".format(idx, town_name))
            for wp in route:
                fd.write("\t\t<waypoint x=\"{}\" y=\"{}\" z=\"{}\"".format(wp.location.x,
                                                                           wp.location.y,
                                                                           wp.location.z)
                         )

                fd.write(" pitch=\"{}\" roll=\"{}\" yaw=\"{}\" " "/>\n".format(wp.rotation.pitch,
                                                                               wp.rotation.roll,
                                                                               wp.rotation.yaw)
                         )
            fd.write("\t</route>\n")

        fd.write("</routes>\n")

def read_routes(route_filename):

    list_route_descriptions = []
    tree = ET.parse(route_filename)
    for route in tree.iter("route"):
        route_town = route.attrib['map']
        route_id = route.attrib['id']
        waypoint_list = []  # the list of waypoints that can be found on this route
        for waypoint in route.iter('waypoint'):
             waypoint_list.append(carla.Transform(
                                    location = carla.Location(x=float(waypoint.attrib['x']),
                                                              y=float(waypoint.attrib['y']),
                                                              z=float(waypoint.attrib['z'])),
                                    rotation = carla.Rotation(roll=float(waypoint.attrib['roll']),
                                                              pitch=float(waypoint.attrib['pitch']),
                                                              yaw=float(waypoint.attrib['yaw']))
                                   )
                                  )  # Waypoints is basically a list of XML nodes

        list_route_descriptions.append(waypoint_list)

    return list_route_descriptions


def view_start_positions(world, routes_to_plot, file_name):

    def draw_route(route_pair, count):


        initial_point, end_point = route_pair[0], route_pair[1]
        _, trajectory = interpolate_trajectory(world, [initial_point.location, end_point.location])

        prev_point = trajectory[0]

        print (" Draw line for trajectoryyy of len ", len(trajectory))
        for point in trajectory[1:]:
            draw_line(prev_point[0].location, point[0].location, color_palet[count],
                      4, alpha=0.6)
            prev_point = point

        draw_text(str(count), end_point.location, (1, 0, 0), 5)



    # We assume the CARLA server is already waiting for a client to connect at
    # host:port. The same way as in the client example.


    color_palet = [(1,0,0), (0,1,0), (0,0,1),
                   (1,1,0), (0,1,1), (1,0,1),
                   (0,0,0), (1,1,1), (0.5,1,0),
                   (0, 0.5, 1),  (0.5,0,1), (1,0.5,0),
                   (0, 1, 0.5), (1,0,0.5), (0.5, 0.5, 1),
                   (1, 0.5, 0.5), (0.5, 1, 0.5), (0.5, 0.5, 1),
                   (1, 0, 0), (0, 1, 0), (0, 0, 1),
                   (1, 1, 0), (0, 1, 1), (1, 0, 1),
                   (0, 0, 0), (1, 1, 1)
                   ]

    x_min, x_max, y_min, y_max = \
        get_map_max_min_positions(world.get_map().get_topology())

    count = 0
    for route_pair in routes_to_plot:

        fig, ax = plt.subplots(1)
        # TODO autoadjust this size.
        plt.xlim((x_min*12)-300, (x_max*12)+300)
        plt.ylim((y_min*12)-300, (y_max*12)+300)
        draw_map(world)
        draw_route(route_pair, count)

        plt.axis('off')
        fig.savefig(os.path.join(file_name, str(count) + '.pdf'),
                    orientation='landscape', bbox_inches='tight')
        plt.close(fig)
        count += 1

    fig_all, ax_all = plt.subplots(1)

    count = 0
    # TODO autoadjust this size.
    plt.xlim((x_min*12)-300, (x_max*12)+300)
    plt.ylim((y_min*12)-300, (y_max*12)+300)
    draw_map(world)
    for route_pair in routes_to_plot:

        draw_route(route_pair, count)
        count += 1

    plt.axis('off')
    fig_all.savefig(file_name + '.pdf',
                    orientation='landscape', bbox_inches='tight')
    plt.close(fig_all)

def generate_pairs(number_of_pairs, spawn_positions, pair_type, distance=0.0):

    """
    Given the spawn positions get ones that are the type of selected pairs, ahead
    they can be
        Straight
        Curve
        DistanceBased
    :param number_of_pairs:
    :param spawn_positions:
    :return:
    """
    if pair_type == 'straight':
        check_pair = is_straight_ahead
    elif pair_type == 'curve' or pair_type == 'one_curve':
        check_pair = is_one_turn_ahead
    elif pair_type == 'navigation':
        check_pair = is_distance_ahead
    else:
        raise ValueError("Wrong Pair Type")

    resulting_pairs = []
    counting_pairs = 0
    while counting_pairs < number_of_pairs:
        random.shuffle(spawn_positions) # Make the choice actually between random positions
        spawn_start = spawn_positions[0]
        for spawn_end in spawn_positions[1:]:
            if spawn_start != spawn_end:
                print (spawn_start, spawn_end)
                if check_pair(spawn_start, spawn_end, distance):
                    print ("Acepted")
                    resulting_pairs.append([spawn_start, spawn_end])
                    counting_pairs += 1

                if counting_pairs >= number_of_pairs:
                    return  resulting_pairs
            spawn_start = spawn_end

    return resulting_pairs



if __name__ == '__main__':


    description = ("CARLA AD Challenge evaluation: evaluate your Agent in CARLA scenarios\n")

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-t', '--town', default='Town02', help='The town name to be used')

    parser.add_argument('-o', '--output',
                        default=None, help='The outputfile route')

    parser.add_argument('-v', '--view',
                        default=None, help='The path to where things are placed ')


    arguments = parser.parse_args()

    if not check_test_server(6669):
        start_test_server(6669, docker_name='carlaped')
        print (" WAITING FOR DOCKER TO BE STARTED")

    client = carla.Client('localhost', 6669)
    print ("\n\n SAVY4 \n\n")
    client.set_timeout(30.0)

    if arguments.output is None and arguments.view is None:
        raise  ValueError("Both output and view are None ")

    if arguments.output is None:
        file_identification = arguments.view
    else:
        file_identification = arguments.output

    # We set the file names for all the cases
    # The output specifies how exactly thje name is going to be
    navigation_filename = arguments.town + '_navigation' + file_identification
    oneturn_filename = arguments.town + '_one_curve' + file_identification
    straight_filename = arguments.town + '_straight' + file_identification

    world = client.load_world(arguments.town)

    spawn_points = world.get_map().get_spawn_points()

    if not os.path.exists('_route_files'):
        os.mkdir('_route_files')

    # NAVIGATION
    if arguments.view is None:
        # navigation_pairs = generate_pairs(25, spawn_points, 'navigation', distance=750.0) 1000.0
        navigation_pairs = generate_pairs(25, spawn_points, 'navigation', distance=500.0)
        if not os.path.exists('_route_files/_' + arguments.town + '_navigation'):
            os.mkdir('_route_files/_' + arguments.town + '_navigation')

        write_routes(navigation_filename, navigation_pairs, town_name=arguments.town)

    else:
        navigation_pairs = read_routes(navigation_filename)

    view_start_positions(world, navigation_pairs,
                         '_route_files/_' + arguments.town + '_navigation')

    exit(1)
    # STRAIGHT
    if arguments.view is None:
        straight_pairs = generate_pairs(25, spawn_points, 'straight', distance=75.0)
        #straight_pairs = generate_pairs(25, spawn_points, 'straight', distance=100.0) for town01

        if not os.path.exists('_route_files/_' + arguments.town + '_straight'):
            os.mkdir('_route_files/_' + arguments.town + '_straight')
        write_routes(straight_filename, straight_pairs, town_name=arguments.town)

    else:
        straight_pairs = read_routes(straight_filename)

    view_start_positions(world, straight_pairs,
                             '_route_files/_' + arguments.town + '_straight')

    # ONE TURN
    if arguments.view is None:
        oneturn_pairs = generate_pairs(25, spawn_points, 'curve', distance=40.0)
        #oneturn_pairs = generate_pairs(25, spawn_points, 'curve', distance=40.0) FOR TOWN01
        if not os.path.exists('_route_files/_' + arguments.town + '_oneturn'):
            os.mkdir('_route_files/_' + arguments.town + '_oneturn')
        write_routes(oneturn_filename, oneturn_pairs, town_name=arguments.town)

    else:
        oneturn_pairs = read_routes(oneturn_filename)

    view_start_positions(world, oneturn_pairs,
                         '_route_files/_' + arguments.town + '_oneturn')