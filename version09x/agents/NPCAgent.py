import sys
import argparse
import logging
import traceback

from agents.navigation.basic_agent import BasicAgent

class NPCAgent(object):

    def __init__(self, agent_params):
        self._agent_params = agent_params
        self._route_assigned = False
        self._agent = None

    def _setup(self, exp):
        """
        Setup the agent for the current ongoing experiment. Basically if it is
        the first time it will setup the agent.
        :param exp:
        :return:
        """
        if not self._agent:
            self._agent = BasicAgent(exp._ego_actor)

        if not self._route_assigned:
            plan = []
            for transform, road_option in exp._route:
                wp = exp._ego_actor.get_world().get_map().get_waypoint(transform.location)
                plan.append((wp, road_option))

            self._agent._local_planner.set_global_plan(plan)
            self._route_assigned = True

    def get_sensors_dict(self):
        """
        The agent sets the sensors that it is going to use. That has to be
        set into the environment for it to produce this data.
        """
        sensors_dict = [{'type': 'sensor.camera.rgb',
                'x': 2.0, 'y': 0.0,
                'z': 1.40, 'roll': 0.0,
                'pitch': -15.0, 'yaw': 0.0,
                'width': 800, 'height': 600,
                'fov': 100,
                'id': 'rgb_central'}
                        ]

        return sensors_dict

    def get_state(self, exp_list):
        """
        The state function that need to be defined to be used by cexp to return
        the state at every iteration.
        :param exp_list: the list of experiments to be processed on this batch.
        :return:
        """

        # The first time this function is call we initialize the agent.
        self._setup(exp_list[0])
        exp = exp_list[0]
        return exp.get_sensor_data()

    def step(self, state):

        """
        The step function, receives the output from the state function ( get_sensors)

        :param state:
        :return:
        """
        # The sensors however are not needed since this basically run an step for the
        # NPC default agent at CARLA:
        control = self._agent.run_step()
        logging.debug("Output %f %f %f " % (control.steer, control.throttle, control.brake))
        return control

    def reset(self):
        self._route_assigned = False
        self._agent = None