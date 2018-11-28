# -*- coding: utf-8 -*-
# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
# @author: german,felipecode


from __future__ import print_function
import abc
from ..carla.client import VehicleControl


class Agent(object):
    def __init__(self):
        self.__metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run_step(self, measurements, sensor_data, directions, target):
        """
        Function to be redefined by an agent.
        :param The measurements like speed, the image data and a target
        :returns A carla Control object, with the steering/gas/brake for the agent
        """

class ForwardAgent(Agent):
    """
    Simple derivation of Agent Class,
    A trivial agent agent that goes straight
    """
    def run_step(self, measurements, sensor_data, directions, target):
        control = VehicleControl()
        control.throttle = 0.9

        return control