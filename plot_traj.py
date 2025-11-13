"""
Run this script with local Python
"""

from pathlib import Path
import csv
import matplotlib.pyplot as plt
from math import pi, sin, cos

# Extract measured velocities
### START CODING HERE ### ~ 1 line
data_file = Path(__file__).parent / "data" / "vel_data.csv"
### END CODING HERE ###
with open(data_file, newline="") as f:
    reader = csv.reader(f)
    vel_data = tuple(reader)
meas_vels = []
for vd in vel_data:
    meas_vels.append((float(vd[0]), float(vd[1])))
# Construct reference velocities
targ_vels = (
    (0.4, 0.0),
    (0.3, pi / 3),
    (0.25, pi / 2),
    (0.0, 2 * pi / 3),
    (-0.25, pi / 2),
    (-0.3, pi / 3),
    (-0.4, 0.0),
    (-0.3, -pi / 3),
    (-0.25, -pi / 2),
    (0.0, -2 * pi / 3),
)
ref_vels = []
for i in range(len(meas_vels)):
    ref_vels.append(targ_vels[i // 40])
# print(len(ref_vels))

# Calculate trajectory
ref_x, ref_y, ref_th = [0], [0], [0]
meas_x, meas_y, meas_th = [0], [0], [0]
dt = 0.05  # seconds
for i in range(len(meas_vels)):
    ### START CODING HERE ### ~ 6 lines
    # Compute trajectory using reference velocities
    ref_dx = ref_vels[i][0] * cos(ref_th[-1]) * dt
    ref_dy = ref_vels[i][0] * sin(ref_th[-1]) * dt
    ref_dth = ref_vels[i][1] * dt
    # Compute trajectory using measured vel
    meas_dx = meas_vels[i][0] * cos(meas_th[-1]) * dt
    meas_dy = meas_vels[i][0] * sin(meas_th[-1]) * dt
    meas_dth = meas_vels[i][1] * dt
    ### END CODING HERE ###
    # Store ref state
    ref_x.append(ref_x[-1] + ref_dx)
    ref_y.append(ref_y[-1] + ref_dy)
    ref_th.append(ref_th[-1] + ref_dth)
    # Store measured state
    meas_x.append(meas_x[-1] + meas_dx)
    meas_y.append(meas_y[-1] + meas_dy)
    meas_th.append(meas_th[-1] + meas_dth)

# Plot data
# fig, ax = plt.subplots(1, 2, figsize=(16, 8))
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
# Plot position trajectory
ax.scatter(ref_x, ref_y)
ax.scatter(meas_x, meas_y, marker="+")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
# 0].set_xlim([-0.25, 3.25])
# 0].set_ylim([-0.25, 3.25])
ax.grid()
ax.legend(["reference", "measured"])
# # Plot orientation traj
# ts = list(range(len(x)))  # create timestamps for x axis
# for i in range(len(x)):
#     ts[i] = 0.05 * i
# ax[1].plot(ts, th, ".", markersize="10")
# ax[1].plot(ts, th_hat, "+", markersize="5")
# ax[1].set_xlabel("Time (s)")
# ax[1].set_ylabel("θ (radians)")
# # ax[1].set_xlim([-0.25, 20.25])
# # ax[1].set_ylim([-pi * 2.5, pi])
# ax[1].grid()
# ax[1].legend(["target", "actual"])
# # Title
# ### CHOOSE APPROPRIATE TITLE ###
# fig.suptitle("Trajectory Compare - Noload", fontsize=16)
# plt.savefig("noload_traj.png")
# # fig.suptitle("Trajectory Compare - Ground", fontsize=16)
# # plt.savefig("ground_traj.png")
plt.show()
