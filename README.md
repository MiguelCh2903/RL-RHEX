# RHex Robot Reinforcement Learning Implementation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Real-world implementation of DroQ algorithm for hexapod locomotion on custom RHex robot with ESP32 microcontroller.

![R-HEX](media/img/img1.png)

## 📖 Project Overview
- **RL Agent**: DroQ algorithm (Stable Baselines3)
- **Hardware**: 6-DoF RHex with ESP32, TB6612 drivers, IMU, and IR binary sensor
- **State Space**: IMU data (orientation, angular velocity) + binary proximity
- **Action Space**: ΔVoltage for 6 motors
- **Training**: 30min on GTX1650 using proprioceptive feedback

![training](media/img/img2.png)

## 🚀 Features
- Custom Gym environment with real-world physics constraints
- Low-latency UDP communication (20Hz update rate)
- Sensor-failure resilient architecture
- Energy-efficient gait learning

## Training
![training video](media/videos/training_first_steps.mp4)

## Evaluation
![evaluation video](media/videos/after_training.gif)