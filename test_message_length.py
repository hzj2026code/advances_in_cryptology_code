import argparse
import csv
import time

import matplotlib.pyplot as plt
import pandas as pd

from common import generate_keypair, load_module, mean_ms, std_ms


PARAMS = [
    ("SLH-DSA-SHA2-128s", "pyspx.sha2_128s"),
    ("SLH-DSA-SHA2-128f", "pyspx.sha2_128f"),
]

MESSAGE_SIZES = [
    32,
    1024,
    10 * 1024,
    100 * 1024,
    1024 * 1024,
]


def benchmark_message_length(param_name, module_name, message_size, repeat):
    spx = load_module(module_name)
    pk, sk = generate_keypair(spx)

    message = b"A" * message_size

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
            raise RuntimeError(f"verification failed: {param_name}, message_size={message_size}")

        verify_times.append(end - start)

    return {
        "parameter_set": param_name,
        "message_size_bytes": message_size,
        "message_size_label": format_size(message_size),
        "signature_bytes": len(sig),
        "sign_avg_ms": mean_ms(sign_times),
        "sign_std_ms": std_ms(sign_times),
        "verify_avg_ms": mean_ms(verify_times),
        "verify_std_ms": std_ms(verify_times),
    }


def format_size(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size // 1024} KB"
    return f"{size // (1024 * 1024)} MB"


def plot_line(df, y, ylabel, title, output):
    plt.figure(figsize=(8, 5))

    for param_name in df["parameter_set"].unique():
        sub = df[df["parameter_set"] == param_name]
        plt.plot(
            sub["message_size_label"],
            sub[y],
            marker="o",
            label=param_name,
        )

    plt.xlabel("Message size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=200)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=30)
    args = parser.parse_args()

    rows = []

    print(f"Message length sensitivity test, repeat = {args.repeat}")

    for param_name, module_name in PARAMS:
        for message_size in MESSAGE_SIZES:
            print(f"testing {param_name}, message size = {format_size(message_size)} ...")
            rows.append(
                benchmark_message_length(
                    param_name,
                    module_name,
                    message_size,
                    args.repeat,
                )
            )

    output = "results/message_length_results.csv"

    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    df = pd.DataFrame(rows)

    plot_line(
        df,
        "sign_avg_ms",
        "Average signing time / ms",
        "Signing Time under Different Message Sizes",
        "figures/message_length_sign_time.png",
    )

    plot_line(
        df,
        "verify_avg_ms",
        "Average verification time / ms",
        "Verification Time under Different Message Sizes",
        "figures/message_length_verify_time.png",
    )

    plot_line(
        df,
        "signature_bytes",
        "Signature size / bytes",
        "Signature Size under Different Message Sizes",
        "figures/message_length_signature_size.png",
    )

    print(f"Experiment finished: {output}")
    print("Figures generated:")
    print("figures/message_length_sign_time.png")
    print("figures/message_length_verify_time.png")
    print("figures/message_length_signature_size.png")


if __name__ == "__main__":
    main()
