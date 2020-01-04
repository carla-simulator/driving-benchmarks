import logging
class DummyAgent(object):

    def get_sensors_dict(self):
        """
        The agent sets the sensors that it is going to use. That has to be
        set into the environment for it to produce this data.
        """
        sensors_dict = [
                        {'type': 'sensor.other.gnss',
                         'x': 0.7, 'y': -0.4, 'z': 1.60,
                         'id': 'GPS'},
                        {'type': 'sensor.camera.rgb',
                         'x': 2.0, 'y': 0.0,
                         'z': 1.40, 'roll': 0.0,
                         'pitch': -15.0, 'yaw': 0.0,
                         'width': 800, 'height': 600,
                         'fov': 100,
                         'id': 'rgb'},
                        {'type': 'sensor.camera.depth',
                         'x': 2.0, 'y': 0.0,
                         'z': 1.40, 'roll': 0.0,
                         'pitch': -15.0, 'yaw': 0.0,
                         'width': 800, 'height': 600,
                         'fov': 100,
                         'id': 'depth'}
                        ]

        return sensors_dict

    def get_state(self, exp_list):
        """
        The state function that need to be defined to be used by cexp to return
        the state at every iteration.
        :param exp_list: the list of experiments to be processed on this batch.
        :return:
        """

        exp = exp_list[0]
        # The first time this function is call we initialize the agent.
        self._setup(exp)
        # Get the directions from the planner like a few papers.
        direction = exp.get_current_direction()

        input = {
            'rgb' : exp.get_sensor_data()['rgb'],
            'direction': direction

        }

        return

    def step(self, state):

        """
        The step function, receives the output from the state function ( get_sensors)

        :param state:
        :return:
        """
        # We print downs the sensors that are being received.
        # The agent received the following sensor data.
        print("=====================>")
        for key, val in state.items():
            if hasattr(val[1], 'shape'):
                shape = val[1].shape
                print("[{} -- {:06d}] with shape {}".format(key, val[0], shape))
            else:
                print("[{} -- {:06d}] ".format(key, val[0]))
        print("<=====================")
        # The sensors however are not needed since this basically run an step for the
        # NPC default agent at CARLA:
        logging.debug("Output %f %f %f " % (control.steer, control.throttle, control.brake))
        return control

    def reset(self):
        print (" Correctly reseted the agent")
        self._route_assigned = False
        self._agent = None