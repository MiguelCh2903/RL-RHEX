from collections import deque
from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

import gymnasium as gym
import numpy as np

class BaseEnv(gym.Env):
    def __init__(self):
        self.host = "192.168.222.10"  # "10.12.1.11"
        self.port = 8888
        self.euler_deque = deque(maxlen=2)

        self.listen_bool = True

        # Action space setting
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        self.current_velocity = np.array([100] * 4, dtype=np.float32)

    def _connect_socket(self):
        try:
            self.s = socket(AF_INET, SOCK_DGRAM)
            self.s.bind((self.host, self.port))
        except OSError:
            pass

    def denormalize_action(self, action):
        denormalized = np.zeros(6)
        self.current_velocity += 8 * action
        np.clip(self.current_velocity, 100, 180, out=self.current_velocity)
        denormalized[[0, 2, 4]] = self.current_velocity[0]
        denormalized[[1, 3, 5]] = self.current_velocity[1]
        return np.round(denormalized)

    def _listen(self):
        while self.listen_bool:
            # Recibir datos por UDP
            message, _ = self.s.recvfrom(1024)
            # Convertir los datos binarios a un array de floats
            received_floats = np.frombuffer(message, dtype=np.float32)
            self.euler_deque.append(received_floats)
        # print("End...")

    def close(self):
        self.listen_bool = False
        sleep(1)
        self.s.close()