# Hand-Drawn Flow Diagram Guide

Draw the following flow on paper using boxes and arrows.

You can copy this layout exactly:

```text
        ┌───────────────────────┐
        │         START         │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Set roll number = 078 │
        │ Set random seed = 78  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Generate grid size,        │
        │ obstacles, start and goal  │
        │ using seed 78              │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Initialize PSO particles   │
        │ positions and velocities   │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Decode particle waypoints  │
        │ into a complete grid path  │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Check path for obstacle    │
        │ collisions                 │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Calculate fitness:         │
        │ path length + collision    │
        │ penalty                    │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Update personal best       │
        │ (pbest) and global best    │
        │ (gbest)                    │
        └───────────┬────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │ Update PSO velocity        │
        │ and particle position      │
        └───────────┬────────────────┘
                    │
                    ▼
              ┌───────────────┐
              │ Stop condition│
              │ reached?      │
              └──────┬───┬────┘
                  No │   │ Yes
                     │   │
                     │   ▼
                     │  ┌───────────────────────┐
                     │  │ Output best path,     │
                     │  │ cost and visualization│
                     │  └───────────┬───────────┘
                     │              │
                     └──────────────┘
                                    ▼
                         ┌──────────────────┐
                         │       END        │
                         └──────────────────┘
```

## Important correction for this assignment

Because this solution uses **PSO**, write:

```text
Update velocity and position
```

Do **not** write:

```text
Update pheromones
```

Pheromone updating belongs to Ant Colony Optimization (ACO), not PSO.

## Easy handwritten version

If you want fewer boxes, draw:

```text
START
  ↓
Set Seed = 78
  ↓
Generate Grid + Obstacles + Start + Goal
  ↓
Initialize PSO Swarm
  ↓
Generate Candidate Paths
  ↓
Check Obstacles
  ↓
Calculate Fitness
  ↓
Update pbest and gbest
  ↓
Update Velocity and Position
  ↓
Stopping Condition Reached?
  ├── No → Repeat Candidate Path Evaluation
  └── Yes
        ↓
Output Best Path + Cost + Plot
        ↓
       END
```

Take a clear photograph of your handwritten diagram and put it in:

```text
images/hand_drawn_flow_diagram.jpg
```
