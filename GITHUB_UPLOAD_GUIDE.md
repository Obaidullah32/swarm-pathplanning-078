# Upload This Project to GitHub from VS Code

## Method: VS Code Terminal + Git

### 1. Open the project folder

In VS Code:

```text
File → Open Folder
```

Select:

```text
swarm-pathplanning-078
```

### 2. Open the VS Code terminal

Use:

```text
Terminal → New Terminal
```

### 3. Initialize Git

Run:

```bash
git init
```

### 4. Make the required meaningful commits

The assignment requires at least 5 meaningful commits.

If you received all files together, you can stage them in logical groups.

#### Commit 1 — Setup and problem generation

```bash
git add requirements.txt .gitignore
git add main.py
git commit -m "Initial setup and seeded grid generation"
```

For a teacher-visible history that genuinely reflects development, the safest approach is to make future edits incrementally rather than fabricating older work. Before submitting, you can still make additional real improvements/edits and commit each separately.

Suggested genuine follow-up commits:

```bash
git add main.py
git commit -m "Implement PSO velocity position and fitness logic"

git add main.py
git commit -m "Add obstacle collision checking"

git add outputs
git commit -m "Add path and convergence visualizations"

git add README.md DIAGRAM_GUIDE.md
git commit -m "Add project documentation and flow diagram guide"
```

After adding your actual hand-drawn photo:

```bash
git add images/hand_drawn_flow_diagram.jpg README.md
git commit -m "Add hand drawn PSO flow diagram"
```

> Important: Git only creates a new commit when there is an actual file change.
> Do not try to create fake commits with unchanged files.

### 5. Create the GitHub repository

On GitHub:

1. Click **New repository**
2. Repository name:

```text
swarm-pathplanning-078
```

3. Set it to **Public**
4. Do not add another README if your local folder already has one.
5. Click **Create repository**

### 6. Connect VS Code project to GitHub

GitHub will show a repository URL similar to:

```text
https://github.com/YOUR-USERNAME/swarm-pathplanning-078.git
```

Copy it and run:

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/swarm-pathplanning-078.git
git push -u origin main
```

### 7. Push later changes

Whenever you modify files:

```bash
git add .
git commit -m "Describe the change"
git push
```

## Before Final Submission

Make sure the GitHub repository contains:

```text
main.py
README.md
requirements.txt
DIAGRAM_GUIDE.md
outputs/pso_best_path.png
outputs/pso_convergence.png
outputs/run_summary.txt
images/hand_drawn_flow_diagram.jpg
```

Also verify:

- Repository is Public.
- README shows name, roll number and seed.
- README includes the hand-drawn diagram image.
- Git history has at least 5 meaningful commits.
- Program runs using `python main.py`.
- GitHub repository link opens without login restrictions.

## Email Submission

Send your public GitHub repository link to:

```text
ahsanjaved5000@gmail.com
```

Subject:

```text
SI ASG1 – UMAIR ZAHID – 078
```
