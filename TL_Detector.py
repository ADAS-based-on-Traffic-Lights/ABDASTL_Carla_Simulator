import glob
import os
import sys
import random
import time 
import cv2
import numpy as np

try:
    sys.path.append(glob.glob('../PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

# Constants
IM_RBG_WIDTH  = 1024 
IM_RBG_HEIGHT = 1024
IM_RBG_FOV = 110
# List of Actors in the world
actor_lists=[]

def process_rgb_image(rgba_image):
    """
    Reads, reshape, and normalize the data from the rgb sensor 
    args:
    - rgba_image [array]: raw_data of the rgba image
    
    output:
    - rgb_image [np_array]: normalized rgb image
    """
    flat_rgba_image = np.array(rgba_image.raw_data)
    rgba_image = flat_rgba_image.reshape(IM_RBG_WIDTH,IM_RBG_HEIGHT,4) # The fourth elements is alpha
    rgb_image = rgba_image[:,:,:3]
    cv2.imshow("",rgb_image)
    cv2.waitKey(1)
    return rgb_camera

# Attempt to connect to the server
try:
    # Initial calls 
    ## The client can be changed to a remote ip server
    client = carla.Client("localhost",2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blue_print_library= world.get_blueprint_library()

    # Create Blueprints of the Actors
    ## Cars Blueprints
    cartec_bp = blue_print_library.filter("model3")[0]
    ## Sensors Blueprints
    rgb_camera_bp = blue_print_library.find("sensor.camera.rgb")
    ### The image resolution of the camera is set here *(Importat for NNs)
    rgb_camera_bp.set_attribute("image_size_x" ,f"{IM_RBG_WIDTH}")
    rgb_camera_bp.set_attribute("image_size_y",f"{IM_RBG_HEIGHT}")
    rgb_camera_bp.set_attribute("fov",f"{IM_RBG_FOV}") 

    # Create the spawn location of the actors 
    ## Cars Spawn locations
    cartec_spawn = random.choice(world.get_map().get_spawn_points())
    ## Sensors Spawn locations
    rgb_camera_spawn = carla.Transform(carla.Location(x=2.5,z=0.7))

    # Create Actors with their respective location and Blueprints
    ## Create actor cartec (car) 
    cartec = world.spawn_actor(cartec_bp, cartec_spawn)
    cartec.apply_control(carla.VehicleControl(throttle=0.5, steer= 0.0))
    actor_lists.append(cartec)
    ## Create actor rgb_camera (sensor)
    rgb_camera = world.spawn_actor(rgb_camera_bp,rgb_camera_spawn,attach_to=cartec)
    rgb_camera.listen(lambda data: process_rgb_image(data))
    actor_lists.append(rgb_camera)

    time.sleep(10)

# Clean up all the actors from the server
finally: 
    for actor in actor_lists:
        actor.destroy()
    print("All actors have been removed") 
