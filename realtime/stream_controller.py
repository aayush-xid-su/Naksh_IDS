import time


def realtime_stream(generator, max_batch_size=4, max_latency=2.0):
    buffer = []
    last_flush = time.time()

    for item in generator:
        buffer.append(item)

        if len(buffer) >= max_batch_size or (time.time() - last_flush) >= max_latency:
            yield buffer
            buffer = []
            last_flush = time.time()
