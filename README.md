# Track Robot's Trajectory

We will set up a odometry system for our robot and track the travel history of it.

## Instructions

### 1. Software Setup

1. Upload the MicroPython's differential drive control suite to your Pico.
2. (Optional) Tweak `wheel_sep` in "diff_drive_controller.py".
3. (Optional) Tune PID parameters for better controlling the wheels.

> [!NOTE]
>
> - For Pico sitting on the PCB, find scripts in [r1b_control](https://github.com/linzhangUCA/r1b_control)
> - For Pico sitting on the breadboard, find scripts in [3421example-motor_control](https://github.com/linzhangUCA/3421example-motor_control)

### 2. Collect Data

You need to collect data under two conditions: 1) with wheels lifted; 2) with robot set on the ground.

1. Either lift the robot up or set it down on the ground.
Then run [collect_vel_data.py](collect_vel_data.py) on Pico using **MicroPython(Raspberry Pi Pico)**
2. Download the data saved on Pico ("vel_data.csv") to this repository on your computer/laptop.
Then delete the data file from the Pico.
3. Rename the downloaded data file as "vel-data-**lifted**.csv" or "vel-data-**ground**.csv" depending on the data collection condition.
Then, save the renamed data file under the [data/](data/) directory in this repository (on your computer/laptop).

### 3. Plot Trajectory

1. Select desired data file by modifying `data_filename` on line 11 in [plot_traj.py](plot_traj.py).
2. Finish coding in [plot_traj.py](plot_traj.py).
3. Run [plot_traj.py](plot_traj.py) using **Local Python** (on your computer/laptop).

## Requirements

### 1. (70%) Plot Trajectories

- Complete `update_pose()` function from line 59 to 66 in [plot_traj.py](plot_traj.py).
Compute the robot's pose of the next instant given the robot's pose and velocity of the current instant.
- Complete steps in line 98 and 99 of [plot_traj.py](plot_traj.py).
Extract correct values to calculate the robot's trajectory using measured velocity data.
- Plot [lifted_traj.png](lifted_traj.png) and [ground_traj.png](ground_traj.png) using the correct data files.

> [!TIP]
> The trajectory image will be automatically rendered after running [plot_traj.py](plot_traj.py).

#### Lifted Trajectory

![lifted_traj](lifted_traj.png)

#### Ground Trajectory

![ground_traj](ground_traj.png)

### 2. (30%) Evaluation and Observation

Evaluate measured trajectory by comparing it to the reference trajectory using the Mean Squared Error (MSE) metric.

> [!TIP]
> Line 106 to 115 in [plot_traj.py](plot_traj.py).

$$MSE = \frac{1}{M} \sum_{t=0}^T (\mathbf{p}_t - \hat{\mathbf{p}}_t)^2$$

- $M$ is the total number of data samples (400).
- $\mathbf{p}_t$ is the robot's reference pose vector at instant $t$, where $t \in {0, 1, 2, \dots, T}$.
- $\hat{\mathbf{p}}_t$ is the robot's measured pose vector at instant $t$.

Please log your MSE below :point_down:
> MSE = ?

2. Observe the measured and reference trajectories, summarize the difference below. :point_down:

> Your observation is: ...

3. The robot's odometry system is solely based on the encoders now.
Are they sufficient to track the robot's pose? Why or why not?
Please write your answers down below. :point_down:

> Your answers and analyses are: ...

## Study Resources

### 1. Reference Frame Setup

#### 1.1. Temporal Frame

- The robot will start moving at the moment of $t_0$, and end the motion at the instant of $t_T$.
- The robot's state will be examined every $\Delta t$ seconds, hence the $i$-th instant $t_i = t_{i-1} + \Delta t$ (where $`i \in \{ 1, 2, \dots, T \}`$).

#### 1.2. Spatial Frame

- Body frame: $`\{x, y\}`$ is attached to the robot and will translate and rotate along the robot's movement.

The body frame's origin is sitting at the geometric center of the robot's base plate. The $x$ axis is always pointing to the head of the robot, and the $y$ axis is perpendicular to the $x$ axis and pointing to the left wheel.

- Global frame: $`\{X, Y\}`$ is fixed on the driving plane and will not move along the robot.

The Global frame will be generated according to the initial pose of the robot. The $`\{X, Y\}`$ frame will overlap with the initial $`\{x, y\}`$ frame.

### 2. Robot's State of Motion (Pose and Velocity)

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

![odom_frame](images/odom_frame.png)

At instant $t_i$, the change of the robot's pose can be calculated _approximately_ as:

```math
\Delta X_i = v_i \cos \theta_i \Delta t
```

```math
\Delta Y_i = v_i \sin \theta_i \Delta t
```

```math
\Delta \theta_i = \omega_i \Delta t

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

## AI Policies

Please acknowledge AI's contributions according to the policies in the syllabus.
