import math
import time
import random

#
# utility per benchmark
#


def timer(label, cb):
    start_time = time.time()  # prendo il tempo all'inizio dell'esecuzione
    cb()  # chiamo il callback
    end_time = time.time()  # prendo il tempo alla fine dell'esecuzione
    # il tempo trascorso è la differenza tra tempo alla fine e tempo all'inizio
    sec = end_time - start_time
    ms = math.floor(sec * 1000)
    print(f"{label}: {ms}ms")
    return ms


def print_table(table, spacing):
    headings = table[0]
    max_lengths = []

    for i, _ in enumerate(headings):
        lengths = [len(row[i]) for row in table]
        max_lengths.append(max(lengths))

    for row in table:
        s = ""
        for i, col in enumerate(row):
            s += col.ljust(max_lengths[i] + spacing)
        print(s)


def benchmark(lst):
    # esegui tutti e misura
    results = []
    for (label, cb) in lst:
        t = timer(label, cb)
        results.append((label, cb, t))

    # il tempo più lungo è la misura di base
    baseline = max([t for (_, _, t) in results])

    # prepara la tabella dei risultati
    table = [("label", "time", "delta", "result")]
    for (label, cb, t) in results:
        delta = t - baseline
        percentage_improvement = math.floor(delta / baseline * 100)

        result = ""
        if delta == 0:
            result = "baseline"
        else:
            result = f"{percentage_improvement}%"

        table.append((label, f"{t}ms", f"{delta}ms", result))

    print("-----------------------------")
    print("BENCHMARK RESULTS:")
    print_table(table, 2)
    print("-----------------------------")