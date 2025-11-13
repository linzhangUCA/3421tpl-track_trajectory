import matplotlib.pyplot as plt
import numpy as np

# --- 1. Generate Sample Data ---
# (Replace this with your actual robot data)
# Let's create a simple circular path
t = np.linspace(0, 2 * np.pi, 100)  # 100 timesteps
radius = 5
x = radius * np.cos(t)
y = radius * np.sin(t)
# Theta is the orientation (tangent to the circle)
# The angle of the position vector is t. The tangent is t + pi/2.
theta = t + np.pi / 2

# --- 2. Set up the Plot ---
fig, ax = plt.subplots(figsize=(8, 8))

# --- 3. Plot the Position Trajectory (x, y) ---
ax.plot(x, y, "b-", label="Trajectory")  # 'b-' = blue solid line

# --- 4. Plot the Orientation (theta) as Arrows ---

# We don't want to plot an arrow for every single point.
# It will be too cluttered. Let's plot one every 'N' steps.
N = 10  # Plot orientation every 10 steps

# Get the components of the orientation vector
# We use trigonometry: u = cos(theta), v = sin(theta)
# These are the (x, y) components of a unit vector pointing at angle theta
u = np.cos(theta[::N])
v = np.sin(theta[::N])

# Plot the arrows using quiver
ax.quiver(
    x[::N],
    y[::N],
    u,
    v,
    color="r",  # Arrow color
    label="Orientation",
    scale=15,  # Controls arrow length (larger number = smaller arrows)
    scale_units="xy",  # Units for scaling
    angles="xy",  # Interpret (u, v) as (dx, dy)
    width=0.005,
)  # Arrow width

# --- 5. Format the Plot ---
ax.set_title("Robot Trajectory and Orientation")
ax.set_xlabel("X Position (meters)")
ax.set_ylabel("Y Position (meters)")

# IMPORTANT: Set equal aspect ratio
# This ensures that a circle looks like a circle, not an ellipse,
# and that 90-degree angles look like 90 degrees.
ax.set_aspect("equal", adjustable="box")

ax.legend()
ax.grid(True)

# --- 6. Show the Plot ---
plt.show()
