import random
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Student configuration
# ============================================================
STUDENT_NAME = "Obaidullah Shahid"
ROLL_NO = 78
SEED = ROLL_NO

# The assignment requires the unique problem to be generated
# from the roll number, so both Python and NumPy use seed 78.
random.seed(SEED)
np.random.seed(SEED)


# ============================================================
# 1. Generate unique problem instance from roll number
# ============================================================
GRID_SIZE = random.randint(20, 25)
OBSTACLE_RATIO = random.uniform(0.12, 0.18)

all_cells = [
    (row, col)
    for row in range(GRID_SIZE)
    for col in range(GRID_SIZE)
]

num_obstacles = int(GRID_SIZE * GRID_SIZE * OBSTACLE_RATIO)
obstacles = set(random.sample(all_cells, num_obstacles))

free_cells = [cell for cell in all_cells if cell not in obstacles]

# Start and goal are also generated from the same seed.
# The distance condition avoids a trivial very-short problem.
while True:
    start = random.choice(free_cells)
    goal = random.choice(free_cells)

    if (
        start != goal
        and math.dist(start, goal) >= GRID_SIZE * 0.65
    ):
        break


# ============================================================
# 2. Helper functions
# ============================================================
def bresenham_line(point_a, point_b):
    """
    Return the grid cells crossed by a straight line between
    point_a and point_b using Bresenham's line algorithm.
    """
    x0, y0 = point_a
    x1, y1 = point_b

    points = []

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    error = dx + dy

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        error2 = 2 * error

        if error2 >= dy:
            error += dy
            x0 += sx

        if error2 <= dx:
            error += dx
            y0 += sy

    return points


def decode_particle(position, number_of_waypoints):
    """
    Convert a PSO particle into a complete grid path.

    Each particle stores intermediate waypoint coordinates:
        [r1, c1, r2, c2, ..., rn, cn]

    Start and goal remain fixed.
    """
    waypoints_array = np.rint(
        position.reshape(number_of_waypoints, 2)
    ).astype(int)

    waypoints_array = np.clip(
        waypoints_array,
        0,
        GRID_SIZE - 1
    )

    route_points = [start]
    route_points.extend(tuple(p) for p in waypoints_array)
    route_points.append(goal)

    full_path = []

    for i in range(len(route_points) - 1):
        segment = bresenham_line(
            route_points[i],
            route_points[i + 1]
        )

        # Avoid repeating the joint point between segments.
        if full_path:
            segment = segment[1:]

        full_path.extend(segment)

    # Remove accidental consecutive duplicates.
    clean_path = []

    for point in full_path:
        if not clean_path or point != clean_path[-1]:
            clean_path.append(point)

    return clean_path, route_points


def calculate_path_length(path):
    """Calculate Euclidean length of a decoded grid path."""
    return sum(
        math.dist(path[i], path[i + 1])
        for i in range(len(path) - 1)
    )


def fitness(position, number_of_waypoints):
    """
    Lower fitness is better.

    Fitness =
        route length
        + a large penalty for obstacle collisions

    The collision penalty makes PSO strongly prefer
    obstacle-free paths.
    """
    path, _ = decode_particle(
        position,
        number_of_waypoints
    )

    collision_count = sum(
        cell in obstacles
        for cell in path
    )

    path_length = calculate_path_length(path)

    collision_penalty = 500 * collision_count

    return path_length + collision_penalty


# ============================================================
# 3. Particle Swarm Optimization
# ============================================================
NUMBER_OF_WAYPOINTS = 5
DIMENSIONS = NUMBER_OF_WAYPOINTS * 2

NUMBER_OF_PARTICLES = 80
MAX_ITERATIONS = 300

INERTIA_WEIGHT = 0.72
COGNITIVE_COEFFICIENT = 1.50
SOCIAL_COEFFICIENT = 1.50

MAX_VELOCITY = 3.0

rng = np.random.default_rng(SEED)

# Create a straight-line waypoint template between start and goal.
base_waypoints = []

for k in range(1, NUMBER_OF_WAYPOINTS + 1):
    fraction = k / (NUMBER_OF_WAYPOINTS + 1)

    row = start[0] + fraction * (goal[0] - start[0])
    col = start[1] + fraction * (goal[1] - start[1])

    base_waypoints.extend([row, col])

base_waypoints = np.array(base_waypoints, dtype=float)

# Initialize particles around the start-to-goal direction,
# but with enough random variation to explore alternate paths.
positions = (
    base_waypoints
    + rng.normal(
        0,
        GRID_SIZE * 0.25,
        size=(NUMBER_OF_PARTICLES, DIMENSIONS)
    )
)

positions = np.clip(
    positions,
    0,
    GRID_SIZE - 1
)

velocities = rng.uniform(
    -1,
    1,
    size=(NUMBER_OF_PARTICLES, DIMENSIONS)
)

personal_best_positions = positions.copy()

personal_best_scores = np.array([
    fitness(position, NUMBER_OF_WAYPOINTS)
    for position in positions
])

best_index = np.argmin(personal_best_scores)

global_best_position = (
    personal_best_positions[best_index].copy()
)

global_best_score = float(
    personal_best_scores[best_index]
)

best_score_history = [global_best_score]


for iteration in range(MAX_ITERATIONS):
    r1 = rng.random(
        (NUMBER_OF_PARTICLES, DIMENSIONS)
    )

    r2 = rng.random(
        (NUMBER_OF_PARTICLES, DIMENSIONS)
    )

    # Standard PSO velocity update:
    # v = w*v + c1*r1*(pbest-x) + c2*r2*(gbest-x)
    velocities = (
        INERTIA_WEIGHT * velocities
        + COGNITIVE_COEFFICIENT
        * r1
        * (personal_best_positions - positions)
        + SOCIAL_COEFFICIENT
        * r2
        * (global_best_position - positions)
    )

    velocities = np.clip(
        velocities,
        -MAX_VELOCITY,
        MAX_VELOCITY
    )

    # Standard PSO position update:
    # x = x + v
    positions = positions + velocities

    positions = np.clip(
        positions,
        0,
        GRID_SIZE - 1
    )

    current_scores = np.array([
        fitness(position, NUMBER_OF_WAYPOINTS)
        for position in positions
    ])

    improved = (
        current_scores
        < personal_best_scores
    )

    personal_best_positions[improved] = (
        positions[improved]
    )

    personal_best_scores[improved] = (
        current_scores[improved]
    )

    best_index = np.argmin(
        personal_best_scores
    )

    candidate_score = float(
        personal_best_scores[best_index]
    )

    if candidate_score < global_best_score:
        global_best_score = candidate_score

        global_best_position = (
            personal_best_positions[
                best_index
            ].copy()
        )

    best_score_history.append(
        global_best_score
    )


# ============================================================
# 4. Decode and report final path
# ============================================================
best_path, best_route_points = decode_particle(
    global_best_position,
    NUMBER_OF_WAYPOINTS
)

best_path_length = calculate_path_length(best_path)

collisions = [
    cell
    for cell in best_path
    if cell in obstacles
]


print("=" * 62)
print("SWARM INTELLIGENCE - PSO PATH PLANNING")
print("=" * 62)
print(f"Student Name : {STUDENT_NAME}")
print(f"Roll Number  : {ROLL_NO:03d}")
print(f"Random Seed  : {SEED}")
print(f"Grid Size    : {GRID_SIZE} x {GRID_SIZE}")
print(f"Obstacles    : {len(obstacles)}")
print(f"Start        : {start}")
print(f"Goal         : {goal}")
print(f"Waypoints    : {best_route_points[1:-1]}")
print(f"Best Cost    : {global_best_score:.4f}")
print(f"Path Length  : {best_path_length:.4f}")
print(f"Collisions   : {len(collisions)}")
print(f"Valid Path   : {'YES' if len(collisions) == 0 else 'NO'}")
print("\nBest path:")
print(best_path)


# ============================================================
# 5. Visualization
# ============================================================
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

grid = np.zeros(
    (GRID_SIZE, GRID_SIZE),
    dtype=int
)

for row, col in obstacles:
    grid[row, col] = 1


fig, ax = plt.subplots(figsize=(8, 8))

ax.imshow(
    grid,
    cmap="Greys",
    origin="upper",
    vmin=0,
    vmax=1
)

path_rows = [point[0] for point in best_path]
path_cols = [point[1] for point in best_path]

ax.plot(
    path_cols,
    path_rows,
    marker="o",
    markersize=3,
    linewidth=2,
    label="PSO Best Path"
)

ax.scatter(
    start[1],
    start[0],
    s=120,
    marker="o",
    label="Start",
    zorder=5
)

ax.scatter(
    goal[1],
    goal[0],
    s=150,
    marker="*",
    label="Goal",
    zorder=5
)

ax.set_title(
    f"PSO Swarm Path Planning - Roll {ROLL_NO:03d}\n"
    f"Cost={global_best_score:.2f}, "
    f"Length={best_path_length:.2f}, "
    f"Collisions={len(collisions)}"
)

ax.set_xlabel("Column")
ax.set_ylabel("Row")

ax.set_xticks(range(GRID_SIZE))
ax.set_yticks(range(GRID_SIZE))

ax.grid(
    True,
    linewidth=0.3,
    alpha=0.45
)

ax.legend(loc="upper right")

plt.tight_layout()

result_file = output_dir / "pso_best_path.png"
plt.savefig(
    result_file,
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)


# Convergence plot
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    range(len(best_score_history)),
    best_score_history
)

ax.set_title(
    "PSO Convergence - Global Best Cost"
)

ax.set_xlabel("Iteration")
ax.set_ylabel("Best Cost")
ax.grid(True, alpha=0.3)

plt.tight_layout()

convergence_file = (
    output_dir / "pso_convergence.png"
)

plt.savefig(
    convergence_file,
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)


# Save a small text output for the repository.
summary_file = output_dir / "run_summary.txt"

with summary_file.open("w", encoding="utf-8") as file:
    file.write(
        "SWARM INTELLIGENCE - PSO PATH PLANNING\n"
    )
    file.write("=" * 45 + "\n")
    file.write(
        f"Student Name: {STUDENT_NAME}\n"
    )
    file.write(
        f"Roll Number: {ROLL_NO:03d}\n"
    )
    file.write(
        f"Seed: {SEED}\n"
    )
    file.write(
        f"Grid Size: {GRID_SIZE} x {GRID_SIZE}\n"
    )
    file.write(
        f"Obstacle Count: {len(obstacles)}\n"
    )
    file.write(
        f"Start: {start}\n"
    )
    file.write(
        f"Goal: {goal}\n"
    )
    file.write(
        f"Best Cost: {global_best_score:.4f}\n"
    )
    file.write(
        f"Path Length: {best_path_length:.4f}\n"
    )
    file.write(
        f"Collisions: {len(collisions)}\n"
    )
    file.write(
        f"Valid Path: "
        f"{'YES' if len(collisions) == 0 else 'NO'}\n"
    )
    file.write(
        f"Path: {best_path}\n"
    )


print("\nSaved files:")
print(f"  {result_file}")
print(f"  {convergence_file}")
print(f"  {summary_file}")
