"""
Run this script with MicroPython (on Pico).
"""

from diff_drive.diff_drive_controller import DiffDriveController
from time import sleep
from math import pi


# SETUP
# Instantiate differential drive robot
bot = DiffDriveController(
    left_wheel_configs={
        "motor_pin_ids": (15, 13, 14),
        "encoder_pin_ids": (18, 19),
    },
    right_wheel_configs={
        "motor_pin_ids": (9, 11, 10),
        "encoder_pin_ids": (16, 17),
    },
    enable_pin_id=12,
)
bot.enable()
### Fill in planned angular, linear velocity commands and duration for each segment BELOW ###
# ref_vels = {
#     "s1": (None, None, None),  # segment 1 (cmd_ang_vel, cmd_lin_vel, dur). for example, (0.0, 0.2, 2)
#     "s2": (None, None, None),  # segment 2
#     "s3": (None, None, None),  # segment 3
#     "s4": (None, None, None),  # segment 4
#     "s5": (None, None, None),  # segment 5
#     "s6": (None, None, None),  # segment 6
#     "s7": (None, None, None),  # segment 7
#     "s8": (None, None, None),  # segment 8
# }
plans = (
    (0.0, 0.2, 2),  # for example, (0.0, 0.2, 2)
    (-2.0, 0.2, 1),
    (0.0, 0.2, 1.2),
    (-2.0, 0.2, 1),
    (-1.5, 0.2, 0.7),
    (0.0, 0.2, 1.7),
    (2.3, 0.0, 0.8),
    (0.0, 0.3, 2),
)
### Fill in planned angular, linear velocity commands and duration for each segment ABOVE ###
# Sample rate
rate = 0.05  # 20 Hz
# Create data storage
vel_data = []

# LOOP
# sleep(2)  # uncomment if autostart on duty
# for i in range(400):  # 50Hz controller, 20 seconds
#     meas_lin_vel, meas_ang_vel = bot.get_vels()
#     print(meas_lin_vel, meas_ang_vel)
#     vel_data.append((meas_lin_vel, meas_ang_vel))
#     bot.set_vels(*ref_vels[i // 40])
#     sleep(0.02)
for i, cmd in enumerate(plans):  # 50Hz controller, 20 seconds
    for _ in range(int(cmd[-1] / rate)):
        bot.set_vels(cmd[0], cmd[1])
        meas_ang_vel, meas_lin_vel = bot.get_vels()
        # print(f"Measured angular velocity: {meas_ang_vel}, linear velocity: {meas_lin_vel}")
        vel_data.append((meas_ang_vel, meas_lin_vel))
        sleep(rate)
    bot.set_vels(0.0, 0.0)  # for checkpoint
    sleep(3)

# TERMINATE
bot.set_vels(0.0, 0.0)
sleep(0.5)
bot.disable()

# SAVE DATA
with open("vel_data.csv", "w") as file:
    for i in range(len(vel_data)):
        file.write(f"{vel_data[i][0]},{vel_data[i][1]}\n")
