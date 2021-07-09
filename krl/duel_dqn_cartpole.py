import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.processors import Processor

class CustomProcessor(Processor):
    '''
    acts as a coupling mechanism between the agent and the environment
    '''

    def process_state_batch(self, batch):
        '''
        Given a state batch, I want to remove the second dimension, because it's
        useless and prevents me from feeding the tensor into my CNN
        '''
        return numpy.squeeze(batch, axis=1)

ENV_NAME = "JSSEnv:jss-v1"


env = gym.make(ENV_NAME, env_config={"instance_path": "instance.txt"})
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model regardless of the dueling architecture
# if you enable dueling network in DQN , DQN will build a dueling network base on your model automatically
# Also, you can build a dueling network by yourself and turn off the dueling network in DQN.

model = Sequential()
model.add(Flatten(input_shape=np.array((1,) + env.observation_space["action_mask"].shape)))
# model.add(Dense(16, name="l1"))
# model.add(Activation("relu"))
# model.add(Dense(16, name="l2"))
# model.add(Activation("relu"))
# model.add(Dense(16, name="l3"))
# model.add(Activation("relu"))
# model.add(Dense(nb_actions, activation="linear", name="l4"))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
# enable the dueling network
# you can specify the dueling_type to one of {'avg','max','naive'}
dqn = DQNAgent(
    model=model,
    nb_actions=nb_actions,
    memory=memory,
    nb_steps_warmup=10,
    enable_dueling_network=True,
    dueling_type="avg",
    target_model_update=1e-2,
    policy=policy,
)
dqn.compile(Adam(lr=1e-3), metrics=["mae"])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=50000, visualize=False, verbose=2)

# After training is done, we save the final weights.
dqn.save_weights("duel_dqn_{}_weights.h5f".format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=False)
