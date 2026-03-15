# WEG Future Leaders — Case Study

## Problem

Given a job consisting of multiple tasks with individual completion times and inter-task dependencies, find the **minimum completion time** and a valid **execution order**.

## Approach

The problem is modeled as a **Directed Acyclic Graph (DAG)** where nodes are tasks and edges represent dependencies. The solution combines two classic techniques:

- **Kahn's Algorithm** for topological sorting — produces a valid execution order that respects all dependencies.
- **Critical Path Method (CPM)** — computes the earliest start/finish time for each task assuming parallel execution.

### Two Interpretations

The case study notes that there may be two valid answers depending on interpretation:

| Interpretation | Logic | Result |
|---|---|---|
| **Parallel** | Independent tasks run simultaneously. Minimum time = longest path through the DAG (critical path).
| **Sequential** | Only one task runs at a time. Minimum time = sum of all durations.

### Parallel Execution Schedule for the example

```
t=0   A starts, B starts, C starts
t=2   B finishes
t=3   A finishes → D starts
t=4   C finishes → E starts (B already done)
t=6   E finishes
t=8   D finishes → F starts (E already done)
t=11  F finishes
```

**Critical path: A → D → F** (3 + 5 + 3 = 11 units)

### Complexity

- **Time:** O(V + E) where V = number of tasks, E = number of dependency edges
- **Space:** O(V + E)

## Usage

```bash
python weg_case_study_solution.py
```

## Expected Output for he example

```
Topological Order: ['A', 'B', 'C', 'D', 'E', 'F']

Parallel Execution:
Minimum completion time = 11 units

Sequential Execution:
Minimum completion time = 19 units

Critical Path Analysis
Critical path: A,D,F
Time breakdown: 11 units
```
