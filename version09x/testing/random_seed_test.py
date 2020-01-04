import os
import logging
import json
import sys
import subprocess
import importlib
import shutil
import numpy as np
import traceback
from PIL import Image
import PIL

from skimage import io

from tqdm import tqdm
from version09x.benchmark import benchmark_env_loop

from cexp.driving_batch import DrivingBatch

def plot_state_difference(image1, image2, image3, id):
    if not os.path.exists('_differences'):
        os.mkdir('_differences')

    if not os.path.exists('_differences/seed_1'):
        os.mkdir('_differences/seed_1')

    if not os.path.exists('_differences/seed_1b'):
        os.mkdir('_differences/seed_1b')

    if not os.path.exists('_differences/seed_2'):
        os.mkdir('_differences/seed_2')

    if not os.path.exists('_differences/diff'):
        os.mkdir('_differences/diff')

    """
    average_intensity1 = ((image1[:,:,0] + image1[:,:,1] + image1[:,:,2])/3).astype(np.uint8)

    print (image1.shape)

    average_intensity2 = ((image2[:,:,0] + image2[:,:,1] + image2[:,:,2])/3).astype(np.uint8)
    # Make this grayscale three channels

    difference_mask = np.round(np.abs(average_intensity1 - average_intensity2)/255)

    print ( " diff sum ", np.sum(np.abs(average_intensity1 - average_intensity2)))

    ploting_image = np.stack([255*difference_mask + image2[:,:, 0]*(1-difference_mask),
                              image2[:,:, 1]*(1-difference_mask),
                              image2[:, :, 2] * (1 - difference_mask)], 2)

    Image.fromarray(ploting_image.astype(np.uint8)).save('_differences/diff/' + str(id) + '.png')
    """
    Image.fromarray(image1.astype(np.uint8)).save('_differences/seed_1/' + str(id) + '.png')

    Image.fromarray(image2.astype(np.uint8)).save('_differences/seed_2/' + str(id) + '.png')
    Image.fromarray(image2.astype(np.uint8)).save('_differences/seed_1b/' + str(id) + '.png')



def test_random_seed_loop(env_data_1, env_data_2, env_data_3):

    batch_1, batch_2, batch_3 = env_data_1[0][0][0][0],\
                       env_data_2[0][0][0][0], env_data_3[0][0][0][0]

    step = 0  # Add the size
    number_of_steps =  min(len(batch_1), len(batch_2), len(batch_3))
    while step < number_of_steps:
        data_point_1, data_point_2, data_point_3 = batch_1[step], batch_2[step], batch_3[step]
        rgb_1 = io.imread(data_point_1['rgb_central'])[:, :, :3]
        rgb_2 = io.imread(data_point_2['rgb_central'])[:, :, :3]
        rgb_1b = io.imread(data_point_3['rgb_central'])[:, :, :3]
        plot_state_difference(rgb_1, rgb_2, rgb_1b, step)

        step += 1

    subprocess.call(['ffmpeg', '-f', 'image2', '-i', os.path.join("_differences/seed_1",
                                                                  '%d.png'),
                     '-vcodec', 'mpeg4', '-y', '_differences/seed1.mp4'])
    subprocess.call(['ffmpeg', '-f', 'image2', '-i', os.path.join("_differences/seed_2",
                                                                  '%d.png'),
                     '-vcodec', 'mpeg4', '-y', '_differences/seed2.mp4'])
    subprocess.call(['ffmpeg', '-f', 'image2', '-i', os.path.join("_differences/seed_1b",
                                                                  '%d.png'),
                     '-vcodec', 'mpeg4', '-y', '_differences/seed1b.mp4'])
    #subprocess.call(['ffmpeg', '-f', 'image2', '-i', os.path.join("_differences/diff",
    #                                                              '%d.png'),
    #                 '-vcodec', 'mpeg4', '-y', '_differences/diff.mp4'])



if __name__ == '__main__':
    #root = logging.getLogger()
    #root.setLevel(logging.DEBUG)

    #handler = logging.StreamHandler(sys.stdout)
    #handler.setLevel(logging.DEBUG)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #handler.setFormatter(formatter)
    #root.addHandler(handler)
    # Run like

    params = {'save_dataset': True,
              'save_sensors': True,
              'make_videos': False,
              'docker_name': 'carlaped',
              'gpu': "0",
              'batch_size': 1,
              'remove_wrong_data': False,
              'non_rendering_mode': False,
              'carla_recording': True
              }
    env_batch = None
    # this could be joined
    benchmark_name = 'version09x/descriptions/random_seed_test.json'

    port = 6666
    recollect = True

    from version09x.agents.NPCAgent import NPCAgent

    while True:
        try:

            # We reattempt in case of failure of the benchmark
            dbatch1 = DrivingBatch(benchmark_name, params, port=port)
            # to load CARLA and the scenarios are made
            # Here some docker was set
            dbatch1.start(agent_name='test_agent_r1')
            # take the path to the class and instantiate an agent
            agent = NPCAgent(None)
            # if there is no name for the checkpoint we set it as the agent module name
            # We accumulate the data separatelly
            episodes_data = []
            if recollect:
                with tqdm(total=len(dbatch1)) as pbar:  # we keep a progress bar

                    for  renv in dbatch1:
                        try:
                            # Just execute the environment.
                            # For this case the rewards doesnt matter.
                            benchmark_env_loop(renv, agent)
                            episodes_data.append(renv.get_data())
                            pbar.update(1)

                        except KeyboardInterrupt:
                            break
                        except Exception as e:
                            traceback.print_exc()
                            # By any exception you have to delete the environment generated data
                            raise e
            else:
                for renv in dbatch1:
                    episodes_data.append(renv.get_data())

            test_random_seed_loop(episodes_data[0], episodes_data[1], episodes_data[2])
            del env_batch
            break
        except KeyboardInterrupt:
            del env_batch
            break
        except:
            traceback.print_exc()
            del env_batch
            break

