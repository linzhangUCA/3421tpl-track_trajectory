# Track Robot's Trajectory

## 1. Overview
It is important for any mobile robot to move along the pre-planned trajectory while localizie itself.
In this assignment, you will practice controling the robot's motion by feeding velocity commands to it. 

### Preparation
1. Set up the differential drive mobile base.
   1. (Recommended) Install the mobile robot [software stack](https://github.com/linzhangUCA/upython_mobile_robot/tree/main/src/upyton_mobile_robot) .
   2. Update properties according to your robot's physical setup.
   3. Tune PID parameters so the robot will quickly and smoothly respond to the velocity commands.
2. (Optional, [VSCode](https://code.visualstudio.com/) recommended) Configure Python environment for the trajectory plotting code:
    1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) on your computer.
    2. Open a terminal/shell in the local assignment repository, then `uv sync` to install dependency Python packages ([Matplotlib](https://matplotlib.org/stable/) and possibly [PyQt6](https://pypi.org/project/PyQt6/)).
    3. To execute a Python scripts: `uv run <script_name>.py`, e.g. `uv run plot_traj.py`.

## 2. Requirements
The robot needs to be automatically tracking the pre-defined trajectory (indicated by the dashed lines) as shown in the figure below.
The trajectory is broken down into 8 (color-coded) segments.
In each segment, control the robot's movement by feeding linear and angular velocity command to it for a certain duration.

![track_traj](./images/track_traj.png)

### 2.1. Plan Trajectory Tracking
Describe how to design the velocity command and the duration for every segment of the track in the [README](README.md). 
- Identify equations and plug in numbers to plan linear velocity for the robot.
- Identify equations and plug in numbers to plan angular velocity for the robot.
- Identify equations and plug in numbers to plan duration of the segment.

> [!IMPORTANT]
> Please format mathmatical expressions following the [guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). 

### 2.2. Implement Trajectory Tracking
- Fill in your planned velocity commands and durations in the [track_traj.py](track_traj.py) script.
- Run [track_traj.py](track_traj.py) script (on Pico using **MicroPython**) to track the trajectory and record the robot's motion data.
- Upload the data file (saved in Pico as "vel_data.csv") to the [data/](./data/) directory of the assignment repository (locally and on Github).
- Fill in correct code in [plot_traj.py](plot_traj.py) to estimate robot's pose at every step.
- Run [plot_traj.py](plot_traj.py) (on a computer using **Local Python**) to measure the actual trajectory.
- Upload the trajectory figure to the [images/](./images/) directory of the assignment repository and display it out in the [README](README.md).

> [!IMPORTANT]
> - Modify code out of the designated sections is not recommended.
> - Be ware of the storage space of your Pico board. 4 Mb maximum.

### 2.3. Demonstrate the Trajectory Tracking Robot
Demonstrate your robot to Dr. Zhang at the designated course.
The ending positions of each segment of the trajectory are the checkpoints.
There are 7 checkpoints because no translations during the 7th (purple) segment.
Distance from where the robot actually ends the segment to the checkpoint will be measured as $d$ in meters.
Penalties, $p$, will be taken based on $d$.

```math
p=
\begin{cases}
   0 &\text{, if } d \leq 0.05 \\
   50 d &\text{, else}
\end{cases}
```

> [!CAUTION]
> - You will need to demonstrate your robot to redeem credits for the plan and the implementation part.

### 2.4. (20%) Evaluate Performance
Evaluate and compare the measured trajectory to the reference trajectory using the Mean Squared Error (MSE) metric.
Write code in [compute_mse.py](compute_mse.py) to compute the metric based on your data.
Upload your code to the assignment repository and report your result in the [README](README.md).

```math
MSE = \frac{1}{M} \sum_{t=0}^T (\mathbf{p}_t - \hat{\mathbf{p}}_t)^2
```
   - $M$ is the total number of steps.
   - $\mathbf{p}_t = [X_t, Y_t, \theta_t]$ is the robot's reference pose vector at instant $t$, where $t \in \{0, 1, 2, \dots, T\}$.
   - $\hat{\mathbf{p}}_t$ is the robot's measured pose vector at instant $t$.
> [!TIP]
> - Write code to calculate the MSE.


### 2.5. Acknowledge AI's Contributions
If AI helped with this assignment, please list out all the contributions from it.

## 3. Study Resources

### 3.1. Reference Frame Setup

#### 3.1.1. Temporal Frame

- The robot will start moving at the moment of $t_0$, and end the motion at the instant of $t_T$.
- The robot's state will be examined every $\Delta t$ seconds, hence the $i$-th instant $t_i = t_{i-1} + \Delta t$ (where $`i \in \{ 1, 2, \dots, T \}`$).

#### 3.1.2. Spatial Frame

- Body frame: $`\{x, y\}`$ is attached to the robot and will translate and rotate along the robot's movement.

The body frame's origin is sitting at the geometric center of the robot's base plate. The $x$ axis is always pointing to the head of the robot, and the $y$ axis is perpendicular to the $x$ axis and pointing to the left wheel.

- Global frame: $`\{X, Y\}`$ is fixed on the driving plane and will not move along the robot.

The Global frame will be generated according to the initial pose of the robot. The $`\{X, Y\}`$ frame will overlap with the initial $`\{x, y\}`$ frame.

### 3.2. Robot's State of Motion (Pose and Velocity)

- The robot's motion will be restricted in the two dimensional $`\{X, Y\}`$ plane.
- The robot's pose at the $i$-th instant can be represented as $(X_i, Y_i, \theta_i)$ referring to the global frame.
$\theta_i$ is the angle from $X$ to $x$, with counterclockwise to be the positive direction.
- The robot's velocity at the $i$-th instant can be represented as $(v_i, \omega_i)$.
$v_i$ is the robot's linear velocity which is always on the $x$ axis.
$\omega_i$ is the robot's angular velocity which is an rotational quantity along the axis perpendicular to the $`\{x, y\}`$ plane.
$\omega_i$ is positive if the direction is counterclockwise.
- The trajectory of the robot can be represented as a sequence of the robot's states and can be illustrated as shown in the following figure.

```math
\{(X_0, Y_0, \theta_0, v_0, \omega_0), (X_1, Y_1, \theta_1, v_1, \omega_1), \dots, (X_T, Y_T, \theta_T, v_T, \omega_T)\}
```

![odometry](images/odometry.png)

At instant $t_i$, the change of the robot's pose can be calculated _approximately_ as:

```math
\Delta X_i \approx v_i \cos \theta_i \Delta t
```

```math
\Delta Y_i \approx v_i \sin \theta_i \Delta t
```

```math
\Delta \theta_i \approx \omega_i \Delta t

```

Therefore, the robot's new pose at $t_{i+1}$ can be calculated as:

```math
X_{i+1} = X_i + \Delta X_i
```

```math
Y_{i+1} = Y_i + \Delta Y_i
```

```math
\theta_{i+1} = \theta_i + \Delta \theta_i
```

