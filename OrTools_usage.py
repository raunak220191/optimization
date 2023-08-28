from ortools.sat.python import cp_model

def optimize_scheduling(batches, num_ocr_processes, num_embed_processes):
    model = cp_model.CpModel()

    num_batches = len(batches)
    num_processes = num_ocr_processes + num_embed_processes

    # Binary variables to represent assignment of batches to processes
    x = {}
    for i in range(num_batches):
        for j in range(num_processes):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # Each batch can only be assigned to one process
    for i in range(num_batches):
        model.Add(sum(x[i, j] for j in range(num_processes)) == 1)

    # Embedding can start only after one batch of OCR is complete
    for i in range(1, num_batches):
        model.Add(sum(x[j, num_ocr_processes] for j in range(i)) >= x[i, num_ocr_processes])

    # Objective: Minimize embeddings (embedding is heavier)
    objective = sum(x[i, num_ocr_processes + 1] for i in range(num_batches))
    model.Minimize(objective)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        ocr_batches = []
        embed_batches = []

        for i in range(num_batches):
            if solver.Value(x[i, num_ocr_processes]):
                ocr_batches.append(batches[i])
            else:
                embed_batches.append(batches[i])

        return ocr_batches, embed_batches

    return None, None

# Usage
batches = [batch1, batch2, batch3, ...]
num_ocr_processes = 5
num_embed_processes = 5

ocr_batches, embed_batches = optimize_scheduling(batches, num_ocr_processes, num_embed_processes)

# Run OCR and embedding processes using ocr_batches and embed_batches
