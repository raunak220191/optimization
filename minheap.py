import heapq

def create_batches(file_sizes, batch_size):
    batches = []
    current_batch = []

    for size in file_sizes:
        if sum(current_batch) + size <= batch_size:
            current_batch.append(size)
        else:
            batches.append(current_batch)
            current_batch = [size]
    
    if current_batch:
        batches.append(current_batch)

    return batches
