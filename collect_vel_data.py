"""
Run this script with Micropython (on Pico).
"""

from diff_drive_controller import DiffDriveController
from time import sleep
from math import pi


# SETUP
# Instantiate wheel
bot = DiffDriveController(
    left_wheel_ids=((15, 13, 14), (11, 10)),
    right_wheel_ids=((16, 18, 17), (19, 20)),
)
# Create velocity candidates
ref_vels = (
    (0.4, 0.0),
    (0.4, pi / 3),
    (0.3, 0.0),
    (0.25, -pi / 2),
    (0.0, -2 * pi / 3),
    (-0.25, -pi / 2),
    (-0.3, 0.0),
    (-0.4, pi / 3),
    (-0.4, 0.0),
    (0.0, 2 * pi / 3),
)
# Create data storage
vel_data = []

# LOOP
# sleep(2)  # get your robot ready!
bot.enable()
for i in range(400):  # 20Hz controller, 20 seconds
    meas_lin_vel, meas_ang_vel = bot.get_vels()
    print(meas_lin_vel, meas_ang_vel)
    vel_data.append((meas_lin_vel, meas_ang_vel))
    bot.set_vels(*ref_vels[i // 40])
    sleep(0.05)

bot.set_vels(0.0, 0.0)
sleep(0.5)
bot.disable()
### UNCOMMENT FOLLOWING 3 LINES WHEN SATISFIED WITH PID GAINS ###
with open("vel_data.csv", "w") as file:
    for i in range(len(vel_data)):
        file.write(f"{vel_data[i][0]},{vel_data[i][1]}\n")
