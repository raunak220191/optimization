batch_size = len(files) // 5
batches = []

heap = [(get_file_size(file), file) for file in files]
heapq.heapify(heap)

for _ in range(5):
    batch = []
    batch_size_remaining = batch_size

    while batch_size_remaining > 0 and heap:
        file_size, file_path = heapq.heappop(heap)
        batch.append(file_path)
        batch_size_remaining -= 1

    batches.append(batch)
