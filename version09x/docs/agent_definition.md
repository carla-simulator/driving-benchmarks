

#### Agent interface 

You have to define some functions in your agent in order for it to be benchmarked.
This interface is made to be as generic as possible so that agents can define
their own rewards and states. It is also made to be parametrizable 
from outside. 


##### The class file name

The class file name should be 


##### The init function

It receives just a set of parameters directly as the first argument.
This argument is sent as a string by the user.


##### def run_step() function

The run step function will receive the object defined by the get_state function.


##### def get_state() function


The get state function receives a list of experiences, that are the current
environments being ran by the cexp. 

This experiment objects have the following functions



##### def get_sensors_dict function


You need to the define the sensors that your agent are going to 
use. This type should be an vector of sensor dictionaries. Some
examples are show on the agents/DummyAgent.py .






Current CARLA benchmarks should go to an webpage.

    get_sensor_dict
    
    step
    
    get_state****
    
    
    

You have to follow this sample class and redefine all the functions

TODO put some tests on this
print aspect

