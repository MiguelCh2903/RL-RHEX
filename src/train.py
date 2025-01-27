import rl_zoo3.train
from rl_zoo3.train import train
from gymnasium.envs.registration import register
from sbx import SAC

rl_zoo3.ALGOS["sac"] = SAC
rl_zoo3.train.ALGOS = rl_zoo3.ALGOS

register(
     id="ForwardEnv",
     entry_point="env:ForwardEnv",
     max_episode_steps=200,
)

register(
     id="StopEnv",
     entry_point="env:StopEnv",
     max_episode_steps=200,
)

if __name__ == "__main__":
    train()
