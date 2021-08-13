import glob
import os
import sys
import random
import time 

try:
    sys.path.append(glob.glob('../PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_lists=[]

# Attempt to connect to the server
try:
    ## The client can be changed to a remote ip server
    client = carla.Client("localhost",2000)
    client.set_timeout(10.0)

    world = client.get_world()

    blue_print_library= world.get_blueprint_library()

    # Create Blueprints of the Actors
    cartec_bp = blue_print_library.filter("model3")[0]
    print(cartec_bp)

    # Create the spawn location of the actors 
    cartec_spawn = random.choice(world.get_map().get_spawn_points())

    # Create Actors with their respective location and Blueprints
    ## Create the actor cartec to 
    cartec = world.spawn_actor(cartec_bp, cartec_spawn)
    cartec.apply_control(carla.VehicleControl(throttle=1.0, steer= 0.0))
    actor_lists.append(cartec)

    time.sleep(10)

# Clean up all the actors from the server
finally: 
    for actor in actor_lists:
        actor.destroy()
    print("All actors have been removed") 
