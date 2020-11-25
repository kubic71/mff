import matplotlib.animation
import matplotlib.pyplot as plt
import wrappers
import gym
import car_racing_environment
import numpy as np
import os
from PIL import Image
import json
import tensorflow as tf
import random
from vae.vae import CVAE
# from env import make_env
from utils import PARSER
args = PARSER.parse_args(['--config_path', 'configs/carracing.config'])

import pygame
pygame.init()
screen = pygame.display.set_mode((600, 300))

frame_skip = 3
seed = 2
env = wrappers.EvaluationWrapper(wrappers.VaeCarWrapper(gym.make(
    "CarRacingSoftFS{}-v0".format(frame_skip))), seed, evaluate_for=15, report_each=1)

DATA_DIR = "export"
model_path_name = "models/tf_vae".format(args.exp_name, args.env_name)
vae = CVAE(args)
vae.set_weights(tf.keras.models.load_model(
    model_path_name, compile=False).get_weights())

filelist = os.listdir(DATA_DIR)
obs = np.load(os.path.join(DATA_DIR, random.choice(filelist)))["obs"]
obs = obs.astype(np.float32)/255.0

def resize(img, factor):
    obs = Image.fromarray(img, mode="RGB").resize((64 * factor, 64 * factor))
    return np.array(obs)


while True:
    state, done = env.reset(start_evaluation=True), False

    while not done:

        batch_z = vae.encode(state.reshape(1, 64, 64, 3)/255)
        reconstruct = vae.decode(batch_z)
        screen.fill((0,0,0))
        screen.blit(pygame.surfarray.make_surface(resize(state, 3)), (0, 0))
        screen.blit(pygame.surfarray.make_surface(resize(reconstruct[0], 3)), (300, 0))
        pygame.display.flip()

        # plt.imshow(state)
        # plt.show()


        # plt.imshow(reconstruct[0])
        # plt.show()

        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


pygame.quit()
frame = random.choice(obs).reshape(1, 64, 64, 3)


print("Original")
plt.imshow(frame[0])
plt.show()

batch_z = vae.encode(frame)
print(batch_z[0])  # print out sampled z
reconstruct = vae.decode(batch_z)

print("Reconstruction")
plt.imshow(reconstruct[0])
plt.show()
