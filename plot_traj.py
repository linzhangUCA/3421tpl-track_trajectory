"""
Run this script with Local Python
"""

import csv
from math import cos, pi, sin
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# SETUP, prepare data
data_dir = Path(__file__).parent / "data"
data_path = data_dir / "vel_data.csv"

with open(data_path, newline="") as f:
    data = csv.reader(f)
    meas_vel_data = tuple(data)
print(f"There are {len(meas_vel_data)} velocity samples recorded")
meas_ang_vels, meas_lin_vels = [], []  # initialize lists to save measured velocities
for mv in meas_vel_data:
    meas_ang_vels.append((float(mv[0])))
    meas_lin_vels.append((float(mv[1])))
# TODO: reconstruct reference velocity list
# cmd_vels = (
#     (0.0, 0.0, 2),
#     (pi / 2, 0.2, 3),
#     ...
# )


def estimate_pose(x, y, theta, ang_vel, lin_vel, dt=0.05):
    """Compute robot's new pose given its old pose and velocity
    Args:
        x: robot's old X coordinate (under the global frame)
        y: robot's old Y coordinate (under the global frame)
        theta: robot's old orientation (angle between global frame's X-axis and body frame's x-axis)
        ang_vel: robot's angular velocity (in the body frame)
        lin_vel: robot's linear velocity (in the body frame)
        dt: time interval (in seconds)
    Returns:
        next_x: robot's new X coordinate (under the global frame)
        next_y: robot's new Y coordinate (under the global frame)
        next_theta: robot's new orientation (angle between global frame's X-axis and body frame's x-axis)
    """
    ### START CODING HERE ###
    # Compute pose change
    delta_x = None
    delta_y = None
    delta_theta = None
    # Compute new pose
    next_x = None
    next_y = None
    next_theta = None
    ### END CODING HERE ###
    if next_theta > pi:  # restrict theta in [-pi, pi]
        next_theta = next_theta - 2 * pi
    elif next_theta < -pi:
        next_theta = next_theta + 2 * pi

    return next_x, next_y, next_theta


# LOOP, calculate trajectory
est_poses = [(0, 0, 0)]
dt = 0.05  # seconds, comply to data collection

for i in range(len(meas_vel_data) - 1):
    ### START CODING HERE ###
    old_x, old_y, old_th = (
        None,
        None,
        None,
    )  # extract old coordinates from est_poses
    meas_ang_vel, meas_lin_vel = (
        None,
        None,
    )  # extract measured angular and linear velocity
    ### END CODING HERE ###
    new_x, new_y, new_th = estimate_pose(
        old_x, old_y, old_th, meas_ang_vel, meas_lin_vel, dt
    )
    est_poses.append((new_x, new_y, new_th))  # store new pose


# Pre-defined traj
def arc_points(center, radius, start_deg, end_deg, num=50):
    theta = np.deg2rad(np.linspace(start_deg, end_deg, num))
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.column_stack([x, y])


segments = [
    np.array([[0.0, 0.0], [0.4, 0.0]]),
    arc_points(center=(0.4, -0.2), radius=0.2, start_deg=90, end_deg=0),
    np.array([[0.6, -0.2], [0.6, -0.44]]),
    arc_points(center=(0.4, -0.44), radius=0.2, start_deg=0, end_deg=-90),
    arc_points(center=(0.4, -0.54), radius=0.1, start_deg=-90, end_deg=-180),
    np.array([[0.3, -0.54], [0.3, -0.2]]),
    np.array([[0.3, -0.2], [0.0, -0.5]]),
]
predef_path = np.vstack(segments)


# Estimated traj
est_x, est_y, est_th = map(list, zip(*est_poses))
est_u = [cos(mth) for mth in est_th]
est_v = [sin(mth) for mth in est_th]


# Plot
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.plot(predef_path[:, 0], predef_path[:, 1], color="royalblue", linewidth=1)
ax.quiver(
    est_x,
    est_y,
    est_u,
    est_v,
    color="#582c83",  # Arrow color
    label="Orientation",
    angles="xy",  # Interpret (u, v) as (dx, dy)
    units="xy",
    scale=20,
    scale_units="width",
    width=0.002,
)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_aspect("equal", adjustable="box")  # 1:1 scale
ax.set_xlim(-0.1, 0.7)
ax.set_ylim(-0.75, 0.1)
ax.grid(True, linestyle="--", alpha=0.5)

ax.legend(["reference", "measured"])
ax.set_title("Measured Trajectory", fontsize=16)
# plt.savefig(f"traj_plot.png")  # uncomment to save figure
plt.show()
