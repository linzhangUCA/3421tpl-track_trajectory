"""
Run this script with MicroPython (on Pico).
"""

from time import sleep

from diff_drive.diff_drive_controller import DiffDriveController

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
plans = (
    (None, None, None),  # segment 1: (ang_vel, lin_vel, dur) for example, (0.0, 0.2, 2)
    (None, None, None),  # segment 2
    (None, None, None),  # segment 3
    (None, None, None),  # segment 4
    (None, None, None),  # segment 5
    (None, None, None),  # segment 6
    (None, None, None),  # segment 7
    (None, None, None),  # segment 8
)
### Fill in planned angular, linear velocity commands and duration for each segment ABOVE ###
# Sample rate
rate = 0.05  # 20 Hz
# Create data storage
vel_data = []

# LOOP
# sleep(2)  # uncomment if autostart on duty
for p in plans:  # 50Hz controller, 20 seconds
    for _ in range(int(p[-1] / rate)):
        bot.set_vels(p[0], p[1])
        meas_ang_vel, meas_lin_vel = bot.get_vels()
        # print(f"Measured angular velocity: {meas_ang_vel}, linear velocity: {meas_lin_vel}")
        vel_data.append((meas_ang_vel, meas_lin_vel))
        sleep(rate)
    bot.set_vels(0.0, 0.0)
    sleep(3)  # for checkpoint

# TERMINATE
bot.set_vels(0.0, 0.0)
sleep(0.5)
bot.disable()

# SAVE DATA
with open("vel_data.csv", "w") as file:
    for i in range(len(vel_data)):
        file.write(f"{vel_data[i][0]},{vel_data[i][1]}\n")
