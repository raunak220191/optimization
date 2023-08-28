from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

num_batches = len(batches)
num_processes = num_ocr_processes + num_embed_processes

x = {}
for i in range(num_batches):
    for j in range(num_processes):
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

# Add constraints
for i in range(num_batches):
    solver.Add(sum(x[i, j] for j in range(num_processes)) == 1)

for j in range(num_processes):
    solver.Add(sum(x[i, j] for i in range(num_batches)) == 1)

# Define objective (minimize embedding)
objective = solver.Objective()
for i in range(num_batches):
    objective.SetCoefficient(x[i, 1], 1)
objective.SetMinimization()

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    for i in range(num_batches):
        for j in range(num_processes):
            if x[i, j].solution_value() == 1:
                if j == 0:
                    ocr_queue.put(batches[i])
                else:
                    embed_queue.put(batches[i])
