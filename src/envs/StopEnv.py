from BaseEnv import *
from threading import Thread

class StopEnv(BaseEnv):
    def __init__(self):
        super().__init__()
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(8,), dtype=np.float32)
        self._connect_socket()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        for i in range(4):
            self.s.sendto(np.array([0] * 4).astype(np.float32).tobytes(), ("192.168.222.122", self.port))  # 10.12.1.59
            sleep(0.1)
        self.listen_bool = False
        self.current_velocity = np.array([100] * 2, dtype=np.float32)
        sleep(1)
        self.listen_bool = True
        Thread(target=self._listen).start()
        sleep(3)
        obs, _ = self.get_obs()
        return obs, {}

    def get_obs(self):
        raw_data = np.array(self.euler_deque)
        average_array = np.mean(raw_data, axis=0)
        normalized_vel = (self.current_velocity - 150) / 50
        obs = np.concatenate((np.clip(average_array[:-1], -1, 1), normalized_vel))
        reward = average_array[-1]
        normalized_vel = (normalized_vel + 1) / 2
        reward += 10*(1 - np.mean(normalized_vel, axis=0))
        return obs, reward

    def step(self, action):
        denormalized_action = self.denormalize_action(action)
        if not np.any(np.isnan(action)):
            for i in range(3):
                self.s.sendto(denormalized_action.astype(np.float32).tobytes(), ("192.168.222.122", self.port))  # 10.12.1.59
                sleep(0.01)
        obs, reward = self.get_obs()
        info = {}
        sleep(0.02)
        return obs, reward, False, False, info