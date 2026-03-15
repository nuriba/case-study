"""
Task Scheduling with Dependencies - Minimum Job Completion Time

Approach: Topological Sort + Critical Path Method
I have used two interpretations for the minimum completion time based on how tasks can be executed:
1. PARALLEL: Tasks without unmet dependencies execute simultaneously.
   → Minimum time = length of the critical path through the directed acyclic graph.
2. SEQUENTIAL: Only one task executes at a time.
   → Minimum time = sum of all task durations. Order is not important because of dependencies; order = any valid topological sort.

Therefore I implemented a single algorithm that computes both the topological order and the earliest start/finish times for each task. 
The key steps are:
- Model tasks and dependencies as a Directed Acyclic Graph.
- Perform topological sort for valid execution order.
- For the parallel case, compute earliest start/finish times via forward pass.
"""

from collections import deque, defaultdict


def solve_job_scheduling(tasks: dict[str, int], dependencies: dict[str, list[str]]):
    """
    Parameters:
        tasks: {task_name: duration}
        dependencies: {task_name: [list of prerequisite tasks]}

    Returns:
        topological_order, parallel_min_time, sequential_min_time, schedule
    """
    # Build adjacency list and in-degree count
    graph = defaultdict(list)      #dependent tasks
    in_degree = {task: 0 for task in tasks}

    for task, prereqs in dependencies.items():
        for prereq in prereqs:
            graph[prereq].append(task)
            in_degree[task] += 1

    #Topological Sort
    queue = deque()
    for task in tasks:
        if in_degree[task] == 0:
            queue.append(task)

    topo_order = []
    # Track earliest start time for each task - Parallel execution
    earliest_start = {task: 0 for task in tasks}

    while queue:
        # Process all tasks at current level
        current = queue.popleft()
        topo_order.append(current)

        for neighbor in graph[current]:
            # The neighbor can't start until this prerequisite finishes
            earliest_start[neighbor] = max(
                earliest_start[neighbor],
                earliest_start[current] + tasks[current]
            )
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(topo_order) != len(tasks):
        raise ValueError("Cycle detected. No valid schedule possible")

    # Parallel: max(earliest_start[t] + duration[t]) across all tasks
    earliest_finish = {t: earliest_start[t] + tasks[t] for t in tasks}
    parallel_min_time = max(earliest_finish.values())

    # Sequential: sum of all durations (order doesn't matter for total)
    sequential_min_time = sum(tasks.values())

    # Build detailed schedule
    schedule = []
    for task in topo_order:
        schedule.append({
            "task": task,
            "duration": tasks[task],
            "earliest_start": earliest_start[task],
            "earliest_finish": earliest_finish[task],
            "dependencies": dependencies.get(task, []),
        })

    return topo_order, parallel_min_time, sequential_min_time, schedule


# Example from the case study
if __name__ == "__main__":
    tasks = {
        "A": 3,
        "B": 2,
        "C": 4,
        "D": 5,
        "E": 2,
        "F": 3,
    }

    #Task: [dependencies]
    dependencies = {
        "A": [],
        "B": [],
        "C": [],
        "D": ["A"],          
        "E": ["B", "C"],    
        "F": ["D", "E"],     
    }

    topo_order, parallel_time, sequential_time, schedule = solve_job_scheduling(
        tasks, dependencies
    )

    print(f"\nTopological Order: {topo_order}")

    print(f"\nParallel Execution:")
    print(f"Minimum completion time = {parallel_time} units")
    print(f"\nSequential Execution:")
    print(f"Minimum completion time = {sequential_time} units")

    # Trace critical path
    print("\nCritical Path Analysis")
    # Find which task finishes last
    bottleneck = max(schedule, key=lambda s: s["earliest_finish"])["task"]

    # Backtrack to find the critical path
    critical_path = []
    current = bottleneck
    while current:
        critical_path.append(current)
        # Find the predecessor that determines this task's earliest start
        prereqs = dependencies.get(current, [])
        if not prereqs:
            break
        # The critical predecessor is the one whose finish time equals our start
        my_start = next(s["earliest_start"] for s in schedule if s["task"] == current)
        critical_pred = max(
            prereqs,
            key=lambda p: next(s["earliest_finish"] for s in schedule if s["task"] == p)
        )
        current = critical_pred

    critical_path.reverse()
    path_str = ",".join(critical_path)
    print(f"Critical path: {path_str}")
    print(f"Time breakdown: {parallel_time} units")
