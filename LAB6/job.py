from ortools.sat.python import cp_model

def job_scheduling_named_jobs():
    # Create the model
    model = cp_model.CpModel()

    # Job definitions: name -> duration
    jobs = {
        'A': 3,
        'B': 2,
        'C': 4
    }

    horizon = sum(jobs.values())  # Max possible time to schedule all jobs

    # Variables: Start and end times for each job
    start_vars = {}
    end_vars = {}
    intervals = []

    for name, duration in jobs.items():
        start = model.NewIntVar(0, horizon, f'start_{name}')
        end = model.NewIntVar(0, horizon, f'end_{name}')
        interval = model.NewIntervalVar(start, duration, end, f'interval_{name}')
        start_vars[name] = start
        end_vars[name] = end
        intervals.append(interval)

    # Add no-overlap constraint: only one job at a time
    model.AddNoOverlap(intervals)

    # Objective: minimize the makespan (latest job end time)
    makespan = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(makespan, list(end_vars.values()))
    model.Minimize(makespan)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Minimum makespan: {solver.Value(makespan)}')
        for name in jobs:
            print(f'Job {name} starts at {solver.Value(start_vars[name])} and ends at {solver.Value(end_vars[name])}')
    else:
        print('No solution found.')

if __name__ == '__main__':
    job_scheduling_named_jobs()