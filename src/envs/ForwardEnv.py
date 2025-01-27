from BaseEnv import *
from threading import Thread

class ForwardEnv(BaseEnv):
    def __init__(self):
        super().__init__()
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(9,), dtype=np.float32)
        self.counter = 0
        self.prev_argmax = 0
        self.prev_max_value = 0
        self._connect_socket()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        for i in range(4):
            self.s.sendto(np.array([0] * 6).astype(np.float32).tobytes(), ("192.168.1.92", self.port))  # 10.12.1.59
            sleep(0.1)
        self.listen_bool = False
        self.current_velocity = np.array([100] * 2, dtype=np.float32)
        self.counter = 0
        self.prev_argmax = 0
        self.prev_max_value = 0
        sleep(1)
        self.listen_bool = True
        Thread(target=self._listen).start()
        sleep(4)
        obs, _ = self.get_obs()
        return obs, {}

    def get_obs(self):
        raw_data = np.array(self.euler_deque)
        average_array = np.mean(raw_data, axis=0)
        normalized_vel = (self.current_velocity - 140) / 40
        obs = np.concatenate((np.clip(average_array[:-1], -1, 1), normalized_vel))
        reward = 4 * average_array[-1]
        normalized_vel = (normalized_vel + 1) / 2
        argmax = np.argmax(normalized_vel)
        max_value = normalized_vel[argmax]
        if argmax == self.prev_argmax:
            self.counter += 1
            if self.counter > 12:
                reward = -4
            else:
                min_value = np.min(normalized_vel)
                if max_value - self.prev_max_value > 0:
                    incr_rew = 30 * np.exp(-pow((max_value - 1)/0.55, 4))
                    incr_rew -= 28 * np.exp(-pow((min_value - 1)/0.6, 6))
                    reward += incr_rew
                else:
                    reward += 2
        else:
            self.counter = 0
        count_obs = np.clip((self.counter - 8) / 8, -1, 1)
        obs = np.append(obs, count_obs).astype(np.float32)
        self.prev_max_value = max_value
        self.prev_argmax = argmax
        return obs, reward

    def step(self, action):
        denormalized_action = self.denormalize_action(action)
        if not np.any(np.isnan(action)):
            for i in range(3):
                self.s.sendto(denormalized_action.astype(np.float32).tobytes(), ("192.168.1.92", self.port))  # 10.12.1.59
                sleep(0.01)
        obs, reward = self.get_obs()
        info = {}
        sleep(0.02)
        return obs, reward, False, False, info