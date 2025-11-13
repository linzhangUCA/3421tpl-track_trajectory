"""
Run this script with local Python
"""

from pathlib import Path
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
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
for i in range(len(meas_vels) - 1):
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
    # Store reference pose
    ref_x.append(ref_x[-1] + ref_dx)
    ref_y.append(ref_y[-1] + ref_dy)
    ref_th.append(ref_th[-1] + ref_dth)
    # Store measured pose
    meas_x.append(meas_x[-1] + meas_dx)
    meas_y.append(meas_y[-1] + meas_dy)
    meas_th.append(meas_th[-1] + meas_dth)

# Plot data
# fig, ax = plt.subplots(1, 2, figsize=(16, 8))
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ref_u, ref_v = [], []
meas_u, meas_v = [], []
for i in range(len(meas_vels)):
    ref_u.append(cos(ref_th[i]))
    ref_v.append(sin(ref_th[i]))
    meas_u.append(cos(meas_th[i]))
    meas_v.append(sin(meas_th[i]))
ax.quiver(
    ref_x,
    ref_y,
    ref_u,
    ref_v,
    color="#7C878E",  # Arrow color
    label="Orientation",
    angles="xy",  # Interpret (u, v) as (dx, dy)
    scale_units="width",
    width=0.002,
)  # Arrow width
ax.quiver(
    meas_x,
    meas_y,
    meas_u,
    meas_v,
    color="#582c83",  # Arrow color
    label="Orientation",
    angles="xy",  # Interpret (u, v) as (dx, dy)
    scale_units="width",
    width=0.002,
)  # Arrow width
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-1.1, 0.8)
ax.grid()
ax.legend(["reference", "measured"])
# Title
### CHOOSE APPROPRIATE TITLE ###
ax.set_title("Trajectory Comparison - Noload", fontsize=16)
plt.savefig("noload_traj.png")
# fig.suptitle("Trajectory Comparison - Ground", fontsize=16)
# plt.savefig("ground_traj.png")
plt.show()
