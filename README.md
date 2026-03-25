# 🏆 FIT5047 Pacman AI — Competition Winner (1st / 150+)

**Best In Class Award for Outstanding Performance** · Monash University FIT5047 (Foundations of Artificial Intelligence)

A full AI agent implementation for the classic Pacman game, covering classical search algorithms and an adversarial game-playing agent that won the end-of-semester class competition.

---

## Project Structure

```
├── agents/
│   └── q2Agent.py          # Adversarial agent (Alpha-Beta Minimax + custom heuristic)
├── problems/
│   ├── q1a_problem.py      # Single-food pathfinding problem
│   ├── q1b_problem.py      # Multi-food pathfinding problem
│   └── q1c_problem.py      # All-food collection problem
├── solvers/
│   ├── q1a_solver.py       # A* solver for Q1a
│   ├── q1b_solver.py       # A* solver with BFS heuristic for Q1b
│   └── q1c_solver.py       # Greedy BFS solver for Q1c
├── assets/
│   ├── Certificates.pdf    # Best In Class Award certificate
│   └── report.pdf          # Project report
├── layouts/                # Pacman map layouts
├── pacman.py               # Main game engine
└── evaluator.py            # Grading/evaluation script
```

---

## Part 1 — Classical Search (Q1)

### Q1a: A* Search — Nearest Food

- **Problem**: Navigate Pacman to the nearest food pellet.
- **State space**: Grid position `(x, y)`.
- **Solver**: A* search with Manhattan distance as the admissible heuristic.
- **Key design**: Position-based state keeps the search space compact, enabling fast expansion.

```bash
python pacman.py -l layouts/q1a_bigMaze.lay -p SearchAgent -a fn=q1a_solver,prob=q1a_problem --timeout=1
```

### Q1b: A* Search — Multi-food Maze

- **Problem**: Find a path to eat the nearest food in a maze containing multiple food pellets.
- **State space**: Full `GameState` (position + remaining food).
- **Solver**: A* with a **precomputed BFS distance map** as the heuristic — all food positions are used as BFS sources simultaneously, so the heuristic returns the true shortest walkable distance to the nearest food, keeping the search both admissible and significantly more informed than Manhattan distance.
- **Optimization**: Weighted cost `0.1 * g(n) + h(n)` to prioritise heuristic guidance and reduce node expansions.

```bash
python pacman.py -l layouts/q1b_mediumCorners.lay -p SearchAgent -a fn=q1b_solver,prob=q1b_problem --timeout=5
```

### Q1c: Greedy BFS — Collect All Food

- **Problem**: Eat every food pellet on the board within a 10-second time limit.
- **State space**: `(pacman_position, frozenset of remaining food)`.
- **Solver**: Iterative Greedy BFS — at each step, BFS finds the closest reachable food and Pacman navigates there, repeating until all food is eaten or time runs out.
- **Why greedy BFS over A\***: Full A* over the complete food-collection state space is computationally intractable for large maps; greedy BFS delivers near-optimal routes well within the time constraint.

```bash
python pacman.py -l layouts/q1c_mediumSearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10
```

---

## Part 2 — Adversarial Search Agent (Q2)

The `Q2_Agent` is the competition agent. It plays against ghost agents in real time, maximising its score while surviving as long as possible.

### Algorithm: Alpha-Beta Minimax

Standard Minimax with **Alpha-Beta pruning** to search 2 plies deep across all agents. Pruning dramatically reduces the number of states evaluated, allowing the agent to make decisions within the strict per-move timeout.

```python
best_action, best_value = self.alphaBeta(
    gameState, depth=2, agentIndex=0,
    alpha=-inf, beta=inf,
    evaluationFunction=self.betterEvaluation
)
```

### Evaluation Function: `betterEvaluation`

The heuristic that drives the agent's decision-making considers five factors:

| Factor | Description |
|---|---|
| **Game score** | Base score from the game engine |
| **Food distance** | BFS-based true shortest distance to the nearest food; closer food → higher score |
| **Capsule distance** | BFS-based distance to the nearest power capsule |
| **Ghost danger** | Heavy penalty when a non-scared ghost can reach Pacman's position next turn; distance-scaled penalty for nearby active ghosts |
| **Scared ghost reward** | Bonus inversely proportional to distance when a ghost is scared (edible) |

All BFS distances are computed on-the-fly using a custom `findNearestTargetDistance` helper to account for walls, rather than relying on inaccurate Manhattan distances.

### Immediate Reward Shaping

Inside the Alpha-Beta loop, states where Pacman's score increased are given a small bonus (`immediate_reward`), while states where the score dropped sharply (e.g. death) receive a large penalty — nudging the agent toward immediate food collection and away from dangerous moves.

### Tuned Hyperparameters

The weights were optimised through experimentation:

```python
self.food_weight         = 110.24
self.capsule_weight      = 105.41
self.ghost_close_penalty = 118.5
self.scared_ghost_reward = 315.7
self.immediate_reward    = 40
```

### Run the Competition Agent

```bash
python pacman.py -l layouts/q2_mediumClassic2.lay -p Q2_Agent --timeout=30
```

---

## Requirements

- Python 3.x
- No external dependencies — uses only the standard library and the provided game engine.

---

## Results

This implementation achieved **1st place out of 150+ students** in the FIT5047 Autonomous Pacman Competition and received the **Best In Class Award for Outstanding Performance**.
