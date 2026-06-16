import argparse
import csv
import time

from common import PARAMS, generate_keypair, load_module, mean_ms, std_ms


def benchmark_one(param_name, module_name, repeat, message):
    spx = load_module(module_name)

    keygen_times = []
    for _ in range(repeat):
        start = time.perf_counter_ns()
        pk, sk = generate_keypair(spx)
        end = time.perf_counter_ns()
        keygen_times.append(end - start)

    pk, sk = generate_keypair(spx)

    sign_times = []
    signatures = []
    for _ in range(repeat):
        start = time.perf_counter_ns()
        sig = spx.sign(message, sk)
        end = time.perf_counter_ns()
        sign_times.append(end - start)
        signatures.append(sig)

    sig = signatures[0]

    verify_times = []
    for _ in range(repeat):
        start = time.perf_counter_ns()
        ok = spx.verify(message, sig, pk)
        end = time.perf_counter_ns()
        if not ok:
            raise RuntimeError(f"verification failed: {param_name}")
        verify_times.append(end - start)

    return {
        "parameter_set": param_name,
        "public_key_bytes": len(pk),
        "secret_key_bytes": len(sk),
        "signature_bytes": len(sig),
        "keygen_avg_ms": mean_ms(keygen_times),
        "keygen_std_ms": std_ms(keygen_times),
        "sign_avg_ms": mean_ms(sign_times),
        "sign_std_ms": std_ms(sign_times),
        "verify_avg_ms": mean_ms(verify_times),
        "verify_std_ms": std_ms(verify_times),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=30)
    parser.add_argument("--message-size", type=int, default=1024)
    args = parser.parse_args()

    message = b"A" * args.message_size
    rows = []

    print(f"repeat = {args.repeat}, message_size = {args.message_size} bytes")

    for param_name, module_name in PARAMS:
        print(f"testing {param_name} ...")
        rows.append(benchmark_one(param_name, module_name, args.repeat, message))

    output = "results/benchmark_results.csv"
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Experiment 2 finished: {output}")


if __name__ == "__main__":
    main()
