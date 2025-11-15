"""
Run this script with Local Python
"""

from pathlib import Path
import csv
import matplotlib.pyplot as plt
from math import pi, sin, cos

# SETUP, prepare data
data_filename = "example_data-lifted.csv"
data_type = "lifted" if "lifted" in data_filename else "ground"

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
ref_poses = [(0, 0, 0)]  # initialize list to store poses
meas_poses = [(0, 0, 0)]
dt = 0.05  # seconds, comply to data collection

for i in range(len(meas_vel_data) - 1):
    # Compute new pose using reference velocity
    ref_x, ref_y, ref_th = (
        ref_poses[-1][0],
        ref_poses[-1][1],
        ref_poses[-1][2],
    )  # extract latest coordinates
    ref_lv, ref_av = (
        ref_lin_vels[i],
        ref_ang_vels[i],
    )  # extract linear and angular velocity
    ref_nx, ref_ny, ref_nth = update_pose(
        ref_x, ref_y, ref_th, ref_lv, ref_av, dt
    )  # compute new pose
    ref_poses.append((ref_nx, ref_ny, ref_nth))  # store new pose
    ### START CODING HERE ###
    # Compute new pose using measured velocity
    meas_x, meas_y, meas_th = None, None, None
    meas_lv, meas_av = None, None
    ### END CODING HERE ###
    meas_nx, meas_ny, meas_nth = update_pose(
        meas_x, meas_y, meas_th, meas_lv, meas_av, dt
    )
    meas_poses.append((meas_nx, meas_ny, meas_nth))  # store new pose

# EVALUATION
pose_errors = []
for i in range(len(ref_poses)):
    pose_errors.append(
        (ref_poses[i][0] - meas_poses[i][0]) ** 2
        + (ref_poses[i][1] - meas_poses[i][1]) ** 2
        + (ref_poses[i][2] - meas_poses[i][2]) ** 2
    )
mse = sum(pose_errors) / len(pose_errors)
print(f"Mean squared error: {sum(pose_errors) / len(pose_errors)}")

# PLOT
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ref_x, ref_y, ref_th = map(list, zip(*ref_poses))
ref_u = [cos(rth) for rth in ref_th]
ref_v = [sin(rth) for rth in ref_th]
meas_x, meas_y, meas_th = map(list, zip(*meas_poses))
meas_u = [cos(mth) for mth in meas_th]
meas_v = [sin(mth) for mth in meas_th]

ax.quiver(
    ref_x,
    ref_y,
    ref_u,
    ref_v,
    color="#7C878E",  # Arrow color
    label="Orientation",
    angles="xy",  # Interpret (u, v) as (dx, dy)
    units="xy",
    scale=20,
    scale_units="width",
    width=0.003,
)
ax.quiver(
    meas_x,
    meas_y,
    meas_u,
    meas_v,
    color="#582c83",  # Arrow color
    label="Orientation",
    angles="xy",  # Interpret (u, v) as (dx, dy)
    units="xy",
    scale=20,
    scale_units="width",
    width=0.003,
)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
# ax.set_xlim(-0.1, 1.2)
# ax.set_ylim(-1.1, 0.8)
ax.grid()
ax.legend(["reference", "measured"])
ax.set_title(f"Trajectory Comparison - {data_type}", fontsize=16)
plt.savefig(f"{data_type}_traj.png")  # Export figure
plt.show()
