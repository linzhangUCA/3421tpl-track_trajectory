"""
Run this script with local Python
"""

from pathlib import Path
import csv
import matplotlib.pyplot as plt
from math import pi, sin, cos

# SETUP, prepare data
data_filename = "vel_data.csv"  # change to "example_data.csv" to test your coding
data_file = Path(__file__).parent / "data" / data_filename
with open(data_file, newline="") as f:
    data = csv.reader(f)
    meas_vel_data = tuple(data)
print(f"There are {len(meas_vel_data)} velocity samples recorded")
meas_lin_vels, meas_ang_vels = [], []  # initialize lists to save measured velocities
for mv in meas_vel_data:
    meas_lin_vels.append((float(mv[0])))
    meas_ang_vels.append((float(mv[1])))
# Construct reference velocity list
ref_vel_candidates = (
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
num_per_cand = len(meas_vel_data) // len(ref_vel_candidates)  # numbers per candidate
ref_lin_vels, ref_ang_vels = [], []
for i in range(len(meas_vel_data)):
    ref_lin_vels.append(ref_vel_candidates[i // num_per_cand][0])
    ref_ang_vels.append(ref_vel_candidates[i // num_per_cand][1])
print(f"10 samples of reference linear velocity: {ref_lin_vels[50:60]}")
print(f"10 samples of measured linear velocity: {meas_lin_vels[50:60]}")
print(f"10 samples of reference angular velocity: {ref_ang_vels[50:60]}")
print(f"10 samples of measured angular velocity: {meas_ang_vels[50:60]}")


def update_pose(x, y, theta, lin_vel, ang_vel, dt):
    """Compute robot's new pose given its old pose and velocity
    Args:
        x: robot's old X coordinate (under the global frame)
        y: robot's old Y coordinate (under the global frame)
        theta: robot's old orientation (angle between global frame's X-axis and body frame's x-axis)
    Returns:
        next_x: robot's new X coordinate (under the global frame)
        next_y: robot's new Y coordinate (under the global frame)
        next_theta: robot's new orientation (angle between global frame's X-axis and body frame's x-axis)
    """
    delta_x = lin_vel * cos(theta) * dt
    delta_y = lin_vel * sin(theta) * dt
    delta_theta = ang_vel * dt
    next_x = x + delta_x
    next_y = y + delta_y
    next_theta = theta + delta_theta

    return next_x, next_y, next_theta


# LOOP, calculate trajectory
# ref_x, ref_y, ref_th = [0], [0], [0]
# meas_x, meas_y, meas_th = [0], [0], [0]
ref_pose = [(0, 0, 0)]
meas_pose = [(0, 0, 0)]
dt = 0.05  # seconds

for i in range(len(meas_vel_data) - 1):
    # Compute trajectory using reference velocities
    # x, y, th = ref_x[-1], ref_y[-1], ref_th[-1]
    # lv, av = ref_vels[i][0], ref_vels[i][1]
    # nx, ny, nth = update_pose(x, y, th, lv, av, dt)
    ref_x, ref_y, ref_th = ref_pose[-1][0], ref_pose[-1][1], ref_pose[-1][2]
    ref_lv, ref_av = ref_lin_vels[i], ref_ang_vels[i]
    ref_nx, ref_ny, ref_nth = update_pose(ref_x, ref_y, ref_th, ref_lv, ref_av, dt)
    ref_pose.append((ref_nx, ref_ny, ref_nth))
    # Compute trajectory using measured vel
    # meas_dx = meas_vels[i][0] * cos(meas_th[-1]) * dt
    # meas_dy = meas_vels[i][0] * sin(meas_th[-1]) * dt
    # meas_dth = meas_vels[i][1] * dt
    meas_x, meas_y, meas_th = meas_pose[-1][0], meas_pose[-1][1], meas_pose[-1][2]
    meas_lv, meas_av = meas_lin_vels[i], meas_ang_vels[i]
    meas_nx, meas_ny, meas_nth = update_pose(
        meas_x, meas_y, meas_th, meas_lv, meas_av, dt
    )
    meas_pose.append((meas_nx, meas_ny, meas_nth))
    # Store reference pose
    # ref_x.append(ref_x[-1] + ref_dx)
    # ref_y.append(ref_y[-1] + ref_dy)
    # ref_th.append(ref_th[-1] + ref_dth)
    # ref_x.append(nx)
    # ref_y.append(ny)
    # ref_th.append(nth)
    # Store measured pose
    # meas_x.append(meas_x[-1] + meas_dx)
    # meas_y.append(meas_y[-1] + meas_dy)
    # meas_th.append(meas_th[-1] + meas_dth)

# Plot data
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ref_x, ref_y, ref_th = map(list, zip(*ref_pose))
ref_u = [cos(rth) for rth in ref_th]
ref_v = [sin(rth) for rth in ref_th]
meas_x, meas_y, meas_th = map(list, zip(*meas_pose))
meas_u = [cos(mth) for mth in meas_th]
meas_v = [sin(mth) for mth in meas_th]

# ref_u, ref_v = [], []
# meas_u, meas_v = [], []
# for i in range(len(meas_vels)):
#     ref_u.append(cos(ref_th[i]))
#     ref_v.append(sin(ref_th[i]))
#     meas_u.append(cos(meas_th[i]))
#     meas_v.append(sin(meas_th[i]))
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
# plt.savefig("noload_traj.png")
# fig.suptitle("Trajectory Comparison - Ground", fontsize=16)
# plt.savefig("ground_traj.png")
plt.show()
